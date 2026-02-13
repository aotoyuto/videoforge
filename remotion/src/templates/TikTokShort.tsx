import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

interface TikTokShortProps {
  title: string;
  points: string[];
  accentColor?: string;
}

export const TikTokShort: React.FC<TikTokShortProps> = ({
  title,
  points,
  accentColor = "#ff6b6b",
}) => {
  const { fps } = useVideoConfig();

  const hookDuration = Math.round(fps * 3);
  const pointDuration = Math.round(fps * 4);
  const ctaDuration = Math.round(fps * 2);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {/* Hook - attention grabber */}
      <Sequence from={0} durationInFrames={hookDuration}>
        <Hook title={title} accentColor={accentColor} fps={fps} />
      </Sequence>

      {/* Points */}
      {points.map((point, i) => (
        <Sequence
          key={i}
          from={hookDuration + i * pointDuration}
          durationInFrames={pointDuration}
        >
          <PointSlide
            index={i + 1}
            text={point}
            accentColor={accentColor}
            fps={fps}
          />
        </Sequence>
      ))}

      {/* CTA */}
      <Sequence
        from={hookDuration + points.length * pointDuration}
        durationInFrames={ctaDuration}
      >
        <CTA accentColor={accentColor} fps={fps} />
      </Sequence>
    </AbsoluteFill>
  );
};

const Hook: React.FC<{
  title: string;
  accentColor: string;
  fps: number;
}> = ({ title, accentColor, fps }) => {
  const frame = useCurrentFrame();

  const scale = spring({ frame, fps, config: { damping: 12, mass: 0.8 } });
  const opacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: accentColor,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          fontSize: 80,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: "#FFFFFF",
          textAlign: "center",
          padding: "0 60px",
          lineHeight: 1.3,
        }}
      >
        {title}
      </div>
    </AbsoluteFill>
  );
};

const PointSlide: React.FC<{
  index: number;
  text: string;
  accentColor: string;
  fps: number;
}> = ({ index, text, accentColor, fps }) => {
  const frame = useCurrentFrame();

  const slideIn = interpolate(frame, [0, fps * 0.3], [100, 0], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "0 60px",
      }}
    >
      <div
        style={{
          opacity,
          transform: `translateX(${slideIn}px)`,
        }}
      >
        <div
          style={{
            fontSize: 120,
            fontFamily: "Yu Gothic, sans-serif",
            fontWeight: "bold",
            color: accentColor,
            marginBottom: 30,
            textAlign: "center",
          }}
        >
          {index}
        </div>
        <div
          style={{
            fontSize: 48,
            fontFamily: "Yu Gothic, sans-serif",
            color: "#FFFFFF",
            textAlign: "center",
            lineHeight: 1.5,
          }}
        >
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const CTA: React.FC<{ accentColor: string; fps: number }> = ({
  accentColor,
  fps,
}) => {
  const frame = useCurrentFrame();
  const pulse =
    1 + Math.sin(frame / (fps * 0.15)) * 0.05;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: accentColor,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          transform: `scale(${pulse})`,
          fontSize: 64,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: "#FFFFFF",
          textAlign: "center",
        }}
      >
        フォローしてね！
      </div>
    </AbsoluteFill>
  );
};
