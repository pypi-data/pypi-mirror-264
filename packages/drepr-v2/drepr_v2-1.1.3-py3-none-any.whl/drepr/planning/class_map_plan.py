from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, TypeAlias, cast

from drepr.models.prelude import (
    DREPR_URI,
    MISSING_VALUE_TYPE,
    Alignment,
    Attr,
    AttrId,
    Cardinality,
    ClassNode,
    DataNode,
    DRepr,
    EdgeId,
    LiteralNode,
    NodeId,
)
from drepr.planning.drepr_model_alignments import DReprModelAlignments
from drepr.planning.topological_sorting import topological_sorting


@dataclass
class ClassesMapExecutionPlan:
    # read_plans: list[ReadPlan]
    # write_plan: WritePlan
    class_map_plans: list[ClassMapPlan]

    @staticmethod
    def create(desc: DRepr):
        reversed_topo_orders = topological_sorting(desc.sm)
        alignments = DReprModelAlignments.create(desc)
        edges_optional = {e.edge_id: not e.is_required for e in desc.sm.edges.values()}
        edges_has_missing_values: dict[EdgeId, bool] = {}
        class_map_plans = []
        class2plan = {}

        # find subject attribute of each class
        class2subj = {}
        for class_id in reversed_topo_orders.topo_order:
            class2subj[class_id] = ClassMapPlan.find_subject(
                desc, class_id, class2subj, alignments
            )

        # figure out if an edge may contain missing values
        n_miss_edges = -1
        while n_miss_edges != len(edges_has_missing_values):
            n_miss_edges = len(edges_has_missing_values)
            for e in desc.sm.edges.values():
                if e.edge_id in edges_has_missing_values:
                    continue
                v = desc.sm.nodes[e.target_id]
                if isinstance(v, DataNode):
                    v_attr = desc.get_attr_by_id(v.attr_id)
                    edges_has_missing_values[e.edge_id] = (
                        len(v_attr.missing_values) > 0
                    ) or v_attr.path.has_optional_steps()
                elif isinstance(v, ClassNode):
                    if any(
                        ve.edge_id not in edges_has_missing_values
                        for ve in desc.sm.iter_outgoing_edges(v.node_id)
                        if not reversed_topo_orders.removed_outgoing_edges[ve.edge_id]
                    ):
                        continue

                    if v.is_blank_node(desc.sm):
                        # it can have missing values when:
                        # (1) at least one edge is mandatory & the edge have missing values
                        # (2) all edges are optional and all of them have missing values
                        have_missing_values = False

                        # (1) at least one edge is mandatory & the edge have missing values
                        for ve in desc.sm.iter_outgoing_edges(v.node_id):
                            if reversed_topo_orders.removed_outgoing_edges[ve.edge_id]:
                                continue

                            if (
                                not edges_optional[ve.edge_id]
                                and edges_has_missing_values[ve.edge_id]
                            ):
                                have_missing_values = True
                                break

                        # (2) all edges are optional and all of them have missing values
                        if not have_missing_values:
                            if all(
                                edges_optional[ve.edge_id]
                                and edges_has_missing_values[ve.edge_id]
                                for ve in desc.sm.iter_outgoing_edges(v.node_id)
                                if not reversed_topo_orders.removed_outgoing_edges[
                                    ve.edge_id
                                ]
                            ):
                                have_missing_values = True
                    else:
                        # it can have missing values when:
                        # (1) at least one edge is mandatory & the edge have missing values
                        # (2) the URI edge have missing values
                        have_missing_values = False

                        # (1) at least one edge is mandatory & the edge have missing values
                        for ve in desc.sm.iter_outgoing_edges(v.node_id):
                            if reversed_topo_orders.removed_outgoing_edges[ve.edge_id]:
                                continue

                            if (
                                not edges_optional[ve.edge_id]
                                and edges_has_missing_values[ve.edge_id]
                            ):
                                have_missing_values = True
                                break

                        # (2) the URI edge have missing values
                        if not have_missing_values:
                            ve_attr = desc.get_attr_by_id(class2subj[v.node_id])
                            if (
                                len(ve_attr.missing_values) > 0
                                or ve_attr.path.has_optional_steps()
                            ):
                                have_missing_values = True

                    edges_has_missing_values[e.edge_id] = have_missing_values
                else:
                    assert isinstance(v, LiteralNode)
                    edges_has_missing_values[e.edge_id] = False

        assert len(edges_has_missing_values) == len(desc.sm.edges) - sum(
            reversed_topo_orders.removed_outgoing_edges.values()
        ), f"{len(edges_has_missing_values)} == {len(desc.sm.edges)} - {sum(reversed_topo_orders.removed_outgoing_edges.values())}"

        # generate plans
        for class_id in reversed_topo_orders.topo_order:
            classplan = ClassMapPlan.create(
                desc,
                class_id,
                class2subj,
                alignments,
                edges_optional,
                edges_has_missing_values,
                reversed_topo_orders.removed_outgoing_edges,
            )
            class2plan[class_id] = classplan
            class_map_plans.append(classplan)

        return ClassesMapExecutionPlan(class_map_plans)


