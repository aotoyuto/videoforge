"""Scene compositor - builds individual scene clips with text overlays."""

from __future__ import annotations

import logging
from pathlib import Path

from ..schema import Scene, TextOverlay
from .ffmpeg import (
    add_text_overlay,
    create_color_video,
    create_image_video,
)

logger = logging.getLogger(__name__)


def render_scene(
    scene: Scene,
    output_dir: Path,
    width: int,
    height: int,
    fps: int,
    base_dir: Path | None = None,
    default_font: str = "Yu Gothic",
    default_font_path: str = "",
) -> Path:
    """Render a single scene to a video clip.

    Args:
        scene: Scene definition.
        output_dir: Directory for temporary files.
        width: Video width.
        height: Video height.
        fps: Frames per second.
        base_dir: Base directory for resolving relative asset paths.
        default_font: Default font family name.
        default_font_path: Default font file path.

    Returns:
        Path to the rendered scene clip.
    """
    scene_id = scene.id or "scene"
    base_clip = output_dir / f"{scene_id}_base.mp4"

    # Step 1: Create the base clip
    if scene.type.value == "color":
        create_color_video(base_clip, scene.color, scene.duration, width, height, fps)

    elif scene.type.value == "image":
        if not scene.source:
            raise ValueError(f"Scene {scene_id}: image type requires 'source'")
        image_path = _resolve_path(scene.source, base_dir)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        create_image_video(base_clip, image_path, scene.duration, width, height, fps, scene.fit.value)

    elif scene.type.value == "video":
        if not scene.source:
            raise ValueError(f"Scene {scene_id}: video type requires 'source'")
        video_path = _resolve_path(scene.source, base_dir)
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        # Copy/trim video to match duration
        from .ffmpeg import run_ffmpeg
        run_ffmpeg([
            "-i", str(video_path),
            "-t", str(scene.duration),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            str(base_clip),
        ])

    elif scene.type.value == "ai_generate":
        if not scene.source_prompt:
            raise ValueError(f"Scene {scene_id}: ai_generate type requires 'source_prompt'")
        logger.warning("AI generation not yet implemented; falling back to color.")
        create_color_video(base_clip, scene.color, scene.duration, width, height, fps)

    else:
        raise ValueError(f"Unknown scene type: {scene.type}")

    # Step 2: Apply text overlays sequentially
    current = base_clip
    for i, overlay in enumerate(scene.text_overlays):
        next_clip = output_dir / f"{scene_id}_text{i}.mp4"
        current = _apply_overlay(
            current, next_clip, overlay, default_font, default_font_path
        )

    return current


def _apply_overlay(
    input_path: Path,
    output_path: Path,
    overlay: TextOverlay,
    default_font: str,
    default_font_path: str,
) -> Path:
    """Apply a single text overlay to a video clip."""
    font = overlay.font or default_font
    font_path = default_font_path if font == default_font else None

    return add_text_overlay(
        input_video=input_path,
        output=output_path,
        text=overlay.content,
        font=font,
        font_size=overlay.font_size,
        color=overlay.color,
        position=overlay.position.value,
        bg_color=overlay.bg_color,
        border_color=overlay.border_color,
        border_width=overlay.border_width,
        start=overlay.start,
        end=overlay.end,
        font_path=font_path,
    )


def _resolve_path(source: str, base_dir: Path | None) -> Path:
    """Resolve a source path, relative to base_dir if needed."""
    p = Path(source)
    if p.is_absolute():
        return p
    if base_dir:
        return base_dir / p
    return p
