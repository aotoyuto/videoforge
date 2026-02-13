# VideoForge

自然言語の指示一つで動画を自動生成するシステム。
Claude Code スキル経由で操作し、FFmpeg + Python + AI APIを組み合わせて実現。

## 特徴

- **自然言語入力** - 「30秒のYouTubeイントロを作って」で動画生成
- **VideoSpec** - YAMLで動画構成を完全記述
- **テロップ・字幕** - 日本語フォント完全対応
- **BGM・ナレーション** - VOICEVOX等のTTS統合
- **AI素材生成** - 画像・動画・音楽をAIで自動生成（オプション）
- **テンプレート** - YouTube/TikTok/プレゼン等のプリセット
- **プラットフォーム最適化** - 出力先に応じた自動エンコード

## クイックスタート

```bash
# インストール
pip install -e .

# VideoSpecから動画生成
videoforge render examples/simple_slideshow.yaml

# テンプレートから生成
videoforge template use youtube_intro --title "AI入門"

# 出力先指定
videoforge render spec.yaml --output my_video.mp4
```

## Claude Code スキル

```bash
# skills/video-create.md を ~/.claude/commands/ にコピー
cp skills/video-create.md ~/.claude/commands/

# Claude Codeで実行
# /video-create 30秒のイントロ動画、タイトルは「AI入門」、BGMは明るい感じで
```

## 必要環境

- Python 3.11+
- FFmpeg (パスが通っていること)
- 日本語フォント (Yu Gothic / Noto Sans JP 等)

### オプション

- VOICEVOX (日本語TTS) - `http://localhost:50021`
- Docker (コンテナ実行)

## VideoSpec 例

```yaml
version: "1.0"
video:
  title: "サンプル動画"
  resolution: [1920, 1080]
  fps: 30

scenes:
  - id: intro
    type: color
    duration: 5.0
    color: "#1a1a2e"
    text_overlays:
      - content: "AI入門"
        position: center
        font_size: 72
        color: "#FFFFFF"

audio:
  bgm:
    source: "assets/bgm.mp3"
    volume: 0.3

export:
  platform: youtube
```

## プロジェクト構造

```
src/videoforge/
├── cli.py          # CLIコマンド
├── schema.py       # VideoSpec Pydanticモデル
├── spec.py         # YAML読み込み・検証
├── config.py       # 設定管理
├── assets/         # AI素材生成パイプライン
├── render/         # FFmpegレンダリングエンジン
├── export/         # プラットフォーム別出力
└── templates/      # 動画テンプレート
```

## ライセンス

MIT
