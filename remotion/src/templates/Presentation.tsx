import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

interface Slide {
  heading: string;
  body: string;
}

interface PresentationProps {
  title: string;
  slides: Slide[];
  theme?: "dark" | "light";
}

const THEMES = {
  dark: {
    bg: "#2c3e50",
    slideBg: "#34495e",
    title: "#FFFFFF",
    heading: "#ecf0f1",
    body: "#bdc3c7",
    accent: "#3498db",
    endBg: "#2c3e50",
  },
  light: {
    bg: "#ecf0f1",
    slideBg: "#FFFFFF",
    title: "#2c3e50",
    heading: "#2c3e50",
    body: "#7f8c8d",
    accent: "#3498db",
    endBg: "#2c3e50",
  },
};

export const Presentation: React.FC<PresentationProps> = ({
  title,
  slides,
  theme = "dark",
}) => {
  const { fps } = useVideoConfig();
  const colors = THEMES[theme];

  const titleDuration = Math.round(fps * 5);
  const slideDuration = Math.round(fps * 6);
  const endDuration = Math.round(fps * 4);

  return (
    <AbsoluteFill style={{ backgroundColor: colors.bg }}>
      {/* Title slide */}
      <Sequence from={0} durationInFrames={titleDuration}>
        <TitleSlide title={title} colors={colors} fps={fps} />
      </Sequence>

      {/* Content slides */}
      {slides.map((slide, i) => (
        <Sequence
          key={i}
          from={titleDuration + i * slideDuration}
          durationInFrames={slideDuration}
        >
          <ContentSlide
            index={i + 1}
            total={slides.length}
            heading={slide.heading}
            body={slide.body}
            colors={colors}
            fps={fps}
          />
        </Sequence>
      ))}

      {/* End slide */}
      <Sequence
        from={titleDuration + slides.length * slideDuration}
        durationInFrames={endDuration}
      >
        <EndSlide colors={colors} fps={fps} />
      </Sequence>
    </AbsoluteFill>
  );
};

const TitleSlide: React.FC<{
  title: string;
  colors: (typeof THEMES)["dark"];
  fps: number;
}> = ({ title, colors, fps }) => {
  const frame = useCurrentFrame();

  const titleScale = spring({
    frame,
    fps,
    config: { damping: 15, mass: 0.8 },
  });
  const subtitleOpacity = interpolate(
    frame,
    [fps * 0.8, fps * 1.3],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

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
          transform: `scale(${titleScale})`,
          fontSize: 64,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: colors.title,
          textAlign: "center",
          padding: "0 80px",
        }}
      >
        {title}
      </div>
      <div
        style={{
          opacity: subtitleOpacity,
          fontSize: 28,
          fontFamily: "Yu Gothic, sans-serif",
          color: colors.body,
          marginTop: 30,
        }}
      >
        プレゼンテーション
      </div>
    </AbsoluteFill>
  );
};

const ContentSlide: React.FC<{
  index: number;
  total: number;
  heading: string;
  body: string;
  colors: (typeof THEMES)["dark"];
  fps: number;
}> = ({ index, total, heading, body, colors, fps }) => {
  const frame = useCurrentFrame();

  const slideIn = interpolate(frame, [0, fps * 0.4], [40, 0], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.slideBg,
        padding: "80px 100px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Slide number */}
      <div
        style={{
          opacity,
          fontSize: 18,
          fontFamily: "Yu Gothic, sans-serif",
          color: colors.accent,
          marginBottom: 10,
          letterSpacing: "0.1em",
        }}
      >
        {index} / {total}
      </div>

      {/* Heading */}
      <div
        style={{
          opacity,
          transform: `translateX(${slideIn}px)`,
          fontSize: 48,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: colors.heading,
          marginBottom: 15,
        }}
      >
        {heading}
      </div>

      {/* Accent line */}
      <div
        style={{
          width: interpolate(frame, [0, fps * 0.5], [0, 80], {
            extrapolateRight: "clamp",
          }),
          height: 4,
          backgroundColor: colors.accent,
          borderRadius: 2,
          marginBottom: 40,
        }}
      />

      {/* Body */}
      <div
        style={{
          opacity: interpolate(
            frame,
            [fps * 0.3, fps * 0.7],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          ),
          fontSize: 32,
          fontFamily: "Yu Gothic, sans-serif",
          color: colors.body,
          lineHeight: 1.8,
          whiteSpace: "pre-wrap",
          flex: 1,
        }}
      >
        {body}
      </div>
    </AbsoluteFill>
  );
};

const EndSlide: React.FC<{
  colors: (typeof THEMES)["dark"];
  fps: number;
}> = ({ colors, fps }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.endBg,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          opacity,
          fontSize: 56,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: colors.title,
        }}
      >
        ありがとうございました
      </div>
    </AbsoluteFill>
  );
};
