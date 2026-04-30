# Experiment Documentation Templates

新規プロジェクトでこのスキルを初めて使う時、以下の 4 ファイル（+ 任意で `experiments/{NNN}/SPEC.md`）を作成する。
詳細な運用は `SKILL.md` を参照。

---

## `docs/agent_brief.md`

```markdown
# Agent Brief — {compe_name}

> 新しい実験の壁打ち・実装前にエージェントが必ず最初に読むファイル。
> 詳細は `docs/experiment_index.md` から該当実験 (`docs/experiment_log.md` または `experiments/{NNN}/SPEC.md`) を引く。
> 採用/封印/条件付きの判断ルールは `docs/decision_rules.md`。

最終更新: YYYY-MM-DD

---

## Current State
- Best LB / CV
- Current Phase
- Active experiments
- Next likely moves

## Must-Know Operational Rules
- 実行コマンドの規約 (`uv run python` 等)
- バージョン管理ルール (`EXP_VERSION` 等)
- Kaggle 提出時の注意 (code/model セット push 等)
- ローカルテストの必須事項
- 評価指標の代理指標 (OOF/CV) 信頼度

## Strategic Conclusions
- 現在の実験設計に効く横断知見

## Do Not Repeat
- 過去に明確に失敗したアプローチ (再試行禁止)

## Open Questions
- 次に検証すべき問い

## Where To Look
- 詳細を見るべきファイルへの案内
```

---

## `docs/decision_rules.md`

```markdown
# Decision Rules — {compe_name}

> 「知見」ではなく**次の判断に直接使うルール**だけを集めたファイル。
> 詳細な経緯は `docs/experiment_log.md` の該当 Experiment セクション。

最終更新: YYYY-MM-DD

---

## Adopted (採用済み・継続する設計)
- カテゴリ別 (モデル / データ / パイプライン 等) に箇条書き

## Rejected (封印・再検討不要)
- カテゴリ別に「失敗内容 + 理由」を 1 行ずつ

## Conditional (条件付き判断 / 未確定)
- 条件次第で採否が変わるもの。次の検証計画と合わせて記載

## Operational Pitfalls (実装/運用で踏みやすい罠)
- 過去に踏んだ実装ミス・運用事故と回避方法
```

---

## `docs/experiment_index.md`

```markdown
# Experiment Index — {compe_name}

> 全実験の索引。詳細は `docs/experiment_log.md` の該当 Experiment セクションを参照。
> 設計仕様 (SPEC.md) があるものは `experiments/{NNN}/SPEC.md` も参照。

最終更新: YYYY-MM-DD

---

## Legend
- LB: スコア (TF=teacher 等を区別)
- Decision: `adopted` / `closed` / `superseded` / `current`
- Links: `log` (experiment_log.md), `spec` (SPEC.md)

---

## Phase 1: {Phase 名}

| Exp | Theme | LB | Decision | Links |
|---|---|---:|---|---|
| 001 | (タイトル) | 0.XXX | adopted | log |

## Phase 2: {Phase 名}

| Exp | Theme | LB | Decision | Links |
|---|---|---:|---|---|
| ... | ... | ... | ... | ... |

---

## Quick lookup
- 現 TOP: `XXX` — 構成
- 旧 TOP / superseded baseline: `XXX`
- 失敗で学んだ大きな実験: `XXX`
```

---

## `docs/experiment_log.md`

```markdown
# Experiment Log

## Current Status
- **Best LB**: (スコア) — 実験XXX (日付)
- **Current Phase**: (現在取り組んでいるフェーズ)
- **Recent milestones**: 日付付きで主要な動き
- **Next Priority**: (次にやるべきこと)

## Strategy

コンペ全体の戦略とフェーズ。`/experiment-log` スキルが勝手に書き換えない領域。

- [ ] Phase 1: (説明)
- [ ] Phase 2: (説明)
- [ ] Phase 3: (説明)

---

## Experiments

### Experiment 001: (タイトル)

#### 仮説

#### アプローチ

#### 前実験からの変更点
（001 の場合は省略）

#### 結果
- CV / LB / 主要数値テーブル

#### 学び・考察

#### 失敗・没アイデアメモ

---

## Key Insights

実験横断で得られた重要な知見。`docs/agent_brief.md` の Strategic Conclusions と内容が重なる場合は、判断に直結する短文を `agent_brief.md` 側に置き、ここでは経緯付きで残す。

- (知見1)
- (知見2)

## Ideas Backlog

やりたいこと・試したいアイデア。完了したら `[x] ~~...~~` で取り消し線、`docs/decision_rules.md` の Adopted / Rejected に反映。

- [ ] (アイデア1)
- [ ] (アイデア2)
```

---

## `experiments/{NNN}/SPEC.md` (任意・大きな実験で推奨)

```markdown
# Experiment {NNN}: {タイトル}

## ゴール
何を達成したいか。LB 目標 / 検証したい仮説。

## 設計
- モデル / アーキテクチャ
- 学習設定 (lr / epochs / batch / scheduler / ema)
- データパイプライン
- 損失関数
- augmentation
- 教師 PL の出所 / 加工方法

## 前実験からの変更点
直前ベースラインから何を変えたか / 変えていないか。

## 検証計画
- バリエーション一覧
- 想定される結果と判断基準

## 結果 / 学び (実験完了後に追記)
- LB / CV
- 学び・考察
- 失敗・没アイデア
```
