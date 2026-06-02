"""EntityProxy and EntityCollection — generic base classes for save entity wrappers.

EntityProxy wraps a single entity's field_info dict + the shared flat cs.Container.
EntityCollection wraps an entire section's worth of entity field_info dicts + the flat container.

All reads and writes route through the flat container (parsed once on open,
built back once on close via FLAT_LAYOUT.build_stream).  No per-entity
sub-containers, no separate BinaryFile I/O for flags.
"""

from __future__ import annotations

from typing import Iterator
import json
from io import StringIO

import construct as cs
from ruamel.yaml import YAML

from .codecs import bits_to_float, float_to_bits


class EntityProxy:
    """Thin wrapper for a single save entity.

    Args:
        flat: The shared FLAT_LAYOUT container (all offsets parsed in one pass).
        field_info: Mapping of field_name → (offset, val_type, length).
                    val_type is one of: "bool", "float", "integer", "sentinel",
                    "ascii", "utf8".
    """

    _float_fields: frozenset[str] = frozenset()
    _ascii_fields: frozenset[str] = frozenset()
    _utf8_fields: frozenset[str] = frozenset()

    def __init__(
        self,
        flat: cs.Container,
        field_info: dict[str, tuple[int, str, int | None]],
    ) -> None:
        object.__setattr__(self, '_flat', flat)
        object.__setattr__(self, '_flds', field_info)

    @property
    def _fields(self) -> list[str]:
        return list(object.__getattribute__(self, '_flds').keys())

    def __getattr__(self, name: str):
        flds = object.__getattribute__(self, '_flds')
        if name.startswith('_') or name not in flds:
            raise AttributeError(name)
        flat = object.__getattribute__(self, '_flat')
        offset, val_type, length = flds[name]
        raw = flat[f"off{offset}"]

        # Class-level type overrides take precedence over effectmap val_type.
        if name in object.__getattribute__(self, '_float_fields'):
            return bits_to_float(raw)
        if name in object.__getattribute__(self, '_ascii_fields'):
            return raw.rstrip(b'\x00').decode('ascii', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        if name in object.__getattribute__(self, '_utf8_fields'):
            return raw.rstrip(b'\x00').decode('utf-8', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw

        # Dispatch on effectmap val_type.
        if val_type == "float":
            return bits_to_float(raw)
        if val_type == "ascii":
            return raw.rstrip(b'\x00').decode('ascii', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        if val_type == "utf8":
            return raw.rstrip(b'\x00').decode('utf-8', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        if val_type == "bool":
            return bool(raw)
        # "integer", "sentinel", or unknown: return raw value.
        return raw

    def __setattr__(self, name: str, value) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        flds = object.__getattribute__(self, '_flds')
        if name not in flds:
            object.__setattr__(self, name, value)
            return
        flat = object.__getattribute__(self, '_flat')
        offset, val_type, length = flds[name]
        key = f"off{offset}"

        if name in object.__getattribute__(self, '_float_fields') or val_type == "float":
            flat[key] = float_to_bits(float(value))

        elif name in object.__getattribute__(self, '_ascii_fields') or val_type == "ascii":
            n = length or 32
            encoded = str(value).encode('ascii', errors='replace')[:n]
            flat[key] = encoded + b'\x00' * (n - len(encoded))

        elif name in object.__getattribute__(self, '_utf8_fields') or val_type == "utf8":
            n = length or 64
            encoded = str(value).encode('utf-8', errors='replace')[:n]
            flat[key] = encoded + b'\x00' * (n - len(encoded))

        elif val_type == "bool":
            existing = flat[key]
            new_bool = bool(value)
            # Preserve game's non-1 truthy raw values (2, 3, 5, 0xa, …).
            if isinstance(existing, int) and bool(existing) == new_bool:
                return
            flat[key] = 1 if new_bool else 0

        else:
            # "integer": always write exact value.
            # "sentinel": skip if logical bool state already matches.
            existing = flat[key]
            new_int = int(value)
            if val_type == "sentinel":
                if isinstance(existing, int) and bool(existing) == bool(new_int):
                    return
            flat[key] = new_int

    def to_dict(self) -> dict:
        return {f: getattr(self, f) for f in self._fields}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_yaml(self) -> str:
        y = YAML()
        y.default_flow_style = False
        buf = StringIO()
        y.dump(self.to_dict(), buf)
        return buf.getvalue()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_dict()!r})"


class EntityCollection:
    """Wraps an entire save section as a collection of EntityProxy objects.

    Args:
        flat: The shared FLAT_LAYOUT container.
        section_info: Mapping of entity_name → field_info dict.
    """

    proxy_class: type[EntityProxy] = EntityProxy
    _section_names: list[str] = []

    def __init__(
        self,
        flat: cs.Container,
        section_info: dict[str, dict[str, tuple[int, str, int | None]]],
    ) -> None:
        object.__setattr__(self, '_flat', flat)
        object.__setattr__(self, '_info', section_info)

    def _proxy(self, name: str) -> EntityProxy:
        info = object.__getattribute__(self, '_info')
        flat = object.__getattribute__(self, '_flat')
        return type(self).proxy_class(flat, info[name])

    def __getattr__(self, name: str) -> EntityProxy:
        if name.startswith('_'):
            raise AttributeError(name)
        info = object.__getattribute__(self, '_info')
        if name not in info:
            raise AttributeError(name)
        return self._proxy(name)

    def __getitem__(self, name: str) -> EntityProxy:
        info = object.__getattribute__(self, '_info')
        if name not in info:
            raise KeyError(name)
        return self._proxy(name)

    def __iter__(self) -> Iterator[tuple[str, EntityProxy]]:
        info = object.__getattribute__(self, '_info')
        return (
            (name, self._proxy(name))
            for name in type(self)._section_names
            if name in info
        )

    def __len__(self) -> int:
        return len(type(self)._section_names)

    def __contains__(self, name: str) -> bool:
        info = object.__getattribute__(self, '_info')
        return name in info

    def to_dict(self) -> dict:
        return {name: proxy.to_dict() for name, proxy in self}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_yaml(self) -> str:
        y = YAML()
        y.default_flow_style = False
        buf = StringIO()
        y.dump(self.to_dict(), buf)
        return buf.getvalue()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({type(self)._section_names!r})"
