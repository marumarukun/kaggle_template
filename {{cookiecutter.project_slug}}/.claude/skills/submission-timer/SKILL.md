---
name: submission-timer
description: Kaggleコンペの提出を監視し、提出から完了までの所要時間を計測する。「提出時間を計測して」「サブミットの時間測って」「提出を監視して」と言ったときに使用。提出一覧をポーリングしてPENDING→COMPLETE/ERRORの変化を検知し、経過時間・スコアを報告する。単なる提出状況の確認（status.sh）には使用しない。
---

# Submission Timer

Kaggleコンペの提出を監視し、PENDING→COMPLETE/ERRORの所要時間を自動計測するスキル。

## 使い方

ユーザーが提出の監視を依頼したら、以下のスクリプトを実行する:

```bash
uv run python .claude/skills/submission-timer/scripts/watch_submission.py \
    --competition <competition-slug> \
    --interval 60 \
    --time-limit <制限時間>   # 省略可。例: 9h, 30m
```

### 引数

| 引数 | 必須 | デフォルト | 説明 |
|------|------|-----------|------|
| `--competition` | Yes | - | コンペティションのスラッグ（例: `birdclef-2026`） |
| `--interval` | No | `60` | ポーリング間隔（秒） |
| `--time-limit` | No | なし | コンペの実行時間制限（例: `9h`, `30m`）。指定時のみ使用率を表示 |

### コンペスラッグの自動取得

引数が省略された場合、`sub/kernel-metadata.json` の `competition_sources` から自動取得を試みる。

## 実行フロー

1. **スナップショット取得**: 現在の提出一覧を取得し、既存の提出IDを記録
2. **待機**: 新しい提出（スナップショットに存在しないPENDING提出）が現れるまでポーリング
3. **計測**: 新しい提出を検知したら、検知時刻を記録し追跡開始
4. **完了検知**: ステータスがCOMPLETEまたはERRORに変わったら結果を報告
5. **報告内容**:
   - 経過時間（検知〜完了）
   - 提出のステータス（COMPLETE / ERROR）
   - スコア（利用可能な場合）
   - 制限時間に対する使用率（`--time-limit` 指定時のみ）

## 使用例

### 基本（コンペスラッグは kernel-metadata.json から自動取得）
```bash
uv run python .claude/skills/submission-timer/scripts/watch_submission.py
```

### 制限時間付き
```bash
uv run python .claude/skills/submission-timer/scripts/watch_submission.py --time-limit 9h
```

### 出力例
```
[12:00:00] コンペ: birdclef-2026
[12:00:00] 制限時間: 9時間0分0秒
[12:00:00] ポーリング間隔: 60秒

[12:00:01] スナップショット取得: 提出20件
[12:00:01] 新しい提出を待機中...
[12:01:01] 新しい提出を検知! Version 54 (ref=12345678)
[12:02:01] PENDING... Version 54 (経過: 1分0秒)
...
==================================================
  COMPLETE!
  提出: Version 54
  経過時間: 14分32秒
  スコア: 0.928
  制限時間に対する使用率: 2.7% (14分32秒 / 9時間0分0秒)
==================================================
```

## エラーハンドリング

- **API呼び出し失敗**: リトライして継続。3回連続失敗で警告を表示するが監視は継続
- **Ctrl+C**: 現在の経過時間を表示して終了
- **提出がERROR**: エラー内容を表示（`errorDescription`フィールド）

## 注意事項

- 計測される時間はキュー待ち時間を含む壁時計時間であり、純粋なNB実行時間ではない
- テストデータの量はステージによって変わるため、同じNBでもステージごとに実行時間は異なる
- 複数の提出が同時にPENDINGの場合、すべてを追跡する
