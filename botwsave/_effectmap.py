"""EffectMap: load the effect map YAML and resolve keypaths and dependencies."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


try:
    from ruamel.yaml import YAML
    _yaml = YAML()
    _yaml.preserve_quotes = True

    def _load_yaml(path: Path) -> Any:
        with path.open() as f:
            return _yaml.load(f)

except ImportError:
    import yaml  # type: ignore

    def _load_yaml(path: Path) -> Any:
        with path.open() as f:
            return yaml.safe_load(f)


_DATA_DIR = Path(__file__).parent / "data"


@dataclass
class Entry:
    offset: int
    value: bool | int | float | str  # True/False = boolean; str = 'float'/'integer'/'ascii'/'utf8'
    unit: str | None = None


@dataclass
class EffectNode:
    """A single leaf node in the effect map (a flag that can be set)."""
    keypath: str
    entries: list[Entry]
    hard_deps: list[str] = field(default_factory=list)
    soft_deps: list[str] = field(default_factory=list)
    rewards: list[dict] = field(default_factory=list)

    @property
    def is_boolean(self) -> bool:
        return all(isinstance(e.value, bool) for e in self.entries)

    @property
    def value_type(self) -> str:
        if not self.entries:
            return "none"
        v = self.entries[0].value
        if isinstance(v, bool):
            return "boolean"
        if isinstance(v, str):
            return v  # 'float', 'integer', 'ascii', 'utf8'
        return "integer"


class EffectMap:
    """Loaded effect map with keypath lookup."""

    def __init__(self, path: Path | None = None):
        self._path = path or (_DATA_DIR / "effectmap.yaml")
        self._raw: dict = _load_yaml(self._path)
        self._cache: dict[str, EffectNode] = {}
        self._all_keys: list[str] | None = None

    def _resolve_raw(self, keypath: str) -> dict | None:
        parts = re.split(r"[./]", keypath.lower())
        node = self._raw
        for part in parts:
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        return node if isinstance(node, dict) else None

    def get(self, keypath: str) -> EffectNode | None:
        if keypath in self._cache:
            return self._cache[keypath]

        raw = self._resolve_raw(keypath)
        if raw is None or "entries" not in raw:
            return None

        entries = [
            Entry(
                offset=e["offset"],
                value=e["value"],
                unit=e.get("unit"),
            )
            for e in raw["entries"]
        ]

        node = EffectNode(
            keypath=keypath,
            entries=entries,
            hard_deps=list(raw.get("harddependencies", [])),
            soft_deps=list(raw.get("softdependencies", [])),
            rewards=list(raw.get("rewards", [])),
        )
        self._cache[keypath] = node
        return node

    def all_keypaths(self) -> list[str]:
        if self._all_keys is not None:
            return self._all_keys

        paths: list[str] = []

        def walk(node: Any, prefix: str) -> None:
            if not isinstance(node, dict):
                return
            if "entries" in node:
                paths.append(prefix)
                # also walk sub-dicts that aren't metadata keys
                for k, v in node.items():
                    if k not in ("entries", "harddependencies", "softdependencies", "rewards", "unit"):
                        walk(v, f"{prefix}.{k}")
            else:
                for k, v in node.items():
                    walk(v, f"{prefix}.{k}" if prefix else k)

        walk(self._raw, "")
        self._all_keys = [p.lstrip(".") for p in paths]
        return self._all_keys

    def search(self, pattern: str) -> list[str]:
        regex = re.compile(pattern, re.IGNORECASE)
        return [k for k in self.all_keypaths() if regex.search(k)]


@dataclass
class DependencyResult:
    keypath: str
    hard_deps: list[str]
    soft_deps: list[str]
    danger_hits: list[str]

    @property
    def is_safe(self) -> bool:
        return len(self.danger_hits) == 0

    def report(self, verbose: bool = False) -> str:
        lines = [f"Flag: {self.keypath}"]
        if self.hard_deps:
            lines.append(f"  Hard deps ({len(self.hard_deps)}): {', '.join(self.hard_deps)}")
        if self.soft_deps:
            lines.append(f"  Soft deps ({len(self.soft_deps)}): {', '.join(self.soft_deps)}")
        if self.danger_hits:
            lines.append(f"  DANGER — would implicate: {', '.join(self.danger_hits)}")
        elif verbose:
            lines.append("  Safe (no danger keys implicated)")
        return "\n".join(lines)


class DependencyGraph:
    """Resolves transitive hard and soft dependencies for a set of keypaths."""

    DEFAULT_DANGER_KEYS = frozenset({
        "championpowers.revalisgale.plus.set",
        "championpowers.daruksprotection.plus.set",
        "championpowers.urbosasfury.plus.set",
        "championpowers.miphasgrace.plus.set",
        "mainquests.freethedivinebeasts.complete.set",
        "mainquests.thechampionsballad.begun.set",
    })
    _CHAMPION_SONG_RE = re.compile(r"^mainquests\.champion\w+\.complete\.set$")

    def __init__(self, effectmap: EffectMap, danger_keys: frozenset[str] | None = None):
        self._em = effectmap
        self._danger = danger_keys if danger_keys is not None else self.DEFAULT_DANGER_KEYS

    def _is_danger(self, keypath: str) -> bool:
        return keypath in self._danger or bool(self._CHAMPION_SONG_RE.match(keypath))

    def resolve(
        self,
        keypath: str,
        *,
        include_soft: bool = True,
        _seen: frozenset[str] | None = None,
    ) -> tuple[set[str], set[str]]:
        """Return (hard_deps, soft_deps) transitively reachable from keypath."""
        if _seen is None:
            _seen = frozenset()
        if keypath in _seen:
            return set(), set()

        node = self._em.get(keypath)
        if node is None:
            return set(), set()

        seen = _seen | {keypath}
        hard: set[str] = set(node.hard_deps)
        soft: set[str] = set(node.soft_deps) if include_soft else set()

        for dep in list(hard):
            if dep not in seen:
                sub_hard, sub_soft = self.resolve(dep, include_soft=include_soft, _seen=seen)
                hard |= sub_hard
                soft |= sub_soft
                seen |= sub_hard | sub_soft | {dep}

        if include_soft:
            for dep in list(soft):
                if dep not in seen:
                    sub_hard, sub_soft = self.resolve(dep, include_soft=include_soft, _seen=seen)
                    hard |= sub_hard
                    soft |= sub_soft
                    seen |= sub_hard | sub_soft | {dep}

        hard.discard(keypath)
        soft.discard(keypath)
        return hard, soft

    def check_safe(
        self,
        keypath: str,
        *,
        include_soft: bool = True,
    ) -> DependencyResult:
        """Check whether setting keypath would implicate any danger keys."""
        hard, soft = self.resolve(keypath, include_soft=include_soft)
        all_deps = hard | soft
        danger_hits = sorted(k for k in all_deps if self._is_danger(k))
        return DependencyResult(
            keypath=keypath,
            hard_deps=sorted(hard),
            soft_deps=sorted(soft),
            danger_hits=danger_hits,
        )

    def what_would_change(
        self,
        keypaths: list[str],
        *,
        include_soft: bool = True,
    ) -> dict[str, DependencyResult]:
        """For each keypath, return its full dependency resolution."""
        return {kp: self.check_safe(kp, include_soft=include_soft) for kp in keypaths}
