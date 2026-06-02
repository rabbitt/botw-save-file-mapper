"""Item catalog: load per-category YAML files and match slot entries to item names."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    from ruamel.yaml import YAML as _YAML
    _yaml = _YAML()
    _yaml.preserve_quotes = True

    def _load_yaml(path: Path) -> dict:
        with path.open() as f:
            return dict(_yaml.load(f) or {})
except ImportError:
    import yaml as _yaml_fallback  # type: ignore
    def _load_yaml(path: Path) -> dict:
        return _yaml_fallback.safe_load(path.read_text()) or {}


_DATA_DIR = Path(__file__).parent / "data"

CATEGORIES = ("weapons", "bows", "arrows", "shields", "armor", "materials", "food", "keyitems")


@lru_cache(maxsize=None)
def get_catalog(category: str) -> dict[str, Any]:
    """Load and cache item catalog for a category."""
    if category not in CATEGORIES:
        raise ValueError(f"Unknown inventory category: {category!r}")
    return _load_yaml(_DATA_DIR / f"{category}.yaml")


def match_slot_entries(entries: list[dict], category: str) -> str | None:
    """Identify the item at a slot by matching its uint32 entry pattern.

    entries: list of {offset, value} dicts read from the slot (relative offsets).
    Returns the item name or None if no match.
    """
    catalog = get_catalog(category)
    for name, item_def in catalog.items():
        item_entries = item_def.get("entries", [])
        if not item_entries or len(entries) < len(item_entries):
            continue
        if all(
            item_entries[i]["offset"] == entries[i]["offset"]
            and item_entries[i]["value"] == entries[i]["value"]
            for i in range(len(item_entries))
        ):
            return name
    return None


def get_item_def(name: str, category: str) -> dict | None:
    """Return the catalog entry for a named item, or None if not found."""
    return get_catalog(category).get(name)


def write_entries_for(name: str, category: str) -> list[dict]:
    """Return the {offset, value} entry list that identifies this item in a slot."""
    item_def = get_item_def(name, category)
    if item_def is None:
        raise KeyError(f"{name!r} not found in {category} catalog")
    return list(item_def.get("entries", []))
