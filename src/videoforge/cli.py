"""VideoForge CLI - command-line interface for video creation."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

from . import __version__

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("videoforge")


@click.group()
@click.version_option(version=__version__, prog_name="videoforge")
def main():
    """VideoForge - Natural language video creation system."""
    pass


@main.command()
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), default=None, help="Output file path")
@click.option(
    "--engine",
    type=click.Choice(["ffmpeg", "remotion"]),
    default="ffmpeg",
    help="Rendering engine (ffmpeg or remotion)",
)
def render(spec_file: str, output: str | None, engine: str):
    """Render a video from a VideoSpec YAML file.

    Examples:
      videoforge render examples/simple_slideshow.yaml
      videoforge render examples/simple_slideshow.yaml --engine remotion
    """
    from .config import Config
    from .spec import load_spec

    click.echo(f"Loading spec: {spec_file}")
    spec = load_spec(spec_file)
    click.echo(f"  Title: {spec.video.title}")
    click.echo(f"  Scenes: {len(spec.scenes)}")
    click.echo(f"  Duration: {spec.total_duration}s")
    click.echo(f"  Resolution: {spec.video.resolution[0]}x{spec.video.resolution[1]}")
    click.echo(f"  Engine: {engine}")

    config = Config.load()
    output_path = Path(output) if output else None
    base_dir = Path(spec_file).parent

    if engine == "remotion":
        from .render.remotion import render_with_remotion

        if output_path is None:
            config.output_dir.mkdir(parents=True, exist_ok=True)
            output_path = config.output_dir / f"{spec.video.title}.mp4"

        click.echo("Rendering with Remotion...")
        result = render_with_remotion(spec, output_path)
    else:
        from .render.engine import RenderEngine

        render_engine = RenderEngine(config)
        click.echo("Rendering with FFmpeg...")
        result = render_engine.render(spec, output_path=output_path, base_dir=base_dir)

    click.echo(f"Done! Video saved to: {result}")


@main.command()
@click.argument("spec_file", type=click.Path(exists=True))
def validate(spec_file: str):
    """Validate a VideoSpec YAML file without rendering.

    Example: videoforge validate examples/simple_slideshow.yaml
    """
    from .spec import load_spec

    try:
        spec = load_spec(spec_file)
        click.echo(f"Valid VideoSpec: {spec.video.title}")
        click.echo(f"  Version: {spec.version}")
        click.echo(f"  Scenes: {len(spec.scenes)}")
        click.echo(f"  Duration: {spec.total_duration}s")
        click.echo(f"  Resolution: {spec.video.resolution[0]}x{spec.video.resolution[1]}")
        click.echo(f"  Platform: {spec.export.platform.value}")
        if spec.audio.bgm:
            click.echo(f"  BGM: {spec.audio.bgm.source or spec.audio.bgm.source_prompt}")
        if spec.audio.narration:
            click.echo(f"  Narration: {len(spec.audio.narration)} segment(s)")
    except Exception as e:
        click.echo(f"Invalid: {e}", err=True)
        sys.exit(1)


@main.group()
def template():
    """Manage video templates."""
    pass


@template.command("list")
def template_list():
    """List available video templates."""
    from importlib.resources import files

    template_dir = files("videoforge") / "templates"
    # Also check local templates directory
    local_dir = Path("templates")

    click.echo("Built-in templates:")
    try:
        for item in sorted(Path(str(template_dir)).glob("*.yaml")):
            name = item.stem
            click.echo(f"  - {name}")
    except Exception:
        click.echo("  (no built-in templates found)")

    if local_dir.exists():
        click.echo("\nLocal templates:")
        for item in sorted(local_dir.glob("*.yaml")):
            name = item.stem
            click.echo(f"  - {name}")


@template.command("use")
@click.argument("template_name")
@click.option("--title", default=None, help="Video title")
@click.option("-o", "--output", type=click.Path(), default=None, help="Output file path")
def template_use(template_name: str, title: str | None, output: str | None):
    """Create a video from a template.

    Example: videoforge template use youtube_intro --title "AI入門"
    """
    from importlib.resources import files

    from .config import Config
    from .render.engine import RenderEngine
    from .spec import load_spec

    # Find template
    template_path = None
    candidates = [
        Path(str(files("videoforge") / "templates")) / f"{template_name}.yaml",
        Path("templates") / f"{template_name}.yaml",
    ]
    for p in candidates:
        if p.exists():
            template_path = p
            break

    if not template_path:
        click.echo(f"Template not found: {template_name}", err=True)
        click.echo("Use 'videoforge template list' to see available templates.", err=True)
        sys.exit(1)

    spec = load_spec(template_path)

    if title:
        spec.video.title = title
        # Replace placeholder title in text overlays
        for scene in spec.scenes:
            for overlay in scene.text_overlays:
                if "{{title}}" in overlay.content:
                    overlay.content = overlay.content.replace("{{title}}", title)

    config = Config.load()
    engine = RenderEngine(config)
    output_path = Path(output) if output else None

    click.echo(f"Using template: {template_name}")
    click.echo(f"Rendering: {spec.video.title}")
    result = engine.render(spec, output_path=output_path, base_dir=template_path.parent)
    click.echo(f"Done! Video saved to: {result}")


@main.group()
def remotion():
    """Remotion rendering engine commands."""
    pass


@remotion.command("studio")
def remotion_studio():
    """Launch Remotion Studio for live preview.

    Opens a browser-based editor where you can preview and edit videos in real-time.
    """
    import subprocess
    import shutil

    from .render.remotion import find_remotion_dir

    remotion_dir = find_remotion_dir()
    npx = shutil.which("npx")
    if not npx:
        click.echo("npx not found. Install Node.js first.", err=True)
        sys.exit(1)

    click.echo(f"Starting Remotion Studio in {remotion_dir}...")
    click.echo("Open http://localhost:3000 in your browser.")
    click.echo("Press Ctrl+C to stop.\n")

    subprocess.run([npx, "remotion", "studio"], cwd=remotion_dir)


@remotion.command("render")
@click.argument("composition", default="VideoForgeComposition")
@click.option("-o", "--output", type=click.Path(), default=None, help="Output file path")
@click.option("--props", type=click.Path(exists=True), default=None, help="Props JSON file")
def remotion_render(composition: str, output: str | None, props: str | None):
    """Render a Remotion composition to video.

    Examples:
      videoforge remotion render YouTubeIntro
      videoforge remotion render Presentation --props my_props.json
    """
    import json
    import subprocess
    import shutil

    from .render.remotion import find_remotion_dir

    remotion_dir = find_remotion_dir()
    npx = shutil.which("npx")

    cmd = [npx, "remotion", "render", composition]

    if output:
        cmd.append(output)
    if props:
        cmd.extend(["--props", str(Path(props).resolve())])

    cmd.extend(["--codec", "h264"])

    click.echo(f"Rendering composition: {composition}")
    result = subprocess.run(cmd, cwd=remotion_dir)
    if result.returncode == 0:
        click.echo("Render complete!")
    else:
        click.echo("Render failed.", err=True)
        sys.exit(1)


@remotion.command("list")
def remotion_list():
    """List available Remotion compositions."""
    from .render.remotion import list_compositions

    click.echo("Available Remotion compositions:")
    for comp in list_compositions():
        click.echo(f"  - {comp}")


@remotion.command("install")
def remotion_install():
    """Install Remotion dependencies (npm install)."""
    import subprocess
    import shutil

    from .render.remotion import find_remotion_dir

    remotion_dir = find_remotion_dir()
    npm = shutil.which("npm")
    if not npm:
        click.echo("npm not found. Install Node.js first.", err=True)
        sys.exit(1)

    click.echo(f"Installing dependencies in {remotion_dir}...")
    result = subprocess.run([npm, "install"], cwd=remotion_dir)
    if result.returncode == 0:
        click.echo("Dependencies installed successfully!")
    else:
        click.echo("Installation failed.", err=True)
        sys.exit(1)


@main.command()
def check():
    """Check system requirements (FFmpeg, Node.js, Remotion, VOICEVOX, etc.)."""
    import shutil

    click.echo("System check:")

    # FFmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        click.echo(f"  FFmpeg: OK ({ffmpeg_path})")
    else:
        click.echo("  FFmpeg: NOT FOUND")

    # FFprobe
    ffprobe_path = shutil.which("ffprobe")
    if ffprobe_path:
        click.echo(f"  FFprobe: OK ({ffprobe_path})")
    else:
        click.echo("  FFprobe: NOT FOUND")

    # Node.js
    node_path = shutil.which("node")
    if node_path:
        import subprocess
        ver = subprocess.run(["node", "--version"], capture_output=True, text=True)
        click.echo(f"  Node.js: OK ({ver.stdout.strip()})")
    else:
        click.echo("  Node.js: NOT FOUND")

    # npx
    npx_path = shutil.which("npx")
    if npx_path:
        click.echo(f"  npx: OK ({npx_path})")
    else:
        click.echo("  npx: NOT FOUND")

    # Remotion
    from .render.remotion import is_remotion_installed
    if is_remotion_installed():
        click.echo("  Remotion: OK (installed)")
    else:
        click.echo("  Remotion: NOT INSTALLED (run: videoforge remotion install)")

    # VOICEVOX
    from .config import Config
    config = Config.load()
    from .assets.tts import VoicevoxTTS
    vv = VoicevoxTTS(config.voicevox_url)
    if vv.is_available():
        click.echo(f"  VOICEVOX: OK ({config.voicevox_url})")
    else:
        click.echo(f"  VOICEVOX: NOT RUNNING ({config.voicevox_url})")

    # Python
    click.echo(f"  Python: {sys.version}")


if __name__ == "__main__":
    main()
