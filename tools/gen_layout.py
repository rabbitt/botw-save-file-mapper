#!/usr/bin/env python3
"""Generate botwsave/_layout.py from botwsave/data/effectmap.yaml.

Run from the project root:
    python tools/gen_layout.py
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

# Allow running from repo root without installing the package.
sys.path.insert(0, str(Path(__file__).parent.parent))

from ruamel.yaml import YAML

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
EFFECTMAP_PATH = REPO_ROOT / "botwsave" / "data" / "effectmap.yaml"
OUTPUT_PATH = REPO_ROOT / "botwsave" / "_layout.py"

# ---------------------------------------------------------------------------
# Sections we want to emit (in order).  Each entry is (section_key, pretty_label)
# ---------------------------------------------------------------------------
SECTIONS_TO_EMIT = [
    ("shrines",        "Shrines"),
    ("towers",         "Towers"),
    ("memories",       "Memories"),
    ("divinebeasts",   "Divine Beasts"),
    ("fairyfountains", "Fairy Fountains"),
    ("ancienttechlabs","Ancient Tech Labs"),
    ("cutscenes",      "Cutscenes"),
    ("horses",         "Horses"),
    ("npcs",           "NPCs"),
    ("runes",          "Runes"),
    ("sheikahslate",   "Sheikah Slate"),
    ("quicktips",      "Quick Tips"),
    ("sidequests",     "Side Quests"),
    ("mainquests",     "Main Quests"),
    ("championpowers", "Champion Powers"),
    ("towns",          "Towns"),
    ("mastersword",    "Master Sword"),
]

# For sections not in the above list that happen to appear in the yaml,
# we skip them — they're too complex or not entity-collections.

HORSE_SECTION_KEY = "horses"

# ---------------------------------------------------------------------------
# Value-type helpers
# ---------------------------------------------------------------------------

def _infer_val_type(val) -> str | None:
    """Return val_type string or None if not representable."""
    if isinstance(val, bool):
        if val is True:
            return "bool"
        # val is False → inverse alias — caller should skip
        return None
    if val == "float":
        return "float"
    if val == "integer":
        return "integer"
    if isinstance(val, int):
        return "integer"
    if val == "ascii":
        return "ascii"
    if val == "utf8":
        return "utf8"
    return None


def _subcon(val_type: str, length: int | None) -> str:
    if val_type in ("bool", "integer", "float"):
        return "cs.Int32ub"
    if val_type == "ascii":
        return f"cs.Bytes({length or 32})"
    if val_type == "utf8":
        return f"cs.Bytes({length or 64})"
    return "cs.Int32ub"


# ---------------------------------------------------------------------------
# Field extraction
# ---------------------------------------------------------------------------

def collect_entity_fields(entity: dict) -> dict[str, tuple[int, str, int | None]]:
    """Extract {field_name: (offset, val_type, length)} for an entity dict.

    Returns fields in insertion order (first seen wins for duplicate offsets).
    """
    result: dict[str, tuple[int, str, int | None]] = {}
    seen_offsets: set[int] = set()

    for flag_key, flag_val in entity.items():
        if not isinstance(flag_val, dict):
            continue

        if "entries" in flag_val:
            # Direct flag (e.g. active, complete, found, pedestal.on/off at top level)
            entries = flag_val["entries"]
            if not entries:
                continue
            entry = entries[0]
            val = entry.get("value")
            # Skip inverse aliases (value is False)
            if val is False:
                continue
            val_type = _infer_val_type(val)
            if val_type is None:
                continue
            offset = int(entry["offset"])
            if offset in seen_offsets:
                continue
            length = entry.get("length")
            result[flag_key] = (offset, val_type, length)
            seen_offsets.add(offset)

        else:
            # Nested flag group (e.g. pedestal.on/off, camera.direction.east/...)
            # Use parent flag_key as field name, find first sub-entry where value is not False
            found_entry = None
            for sub_key, sub_val in flag_val.items():
                if not isinstance(sub_val, dict):
                    continue
                if "entries" not in sub_val:
                    continue
                entries = sub_val["entries"]
                if not entries:
                    continue
                entry = entries[0]
                val = entry.get("value")
                if val is False:
                    continue
                # Found a good sub-entry
                found_entry = entry
                break

            if found_entry is None:
                continue
            val = found_entry.get("value")
            val_type = _infer_val_type(val)
            if val_type is None:
                continue
            offset = int(found_entry["offset"])
            if offset in seen_offsets:
                continue
            length = found_entry.get("length")
            result[flag_key] = (offset, val_type, length)
            seen_offsets.add(offset)

    return result


def collect_entity_fields_horses(entity: dict) -> dict[str, tuple[int, str, int | None]]:
    """Like collect_entity_fields but skip ascii/utf8 fields (stride-8 strings)."""
    fields = collect_entity_fields(entity)
    return {
        k: v for k, v in fields.items()
        if v[1] not in ("ascii", "utf8")
    }


# ---------------------------------------------------------------------------
# Code generation helpers
# ---------------------------------------------------------------------------

def _align(names: list[str]) -> int:
    """Width for aligning the '/' in construct field definitions."""
    return max((len(n) for n in names), default=0) if names else 0


def _emit_entity_struct(entity_name: str, fields: dict[str, tuple[int, str, int | None]]) -> str:
    """Return lines like:  "entity_name" / cs.Struct(...)"""
    if not fields:
        return ""
    field_names = list(fields.keys())
    col = _align(field_names)
    lines = [f'    "{entity_name}" / cs.Struct(']
    for fname, (offset, val_type, length) in fields.items():
        subcon = _subcon(val_type, length)
        pad = " " * (col - len(fname))
        lines.append(f'        "{fname}"{pad} / cs.Pointer({offset}, {subcon}),')
    lines.append("    ),")
    return "\n".join(lines)


def _emit_section(
    section_key: str,
    section_label: str,
    section_data: dict,
    is_horses: bool = False,
) -> tuple[str, list[str], frozenset[str], dict[str, frozenset[str]]]:
    """Return (code_block, entity_names, simple_set, extra_keys_dict).

    simple_set and extra_keys_dict are only meaningful for shrines.
    """
    STANDARD_KEYS = frozenset({"active", "complete", "found", "pedestal"})
    SHRINE_STD = frozenset({"active", "complete", "found", "pedestal"})

    entity_names: list[str] = []
    entity_blocks: list[str] = []
    simple_set: set[str] = set()
    extra_keys_dict: dict[str, frozenset[str]] = {}

    for entity_name, entity_val in section_data.items():
        if not isinstance(entity_val, dict):
            continue
        # Skip meta/aggregate entities (ones with all-empty entries)
        if is_horses:
            fields = collect_entity_fields_horses(entity_val)
        else:
            fields = collect_entity_fields(entity_val)
        if not fields:
            continue

        entity_names.append(entity_name)
        block = _emit_entity_struct(entity_name, fields)
        entity_blocks.append(block)

        # Shrine-specific bookkeeping
        if section_key == "shrines":
            fkeys = frozenset(fields.keys())
            extra = fkeys - SHRINE_STD
            if not extra:
                simple_set.add(entity_name)
            else:
                extra_keys_dict[entity_name] = extra

    if not entity_names:
        return ("", [], frozenset(), {})

    prefix = section_key.upper().replace(".", "_")
    layout_var = f"{prefix}_LAYOUT"
    names_var = f"{prefix}_NAMES"

    # Section header comment
    dashes = "─" * (76 - len(section_label) - 4)
    header = f"# ── {section_label} {dashes}"

    lines: list[str] = [header, ""]
    lines.append(f"{layout_var} = cs.Struct(")
    for block in entity_blocks:
        lines.append(block)
    lines.append(")")
    lines.append("")
    names_list = ", ".join(f'"{n}"' for n in entity_names)
    lines.append(f'{names_var}: list[str] = [{names_list}]')

    # Shrine extras
    if section_key == "shrines":
        simple_sorted = sorted(simple_set)
        extra_sorted = dict(sorted(extra_keys_dict.items()))

        simple_str = ", ".join(f'"{n}"' for n in simple_sorted)
        lines.append(f"")
        lines.append(f"SHRINE_SIMPLE: frozenset[str] = frozenset({{{simple_str}}})")

        lines.append(f"")
        lines.append("SHRINE_EXTRA_KEYS: dict[str, frozenset[str]] = {")
        for ename, ekeys in extra_sorted.items():
            ks = ", ".join(f'"{k}"' for k in sorted(ekeys))
            lines.append(f'    "{ename}": frozenset({{{ks}}}),')
        lines.append("}")

    # Horse extras comment
    if section_key == "horses":
        lines.insert(1, "# NOTE: stride-8 string fields (name/type/saddle/reins/mane) are excluded.")
        lines.insert(2, "# Only bond (float), color (integer), and selected.slot are mapped here.")
        lines.insert(3, "# Stub: HorseProxy.name / .type / .saddle / .reins / .mane raise NotImplementedError.")
        lines.insert(4, "")

    return ("\n".join(lines), entity_names, frozenset(simple_set), extra_keys_dict)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    yaml = YAML()
    effectmap: dict = yaml.load(EFFECTMAP_PATH.read_text())

    output_parts: list[str] = [
        "# AUTO-GENERATED from botwsave/data/effectmap.yaml — do not edit by hand.",
        "# Regenerate with: python tools/gen_layout.py",
        "# fmt: off",
        "",
        "from __future__ import annotations",
        "import construct as cs",
        "",
    ]

    layouts_entries: list[str] = []
    names_entries: list[str] = []

    summary: dict[str, int] = {}

    for section_key, section_label in SECTIONS_TO_EMIT:
        section_data = effectmap.get(section_key)
        if not section_data or not isinstance(section_data, dict):
            continue

        is_horses = (section_key == HORSE_SECTION_KEY)
        code_block, entity_names, simple_set, extra_keys = _emit_section(
            section_key, section_label, section_data, is_horses=is_horses
        )

        if not entity_names:
            continue

        output_parts.append(code_block)
        output_parts.append("")

        prefix = section_key.upper().replace(".", "_")
        layout_var = f"{prefix}_LAYOUT"
        names_var = f"{prefix}_NAMES"
        layouts_entries.append(f'    "{section_key}": {layout_var},')
        names_entries.append(f'    "{section_key}": {names_var},')

        summary[section_key] = len(entity_names)

    # Registry
    output_parts.append("# ── Registry " + "─" * 64)
    output_parts.append("")
    output_parts.append("LAYOUTS: dict[str, cs.Struct] = {")
    output_parts.extend(layouts_entries)
    output_parts.append("}")
    output_parts.append("")
    output_parts.append("NAMES: dict[str, list[str]] = {")
    output_parts.extend(names_entries)
    output_parts.append("}")
    output_parts.append("")

    # Compatibility aliases: SHRINE_LAYOUT / SHRINE_NAMES, TOWER_LAYOUT / TOWER_NAMES, etc.
    # (singular / short form for use by entities.py and external callers)
    SINGULAR_MAP = {
        "shrines":        "SHRINE",
        "towers":         "TOWER",
        "memories":       "MEMORY",
        "divinebeasts":   "DIVINEBEAST",
        "fairyfountains": "FAIRYFOUNTAIN",
        "ancienttechlabs":"ANCIENTTECHLAB",
        "cutscenes":      "CUTSCENE",
        "horses":         "HORSE",
        "npcs":           "NPC",
        "runes":          "RUNE",
        "sheikahslate":   "SHEIKAHSLATE",
        "quicktips":      "QUICKTIP",
        "sidequests":     "SIDEQUEST",
        "mainquests":     "MAINQUEST",
        "championpowers": "CHAMPIONPOWER",
        "towns":          "TOWN",
        "mastersword":    "MASTERSWORD",
    }
    output_parts.append("# ── Compatibility aliases (singular / short form) " + "─" * 28)
    output_parts.append("")
    for section_key, _section_label in SECTIONS_TO_EMIT:
        if section_key not in summary:
            continue
        prefix = section_key.upper().replace(".", "_")  # e.g. SHRINES
        layout_var = f"{prefix}_LAYOUT"
        names_var = f"{prefix}_NAMES"
        short = SINGULAR_MAP.get(section_key, prefix)
        if short != prefix:
            short_layout = f"{short}_LAYOUT"
            short_names  = f"{short}_NAMES"
            output_parts.append(f"{short_layout} = {layout_var}")
            output_parts.append(f"{short_names}: list[str] = {names_var}")
    output_parts.append("")

    content = "\n".join(output_parts)
    OUTPUT_PATH.write_text(content)

    print(f"Written {OUTPUT_PATH}")
    print(f"Sections generated: {len(summary)}")
    for section_key, count in summary.items():
        print(f"  {section_key}: {count} entities")


if __name__ == "__main__":
    main()
