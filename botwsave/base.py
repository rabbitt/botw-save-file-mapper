"""EntityProxy and EntityCollection — generic base classes for save entity wrappers.

EntityProxy wraps a parsed construct Container for a single save entity.
EntityCollection wraps a parsed construct Container for a section of entities.
"""

from __future__ import annotations

from typing import Iterator
import json
from io import StringIO

import construct as cs
from ruamel.yaml import YAML

from .codecs import bits_to_float, float_to_bits


class EntityProxy:
    """Wraps a parsed construct Container for a single save entity."""

    _float_fields: frozenset[str] = frozenset()
    _ascii_fields: frozenset[str] = frozenset()
    _utf8_fields: frozenset[str] = frozenset()

    def __init__(self, container: cs.Container) -> None:
        object.__setattr__(self, '_c', container)

    @property
    def _fields(self) -> list[str]:
        c = object.__getattribute__(self, '_c')
        return [k for k in c.keys() if not k.startswith('_')]

    def __getattr__(self, name: str):
        c = object.__getattribute__(self, '_c')
        if name.startswith('_') or name not in c:
            raise AttributeError(name)
        raw = c[name]
        if name in object.__getattribute__(self, '_float_fields'):
            return bits_to_float(raw)
        if name in object.__getattribute__(self, '_ascii_fields'):
            return raw.rstrip(b'\x00').decode('ascii', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        if name in object.__getattribute__(self, '_utf8_fields'):
            return raw.rstrip(b'\x00').decode('utf-8', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        return raw

    def __setattr__(self, name: str, value) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        c = object.__getattribute__(self, '_c')
        if name not in c:
            object.__setattr__(self, name, value)
            return
        if name in object.__getattribute__(self, '_float_fields'):
            c[name] = float_to_bits(float(value))
        elif name in object.__getattribute__(self, '_ascii_fields'):
            length = len(c[name])
            encoded = str(value).encode('ascii', errors='replace')[:length]
            c[name] = encoded + b'\x00' * (length - len(encoded))
        elif name in object.__getattribute__(self, '_utf8_fields'):
            length = len(c[name])
            encoded = str(value).encode('utf-8', errors='replace')[:length]
            c[name] = encoded + b'\x00' * (length - len(encoded))
        else:
            existing = c[name]
            new_int = int(value)
            # Preserve the game's exact raw value when the logical state is already
            # correct (game sometimes writes 2, 3, 5, 0xa, etc. for "true").
            if isinstance(existing, int) and bool(new_int) == bool(existing):
                return
            c[name] = new_int

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
    """Wraps a parsed construct Container for a section (collection of entities)."""

    proxy_class: type[EntityProxy] = EntityProxy
    _section_names: list[str] = []  # override in subclasses

    def __init__(self, container: cs.Container) -> None:
        object.__setattr__(self, '_c', container)

    def __getattr__(self, name: str) -> EntityProxy:
        if name.startswith('_'):
            raise AttributeError(name)
        c = object.__getattribute__(self, '_c')
        if name not in c:
            raise AttributeError(name)
        cls = type(self).proxy_class
        return cls(c[name])

    def __getitem__(self, name: str) -> EntityProxy:
        c = object.__getattribute__(self, '_c')
        return type(self).proxy_class(c[name])

    def __iter__(self) -> Iterator[tuple[str, EntityProxy]]:
        c = object.__getattribute__(self, '_c')
        cls = type(self).proxy_class
        return ((name, cls(c[name])) for name in type(self)._section_names if name in c)

    def __len__(self) -> int:
        return len(type(self)._section_names)

    def __contains__(self, name: str) -> bool:
        return name in type(self)._section_names

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
