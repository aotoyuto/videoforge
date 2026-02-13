# VideoForge

自然言語から動画を自動生成するシステム。

## 技術スタック
- Python 3.11+ / FFmpeg
- Pydantic (VideoSpec スキーマ)
- Click (CLI)
- VOICEVOX (日本語TTS)

## プロジェクト構造
- `src/videoforge/` - メインパッケージ
  - `schema.py` - VideoSpec Pydanticモデル
  - `spec.py` - YAML読み込み・検証
  - `cli.py` - CLIコマンド
  - `config.py` - 設定管理 (.env)
  - `render/` - FFmpegレンダリングエンジン
  - `assets/` - アセットパイプライン (TTS, AI生成)
  - `export/` - プラットフォーム別出力設定
  - `templates/` - 動画テンプレートYAML
- `examples/` - サンプルVideoSpec
- `skills/` - Claude Codeスキル定義
- `tests/` - pytest テスト

## コマンド
```bash
pip install -e .                              # インストール
videoforge render examples/simple_slideshow.yaml  # レンダリング
videoforge validate examples/simple_slideshow.yaml  # 検証のみ
videoforge template list                      # テンプレート一覧
videoforge check                              # 環境チェック
pytest tests/                                 # テスト実行
```

## 規約
- VideoSpec は YAML で記述
- 日本語フォントは "Yu Gothic" がデフォルト (Docker では "Noto Sans CJK JP")
- AI プロバイダーは Protocol ベースのプラグイン方式
- APIキー未設定のプロバイダーは自動スキップ
