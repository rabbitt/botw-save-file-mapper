"""botwsave CLI — read, write, and export BotW Wii U save flags."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from ruamel.yaml import YAML

from .effectmap import EffectMap
from .save import SaveFile, FlagReadError, FlagWriteError
from .config import Config


def _open_save(ctx: click.Context, readonly: bool = False) -> SaveFile:
    save_path = ctx.obj.get("save_file")
    if not save_path:
        click.echo("Error: no save file specified (pass as first argument or set in config.yaml).", err=True)
        sys.exit(1)
    em_path = ctx.obj.get("effectmap_path")
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    dry_run = ctx.obj.get("dry_run", False)
    return SaveFile(save_path, effectmap=em, dry_run=dry_run, readonly=readonly)


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------

@click.group()
@click.argument("save_file", required=False)
@click.option("--effectmap", "effectmap_path", envvar="BOTWSAVE_EFFECTMAP",
              help="Path to effectmap YAML (default: bundled).")
@click.option("--dry-run", is_flag=True, default=False,
              help="Validate without writing anything.")
@click.pass_context
def cli(ctx: click.Context, save_file: str | None, effectmap_path: str | None, dry_run: bool) -> None:
    """botwsave — BotW Wii U save file editor.

    \b
    SAVE_FILE: path to game_data.sav
    """
    ctx.ensure_object(dict)
    cfg = Config.load(save_file=save_file, effectmap_path=effectmap_path, dry_run=dry_run)
    ctx.obj["save_file"] = cfg.save_file
    ctx.obj["effectmap_path"] = cfg.effectmap_path
    ctx.obj["dry_run"] = cfg.dry_run


# ---------------------------------------------------------------------------
# Flag commands
# ---------------------------------------------------------------------------

@cli.command("get")
@click.argument("keypath")
@click.pass_context
def get_flag(ctx: click.Context, keypath: str) -> None:
    """Read a flag value from the save file."""
    with _open_save(ctx, readonly=True) as save:
        try:
            click.echo(f"{keypath} = {save.get_flag(keypath)!r}")
        except FlagReadError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command("set")
@click.argument("keypath")
@click.argument("value")
@click.option("--unsafe", is_flag=True, default=False, help="Bypass danger-key check.")
@click.pass_context
def set_flag(ctx: click.Context, keypath: str, value: str, unsafe: bool) -> None:
    """Write a flag value to the save file."""
    parsed = _parse_value(value)
    with _open_save(ctx) as save:
        try:
            save.set_flag(keypath, parsed, unsafe=unsafe)
            action = "Would set" if save.dry_run else "Set"
            click.echo(f"{action}: {keypath} = {parsed!r}")
        except FlagWriteError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command("deps")
@click.argument("keypath")
@click.option("--no-soft", is_flag=True, default=False, help="Hard deps only.")
@click.option("--verbose", "-v", is_flag=True, default=False)
@click.pass_context
def deps(ctx: click.Context, keypath: str, no_soft: bool, verbose: bool) -> None:
    """Show the dependency graph for a flag (no save file needed)."""
    em_path = ctx.obj.get("effectmap_path")
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    from .effectmap import DependencyGraph
    result = DependencyGraph(em).check_safe(keypath, include_soft=not no_soft)
    click.echo(result.report(verbose=verbose))


@cli.command("check-safe")
@click.argument("keypaths", nargs=-1, required=True)
@click.option("--no-soft", is_flag=True, default=False)
@click.pass_context
def check_safe(ctx: click.Context, keypaths: tuple[str, ...], no_soft: bool) -> None:
    """Check whether setting keypaths would implicate any danger keys."""
    em_path = ctx.obj.get("effectmap_path")
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    from .effectmap import DependencyGraph
    graph = DependencyGraph(em)
    any_danger = False
    for kp in keypaths:
        result = graph.check_safe(kp, include_soft=not no_soft)
        click.echo(result.report(verbose=True))
        if not result.is_safe:
            any_danger = True
    sys.exit(1 if any_danger else 0)


@cli.command("search")
@click.argument("pattern")
@click.pass_context
def search(ctx: click.Context, pattern: str) -> None:
    """Search known keypaths by regex pattern."""
    em_path = ctx.obj.get("effectmap_path")
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    matches = em.search(pattern)
    if matches:
        click.echo("\n".join(matches))
    else:
        click.echo(f"No keypaths match {pattern!r}", err=True)


# ---------------------------------------------------------------------------
# Model commands
# ---------------------------------------------------------------------------

@cli.command("stats")
@click.option("--set-rupees", type=int, help="Set rupee count.")
@click.option("--set-hearts", type=float, help="Set heart containers (e.g. 13.0).")
@click.option("--set-stamina", type=float, help="Set stamina vessels (e.g. 2.0).")
@click.pass_context
def stats_cmd(ctx: click.Context, set_rupees: int | None, set_hearts: float | None,
              set_stamina: float | None) -> None:
    """Read (and optionally modify) player stats."""
    if set_rupees is None and set_hearts is None and set_stamina is None:
        with _open_save(ctx, readonly=True) as save:
            s = save.read_stats()
            click.echo(f"Shrines completed:  {s.shrinescompleted}")
            click.echo(f"Heart containers:   {s.heartcontainers}")
            click.echo(f"Hearts filled:      {s.heartsfilled}")
            click.echo(f"Stamina vessels:    {s.staminavessels}")
            click.echo(f"Rupees:             {s.rupees}")
    else:
        with _open_save(ctx) as save:
            s = save.read_stats()
            if set_rupees is not None:
                s.rupees = set_rupees
            if set_hearts is not None:
                s.heartcontainers = set_hearts
                s.heartsfilled = set_hearts
            if set_stamina is not None:
                s.staminavessels = set_stamina
            save.write_stats(s)
            click.echo("Stats updated.")


@cli.command("inventory")
@click.option("--json", "as_json", is_flag=True, default=False, help="Output as JSON.")
@click.pass_context
def inventory_cmd(ctx: click.Context, as_json: bool) -> None:
    """Read and display the current inventory."""
    with _open_save(ctx, readonly=True) as save:
        inv = save.read_inventory()
        if as_json:
            click.echo(json.dumps(inv.to_dict(), indent=2))
        else:
            click.echo(f"Weapons ({len(inv.weapons)}):   " + ", ".join(w.name for w in inv.weapons))
            click.echo(f"Bows    ({len(inv.bows)}):   " + ", ".join(b.name for b in inv.bows))
            click.echo(f"Arrows  ({len(inv.arrows)}):   " + ", ".join(f"{a.name}×{a.quantity}" for a in inv.arrows))
            click.echo(f"Shields ({len(inv.shields)}):   " + ", ".join(s.name for s in inv.shields))
            click.echo(f"Armor   ({len(inv.armor)}):   " + ", ".join(a.name for a in inv.armor))
            click.echo(f"Mats    ({len(inv.materials)}):   " + ", ".join(f"{m.name}×{m.quantity}" for m in inv.materials))
            click.echo(f"Food    ({len(inv.food)}):   " + ", ".join(f.name for f in inv.food))
            click.echo(f"Key     ({len(inv.keyitems)}):   " + ", ".join(k.name for k in inv.keyitems))


@cli.command("clock")
@click.pass_context
def clock_cmd(ctx: click.Context) -> None:
    """Read the in-game clock and blood moon counter."""
    with _open_save(ctx, readonly=True) as save:
        c = save.read_clock()
        click.echo(f"Time:              {c.time}")
        secs = c.bloodmoon.counter
        h, rem = divmod(int(secs), 3600)
        m, s = divmod(rem, 60)
        counter_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        click.echo(f"Blood moon timer:  {counter_str} ({secs:.3f}s)")
        click.echo(f"Blood moon tonight: {c.bloodmoon.tonight}")


# ---------------------------------------------------------------------------
# YAML export / import
# ---------------------------------------------------------------------------

@cli.command("export")
@click.argument("output", required=False)
@click.pass_context
def export_cmd(ctx: click.Context, output: str | None) -> None:
    """Export the full save to YAML.

    \b
    OUTPUT: destination path (default: stdout)
    """
    with _open_save(ctx, readonly=True) as save:
        data = save.export_yaml()
        if output:
            save.export_yaml(output)
            click.echo(f"Exported to {output}")
        else:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(data, sys.stdout)


@cli.command("import")
@click.argument("input_file")
@click.pass_context
def import_cmd(ctx: click.Context, input_file: str) -> None:
    """Import a save YAML (no soft-dependency cascade).

    \b
    INPUT_FILE: path to YAML exported by 'botwsave export'
    """
    with _open_save(ctx) as save:
        save.import_yaml(input_file)
        action = "Would import" if save.dry_run else "Imported"
        click.echo(f"{action}: {input_file}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_value(raw: str) -> bool | int | float | str:
    if raw.lower() in ("true", "yes", "on", "1"):
        return True
    if raw.lower() in ("false", "no", "off", "0"):
        return False
    try:
        return int(raw, 0)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def main() -> None:
    cli(obj={})
