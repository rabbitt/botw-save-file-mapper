"""Build a construct.Struct that covers every byte of the BotW Wii U save file.

Known offsets from the effectmap become typed named fields (f{offset:08x}).
Every gap — within identified clusters and between them — becomes a Bytes(n)
field that is parsed and built verbatim, guaranteeing bit-perfect round-trips
for all bytes that aren't explicitly written.

Field naming convention: f{offset:08x} for known fields, _g{cursor:08x} for gaps.
"""

from __future__ import annotations

from typing import Any

import construct as cs

FILE_SIZE = 1_027_200

# Module-level schema cache keyed by id(effectmap_raw dict).
# The default effectmap produces one schema that is reused for every SaveFile.
_schema_cache: dict[int, cs.Struct] = {}


def _collect_offsets(effectmap_raw: dict) -> list[tuple[int, int, str]]:
    """Walk the effectmap and return sorted [(offset, size, value_type), ...].

    When multiple keypaths share the same offset (e.g. .set / .unset),
    the first one encountered determines the field type — they all read/write
    the same construct field.
    """
    seen: dict[int, tuple[int, str]] = {}

    def walk(node: Any) -> None:
        if not isinstance(node, dict):
            return
        if "entries" in node:
            for e in node["entries"]:
                off = int(e["offset"])
                if off not in seen:
                    val = e["value"]
                    if val in ("ascii", "utf8"):
                        size = int(e.get("length") or 4)
                    else:
                        size = 4
                    type_str = str(val) if isinstance(val, str) else ("bool" if isinstance(val, bool) else "integer")
                    seen[off] = (size, type_str)
            return  # don't recurse into entry metadata
        for v in node.values():
            walk(v)

    walk(effectmap_raw)
    return sorted((off, sz, typ) for off, (sz, typ) in seen.items())


def build_file_struct(effectmap_raw: dict, file_size: int = FILE_SIZE) -> cs.Struct:
    """Build a construct.Struct covering all FILE_SIZE bytes of the save file.

    Every byte is accounted for: known offsets get named typed fields,
    all gaps become anonymous Bytes fields that round-trip unchanged.
    """
    entries = _collect_offsets(effectmap_raw)
    subcons: list = []
    cursor = 0

    for off, size, val_type in entries:
        if off < cursor:
            continue  # overlapping entry (same offset, different keypath) — skip

        gap = off - cursor
        if gap > 0:
            subcons.append(f"_g{cursor:08x}" / cs.Bytes(gap))

        field_name = f"f{off:08x}"
        if val_type in ("ascii", "utf8"):
            subcons.append(field_name / cs.Bytes(size))
        else:
            # All numeric fields (bool, integer, float) are raw uint32 on disk.
            # Float interpretation is handled by callers via codecs, not here.
            subcons.append(field_name / cs.Int32ub)

        cursor = off + size

    tail = file_size - cursor
    if tail > 0:
        subcons.append(f"_g{cursor:08x}" / cs.Bytes(tail))

    return cs.Struct(*subcons)


def get_file_struct(effectmap_raw: dict, file_size: int = FILE_SIZE) -> cs.Struct:
    """Return the cached construct.Struct for this effectmap, building if needed."""
    key = id(effectmap_raw)
    if key not in _schema_cache:
        _schema_cache[key] = build_file_struct(effectmap_raw, file_size)
    return _schema_cache[key]
