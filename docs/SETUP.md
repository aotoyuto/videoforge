# VideoForge セットアップガイド

VideoForge の環境構築から動画生成までの完全ガイドです。

---

## 目次

1. [必要環境の確認](#1-必要環境の確認)
2. [リポジトリのクローン](#2-リポジトリのクローン)
3. [Python 環境セットアップ](#3-python-環境セットアップ)
4. [Remotion 環境セットアップ](#4-remotion-環境セットアップ)
5. [VOICEVOX セットアップ（オプション）](#5-voicevox-セットアップオプション)
6. [Claude Code スキル登録](#6-claude-code-スキル登録)
7. [環境チェック](#7-環境チェック)
8. [使い方：FFmpeg エンジン](#8-使い方ffmpeg-エンジン)
9. [使い方：Remotion エンジン](#9-使い方remotion-エンジン)
10. [使い方：Claude Code で自然言語動画作成](#10-使い方claude-code-で自然言語動画作成)
11. [Docker セットアップ（オプション）](#11-docker-セットアップオプション)
12. [トラブルシューティング](#12-トラブルシューティング)

---

## 1. 必要環境の確認

### 必須

| ツール | バージョン | 確認コマンド |
|--------|-----------|-------------|
| Python | 3.11 以上 | `python --version` |
| FFmpeg | 5.0 以上 | `ffmpeg -version` |
| Node.js | 18 以上 | `node --version` |
| npm | 9 以上 | `npm --version` |
| Git | 任意 | `git --version` |

### オプション

| ツール | 用途 | 入手先 |
|--------|------|--------|
| VOICEVOX | 日本語TTS（ナレーション） | https://voicevox.hiroshiba.jp/ |
| Docker | コンテナ実行 | https://www.docker.com/ |
| Claude Code | 自然言語動画作成 | https://claude.ai/claude-code |

### インストールされていない場合

**FFmpeg (Windows):**
```bash
# winget
winget install FFmpeg

# または Chocolatey
choco install ffmpeg

# または公式サイトからダウンロード
# https://ffmpeg.org/download.html
# ダウンロード後、bin/ フォルダへのパスを環境変数 PATH に追加
```

**Node.js:**
```bash
# winget
winget install OpenJS.NodeJS.LTS

# または公式サイト
# https://nodejs.org/
```

---

## 2. リポジトリのクローン

```bash
# GitHub からクローン
git clone https://github.com/aotoyuto/videoforge.git

# プロジェクトディレクトリに移動
cd videoforge
```

既にローカルにある場合:
```bash
cd C:\Users\ThinkPad\Desktop\videoforge
```

---

## 3. Python 環境セットアップ

### 3.1 仮想環境の作成（推奨）

```bash
# 仮想環境を作成
python -m venv .venv

# 有効化 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 有効化 (Windows CMD)
.\.venv\Scripts\activate.bat

# 有効化 (Git Bash / WSL)
source .venv/bin/activate
```

### 3.2 パッケージのインストール

```bash
# 基本インストール（編集可能モード）
pip install -e .

# VOICEVOX TTS も使う場合
pip install -e ".[tts]"

# AI画像生成も使う場合
pip install -e ".[ai]"

# 全部入り
pip install -e ".[all]"

# 開発用（テスト・リンター）
pip install -e ".[dev]"
```

### 3.3 環境変数の設定

```bash
# テンプレートからコピー
cp .env.example .env
```

`.env` を編集して必要な設定を記入:
```env
# VOICEVOX（ローカルで起動する場合はデフォルトのまま）
VOICEVOX_URL=http://localhost:50021

# 出力先ディレクトリ
OUTPUT_DIR=./output

# 日本語フォント設定
DEFAULT_FONT=Yu Gothic
```

AI サービスを使う場合は、対応する API キーも設定してください。

---

## 4. Remotion 環境セットアップ

### 4.1 依存関係のインストール

```bash
cd remotion
npm install
```

### 4.2 Windows 固有の依存関係

通常は `npm install` で自動的にインストールされますが、
エラーが出た場合は以下を手動でインストール:

```bash
npm install @remotion/compositor-win32-x64-msvc
```

### 4.3 動作確認：Remotion Studio

```bash
# remotion/ ディレクトリ内で実行
npm run dev
```

ブラウザで `http://localhost:3000` を開くと Remotion Studio が起動します。
左サイドバーからテンプレートを選んでプレビューできます。

### 4.4 テスト：レンダリング

```bash
# YouTubeIntro テンプレートをレンダリング
npx remotion render YouTubeIntro output/test_intro.mp4
```

`output/test_intro.mp4` が生成されれば成功です。

---

## 5. VOICEVOX セットアップ（オプション）

VOICEVOX を使うと、テキストから日本語音声を自動生成できます。

### 5.1 インストール

1. https://voicevox.hiroshiba.jp/ からダウンロード
2. インストーラーを実行
3. VOICEVOX を起動

### 5.2 起動確認

VOICEVOX を起動した状態で:

```bash
# ブラウザで確認
# http://localhost:50021/docs にアクセス → Swagger UI が表示されればOK

# コマンドで確認
curl http://localhost:50021/version
```

### 5.3 話者一覧の確認

```bash
curl http://localhost:50021/speakers
```

VideoSpec の `speaker_id` にはここで確認できるIDを指定します。
代表的な話者:
- `0` - 四国めたん (ノーマル)
- `1` - ずんだもん (ノーマル)
- `2` - 四国めたん (あまあま)
- `3` - ずんだもん (あまあま)

---

## 6. Claude Code スキル登録

### 6.1 スキルファイルのコピー

```bash
# video-create スキル
cp skills/video-create.md ~/.claude/commands/video-create.md

# video-template スキル
cp skills/video-template.md ~/.claude/commands/video-template.md
```

Windows の場合:
```bash
copy skills\video-create.md %USERPROFILE%\.claude\commands\video-create.md
copy skills\video-template.md %USERPROFILE%\.claude\commands\video-template.md
```

### 6.2 確認

Claude Code を起動して `/video-create` と入力すると、スキルが呼び出されます。

---

## 7. 環境チェック

全ての環境が正しくセットアップされたか確認:

```bash
videoforge check
```

出力例:
```
System check:
  FFmpeg: OK (C:\tools\ffmpeg\bin\ffmpeg.exe)
  FFprobe: OK (C:\tools\ffmpeg\bin\ffprobe.exe)
  Node.js: OK (v24.12.0)
  npx: OK (C:\Program Files\nodejs\npx.cmd)
  Remotion: OK (installed)
  VOICEVOX: OK (http://localhost:50021)
  Python: 3.12.10 (...)
```

---

## 8. 使い方：FFmpeg エンジン

### 8.1 サンプル動画を生成

```bash
# シンプルなスライドショー
videoforge render examples/simple_slideshow.yaml

# 出力先を指定
videoforge render examples/simple_slideshow.yaml -o output/my_video.mp4
```

### 8.2 テンプレートから生成

```bash
# テンプレート一覧を確認
videoforge template list

# YouTubeイントロを生成
videoforge template use youtube_intro --title "AI入門"

# プレゼンテーションを生成
videoforge template use presentation --title "月次報告"
```

### 8.3 VideoSpec を自分で書く

```yaml
# my_video.yaml
version: "1.0"
video:
  title: "テスト動画"
  resolution: [1920, 1080]
  fps: 30

scenes:
  - id: title
    type: color
    duration: 5.0
    color: "#2c3e50"
    text_overlays:
      - content: "Hello VideoForge!"
        position: center
        font_size: 64
        color: "#FFFFFF"

export:
  platform: youtube
```

```bash
videoforge render my_video.yaml -o output/test.mp4
```

---

## 9. 使い方：Remotion エンジン

### 9.1 Remotion Studio でプレビュー

```bash
cd remotion
npm run dev
```

ブラウザで http://localhost:3000 を開き、左サイドバーからテンプレートを選択。
プロパティパネルでリアルタイムに値を変更してプレビューできます。

### 9.2 テンプレートからレンダリング

```bash
cd remotion

# YouTubeイントロ
npx remotion render YouTubeIntro output/intro.mp4 \
  --props '{"title":"AI入門","subtitle":"Episode 1","accentColor":"#ff6b6b"}'

# TikTokショート（縦型）
npx remotion render TikTokShort output/tiktok.mp4 \
  --props '{"title":"3つのコツ","points":["具体的に書く","文脈を伝える","形式を指定する"]}'

# テキスト解説動画
npx remotion render TextExplainer output/explainer.mp4 \
  --props '{"title":"ChatGPTの使い方","sections":[{"heading":"基本","body":"ChatGPTとは..."},{"heading":"コツ","body":"具体的に質問する"}]}'

# プレゼンテーション
npx remotion render Presentation output/presentation.mp4 \
  --props '{"title":"月次報告","slides":[{"heading":"売上","body":"前月比120%"},{"heading":"課題","body":"人材確保が急務"}],"theme":"dark"}'
```

### 9.3 VideoSpec から Remotion レンダリング

```bash
# プロジェクトルートで実行
videoforge render examples/simple_slideshow.yaml --engine remotion -o output/remotion_test.mp4
```

### 9.4 propsファイルを使う場合

`props.json` を作成:
```json
{
  "title": "AI入門講座",
  "subtitle": "Episode 1: AIとは何か？",
  "accentColor": "#3498db"
}
```

```bash
cd remotion
npx remotion render YouTubeIntro output/intro.mp4 --props props.json
```

---

## 10. 使い方：Claude Code で自然言語動画作成

これが VideoForge の真骨頂です。

### 10.1 基本ワークフロー

```bash
# ターミナル1: Remotion Studio を起動
cd C:\Users\ThinkPad\Desktop\videoforge\remotion
npm run dev

# ターミナル2: Claude Code を起動
cd C:\Users\ThinkPad\Desktop\videoforge
claude
```

### 10.2 自然言語で指示する例

Claude Code 内で以下のように指示:

**FFmpeg エンジン（シンプル）:**
```
/video-create 30秒のスライドショー、タイトルは「旅行の思い出」、3つのスライドで
```

**Remotion エンジン（リッチ）:**
```
/video-create YouTubeのイントロを作って。タイトルは「プログラミング講座」、アニメーション付きで、Remotionで
```

**テンプレート使用:**
```
/video-template youtube_intro タイトルは「データサイエンス入門」
```

### 10.3 Remotion で完全カスタム動画を作る

Claude Code に直接 Remotion コンポーネントを書かせることもできます:

```
remotion/src/ に新しいコンポーネントを作って。
内容: 宇宙をテーマにした30秒のプロモーション動画。
星がキラキラ光るアニメーション背景に、
「未来を創る」というタイトルがフェードインして、
3つのポイントが順番にスライドインする。
最後にCTAで「今すぐ登録」と表示。
```

Claude が React コンポーネントを生成 → Remotion Studio でリアルタイムプレビュー → `npx remotion render` でMP4出力、という流れになります。

---

## 11. Docker セットアップ（オプション）

### 11.1 Docker Compose で起動

```bash
# ビルド＆起動（VOICEVOX込み）
docker compose up --build

# バックグラウンド起動
docker compose up -d --build
```

### 11.2 Docker でレンダリング

```bash
# サンプル動画を生成
docker compose run videoforge render examples/simple_slideshow.yaml

# テンプレートから生成
docker compose run videoforge template use youtube_intro --title "AI入門"
```

出力は `output/` ディレクトリに保存されます（ホストマシンにマウント済み）。

### 11.3 Docker 環境のカスタマイズ

`docker-compose.yml` の `environment` セクションで設定を変更できます。
Docker 環境では日本語フォントに "Noto Sans CJK JP" を使用します。

---

## 12. トラブルシューティング

### FFmpeg が見つからない

```
RuntimeError: FFmpeg not found
```

**対処法:**
```bash
# FFmpeg がインストールされているか確認
ffmpeg -version

# パスが通っているか確認
where ffmpeg    # Windows
which ffmpeg    # Linux/Mac
```

パスが通っていない場合は環境変数 `PATH` に FFmpeg の `bin/` ディレクトリを追加してください。

### Remotion のインストールエラー

```
npm ERR! ...
```

**対処法:**
```bash
# node_modules を削除して再インストール
cd remotion
rm -rf node_modules package-lock.json
npm install

# Windows 固有の依存関係を追加
npm install @remotion/compositor-win32-x64-msvc
```

### 日本語テキストが文字化けする

**対処法:**
- "Yu Gothic" フォントがインストールされているか確認
  （Windows 10/11 にはデフォルトで含まれています）
- `.env` で `DEFAULT_FONT` と `DEFAULT_FONT_PATH` を確認
- Docker の場合は "Noto Sans CJK JP" が自動インストールされます

### VOICEVOX に接続できない

```
VOICEVOX: NOT RUNNING
```

**対処法:**
1. VOICEVOX アプリが起動しているか確認
2. `http://localhost:50021/version` にブラウザでアクセスして確認
3. `.env` の `VOICEVOX_URL` が正しいか確認
4. ファイアウォールがポート 50021 をブロックしていないか確認

### Remotion Studio が開かない

**対処法:**
```bash
cd remotion
npm run dev

# ポートが使われている場合
npx remotion studio --port 3001
```

### レンダリングが遅い

- **FFmpeg**: `-preset ultrafast` を試す（品質は下がります）
- **Remotion**: `--concurrency` オプションでCPUコア数を指定
  ```bash
  npx remotion render YouTubeIntro output.mp4 --concurrency=4
  ```

### VideoSpec の YAML エラー

```bash
# YAML の構文チェック
videoforge validate my_spec.yaml
```

よくあるミス:
- インデントが揃っていない（スペース2つ推奨）
- 文字列にコロン `:` を含む場合はクォートで囲む
- `resolution` は `[1920, 1080]` の配列形式で指定

---

## 次のステップ

セットアップが完了したら、以下を試してみてください:

1. `videoforge render examples/simple_slideshow.yaml` でFFmpegエンジンを体験
2. `cd remotion && npm run dev` でRemotion Studioを体験
3. Claude Code で `/video-create YouTubeイントロ、タイトルは「テスト」` を実行
4. `examples/` のYAMLを編集してカスタム動画を作成
5. `remotion/src/templates/` を参考に独自テンプレートを作成
