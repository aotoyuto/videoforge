"""FFmpeg command builder and executor."""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def find_ffmpeg() -> str:
    """Find FFmpeg executable path."""
    path = shutil.which("ffmpeg")
    if not path:
        raise RuntimeError(
            "FFmpeg not found. Please install FFmpeg and ensure it's on your PATH."
        )
    return path


def run_ffmpeg(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run an FFmpeg command and return the result."""
    ffmpeg = find_ffmpeg()
    cmd = [ffmpeg, "-y"] + args  # -y to overwrite output
    logger.info("FFmpeg command: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=600,
    )

    if result.returncode != 0:
        logger.error("FFmpeg stderr:\n%s", result.stderr)
        raise RuntimeError(f"FFmpeg failed (exit {result.returncode}):\n{result.stderr[-500:]}")

    return result


def probe_duration(file_path: Path) -> float:
    """Get the duration of a media file in seconds."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe not found.")

    result = subprocess.run(
        [
            ffprobe,
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ],
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def create_color_video(
    output: Path,
    color: str,
    duration: float,
    width: int,
    height: int,
    fps: int,
) -> Path:
    """Create a solid color video clip."""
    hex_color = color.lstrip("#")
    run_ffmpeg([
        "-f", "lavfi",
        "-i", f"color=c=0x{hex_color}:s={width}x{height}:d={duration}:r={fps}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        str(output),
    ])
    return output


def create_image_video(
    output: Path,
    image_path: Path,
    duration: float,
    width: int,
    height: int,
    fps: int,
    fit: str = "cover",
) -> Path:
    """Create a video clip from a static image with scaling."""
    if fit == "cover":
        scale_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height}"
        )
    elif fit == "contain":
        scale_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
        )
    else:  # stretch
        scale_filter = f"scale={width}:{height}"

    run_ffmpeg([
        "-loop", "1",
        "-i", str(image_path),
        "-vf", scale_filter,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-r", str(fps),
        str(output),
    ])
    return output


def add_text_overlay(
    input_video: Path,
    output: Path,
    text: str,
    font: str,
    font_size: int,
    color: str,
    position: str,
    bg_color: str | None = None,
    border_color: str | None = None,
    border_width: int = 0,
    start: float | None = None,
    end: float | None = None,
    font_path: str | None = None,
) -> Path:
    """Add a text overlay to a video using FFmpeg drawtext filter."""
    # Position mapping
    pos_map = {
        "center": "x=(w-text_w)/2:y=(h-text_h)/2",
        "top_center": "x=(w-text_w)/2:y=h*0.05",
        "bottom_center": "x=(w-text_w)/2:y=h*0.85",
        "top_left": "x=w*0.05:y=h*0.05",
        "top_right": "x=w*0.95-text_w:y=h*0.05",
        "bottom_left": "x=w*0.05:y=h*0.85",
        "bottom_right": "x=w*0.95-text_w:y=h*0.85",
    }
    pos_expr = pos_map.get(position, pos_map["bottom_center"])

    # Escape text for FFmpeg (colon, backslash, single quote)
    escaped_text = text.replace("\\", "\\\\").replace("'", "'\\''").replace(":", "\\:")

    # Build drawtext filter
    parts = [f"text='{escaped_text}'"]

    if font_path:
        parts.append(f"fontfile='{font_path}'")
    else:
        parts.append(f"font='{font}'")

    parts.append(f"fontsize={font_size}")

    # Convert hex color to FFmpeg format
    hex_c = color.lstrip("#")
    parts.append(f"fontcolor=0x{hex_c}")

    parts.append(pos_expr)

    if bg_color:
        hex_bg = bg_color.lstrip("#")
        if len(hex_bg) == 8:
            parts.append(f"box=1:boxcolor=0x{hex_bg[:6]}@0x{hex_bg[6:]}:boxborderw=10")
        else:
            parts.append(f"box=1:boxcolor=0x{hex_bg}@0.5:boxborderw=10")

    if border_color and border_width > 0:
        hex_border = border_color.lstrip("#")
        parts.append(f"bordercolor=0x{hex_border}:borderw={border_width}")

    # Enable/disable timing
    if start is not None or end is not None:
        enable_parts = []
        if start is not None:
            enable_parts.append(f"gte(t,{start})")
        if end is not None:
            enable_parts.append(f"lte(t,{end})")
        enable_expr = "*".join(enable_parts)
        parts.append(f"enable='{enable_expr}'")

    drawtext = "drawtext=" + ":".join(parts)

    run_ffmpeg([
        "-i", str(input_video),
        "-vf", drawtext,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        str(output),
    ])
    return output


def concat_videos(output: Path, video_files: list[Path]) -> Path:
    """Concatenate multiple video files using the concat demuxer."""
    if not video_files:
        raise ValueError("No video files to concatenate")

    if len(video_files) == 1:
        import shutil as _shutil
        _shutil.copy2(video_files[0], output)
        return output

    # Create concat list file
    list_file = output.parent / "_concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for vf in video_files:
            # Use forward slashes for FFmpeg on Windows
            safe_path = str(vf.resolve()).replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    try:
        run_ffmpeg([
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(output),
        ])
    finally:
        list_file.unlink(missing_ok=True)

    return output


def mix_audio(
    video_path: Path,
    audio_path: Path,
    output: Path,
    audio_volume: float = 0.3,
    fade_in: float = 0.0,
    fade_out: float = 0.0,
    video_duration: float | None = None,
) -> Path:
    """Mix an audio track into a video file."""
    audio_filters = [f"volume={audio_volume}"]

    if fade_in > 0:
        audio_filters.append(f"afade=t=in:st=0:d={fade_in}")

    if fade_out > 0 and video_duration:
        fade_start = max(0, video_duration - fade_out)
        audio_filters.append(f"afade=t=out:st={fade_start}:d={fade_out}")

    af = ",".join(audio_filters)

    run_ffmpeg([
        "-i", str(video_path),
        "-i", str(audio_path),
        "-filter_complex",
        f"[1:a]{af}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output),
    ])
    return output


def add_audio_to_video(
    video_path: Path,
    audio_path: Path,
    output: Path,
    audio_volume: float = 0.3,
    fade_in: float = 0.0,
    fade_out: float = 0.0,
    video_duration: float | None = None,
) -> Path:
    """Add audio to a video that has no audio stream."""
    audio_filters = [f"volume={audio_volume}"]

    if fade_in > 0:
        audio_filters.append(f"afade=t=in:st=0:d={fade_in}")

    if fade_out > 0 and video_duration:
        fade_start = max(0, video_duration - fade_out)
        audio_filters.append(f"afade=t=out:st={fade_start}:d={fade_out}")

    af = ",".join(audio_filters)

    run_ffmpeg([
        "-i", str(video_path),
        "-i", str(audio_path),
        "-af", af,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output),
    ])
    return output
