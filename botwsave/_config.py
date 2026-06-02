"""Config loading: CLI args > config.yaml > sane defaults. Auto-converts config.json once."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


try:
    from ruamel.yaml import YAML as _YAML
    _yaml = _YAML()
    _yaml.default_flow_style = False

    def _load_yaml(path: Path) -> dict:
        with path.open() as f:
            return dict(_yaml.load(f) or {})

    def _dump_yaml(data: dict, path: Path) -> None:
        with path.open("w") as f:
            _yaml.dump(data, f)

except ImportError:
    import yaml  # type: ignore

    def _load_yaml(path: Path) -> dict:
        return yaml.safe_load(path.read_text()) or {}

    def _dump_yaml(data: dict, path: Path) -> None:
        path.write_text(yaml.dump(data, default_flow_style=False))


@dataclass
class Config:
    save_file: str | None = None
    effectmap_path: str | None = None
    dry_run: bool = False
    skip_soft_deps: bool = False
    extra: dict = field(default_factory=dict)

    @classmethod
    def load(
        cls,
        config_dir: Path | None = None,
        *,
        save_file: str | None = None,
        effectmap_path: str | None = None,
        dry_run: bool | None = None,
        skip_soft_deps: bool | None = None,
    ) -> "Config":
        """Load config from YAML, auto-converting config.json if present. CLI args override."""
        search_dirs = [Path.cwd()]
        if config_dir:
            search_dirs.insert(0, config_dir)

        file_cfg: dict[str, Any] = {}
        for d in search_dirs:
            yaml_path = d / "config.yaml"
            json_path = d / "config.json"
            if yaml_path.exists():
                file_cfg = _load_yaml(yaml_path)
                break
            elif json_path.exists():
                raw = json.loads(json_path.read_text())
                file_cfg = _convert_json_config(raw)
                _dump_yaml(file_cfg, d / "config.yaml")
                print(f"[botwsave] Auto-converted {json_path} → {d / 'config.yaml'}")
                break

        cfg = cls(
            save_file=save_file or file_cfg.get("save_file"),
            effectmap_path=effectmap_path or file_cfg.get("effectmap_path"),
            dry_run=dry_run if dry_run is not None else file_cfg.get("dry_run", False),
            skip_soft_deps=skip_soft_deps if skip_soft_deps is not None else file_cfg.get("skip_soft_deps", False),
            extra={k: v for k, v in file_cfg.items() if k not in ("save_file", "effectmap_path", "dry_run", "skip_soft_deps")},
        )
        return cfg


def _convert_json_config(raw: dict) -> dict:
    """Convert Node.js config.json structure to botwsave config.yaml structure."""
    out: dict[str, Any] = {}
    if "savefile" in raw:
        out["save_file"] = raw["savefile"]
    if "mapfilepath" in raw:
        out["effectmap_path"] = str(Path(raw["mapfilepath"]) / "effectmap.json")
    for k, v in raw.items():
        if k not in ("savefile", "mapfilepath"):
            out[k] = v
    return out