@dataclass
class ClassMapPlan:
    class_id: str
    subject: Subject
    data_props: list[DataProp]
    literal_props: list[LiteralProp]
    object_props: list[ObjectProp]
    buffered_object_props: list[ObjectProp]

    @staticmethod
    def create(
        desc: DRepr,
        class_id: NodeId,
        class2subj: dict[NodeId, AttrId],
        inference: DReprModelAlignments,
        edges_optional: dict[EdgeId, bool],
        edges_missing_values: dict[EdgeId, bool],
        removed_edges: dict[EdgeId, bool],
    ):
        subj = class2subj[class_id]
        uri_dnode: Optional[DataNode] = None
        for e in desc.sm.iter_outgoing_edges(class_id):
            if e.get_abs_iri(desc.sm) == DREPR_URI:
                tmp = desc.sm.nodes[e.target_id]
                assert isinstance(tmp, DataNode)
                uri_dnode = tmp
                break

        # generate other properties
        literal_props = []
        data_props: list[DataProp] = []
        object_props = []
        buffered_object_props = []

        for e in desc.sm.iter_outgoing_edges(class_id):
            target = desc.sm.nodes[e.target_id]
            if isinstance(target, DataNode):
                attribute = desc.get_attr_by_id(target.attr_id)

                if e.get_abs_iri(desc.sm) != DREPR_URI:
                    alignments = inference.get_alignments(subj, target.attr_id)
                    alignments_cardinality = inference.estimate_cardinality(alignments)

                    if attribute.value_type.is_list():
                        if alignments_cardinality.is_one_to_star():
                            alignments_cardinality = Cardinality.OneToMany
                        else:
                            assert (
                                alignments_cardinality.is_many_to_star()
                            ), alignments_cardinality
                            alignments_cardinality = Cardinality.ManyToMany

                    data_props.append(
                        DataProp(
                            alignments=alignments,
                            alignments_cardinality=inference.estimate_cardinality(
                                alignments
                            ),
                            predicate=e.get_abs_iri(desc.sm),
                            attr=attribute,
                            is_optional=edges_optional[e.edge_id],
                            missing_values=set(attribute.missing_values),
                            missing_path=attribute.path.has_optional_steps(),
                            datatype=(
                                target.data_type
                                if target.data_type is not None
                                else None
                            ),
                        )
                    )
            elif isinstance(target, LiteralNode):
                literal_props.append(
                    LiteralProp(predicate=e.get_abs_iri(desc.sm), value=target.value)
                )
            elif isinstance(target, ClassNode):
                attribute = desc.get_attr_by_id(class2subj[e.target_id])

                alignments = inference.get_alignments(subj, attribute.id)

                if target.is_blank_node(desc.sm):
                    prop = BlankObject(
                        attr=attribute,
                        alignments_cardinality=inference.estimate_cardinality(
                            alignments
                        ),
                        alignments=alignments,
                        predicate=e.get_abs_iri(desc.sm),
                        class_id=class_id,
                        is_optional=edges_optional[e.edge_id],
                        can_target_missing=edges_missing_values[e.edge_id],
                    )
                else:
                    prop = IDObject(
                        attr=attribute,
                        alignments_cardinality=inference.estimate_cardinality(
                            alignments
                        ),
                        alignments=alignments,
                        predicate=e.get_abs_iri(desc.sm),
                        class_id=class_id,
                        is_optional=edges_optional[e.edge_id],
                        can_target_missing=edges_missing_values[e.edge_id],
                        missing_values=set(attribute.missing_values),
                    )

                if removed_edges[e.edge_id]:
                    buffered_object_props.append(prop)
                else:
                    object_props.append(prop)

        subj_attr = desc.get_attr_by_id(subj)

        if uri_dnode is None:
            subject = BlankSubject(
                attr=subj_attr,
            )
        else:
            # get missing values from the real subjects
            missing_values = set(subj_attr.missing_values)
            (uri_dnode_inedge,) = [
                e
                for e in desc.sm.get_edges_between_nodes(class_id, uri_dnode.node_id)
                if e.get_abs_iri(desc.sm) == DREPR_URI
            ]

            if uri_dnode.attr_id == subj:
                subject = InternalIDSubject(
                    attr=subj_attr,
                    is_optional=edges_optional[uri_dnode_inedge.edge_id],
                    missing_values=missing_values,
                )
            else:
                subject = ExternalIDSubject(
                    attr=subj_attr,
                    is_optional=edges_optional[uri_dnode_inedge.edge_id],
                    missing_values=missing_values,
                )

        return ClassMapPlan(
            class_id=class_id,
            subject=subject,
            data_props=data_props,
            literal_props=literal_props,
            object_props=object_props,
            buffered_object_props=buffered_object_props,
        )

    @staticmethod
    def find_subject(
        desc: DRepr,
        class_id: NodeId,
        class2subj: dict[NodeId, AttrId],
        desc_aligns: DReprModelAlignments,
    ):
        """
        Find the subject of the class among the attributes of the class.

        The subject has *-to-one relationship with other attributes.
        """
        # get data nodes, attributes, and the attribute that contains URIs of the class
        data_nodes: list[DataNode] = []
        attrs: list[AttrId] = []
        uri_attr: Optional[AttrId] = None

        for e in desc.sm.iter_outgoing_edges(class_id):
            target = desc.sm.nodes[e.target_id]

            if isinstance(target, DataNode):
                data_nodes.append(target)
                attrs.append(target.attr_id)

                if e.get_abs_iri(desc.sm) == DREPR_URI:
                    uri_attr = target.attr_id

        # if the subject attribute is provided, then, we will use it.
        subjs = []
        for u in data_nodes:
            if any(
                e.is_subject
                for e in desc.sm.get_edges_between_nodes(class_id, u.node_id)
            ):
                subjs.append(u.attr_id)

        if len(subjs) == 0:
            if len(attrs) == 0:
                # there is a special case where the class has no data node, but only links to other classes
                # we need to get the subject from the other classes
                other_attrs = []
                for e in desc.sm.iter_outgoing_edges(class_id):
                    target = desc.sm.nodes[e.target_id]
                    if isinstance(target, ClassNode):
                        # we must have inferred the subject of the target class before (because of the topological sorting)
                        assert target.node_id in class2subj
                        target_subj = class2subj[target.node_id]
                        other_attrs.append(target_subj)
                subjs = desc_aligns.infer_subject(other_attrs)
            else:
                # invoke the inference to find the subject attribute
                subjs = desc_aligns.infer_subject(attrs)

        if len(subjs) == 0:
            raise Exception(
                "There is no subject attribute of class: {} ({}). Users need to specify it explicitly".format(
                    cast(ClassNode, desc.sm.nodes[class_id]).label, class_id
                )
            )

        return ClassMapPlan.select_subject(desc, class_id, subjs, attrs, uri_attr)

    @staticmethod
    def select_subject(
        desc: DRepr,
        class_id: NodeId,
        subjs: list[AttrId],
        attrs: list[AttrId],
        uri_attr: Optional[AttrId],
    ) -> AttrId:
        if uri_attr is not None and uri_attr in subjs:
            return uri_attr
        return subjs[0]


