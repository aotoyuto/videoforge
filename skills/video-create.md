# 動画作成 (Video Create)

自然言語の指示から動画を自動生成します。
**2つのエンジン対応**: FFmpeg（シンプル・高速）と Remotion（リッチなアニメーション）。

## 使い方

```
/video-create $ARGUMENTS
```

## ワークフロー

### Step 1: 要件を解析

ユーザーの指示 (`$ARGUMENTS`) を解析して以下の要素を抽出してください:

- **動画の目的・タイトル** (例: "AI入門", "商品紹介")
- **長さ** (例: "30秒", "1分") → デフォルト: 30秒
- **プラットフォーム** (例: "YouTube", "TikTok", "Instagram") → デフォルト: YouTube
- **テロップ・テキスト内容**
- **BGM・音楽のイメージ** (例: "明るい", "落ち着いた")
- **ナレーションの有無**
- **使用したい素材** (画像・動画のパス)
- **テンプレート指定** (例: "イントロ", "プレゼン")
- **エンジン指定**: "リッチ" "アニメーション" "Remotion" → Remotion、それ以外 → FFmpeg

### Step 2: エンジン選択

**Remotion を使う場合** (アニメーション重視、リッチなエフェクト):

1. `C:\Users\ThinkPad\Desktop\videoforge\remotion\` ディレクトリで作業
2. Remotion Studio を使ったライブプレビュー可能
3. React コンポーネントとして動画を作成
4. `npx remotion render` でMP4出力

**FFmpeg を使う場合** (シンプル、高速):

1. VideoSpec YAML を生成
2. `videoforge render` で実行

### Step 3A: Remotion で作成する場合

#### 方法1: 直接Reactコンポーネントを書く（最も柔軟）

Remotion プロジェクト内で新しいコンポーネントを作成してください:

```
C:\Users\ThinkPad\Desktop\videoforge\remotion\src\
```

**基本構造:**
```tsx
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

export const MyVideo: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
      <div style={{
        opacity,
        fontSize: 72,
        fontFamily: "Yu Gothic, sans-serif",
        color: "#FFFFFF",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100%",
      }}>
        {title}
      </div>
    </AbsoluteFill>
  );
};
```

Remotion の主要API:
- `useCurrentFrame()` - 現在のフレーム番号
- `useVideoConfig()` - fps, width, height, durationInFrames
- `interpolate(frame, inputRange, outputRange)` - アニメーション補間
- `spring({ frame, fps })` - バネアニメーション
- `<Sequence from={frame} durationInFrames={n}>` - タイムライン配置
- `<AbsoluteFill>` - フルスクリーンレイヤー
- `<Img src={...}>` - 画像表示
- `<Video src={...}>` - 動画埋め込み

Root.tsx に Composition を登録してからレンダリング:

```bash
cd C:\Users\ThinkPad\Desktop\videoforge\remotion
npx remotion render MyCompositionId output.mp4 --props props.json
```

#### 方法2: 既存テンプレートを使う

利用可能なRemotion Composition:
- `YouTubeIntro` - props: `{ title, subtitle?, accentColor? }`
- `TikTokShort` - props: `{ title, points: string[], accentColor? }`
- `TextExplainer` - props: `{ title, sections: [{ heading, body }] }`
- `Presentation` - props: `{ title, slides: [{ heading, body }], theme?: "dark"|"light" }`
- `VideoForgeComposition` - VideoSpec 形式のprops（汎用）

```bash
cd C:\Users\ThinkPad\Desktop\videoforge\remotion
npx remotion render YouTubeIntro output.mp4 --props '{"title":"AI入門","subtitle":"Episode 1"}'
```

#### 方法3: VideoSpec YAML → Remotion

```bash
cd C:\Users\ThinkPad\Desktop\videoforge
python -m videoforge.cli render spec.yaml --engine remotion -o output.mp4
```

### Step 3B: FFmpeg で作成する場合

VideoSpec YAML を生成して保存:

```yaml
version: "1.0"
video:
  title: "タイトル"
  resolution: [1920, 1080]
  fps: 30

scenes:
  - id: scene_名前
    type: color
    duration: 秒数
    color: "#hex色"
    text_overlays:
      - content: "テキスト"
        position: center
        font: "Yu Gothic"
        font_size: 48
        color: "#FFFFFF"
    transition_out: fade
    transition_duration: 0.5

audio:
  bgm:
    source: "BGMファイルパス"
    volume: 0.3

export:
  platform: youtube
  codec: h264
```

保存先: `C:\Users\ThinkPad\Desktop\videoforge\output\{タイトル}_spec.yaml`

レンダリング:
```bash
cd C:\Users\ThinkPad\Desktop\videoforge
python -m videoforge.cli render output/{タイトル}_spec.yaml -o output/{タイトル}.mp4
```

### Step 4: 結果を報告

- 出力ファイルパス
- 動画の長さ
- 解像度
- 使用エンジン（FFmpeg or Remotion）

## Remotion Studio でライブプレビュー

```bash
cd C:\Users\ThinkPad\Desktop\videoforge\remotion
npm run dev
# ブラウザで http://localhost:3000 を開く
```

## セットアップ（初回のみ）

```bash
cd C:\Users\ThinkPad\Desktop\videoforge\remotion
npm install
```

## 注意事項

- Remotion はリッチなアニメーション・エフェクトに強い（CSS、React の全機能が使える）
- FFmpeg はシンプルなスライドショーやテロップ付き動画に向く
- 日本語フォントは "Yu Gothic" をデフォルトで使用
- BGMファイルがない場合は audio セクションを省略
- VOICEVOX が起動していない場合はナレーションをスキップ
