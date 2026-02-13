import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

interface Section {
  heading: string;
  body: string;
}

interface TextExplainerProps {
  title: string;
  sections: Section[];
}

export const TextExplainer: React.FC<TextExplainerProps> = ({
  title,
  sections,
}) => {
  const { fps } = useVideoConfig();

  const introDuration = Math.round(fps * 3);
  const sectionDuration = Math.round(fps * 6);
  const outroDuration = Math.round(fps * 4);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1117" }}>
      {/* Intro */}
      <Sequence from={0} durationInFrames={introDuration}>
        <IntroSlide title={title} fps={fps} />
      </Sequence>

      {/* Sections */}
      {sections.map((section, i) => (
        <Sequence
          key={i}
          from={introDuration + i * sectionDuration}
          durationInFrames={sectionDuration}
        >
          <SectionSlide
            index={i + 1}
            heading={section.heading}
            body={section.body}
            fps={fps}
          />
        </Sequence>
      ))}

      {/* Outro */}
      <Sequence
        from={introDuration + sections.length * sectionDuration}
        durationInFrames={outroDuration}
      >
        <OutroSlide fps={fps} />
      </Sequence>
    </AbsoluteFill>
  );
};

const IntroSlide: React.FC<{ title: string; fps: number }> = ({
  title,
  fps,
}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });
  const lineWidth = spring({
    frame,
    fps,
    config: { damping: 15, mass: 0.5 },
  }) * 300;

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
          opacity,
          fontSize: 64,
          fontFamily: "Yu Gothic, sans-serif",
          fontWeight: "bold",
          color: "#58a6ff",
          textAlign: "center",
        }}
      >
        {title}
      </div>
      <div
        style={{
          width: lineWidth,
          height: 2,
          backgroundColor: "#58a6ff",
          marginTop: 20,
          borderRadius: 1,
        }}
      />
    </AbsoluteFill>
  );
};

const SectionSlide: React.FC<{
  index: number;
  heading: string;
  body: string;
  fps: number;
}> = ({ index, heading, body, fps }) => {
  const frame = useCurrentFrame();

  const headingOpacity = interpolate(frame, [0, fps * 0.4], [0, 1], {
    extrapolateRight: "clamp",
  });
  const bodyOpacity = interpolate(
    frame,
    [fps * 0.3, fps * 0.7],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const bodyY = interpolate(frame, [fps * 0.3, fps * 0.7], [20, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        padding: "80px 120px",
      }}
    >
      {/* Section number + heading */}
      <div style={{ opacity: headingOpacity, marginBottom: 40 }}>
        <span
          style={{
            fontSize: 24,
            fontFamily: "Yu Gothic, sans-serif",
            color: "#58a6ff",
            letterSpacing: "0.15em",
            textTransform: "uppercase",
          }}
        >
          Point {index}
        </span>
        <div
          style={{
            fontSize: 48,
            fontFamily: "Yu Gothic, sans-serif",
            fontWeight: "bold",
            color: "#c9d1d9",
            marginTop: 10,
          }}
        >
          {heading}
        </div>
        <div
          style={{
            width: 60,
            height: 3,
            backgroundColor: "#58a6ff",
            marginTop: 15,
            borderRadius: 2,
          }}
        />
      </div>

      {/* Body text */}
      <div
        style={{
          opacity: bodyOpacity,
          transform: `translateY(${bodyY}px)`,
          fontSize: 32,
          fontFamily: "Yu Gothic, sans-serif",
          color: "#8b949e",
          lineHeight: 1.8,
          whiteSpace: "pre-wrap",
        }}
      >
        {body}
      </div>
    </AbsoluteFill>
  );
};

const OutroSlide: React.FC<{ fps: number }> = ({ fps }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#161b22",
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
          color: "#FFFFFF",
        }}
      >
        まとめ
      </div>
    </AbsoluteFill>
  );
};
