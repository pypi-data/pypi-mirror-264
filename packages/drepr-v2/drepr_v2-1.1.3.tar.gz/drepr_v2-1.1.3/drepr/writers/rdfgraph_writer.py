from __future__ import annotations

from typing import Any, Optional

from rdflib import RDF, BNode, Graph, Literal, Namespace, URIRef

from drepr.models.sm import DREPR_URI
from drepr.writers.base import StreamClassWriter

SubjVal = str | tuple | int | bool


class RDFGraphWriter(StreamClassWriter):
    def __init__(self, prefixes: dict[str, str]):
        self.g: Graph = Graph()
        for prefix, ns in prefixes.items():
            self.g.bind(prefix, Namespace(ns))

        self.written_records: dict[SubjVal, BNode | URIRef] = {}
        self.origin_subj: SubjVal = ""
        self.subj: Optional[URIRef | BNode] = None
        self.buffer: list[tuple[URIRef, URIRef | BNode | Literal]] = []
        self.is_buffered: bool = False
        self.has_subj_data: bool = False

    def has_written_record(self, subj: SubjVal) -> bool:
        return subj in self.written_records

    def begin_record(
        self, class_uri: str, subj: SubjVal, is_blank: bool, is_buffered: bool
    ):
        self.origin_subj = subj
        if is_blank:
            self.subj = BNode()
        else:
            # subj will be a string for URIRef
            self.subj = URIRef(subj)  # type: ignore

        if is_buffered:
            self.buffer = [(RDF.type, URIRef(class_uri))]
        else:
            self.g.add((self.subj, RDF.type, URIRef(class_uri)))
        self.is_buffered = is_buffered

    def end_record(self):
        if self.subj is None:
            # has been aborted
            return

        if len(self.buffer) > 0:
            for pred, obj in self.buffer:
                self.g.add((self.subj, pred, obj))
            self.buffer = []
        self.written_records[self.origin_subj] = self.subj
        self.subj = None

    def abort_record(self):
        """Abort the record that is being written"""
        self.subj = None
        self.buffer = []

    def is_record_empty(self):
        return not self.has_subj_data

    def write_data_property(self, predicate_id: str, value: Any, dtype: Optional[str]):
        if dtype == DREPR_URI:
            value = URIRef(value)
        else:
            value = Literal(value, datatype=dtype)

        if self.is_buffered:
            self.buffer.append((URIRef(predicate_id), value))
        else:
            assert self.subj is not None
            self.g.add((self.subj, URIRef(predicate_id), value))

    def write_object_property(
        self,
        predicate_id: str,
        object: SubjVal,
        is_subject_blank: bool,
        is_object_blank: bool,
        is_new_subj: bool,
    ):
        object = self.written_records[object]
        if self.is_buffered:
            self.buffer.append((URIRef(predicate_id), object))
        else:
            assert self.subj is not None
            self.g.add((self.subj, URIRef(predicate_id), object))

    def write_to_string(self):
        return self.g.serialize(format="ttl")

    def write_to_file(self, filepath):
        self.g.serialize(filepath, format="ttl")
