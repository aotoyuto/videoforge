"""VideoSpec YAML parser and validator."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from .schema import VideoSpec


def load_spec(path: str | Path) -> VideoSpec:
    """Load and validate a VideoSpec from a YAML file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"VideoSpec file not found: {path}")

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"Empty VideoSpec file: {path}")

    return parse_spec(raw)


def parse_spec(data: dict) -> VideoSpec:
    """Parse and validate a VideoSpec from a dictionary."""
    try:
        return VideoSpec.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Invalid VideoSpec:\n{e}") from e


def dump_spec(spec: VideoSpec) -> str:
    """Serialize a VideoSpec to YAML string."""
    data = spec.model_dump(mode="json", exclude_none=True)
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)


def save_spec(spec: VideoSpec, path: str | Path) -> Path:
    """Save a VideoSpec to a YAML file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(dump_spec(spec))
    return path
