import React from "react";
import {
  AbsoluteFill,
  Img,
  Video,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import type { Scene } from "../types";
import { TextOverlay } from "./TextOverlay";

/**
 * Renders a single scene with its background and text overlays.
 */
export const SceneRenderer: React.FC<{ scene: Scene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durationInFrames = scene.duration * fps;

  // Transition opacity
  let opacity = 1;
  const transitionFrames = scene.transition_duration * fps;

  if (scene.transition_in === "fade" && frame < transitionFrames) {
    opacity = interpolate(frame, [0, transitionFrames], [0, 1], {
      extrapolateRight: "clamp",
    });
  }

  if (
    scene.transition_out === "fade" &&
    frame > durationInFrames - transitionFrames
  ) {
    opacity = interpolate(
      frame,
      [durationInFrames - transitionFrames, durationInFrames],
      [1, 0],
      { extrapolateLeft: "clamp" }
    );
  }

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* Background */}
      <SceneBackground scene={scene} />

      {/* Text Overlays */}
      {scene.text_overlays.map((overlay, i) => (
        <TextOverlay
          key={i}
          overlay={overlay}
          sceneDurationInFrames={durationInFrames}
        />
      ))}
    </AbsoluteFill>
  );
};

const SceneBackground: React.FC<{ scene: Scene }> = ({ scene }) => {
  const { width, height } = useVideoConfig();

  switch (scene.type) {
    case "color":
      return (
        <AbsoluteFill
          style={{ backgroundColor: scene.color || "#000000" }}
        />
      );

    case "image":
      if (!scene.source) {
        return (
          <AbsoluteFill style={{ backgroundColor: scene.color || "#000" }} />
        );
      }
      return (
        <AbsoluteFill>
          <Img
            src={scene.source}
            style={{
              width: "100%",
              height: "100%",
              objectFit:
                scene.fit === "cover"
                  ? "cover"
                  : scene.fit === "contain"
                    ? "contain"
                    : "fill",
            }}
          />
        </AbsoluteFill>
      );

    case "video":
      if (!scene.source) {
        return <AbsoluteFill style={{ backgroundColor: "#000" }} />;
      }
      return (
        <AbsoluteFill>
          <Video
            src={scene.source}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        </AbsoluteFill>
      );

    default:
      return (
        <AbsoluteFill
          style={{ backgroundColor: scene.color || "#000000" }}
        />
      );
  }
};
