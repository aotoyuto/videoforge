# VideoForge

自然言語から動画を自動生成するシステム。

## 技術スタック
- **Python 3.11+** / FFmpeg - コアレンダリング
- **Remotion** (React/TypeScript) - リッチアニメーション動画
- Pydantic (VideoSpec スキーマ)
- Click (CLI)
- VOICEVOX (日本語TTS)

## デュアルエンジン
- **FFmpeg**: `videoforge render spec.yaml` - 高速・シンプル
- **Remotion**: `videoforge render spec.yaml --engine remotion` - リッチアニメーション
- Remotion は `remotion/` ディレクトリの React プロジェクト

## プロジェクト構造
- `src/videoforge/` - Python パッケージ
  - `schema.py` - VideoSpec Pydanticモデル
  - `spec.py` - YAML読み込み・検証
  - `cli.py` - CLIコマンド (render, remotion, template, check)
  - `config.py` - 設定管理 (.env)
  - `render/engine.py` - FFmpegレンダラー
  - `render/remotion.py` - Remotionブリッジ (Python→npx remotion render)
  - `assets/` - アセットパイプライン (TTS, AI生成)
  - `export/` - プラットフォーム別出力設定
  - `templates/` - 動画テンプレートYAML
- `remotion/` - Remotion プロジェクト
  - `src/Root.tsx` - Composition 登録
  - `src/components/` - TextOverlay, SceneRenderer
  - `src/compositions/` - VideoForgeComposition (汎用)
  - `src/templates/` - YouTubeIntro, TikTokShort, TextExplainer, Presentation
- `examples/` - サンプルVideoSpec
- `skills/` - Claude Codeスキル定義
- `tests/` - pytest テスト

## コマンド
```bash
pip install -e .                                            # Python インストール
cd remotion && npm install                                  # Remotion インストール
videoforge render examples/simple_slideshow.yaml            # FFmpeg レンダリング
videoforge render spec.yaml --engine remotion               # Remotion レンダリング
videoforge remotion studio                                  # Remotion Studio
videoforge remotion render YouTubeIntro                     # テンプレート直接レンダリング
videoforge check                                            # 環境チェック
pytest tests/                                               # テスト
```

## Remotion で動画作成する流れ
1. `remotion/src/` にReactコンポーネントを作成（Claude Codeが自然言語から自動生成）
2. `Root.tsx` に Composition を登録
3. `npx remotion studio` でプレビュー
4. `npx remotion render CompositionId output.mp4` でMP4出力

## 規約
- VideoSpec は YAML で記述
- 日本語フォントは "Yu Gothic" がデフォルト (Docker では "Noto Sans CJK JP")
- AI プロバイダーは Protocol ベースのプラグイン方式
- Remotion コンポーネントは TypeScript + React
- Remotion props は zod スキーマでバリデーション
