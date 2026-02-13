"""Remotion rendering bridge - converts VideoSpec to Remotion props and renders via CLI."""

from __future__ import annotations

import json
import logging
import subprocess
import shutil
from pathlib import Path

from ..schema import VideoSpec

logger = logging.getLogger(__name__)

REMOTION_DIR = Path(__file__).resolve().parent.parent.parent.parent / "remotion"


def find_remotion_dir() -> Path:
    """Find the Remotion project directory."""
    if REMOTION_DIR.exists() and (REMOTION_DIR / "package.json").exists():
        return REMOTION_DIR
    raise RuntimeError(
        f"Remotion project not found at {REMOTION_DIR}. "
        "Run 'cd remotion && npm install' first."
    )


def is_remotion_installed() -> bool:
    """Check if Remotion dependencies are installed."""
    try:
        remotion_dir = find_remotion_dir()
        return (remotion_dir / "node_modules").exists()
    except RuntimeError:
        return False


def videospec_to_props(spec: VideoSpec) -> dict:
    """Convert a VideoSpec to Remotion input props (JSON-serializable dict)."""
    return spec.model_dump(mode="json", exclude_none=True)


def render_with_remotion(
    spec: VideoSpec,
    output_path: Path,
    composition_id: str = "VideoForgeComposition",
) -> Path:
    """Render a video using Remotion.

    Args:
        spec: The VideoSpec to render.
        output_path: Where to save the output video.
        composition_id: Remotion composition ID to render.

    Returns:
        Path to the rendered video.
    """
    remotion_dir = find_remotion_dir()

    if not is_remotion_installed():
        raise RuntimeError(
            "Remotion dependencies not installed. Run: cd remotion && npm install"
        )

    # Write props to temp JSON file
    props = videospec_to_props(spec)
    props_file = remotion_dir / ".tmp_props.json"
    props_file.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")

    # Calculate total frames
    fps = spec.video.fps
    total_frames = sum(int(s.duration * fps) for s in spec.scenes)
    width, height = spec.video.resolution

    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        npx = shutil.which("npx")
        if not npx:
            raise RuntimeError("npx not found. Please install Node.js.")

        cmd = [
            npx, "remotion", "render",
            composition_id,
            str(output_path),
            "--props", str(props_file),
            "--width", str(width),
            "--height", str(height),
            "--fps", str(fps),
            "--frames", f"0-{total_frames - 1}",
            "--codec", "h264",
        ]

        logger.info("Remotion render command: %s", " ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=remotion_dir,
            timeout=600,
        )

        if result.returncode != 0:
            logger.error("Remotion stderr:\n%s", result.stderr)
            raise RuntimeError(
                f"Remotion render failed (exit {result.returncode}):\n{result.stderr[-500:]}"
            )

        logger.info("Remotion render complete: %s", output_path)
        return output_path

    finally:
        props_file.unlink(missing_ok=True)


def render_template(
    template_id: str,
    props: dict,
    output_path: Path,
) -> Path:
    """Render a pre-built Remotion template.

    Args:
        template_id: Composition ID (e.g. "YouTubeIntro", "TikTokShort").
        props: Template-specific props.
        output_path: Where to save the output.

    Returns:
        Path to the rendered video.
    """
    remotion_dir = find_remotion_dir()

    if not is_remotion_installed():
        raise RuntimeError(
            "Remotion dependencies not installed. Run: cd remotion && npm install"
        )

    props_file = remotion_dir / ".tmp_props.json"
    props_file.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")

    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        npx = shutil.which("npx")
        if not npx:
            raise RuntimeError("npx not found.")

        cmd = [
            npx, "remotion", "render",
            template_id,
            str(output_path),
            "--props", str(props_file),
            "--codec", "h264",
        ]

        logger.info("Remotion template render: %s", " ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=remotion_dir,
            timeout=600,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Remotion render failed:\n{result.stderr[-500:]}"
            )

        return output_path

    finally:
        props_file.unlink(missing_ok=True)


def list_compositions() -> list[str]:
    """List available Remotion compositions."""
    return [
        "VideoForgeComposition",
        "YouTubeIntro",
        "TikTokShort",
        "TextExplainer",
        "Presentation",
    ]
