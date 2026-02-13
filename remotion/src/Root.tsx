import { Composition } from "remotion";
import { VideoForgeComposition } from "./compositions/VideoForgeComposition";
import { VideoSpecSchema } from "./types";
import { YouTubeIntro } from "./templates/YouTubeIntro";
import { TikTokShort } from "./templates/TikTokShort";
import { TextExplainer } from "./templates/TextExplainer";
import { Presentation } from "./templates/Presentation";

// Default props for preview
const defaultSpec = {
  version: "1.0",
  video: {
    title: "VideoForge Preview",
    resolution: [1920, 1080] as [number, number],
    fps: 30,
    background_color: "#000000",
  },
  scenes: [
    {
      id: "title",
      type: "color" as const,
      duration: 4,
      color: "#1a1a2e",
      text_overlays: [
        {
          content: "VideoForge + Remotion",
          position: "center" as const,
          font: "Yu Gothic",
          font_size: 72,
          color: "#FFFFFF",
          animation: "fade_in" as const,
        },
      ],
      transition_out: "fade" as const,
      transition_duration: 0.5,
    },
    {
      id: "slide",
      type: "color" as const,
      duration: 3,
      color: "#2c3e50",
      text_overlays: [
        {
          content: "自然言語で動画を作成",
          position: "center" as const,
          font: "Yu Gothic",
          font_size: 48,
          color: "#ecf0f1",
          animation: "fade_in" as const,
        },
      ],
      transition_out: "none" as const,
      transition_duration: 0.5,
    },
  ],
  audio: {},
  export: { format: "mp4", codec: "h264", platform: "youtube", quality: "high" },
};

export const RemotionRoot: React.FC = () => {
  const totalFrames = defaultSpec.scenes.reduce(
    (sum, s) => sum + s.duration * defaultSpec.video.fps,
    0
  );

  return (
    <>
      {/* Main dynamic composition - renders any VideoSpec */}
      <Composition
        id="VideoForgeComposition"
        component={VideoForgeComposition}
        durationInFrames={totalFrames}
        fps={defaultSpec.video.fps}
        width={defaultSpec.video.resolution[0]}
        height={defaultSpec.video.resolution[1]}
        schema={VideoSpecSchema}
        defaultProps={defaultSpec}
      />

      {/* Pre-built templates */}
      <Composition
        id="YouTubeIntro"
        component={YouTubeIntro}
        durationInFrames={210}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "チャンネル名",
          subtitle: "Episode 1",
          accentColor: "#ff6b6b",
        }}
      />

      <Composition
        id="TikTokShort"
        component={TikTokShort}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: "動画タイトル",
          points: ["ポイント1", "ポイント2", "ポイント3"],
          accentColor: "#ff6b6b",
        }}
      />

      <Composition
        id="TextExplainer"
        component={TextExplainer}
        durationInFrames={570}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "解説テーマ",
          sections: [
            { heading: "ポイント1", body: "詳しい説明文をここに。" },
            { heading: "ポイント2", body: "二つ目の説明をここに。" },
          ],
        }}
      />

      <Composition
        id="Presentation"
        component={Presentation}
        durationInFrames={510}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "プレゼンテーション",
          slides: [
            { heading: "第1章", body: "ここに説明を。" },
            { heading: "第2章", body: "次の内容を。" },
          ],
          theme: "dark" as const,
        }}
      />
    </>
  );
};
