import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import type { TextOverlay as TextOverlayType } from "../types";

/**
 * Renders a styled text overlay with animations.
 */
export const TextOverlay: React.FC<{
  overlay: TextOverlayType;
  sceneDurationInFrames: number;
}> = ({ overlay, sceneDurationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const startFrame = overlay.start != null ? overlay.start * fps : 0;
  const endFrame =
    overlay.end != null ? overlay.end * fps : sceneDurationInFrames;

  // Visibility
  if (frame < startFrame || frame > endFrame) return null;

  const localFrame = frame - startFrame;
  const localDuration = endFrame - startFrame;

  // Animation
  let opacity = 1;
  let translateY = 0;

  switch (overlay.animation) {
    case "fade_in":
      opacity = interpolate(localFrame, [0, fps * 0.5], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    case "fade_out":
      opacity = interpolate(
        localFrame,
        [localDuration - fps * 0.5, localDuration],
        [1, 0],
        { extrapolateLeft: "clamp" }
      );
      break;
    case "slide_up":
      translateY = interpolate(localFrame, [0, fps * 0.4], [60, 0], {
        extrapolateRight: "clamp",
      });
      opacity = interpolate(localFrame, [0, fps * 0.3], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    case "slide_down":
      translateY = interpolate(localFrame, [0, fps * 0.4], [-60, 0], {
        extrapolateRight: "clamp",
      });
      opacity = interpolate(localFrame, [0, fps * 0.3], [0, 1], {
        extrapolateRight: "clamp",
      });
      break;
    case "typewriter": {
      const charsToShow = Math.floor(
        interpolate(localFrame, [0, fps * 1.5], [0, overlay.content.length], {
          extrapolateRight: "clamp",
        })
      );
      return (
        <div style={getContainerStyle(overlay)}>
          <span style={getTextStyle(overlay)}>
            {overlay.content.slice(0, charsToShow)}
            <span style={{ opacity: frame % (fps / 2) < fps / 4 ? 1 : 0 }}>
              |
            </span>
          </span>
        </div>
      );
    }
  }

  return (
    <div
      style={{
        ...getContainerStyle(overlay),
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <span style={getTextStyle(overlay)}>{overlay.content}</span>
    </div>
  );
};

function getContainerStyle(
  overlay: TextOverlayType
): React.CSSProperties {
  const base: React.CSSProperties = {
    position: "absolute",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "12px 24px",
    zIndex: 10,
  };

  if (overlay.bg_color) {
    base.backgroundColor = overlay.bg_color;
    base.borderRadius = "8px";
  }

  // Position mapping
  switch (overlay.position) {
    case "center":
      base.top = "50%";
      base.left = "50%";
      base.transform = "translate(-50%, -50%)";
      break;
    case "top_center":
      base.top = "5%";
      base.left = "50%";
      base.transform = "translateX(-50%)";
      break;
    case "bottom_center":
      base.bottom = "8%";
      base.left = "50%";
      base.transform = "translateX(-50%)";
      break;
    case "top_left":
      base.top = "5%";
      base.left = "5%";
      break;
    case "top_right":
      base.top = "5%";
      base.right = "5%";
      break;
    case "bottom_left":
      base.bottom = "8%";
      base.left = "5%";
      break;
    case "bottom_right":
      base.bottom = "8%";
      base.right = "5%";
      break;
  }

  return base;
}

function getTextStyle(overlay: TextOverlayType): React.CSSProperties {
  const style: React.CSSProperties = {
    fontFamily: overlay.font || "Yu Gothic, sans-serif",
    fontSize: overlay.font_size || 48,
    color: overlay.color || "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.4,
    whiteSpace: "pre-wrap",
  };

  if (overlay.border_color && overlay.border_width > 0) {
    style.textShadow = `
      ${overlay.border_width}px ${overlay.border_width}px 0 ${overlay.border_color},
      -${overlay.border_width}px ${overlay.border_width}px 0 ${overlay.border_color},
      ${overlay.border_width}px -${overlay.border_width}px 0 ${overlay.border_color},
      -${overlay.border_width}px -${overlay.border_width}px 0 ${overlay.border_color}
    `;
  }

  return style;
}
