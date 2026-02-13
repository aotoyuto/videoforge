"""Transition effects between scenes."""

from __future__ import annotations

from pathlib import Path

from .ffmpeg import run_ffmpeg


# FFmpeg xfade transition name mapping
XFADE_MAP = {
    "fade": "fade",
    "crossfade": "fade",
    "wipe_left": "wipeleft",
    "wipe_right": "wiperight",
    "dissolve": "dissolve",
}


def apply_xfade(
    clip_a: Path,
    clip_b: Path,
    output: Path,
    transition: str,
    duration: float,
    offset: float,
) -> Path:
    """Apply an xfade transition between two video clips.

    Args:
        clip_a: First video clip.
        clip_b: Second video clip.
        output: Output file path.
        transition: Transition type name.
        duration: Duration of the transition in seconds.
        offset: Time offset in clip_a where the transition starts.
    """
    xfade_name = XFADE_MAP.get(transition, "fade")

    run_ffmpeg([
        "-i", str(clip_a),
        "-i", str(clip_b),
        "-filter_complex",
        f"xfade=transition={xfade_name}:duration={duration}:offset={offset}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(output),
    ])
    return output
