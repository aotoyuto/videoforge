# 動画テンプレート選択 (Video Template)

VideoForge のテンプレートから動画を作成します。

## 使い方

```
/video-template $ARGUMENTS
```

## ワークフロー

### Step 1: テンプレート選択

`$ARGUMENTS` からテンプレート名とパラメータを特定してください。

利用可能テンプレート:

| テンプレート | 用途 | デフォルト長さ |
|-------------|------|-------------|
| youtube_intro | YouTubeイントロ | 7秒 |
| youtube_outro | YouTubeアウトロ | 10秒 |
| tiktok_short | TikTokショート | 15秒 |
| presentation | プレゼン | 17秒 |
| photo_montage | フォトモンタージュ | 15秒 |
| text_explainer | テキスト解説 | 19秒 |

### Step 2: テンプレートをカスタマイズ

テンプレート YAML を読み込み、ユーザーの要望に合わせてカスタマイズ:

1. テンプレートファイルを読む: `C:\Users\ThinkPad\Desktop\videoforge\src\videoforge\templates\{名前}.yaml`
2. `{{title}}` をユーザー指定のタイトルに置換
3. 必要に応じてシーンの追加・削除・テキスト変更
4. カスタマイズした YAML を保存

### Step 3: レンダリング

```bash
cd C:\Users\ThinkPad\Desktop\videoforge
python -m videoforge.cli render output/{タイトル}_spec.yaml -o output/{タイトル}.mp4
```

### Step 4: 結果報告

出力ファイルパス、長さ、解像度を報告。
