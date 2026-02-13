# VideoForge

自然言語の指示一つで動画を自動生成するシステム。
Claude Code スキル経由で操作し、**FFmpeg** + **Remotion** + AI APIを組み合わせて実現。

## 特徴

- **自然言語入力** - 「30秒のYouTubeイントロを作って」で動画生成
- **デュアルエンジン** - FFmpeg（高速・シンプル）+ Remotion（リッチアニメーション）
- **VideoSpec** - YAMLで動画構成を完全記述
- **Remotion テンプレート** - React コンポーネントで高品質テンプレート
- **テロップ・字幕** - 日本語フォント完全対応
- **BGM・ナレーション** - VOICEVOX等のTTS統合
- **AI素材生成** - 画像・動画・音楽をAIで自動生成（オプション）
- **プラットフォーム最適化** - YouTube/TikTok/Instagram向け自動エンコード

## クイックスタート

### FFmpeg エンジン（シンプル・高速）

```bash
pip install -e .
videoforge render examples/simple_slideshow.yaml
videoforge template use youtube_intro --title "AI入門"
```

### Remotion エンジン（リッチアニメーション）

```bash
# セットアップ（初回のみ）
cd remotion && npm install

# Remotion Studio でライブプレビュー
npm run dev
# → http://localhost:3000 でブラウザプレビュー

# テンプレートからレンダリング
npx remotion render YouTubeIntro output.mp4 --props '{"title":"AI入門"}'

# VideoSpec → Remotion レンダリング
videoforge render examples/simple_slideshow.yaml --engine remotion
```

### Claude Code で自然言語動画作成

```bash
# スキルのインストール
cp skills/video-create.md ~/.claude/commands/

# Claude Code で実行
# /video-create 30秒のYouTubeイントロ、タイトルは「AI入門」、リッチなアニメーションで
```

Claude Code 内で Remotion プロジェクト (`remotion/`) を直接編集し、自然言語でReactコンポーネントを生成・レンダリングできます。

## 必要環境

- Python 3.11+
- FFmpeg (パスが通っていること)
- Node.js 18+ (Remotion エンジン用)
- 日本語フォント (Yu Gothic / Noto Sans JP 等)

### オプション

- VOICEVOX (日本語TTS) - `http://localhost:50021`
- Docker (コンテナ実行)

## Remotion テンプレート

| Composition | 用途 | Props |
|------------|------|-------|
| `YouTubeIntro` | YouTubeイントロ | `title`, `subtitle?`, `accentColor?` |
| `TikTokShort` | TikTokショート | `title`, `points[]`, `accentColor?` |
| `TextExplainer` | テキスト解説 | `title`, `sections[{heading,body}]` |
| `Presentation` | プレゼン | `title`, `slides[{heading,body}]`, `theme?` |
| `VideoForgeComposition` | 汎用 (VideoSpec) | VideoSpec YAML 形式 |

## プロジェクト構造

```
videoforge/
├── src/videoforge/           # Python パッケージ
│   ├── cli.py                # CLI (render, remotion, template, check)
│   ├── schema.py             # VideoSpec Pydantic モデル
│   ├── render/               # FFmpeg + Remotion レンダラー
│   ├── assets/               # AI素材パイプライン (TTS, 画像, 音楽)
│   ├── export/               # プラットフォーム別設定
│   └── templates/            # YAML テンプレート
├── remotion/                 # Remotion プロジェクト
│   ├── src/
│   │   ├── Root.tsx          # Composition 登録
│   │   ├── components/       # 共通コンポーネント
│   │   ├── compositions/     # メイン Composition
│   │   └── templates/        # テンプレート (YouTube, TikTok, etc.)
│   └── package.json
├── examples/                 # サンプル VideoSpec
├── skills/                   # Claude Code スキル
├── Dockerfile
└── docker-compose.yml
```

## コマンド一覧

```bash
# FFmpeg レンダリング
videoforge render spec.yaml [-o output.mp4]

# Remotion レンダリング
videoforge render spec.yaml --engine remotion [-o output.mp4]
videoforge remotion studio          # Remotion Studio 起動
videoforge remotion render YouTubeIntro [-o output.mp4]
videoforge remotion list            # Composition 一覧
videoforge remotion install         # npm install

# テンプレート
videoforge template list
videoforge template use youtube_intro --title "タイトル"

# ユーティリティ
videoforge check                    # 環境チェック
videoforge validate spec.yaml       # VideoSpec 検証
```

## ライセンス

MIT
