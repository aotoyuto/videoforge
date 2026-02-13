import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

interface YouTubeIntroProps {
  title: string;
  subtitle?: string;
  accentColor?: string;
}

export const YouTubeIntro: React.FC<YouTubeIntroProps> = ({
  title,
  subtitle,
  accentColor = "#ff6b6b",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a1a" }}>
      {/* Animated background gradient */}
      <Sequence from={0} durationInFrames={fps * 7}>
        <AnimatedBackground
          accentColor={accentColor}
          fps={fps}
          width={width}
          height={height}
        />
      </Sequence>

      {/* Title */}
      <Sequence from={Math.round(fps * 0.8)} durationInFrames={fps * 5}>
        <TitleCard title={title} subtitle={subtitle} fps={fps} />
      </Sequence>

      {/* Fade out */}
      <Sequence from={Math.round(fps * 5.5)} durationInFrames={Math.round(fps * 1.5)}>
        <FadeOut fps={fps} />
      </Sequence>
    </AbsoluteFill>
  );
};

const AnimatedBackground: React.FC<{
  accentColor: string;
  fps: number;
  width: number;
  height: number;
}> = ({ accentColor, fps, width, height }) => {
  const frame = useCurrentFrame();

  const gradientAngle = interpolate(frame, [0, fps * 7], [0, 360]);
  const scale = interpolate(frame, [0, fps * 3], [1, 1.2], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `
          radial-gradient(
            ellipse at ${50 + Math.sin(frame / 30) * 20}% ${50 + Math.cos(frame / 25) * 15}%,
            ${accentColor}22 0%,
            transparent 60%
          ),
          linear-gradient(${gradientAngle}deg, #0a0a1a, #1a1a3e, #0a0a1a)
        `,
        transform: `scale(${scale})`,
      }}
    />
  );
};

const TitleCard: React.FC<{
  title: string;
  subtitle?: string;
  fps: number;
}> = ({ title, subtitle, fps }) => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, fps * 0.6], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [0, fps * 0.5], [30, 0], {
    extrapolateRight: "clamp",
  });

  const subtitleOpacity = interpolate(
    frame,
    [fps * 0.5, fps * 1.0],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Decorative line
  const lineWidth = spring({ frame, fps, config: { damping: 20 } }) * 200;

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
          fontSize: 72,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: "#FFFFFF",
          textAlign: "center",
          letterSpacing: "0.05em",
        }}
      >
        {title}
      </div>

      {/* Decorative line */}
      <div
        style={{
          width: lineWidth,
          height: 3,
          backgroundColor: "#ff6b6b",
          margin: "20px 0",
          borderRadius: 2,
        }}
      />

      {subtitle && (
        <div
          style={{
            opacity: subtitleOpacity,
            fontSize: 28,
            fontFamily: "Yu Gothic, sans-serif",
            color: "#888888",
            letterSpacing: "0.1em",
          }}
        >
          {subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};

const FadeOut: React.FC<{ fps: number }> = ({ fps }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, fps * 1.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return <AbsoluteFill style={{ backgroundColor: "#000", opacity }} />;
};
