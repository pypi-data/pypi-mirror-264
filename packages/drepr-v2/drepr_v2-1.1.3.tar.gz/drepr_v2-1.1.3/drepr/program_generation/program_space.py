from __future__ import annotations

from collections import namedtuple

ResourceKey = namedtuple("ResourceKey", ["resource"])


class VarSpace:
    output_file = lambda: ("output_file",)
    resource = lambda resource: ResourceKey(
        f"resource={resource}",
    )
    resource_data = lambda resource: (f"resource-data={resource}",)
    preprocessing_udf_value = lambda preprocessing_id: (
        f"preprocessing-id={preprocessing_id}",
        "udf-value",
    )
    preprocessing_udf_context = lambda preprocessing_id: (
        f"preprocessing-id={preprocessing_id}",
        "udf-context",
    )
    writer = lambda: ("writer",)
    attr_index_dim = lambda resource, attr, di: (
        f"resource={resource}",
        f"attr={attr}",
        f"index-dim={di}",
    )
    attr_value_dim = lambda resource, attr, di: (
        f"resource={resource}",
        f"attr={attr}",
        f"value-dim={di}",
    )
    attr_values_dim = lambda resource, attr, di: (
        f"resource={resource}",
        f"attr={attr}",
        f"values-dim={di}",
    )
    attr_missing_values = lambda attr: (f"attr-missing-values={attr}",)
    has_attr_value_dim = lambda resource, attr, di: (
        f"resource={resource}",
        f"attr={attr}",
        f"has-value-dim={di}",
    )
