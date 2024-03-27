class NamespaceMixin:
    prefixes: dict[str, str]

    @classmethod
    def is_rel_iri(cls, iri: str) -> bool:
        return iri.find("://") == -1 and iri.find(":") != -1

    def get_rel_iri(self, abs_iri: str) -> str:
        """Convert an absolute IRI to a relative IRI."""
        assert not self.is_rel_iri(abs_iri)
        for prefix, uri in self.prefixes.items():
            if abs_iri.startswith(uri):
                return f"{prefix}:{abs_iri.replace(uri, '')}"
        raise ValueError(
            "Cannot create relative IRI because there is no suitable prefix"
        )

    def get_abs_iri(self, rel_iri: str) -> str:
        """Convert a relative IRI to an absolute IRI."""
        assert self.is_rel_iri(rel_iri)
        prefix, val = rel_iri.split(":", 1)
        if prefix not in self.prefixes:
            raise ValueError(
                f"Cannot create absolute IRI because the prefix {prefix} does not exist"
            )
        return f"{self.prefixes[prefix]}{val}"