@dataclass
class BlankSubject:
    attr: Attr


@dataclass
class InternalIDSubject:
    attr: Attr
    is_optional: bool
    missing_values: set[MISSING_VALUE_TYPE]


@dataclass
class ExternalIDSubject:
    attr: Attr
    is_optional: bool
    missing_values: set[MISSING_VALUE_TYPE]


Subject: TypeAlias = BlankSubject | InternalIDSubject | ExternalIDSubject


@dataclass
class DataProp:
    alignments: list[Alignment]
    alignments_cardinality: Cardinality
    predicate: str
    attr: Attr
    is_optional: bool
    missing_values: set[MISSING_VALUE_TYPE]
    missing_path: bool
    datatype: Optional[str]

    @property
    def can_target_missing(self):
        return len(self.missing_values) > 0 or self.missing_path


@dataclass
class LiteralProp:
    predicate: str
    value: Any


@dataclass
class BlankObject:
    attr: Attr
    alignments: list[Alignment]
    alignments_cardinality: Cardinality
    predicate: str
    class_id: NodeId
    is_optional: bool
    # whether an instance of the target class can be missing
    can_target_missing: bool


@dataclass
class IDObject:
    attr: Attr
    alignments: list[Alignment]
    alignments_cardinality: Cardinality
    predicate: str
    class_id: NodeId
    is_optional: bool
    # whether an instance of the target class can be missing
    can_target_missing: bool
    missing_values: set[MISSING_VALUE_TYPE]


ObjectProp = BlankObject | IDObject
