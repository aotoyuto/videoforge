"""Main rendering pipeline orchestrator."""

from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path

from ..config import Config
from ..schema import VideoSpec
from .compositor import render_scene
from .ffmpeg import add_audio_to_video, concat_videos
from .transitions import apply_xfade

logger = logging.getLogger(__name__)


class RenderEngine:
    """Orchestrates the full video rendering pipeline.

    Pipeline: VideoSpec → scene clips → transitions → concat → audio mix → export
    """

    def __init__(self, config: Config | None = None):
        self.config = config or Config.load()

    def render(
        self,
        spec: VideoSpec,
        output_path: Path | None = None,
        base_dir: Path | None = None,
    ) -> Path:
        """Render a complete video from a VideoSpec.

        Args:
            spec: The video specification.
            output_path: Where to save the final video. Auto-generated if None.
            base_dir: Base directory for resolving relative asset paths.

        Returns:
            Path to the rendered video file.
        """
        if output_path is None:
            self.config.output_dir.mkdir(parents=True, exist_ok=True)
            safe_title = "".join(
                c if c.isalnum() or c in "-_ " else "_" for c in spec.video.title
            ).strip()
            output_path = self.config.output_dir / f"{safe_title or 'output'}.mp4"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        width, height = spec.video.resolution
        fps = spec.video.fps

        with tempfile.TemporaryDirectory(prefix="videoforge_") as tmpdir:
            tmp = Path(tmpdir)

            # Step 1: Render individual scenes
            logger.info("Rendering %d scenes...", len(spec.scenes))
            scene_clips: list[Path] = []
            for i, scene in enumerate(spec.scenes):
                if not scene.id:
                    scene.id = f"scene_{i}"
                logger.info("  Scene %d/%d: %s", i + 1, len(spec.scenes), scene.id)
                clip = render_scene(
                    scene=scene,
                    output_dir=tmp,
                    width=width,
                    height=height,
                    fps=fps,
                    base_dir=base_dir,
                    default_font=self.config.default_font,
                    default_font_path=self.config.default_font_path,
                )
                scene_clips.append(clip)

            # Step 2: Apply transitions between scenes
            if len(scene_clips) > 1:
                logger.info("Applying transitions...")
                scene_clips = self._apply_transitions(spec, scene_clips, tmp)

            # Step 3: Concatenate all scene clips
            logger.info("Concatenating scenes...")
            concat_output = tmp / "concat.mp4"
            concat_videos(concat_output, scene_clips)

            # Step 4: Generate narration audio (if any)
            narration_audio = None
            if spec.audio.narration:
                logger.info("Generating narration...")
                narration_audio = self._generate_narration(spec, tmp, base_dir)

            # Step 5: Mix audio (BGM + narration)
            final_video = concat_output
            if spec.audio.bgm and spec.audio.bgm.source:
                logger.info("Mixing BGM...")
                bgm_path = self._resolve_audio(spec.audio.bgm.source, base_dir)
                if bgm_path.exists():
                    mixed = tmp / "with_bgm.mp4"
                    add_audio_to_video(
                        video_path=final_video,
                        audio_path=bgm_path,
                        output=mixed,
                        audio_volume=spec.audio.bgm.volume,
                        fade_in=spec.audio.bgm.fade_in,
                        fade_out=spec.audio.bgm.fade_out,
                        video_duration=spec.total_duration,
                    )
                    final_video = mixed
                else:
                    logger.warning("BGM file not found: %s", bgm_path)

            # Step 6: Copy to output
            shutil.copy2(final_video, output_path)
            logger.info("Video saved to: %s", output_path)

        return output_path

    def _apply_transitions(
        self, spec: VideoSpec, clips: list[Path], tmp: Path
    ) -> list[Path]:
        """Apply transitions between consecutive clips."""
        result = [clips[0]]
        cumulative_duration = spec.scenes[0].duration

        for i in range(1, len(clips)):
            prev_scene = spec.scenes[i - 1]
            curr_scene = spec.scenes[i]

            transition_type = prev_scene.transition_out.value
            if transition_type == "none":
                transition_type = curr_scene.transition_in.value

            if transition_type != "none":
                duration = prev_scene.transition_duration
                offset = cumulative_duration - duration
                merged = tmp / f"transition_{i}.mp4"
                try:
                    apply_xfade(result[-1], clips[i], merged, transition_type, duration, offset)
                    result[-1] = merged
                    cumulative_duration += curr_scene.duration - duration
                except RuntimeError:
                    logger.warning("Transition failed for scene %d, using hard cut.", i)
                    result.append(clips[i])
                    cumulative_duration += curr_scene.duration
            else:
                result.append(clips[i])
                cumulative_duration += curr_scene.duration

        return result

    def _generate_narration(
        self, spec: VideoSpec, tmp: Path, base_dir: Path | None
    ) -> Path | None:
        """Generate narration audio from TTS. Returns combined narration audio path."""
        # TTS generation will be implemented in assets/tts.py
        # For now, log a warning
        logger.warning("Narration TTS not yet fully integrated in render pipeline.")
        return None

    def _resolve_audio(self, source: str, base_dir: Path | None) -> Path:
        """Resolve an audio source path."""
        p = Path(source)
        if p.is_absolute():
            return p
        if base_dir:
            return base_dir / p
        return p
