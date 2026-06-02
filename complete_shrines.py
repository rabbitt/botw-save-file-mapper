#!/usr/bin/env python3
"""
Complete all simple shrines and activate all towers in a BotW Wii U save file.

Writes flags directly to the binary save — no JSON intermediary, no Node.js.
Every write is gated through a dependency safety check against champion ability
danger keys before touching the file.

Simple shrine definition: exactly the keys {active, complete, found, pedestal}
(including their inverse forms inactive/incomplete/notfound).
Shrines with unearthed, ischampionsballad, monsterbase, or buried are skipped.

Usage:
    python complete_shrines.py game_data.sav
    python complete_shrines.py game_data.sav --dry-run
    python complete_shrines.py game_data.sav --shrines-only
    python complete_shrines.py game_data.sav --towers-only
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from botwsave import SaveFile, EffectMap, DependencyGraph
from botwsave._effectmap import DependencyResult


# Keys that definitively mark a shrine as non-simple
_COMPLEX_KEYS = frozenset({"unearthed", "ischampionsballad", "monsterbase", "monsterbaseconquered", "buried"})

# Shrine effectmap keys we actively set (positive flags only; inverses are excluded)
_SHRINE_SET_KEYS = ("found", "active", "complete", "pedestal.on")

# Meta-entries to skip (0 entries, aggregate-only)
_SHRINE_META = frozenset({"allchampionsballad", "allmainquest", "resurrection"})
_TOWER_META = frozenset({"all"})


def _is_simple_shrine(shrine_data: dict) -> bool:
    return not (set(shrine_data.keys()) & _COMPLEX_KEYS)


def _collect_shrine_flags(effectmap_raw: dict) -> list[str]:
    """Return ordered list of keypaths to set for all simple shrines."""
    shrines = effectmap_raw.get("shrines", {})
    flags = []
    for name, data in sorted(shrines.items()):
        if name in _SHRINE_META:
            continue
        if not _is_simple_shrine(data):
            continue
        for suffix in _SHRINE_SET_KEYS:
            flags.append(f"shrines.{name}.{suffix}")
    return flags


def _collect_tower_flags(effectmap_raw: dict) -> list[str]:
    """Return ordered list of keypaths to set for all towers."""
    towers = effectmap_raw.get("towers", {})
    flags = []
    for name, data in sorted(towers.items()):
        if name in _TOWER_META:
            continue
        if "active" not in data:
            continue
        for suffix in ("found", "active"):
            flags.append(f"towers.{name}.{suffix}")
    return flags


def _check_all_safe(flags: list[str], graph: DependencyGraph) -> tuple[list[str], list[DependencyResult]]:
    """Return (safe_flags, blocked_results). Blocked = any danger hits."""
    safe = []
    blocked = []
    for kp in flags:
        result = graph.check_safe(kp, include_soft=False)
        if result.is_safe:
            safe.append(kp)
        else:
            blocked.append(result)
    return safe, blocked


def _apply_flags(
    save: SaveFile,
    flags: list[str],
    dry_run: bool,
) -> tuple[int, int, int]:
    """Write flags, returning (written, skipped_already_set, errors)."""
    written = skipped = errors = 0
    for kp in flags:
        try:
            current = save.get_flag(kp)
            if current is True:
                skipped += 1
                continue
            if not dry_run:
                save.set_flag(kp, True, unsafe=False)
            written += 1
        except Exception as e:
            print(f"  ERROR {kp}: {e}", file=sys.stderr)
            errors += 1
    return written, skipped, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Complete all simple shrines and activate all towers in a BotW Wii U save.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("save_file", help="Path to game_data.sav")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing.")
    parser.add_argument("--shrines-only", action="store_true", help="Only process shrines.")
    parser.add_argument("--towers-only", action="store_true", help="Only process towers.")
    parser.add_argument("--effectmap", help="Path to effectmap YAML (default: bundled data).")
    args = parser.parse_args()

    save_path = Path(args.save_file)
    if not save_path.exists():
        print(f"Error: save file not found: {save_path}", file=sys.stderr)
        return 1

    em_path = Path(args.effectmap) if args.effectmap else None
    em = EffectMap(em_path) if em_path else EffectMap()
    graph = DependencyGraph(em)

    # Use raw dict to enumerate shrines/towers without instantiating every node
    em_raw = em._raw

    do_shrines = not args.towers_only
    do_towers = not args.shrines_only

    # Collect flags
    shrine_flags: list[str] = _collect_shrine_flags(em_raw) if do_shrines else []
    tower_flags: list[str] = _collect_tower_flags(em_raw) if do_towers else []
    all_flags = shrine_flags + tower_flags

    # Safety check — hard deps only (we bypass soft deps entirely)
    safe_flags, blocked = _check_all_safe(all_flags, graph)

    if blocked:
        print("SAFETY CHECK FAILED — the following flags would implicate danger keys:")
        for r in blocked:
            print(f"  {r.report()}")
        print("\nAborting. No changes were made.")
        return 2

    tag = "[DRY RUN] " if args.dry_run else ""
    print(f"{tag}Processing {len(safe_flags)} flags "
          f"({len(shrine_flags)} shrine, {len(tower_flags)} tower)")

    with SaveFile(save_path, effectmap=em, dry_run=args.dry_run) as save:
        shrine_written = shrine_skipped = shrine_errors = 0
        tower_written = tower_skipped = tower_errors = 0

        if shrine_flags:
            shrine_safe = [f for f in shrine_flags if f in set(safe_flags)]
            shrine_written, shrine_skipped, shrine_errors = _apply_flags(save, shrine_safe, args.dry_run)

        if tower_flags:
            tower_safe = [f for f in tower_flags if f in set(safe_flags)]
            tower_written, tower_skipped, tower_errors = _apply_flags(save, tower_safe, args.dry_run)

    # Summary
    print()
    print("=" * 52)
    action = "Would write" if args.dry_run else "Wrote"
    if do_shrines:
        print(f"  Shrines: {action} {shrine_written} flags  "
              f"(skipped {shrine_skipped} already set, {shrine_errors} errors)")
    if do_towers:
        print(f"  Towers:  {action} {tower_written} flags  "
              f"(skipped {tower_skipped} already set, {tower_errors} errors)")
    total_written = shrine_written + tower_written
    total_errors = shrine_errors + tower_errors
    print(f"  Total:   {action} {total_written} flags")
    if args.dry_run:
        print("\n  (no changes written — dry run)")
    print("=" * 52)

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
