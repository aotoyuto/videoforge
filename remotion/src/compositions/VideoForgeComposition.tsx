import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import type { VideoSpec } from "../types";
import { SceneRenderer } from "../components/SceneRenderer";

/**
 * Main VideoForge composition.
 * Renders a complete video from a VideoSpec, placing each scene
 * as a Remotion Sequence with calculated timing.
 */
export const VideoForgeComposition: React.FC<VideoSpec> = (spec) => {
  const { fps } = useVideoConfig();

  // Calculate scene start frames
  let currentFrame = 0;
  const sceneTimings = spec.scenes.map((scene) => {
    const startFrame = currentFrame;
    const durationInFrames = Math.round(scene.duration * fps);
    currentFrame += durationInFrames;
    return { scene, startFrame, durationInFrames };
  });

  return (
    <AbsoluteFill
      style={{ backgroundColor: spec.video.background_color || "#000000" }}
    >
      {sceneTimings.map(({ scene, startFrame, durationInFrames }, i) => (
        <Sequence
          key={scene.id || `scene-${i}`}
          from={startFrame}
          durationInFrames={durationInFrames}
          name={scene.id || `Scene ${i + 1}`}
        >
          <SceneRenderer scene={scene} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
