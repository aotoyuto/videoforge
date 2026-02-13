# 動画作成 (Video Create)

自然言語の指示から動画を自動生成します。

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

### Step 2: VideoSpec YAML を生成

上記の解析結果をもとに、VideoForge の VideoSpec YAML を生成してください。

YAML のフォーマット:

```yaml
version: "1.0"
video:
  title: "タイトル"
  resolution: [1920, 1080]  # YouTube=16:9, TikTok/Reels=[1080, 1920]
  fps: 30

scenes:
  - id: scene_名前
    type: color          # color / image / video
    duration: 秒数
    color: "#hex色"      # type=colorの場合
    source: "パス"       # type=image/videoの場合
    text_overlays:
      - content: "テキスト"
        position: center   # center / top_center / bottom_center / top_left / bottom_left / top_right / bottom_right
        font: "Yu Gothic"
        font_size: 48
        color: "#FFFFFF"
        bg_color: "#00000088"  # 半透明背景 (オプション)
        start: 0.5        # 表示開始秒 (オプション)
        end: 4.5           # 表示終了秒 (オプション)
    transition_out: fade   # none / fade / crossfade / wipe_left / dissolve
    transition_duration: 0.5

audio:
  bgm:
    source: "BGMファイルパス"  # ローカルファイルがある場合
    volume: 0.3
    fade_in: 1.0
    fade_out: 2.0
  narration:
    - scene: scene_id
      text: "ナレーションテキスト"
      voice: voicevox
      speaker_id: 1

export:
  platform: youtube    # youtube / tiktok / instagram
  codec: h264
```

### Step 3: YAML ファイルを保存

生成した YAML を VideoForge プロジェクトディレクトリ内に保存してください:

```
C:\Users\ThinkPad\Desktop\videoforge\output\{タイトル}_spec.yaml
```

### Step 4: レンダリング実行

以下のコマンドでレンダリングを実行してください:

```bash
cd C:\Users\ThinkPad\Desktop\videoforge
python -m videoforge.cli render output/{タイトル}_spec.yaml -o output/{タイトル}.mp4
```

### Step 5: 結果を報告

レンダリング結果をユーザーに報告:
- 出力ファイルパス
- 動画の長さ
- 解像度
- 含まれるシーン数

## テンプレート一覧

利用可能なテンプレート:
- `youtube_intro` - YouTubeイントロ (7秒)
- `youtube_outro` - YouTubeアウトロ (10秒)
- `tiktok_short` - TikTokショート動画 (15秒)
- `presentation` - プレゼンテーション
- `photo_montage` - フォトモンタージュ
- `text_explainer` - テキスト解説動画

テンプレートを使う場合:

```bash
cd C:\Users\ThinkPad\Desktop\videoforge
python -m videoforge.cli template use テンプレート名 --title "タイトル" -o output/出力.mp4
```

## 注意事項

- BGMファイルがない場合は `audio.bgm` セクションを省略
- VOICEVOX が起動していない場合はナレーションをスキップ
- 画像を使う場合は絶対パスまたは VideoSpec からの相対パスで指定
- 日本語フォントは "Yu Gothic" をデフォルトで使用
