"""botwsave CLI — read and write BotW Wii U save flags."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from ._effectmap import EffectMap
from ._save import SaveFile, FlagReadError, FlagWriteError
from ._config import Config


def _make_save(ctx: click.Context, path: str, dry_run: bool, readonly: bool = False) -> SaveFile:
    em_path = ctx.obj.get("effectmap_path") if ctx.obj else None
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    return SaveFile(path, effectmap=em, dry_run=dry_run, readonly=readonly)


@click.group()
@click.argument("save_file", required=False)
@click.option("--effectmap", "effectmap_path", envvar="BOTWSAVE_EFFECTMAP", help="Path to effectmap YAML.")
@click.option("--dry-run", is_flag=True, default=False, help="Parse and validate without writing.")
@click.pass_context
def cli(ctx: click.Context, save_file: str | None, effectmap_path: str | None, dry_run: bool) -> None:
    """botwsave — BotW Wii U save file editor.\n\nSAVE_FILE: path to game_data.sav"""
    ctx.ensure_object(dict)
    cfg = Config.load(
        save_file=save_file,
        effectmap_path=effectmap_path,
        dry_run=dry_run,
    )
    ctx.obj["save_file"] = cfg.save_file
    ctx.obj["effectmap_path"] = cfg.effectmap_path
    ctx.obj["dry_run"] = cfg.dry_run


@cli.command("get")
@click.argument("keypath")
@click.pass_context
def get_flag(ctx: click.Context, keypath: str) -> None:
    """Read a flag value from the save file."""
    save_path = ctx.obj.get("save_file")
    if not save_path:
        click.echo("Error: no save file specified.", err=True)
        sys.exit(1)

    with _make_save(ctx, save_path, dry_run=False, readonly=True) as save:
        try:
            val = save.get_flag(keypath)
            click.echo(f"{keypath} = {val!r}")
        except FlagReadError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command("set")
@click.argument("keypath")
@click.argument("value")
@click.option("--unsafe", is_flag=True, default=False, help="Bypass danger key check.")
@click.pass_context
def set_flag(ctx: click.Context, keypath: str, value: str, unsafe: bool) -> None:
    """Write a flag value to the save file."""
    save_path = ctx.obj.get("save_file")
    dry_run = ctx.obj.get("dry_run", False)
    if not save_path:
        click.echo("Error: no save file specified.", err=True)
        sys.exit(1)

    parsed = _parse_value(value)

    with _make_save(ctx, save_path, dry_run=dry_run) as save:
        try:
            save.set_flag(keypath, parsed, unsafe=unsafe)
            action = "Would set" if dry_run else "Set"
            click.echo(f"{action}: {keypath} = {parsed!r}")
        except FlagWriteError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command("deps")
@click.argument("keypath")
@click.option("--no-soft", is_flag=True, default=False, help="Only show hard dependencies.")
@click.option("--verbose", "-v", is_flag=True, default=False)
@click.pass_context
def deps(ctx: click.Context, keypath: str, no_soft: bool, verbose: bool) -> None:
    """Show dependency graph for a flag (no file needed)."""
    em_path = ctx.obj.get("effectmap_path") if ctx.obj else None
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    from ._effectmap import DependencyGraph
    graph = DependencyGraph(em)
    result = graph.check_safe(keypath, include_soft=not no_soft)
    click.echo(result.report(verbose=verbose))


@cli.command("search")
@click.argument("pattern")
@click.pass_context
def search(ctx: click.Context, pattern: str) -> None:
    """Search known keypaths by regex pattern."""
    em_path = ctx.obj.get("effectmap_path") if ctx.obj else None
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    matches = em.search(pattern)
    for m in matches:
        click.echo(m)
    if not matches:
        click.echo(f"No keypaths match {pattern!r}", err=True)


@cli.command("check-safe")
@click.argument("keypaths", nargs=-1, required=True)
@click.option("--no-soft", is_flag=True, default=False)
@click.pass_context
def check_safe(ctx: click.Context, keypaths: tuple[str, ...], no_soft: bool) -> None:
    """Check whether setting keypaths would implicate any danger keys."""
    em_path = ctx.obj.get("effectmap_path") if ctx.obj else None
    em = EffectMap(Path(em_path)) if em_path else EffectMap()
    from ._effectmap import DependencyGraph
    graph = DependencyGraph(em)

    any_danger = False
    for kp in keypaths:
        result = graph.check_safe(kp, include_soft=not no_soft)
        click.echo(result.report(verbose=True))
        if not result.is_safe:
            any_danger = True

    sys.exit(1 if any_danger else 0)


def _parse_value(raw: str) -> bool | int | float | str:
    if raw.lower() in ("true", "yes", "1", "on"):
        return True
    if raw.lower() in ("false", "no", "0", "off"):
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
