#!/usr/bin/env python3
"""Generate botwsave/_layout.py from botwsave/data/effectmap.yaml.

Run from the project root:
    python tools/gen_layout.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).parent.parent
EFFECTMAP_PATH = REPO_ROOT / "botwsave" / "data" / "effectmap.yaml"
OUTPUT_PATH = REPO_ROOT / "botwsave" / "_layout.py"

ENTITY_SECTIONS = [
    ("shrines",         "Shrines"),
    ("towers",          "Towers"),
    ("memories",        "Memories"),
    ("divinebeasts",    "Divine Beasts"),
    ("fairyfountains",  "Fairy Fountains"),
    ("ancienttechlabs", "Ancient Tech Labs"),
    ("cutscenes",       "Cutscenes"),
    ("horses",          "Horses"),
    ("npcs",            "NPCs"),
    ("runes",           "Runes"),
    ("sheikahslate",    "Sheikah Slate"),
    ("quicktips",       "Quick Tips"),
    ("sidequests",      "Side Quests"),
    ("mainquests",      "Main Quests"),
    ("championpowers",  "Champion Powers"),
    ("towns",           "Towns"),
    ("mastersword",     "Master Sword"),
]


# ---------------------------------------------------------------------------
# Value-type inference
# ---------------------------------------------------------------------------

def _infer_val_type(val) -> str | None:
    """Return val_type string, or None if the entry should be skipped."""
    if val is True:
        return "bool"
    if val is False:
        return None          # inverse alias — skip
    if val == "float":
        return "float"
    if val == "integer":
        return "integer"
    if isinstance(val, int):
        return "sentinel"    # enum literal (camera direction, runes.alldisabled, …)
    if val == "ascii":
        return "ascii"
    if val == "utf8":
        return "utf8"
    return None


# ---------------------------------------------------------------------------
# Pass 1: collect every unique offset → (val_type, length) from entire map
# ---------------------------------------------------------------------------

def collect_all_offsets(effectmap: dict) -> dict[int, tuple[str, int | None]]:
    """Walk all sections; return {offset: (val_type, length)}.

    Skips inverse aliases (value=False) and horse stride-8 strings.
    First occurrence of each offset wins.
    """
    result: dict[int, tuple[str, int | None]] = {}

    def _walk(node: object, is_horse: bool = False) -> None:
        if not isinstance(node, dict):
            return
        if "entries" in node:
            for entry in node["entries"]:
                raw_offset = entry.get("offset")
                if raw_offset is None:
                    continue
                val = entry.get("value")
                val_type = _infer_val_type(val)
                if val_type is None:
                    continue
                if is_horse and val_type in ("ascii", "utf8"):
                    continue   # stride-8 strings not yet supported
                offset = int(raw_offset)
                if offset not in result:
                    result[offset] = (val_type, entry.get("length"))
        else:
            for v in node.values():
                if isinstance(v, dict):
                    _walk(v, is_horse)

    for section_key, section_data in effectmap.items():
        _walk(section_data, is_horse=(section_key == "horses"))

    return result


# ---------------------------------------------------------------------------
# Pass 2: collect per-entity field info for entity sections
# ---------------------------------------------------------------------------

def collect_entity_section_info(
    section_key: str, section_data: dict
) -> dict[str, dict[str, tuple[int, str, int | None]]]:
    """Return {entity_name: {field_name: (offset, val_type, length)}}."""
    is_horse = section_key == "horses"
    result: dict[str, dict[str, tuple[int, str, int | None]]] = {}

    for entity_name, entity_val in section_data.items():
        if not isinstance(entity_val, dict):
            continue

        fields: dict[str, tuple[int, str, int | None]] = {}
        seen_offsets: set[int] = set()

        for flag_key, flag_val in entity_val.items():
            if not isinstance(flag_val, dict):
                continue

            if "entries" in flag_val:
                # Direct flag: entity.flag_key
                entry = flag_val["entries"][0] if flag_val["entries"] else None
                if entry is None:
                    continue
                val = entry.get("value")
                val_type = _infer_val_type(val)
                if val_type is None:
                    continue
                if is_horse and val_type in ("ascii", "utf8"):
                    continue
                offset = int(entry["offset"])
                if offset in seen_offsets:
                    continue
                fields[flag_key] = (offset, val_type, entry.get("length"))
                seen_offsets.add(offset)

            else:
                # Nested group (pedestal.on/off, plus.set/unset, …).
                # Use the parent flag_key as field name; first non-skip sub-entry wins.
                for sub_val in flag_val.values():
                    if not isinstance(sub_val, dict) or "entries" not in sub_val:
                        continue
                    entries = sub_val["entries"]
                    if not entries:
                        continue
                    entry = entries[0]
                    val = entry.get("value")
                    val_type = _infer_val_type(val)
                    if val_type is None:
                        continue
                    if is_horse and val_type in ("ascii", "utf8"):
                        continue
                    offset = int(entry["offset"])
                    if offset in seen_offsets:
                        continue
                    fields[flag_key] = (offset, val_type, entry.get("length"))
                    seen_offsets.add(offset)
                    break

        if fields:
            result[entity_name] = fields

    return result


# ---------------------------------------------------------------------------
# Code emitters
# ---------------------------------------------------------------------------

def emit_flat_layout(offsets: dict[int, tuple[str, int | None]]) -> str:
    """Emit FLAT_LAYOUT = cs.Struct(...)."""
    lines = ["FLAT_LAYOUT = cs.Struct("]
    for offset in sorted(offsets):
        val_type, length = offsets[offset]
        if val_type in ("ascii", "utf8"):
            n = length or (32 if val_type == "ascii" else 64)
            subcon = f"cs.Bytes({n})"
        else:
            subcon = "cs.Int32ub"
        lines.append(f'    "off{offset}" / cs.Pointer({offset}, {subcon}),')
    lines.append(")")
    return "\n".join(lines)


def emit_entity_field_info(
    entity_sections: dict[str, dict[str, dict[str, tuple[int, str, int | None]]]]
) -> str:
    """Emit ENTITY_FIELD_INFO = {...}."""
    lines = ["ENTITY_FIELD_INFO: dict[str, dict[str, dict[str, tuple]]] = {"]
    for section_key, section_info in entity_sections.items():
        if not section_info:
            continue
        lines.append(f'    "{section_key}": {{')
        for entity_name, fields in section_info.items():
            lines.append(f'        "{entity_name}": {{')
            for field_name, (offset, val_type, length) in fields.items():
                lines.append(
                    f'            "{field_name}": ({offset}, "{val_type}", {length!r}),'
                )
            lines.append("        },")
        lines.append("    },")
    lines.append("}")
    return "\n".join(lines)


def emit_names(
    entity_sections: dict[str, dict[str, dict]]
) -> str:
    """Emit NAMES = {...}."""
    lines = ["NAMES: dict[str, list[str]] = {"]
    for section_key, section_info in entity_sections.items():
        names_str = ", ".join(f'"{n}"' for n in section_info)
        lines.append(f'    "{section_key}": [{names_str}],')
    lines.append("}")
    return "\n".join(lines)


def emit_shrine_extras(shrine_info: dict[str, dict[str, tuple]]) -> str:
    """Emit SHRINE_SIMPLE and SHRINE_EXTRA_KEYS."""
    STANDARD = frozenset({"active", "complete", "found", "pedestal"})
    simple: set[str] = set()
    extra_keys: dict[str, frozenset[str]] = {}

    for entity_name, fields in shrine_info.items():
        fkeys = frozenset(fields)
        extra = fkeys - STANDARD
        if not extra:
            simple.add(entity_name)
        else:
            extra_keys[entity_name] = extra

    simple_str = ", ".join(f'"{n}"' for n in sorted(simple))
    lines = [
        f"SHRINE_SIMPLE: frozenset[str] = frozenset({{{simple_str}}})",
        "",
        "SHRINE_EXTRA_KEYS: dict[str, frozenset[str]] = {",
    ]
    for ename, ekeys in sorted(extra_keys.items()):
        ks = ", ".join(f'"{k}"' for k in sorted(ekeys))
        lines.append(f'    "{ename}": frozenset({{{ks}}}),')
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    yaml = YAML()
    effectmap: dict = yaml.load(EFFECTMAP_PATH.read_text())

    all_offsets = collect_all_offsets(effectmap)

    entity_sections: dict[str, dict] = {}
    for section_key, _ in ENTITY_SECTIONS:
        section_data = effectmap.get(section_key)
        if section_data and isinstance(section_data, dict):
            info = collect_entity_section_info(section_key, section_data)
            if info:
                entity_sections[section_key] = info

    parts = [
        "# AUTO-GENERATED from botwsave/data/effectmap.yaml — do not edit by hand.",
        "# Regenerate with: python tools/gen_layout.py",
        "# fmt: off",
        "",
        "from __future__ import annotations",
        "import construct as cs",
        "",
        "# ── Flat layout (one Pointer field per unique offset) ──────────────────────",
        "",
        emit_flat_layout(all_offsets),
        "",
        "# ── Entity field info (section → entity → field → (offset, val_type, len)) ─",
        "",
        emit_entity_field_info(entity_sections),
        "",
        "# ── Section names ──────────────────────────────────────────────────────────",
        "",
        emit_names(entity_sections),
        "",
        "# ── Shrine extras ──────────────────────────────────────────────────────────",
        "",
        emit_shrine_extras(entity_sections.get("shrines", {})),
        "",
    ]

    OUTPUT_PATH.write_text("\n".join(parts))

    print(f"Written {OUTPUT_PATH}")
    print(f"Unique offsets in FLAT_LAYOUT: {len(all_offsets)}")
    for section_key, info in entity_sections.items():
        print(f"  {section_key}: {len(info)} entities")


if __name__ == "__main__":
    main()
