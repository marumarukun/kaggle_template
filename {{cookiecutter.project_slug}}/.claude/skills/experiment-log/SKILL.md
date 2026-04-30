---
name: experiment-log
description: Kaggle実験の記録・参照・次の実験提案を行う。「実験を記録して」「実験ログを更新」「実験結果をまとめて」「ログに追加して」と言ったとき（記録モード）、または「次何やる？」「実験履歴を見せて」「アイデアある？」「これまでの実験を振り返って」と言ったとき（参照モード）に使用。実験コード・git履歴・出力ファイルを自動分析し、用途別の複数ドキュメントを更新する。単なるコードレビューやバグ修正には使用しない。
---

# Experiment Log

Kaggleコンペティションの実験履歴を、用途別の複数ドキュメントで管理するスキル。AIが実験コードを自動分析してドラフトを作成し、ユーザーが確認・承認する。

## Important

- 実験履歴は **用途別に分けて管理** する。1ファイル集中ではない
  - **`docs/agent_brief.md`**: 新実験前に必ず読む短い作戦メモ（Current State / Rules / Strategic Conclusions / Do Not Repeat / Open Questions）
  - **`docs/decision_rules.md`**: 採用・封印・条件付きの判断ルール集
  - **`docs/experiment_index.md`**: 実験ごとの短い索引テーブル
  - **`docs/experiment_log.md`**: 詳細な時系列ログ（原本）
  - **`experiments/{NNN}/SPEC.md`**: 個別実験の設計仕様（任意）
- 参照時はまず `agent_brief.md` と `decision_rules.md` を読み、必要な詳細だけ `experiment_index.md` 経由で `experiment_log.md` の該当セクションを掘る
- 記録時は詳細ログだけでなく、次の意思決定に影響する内容を `agent_brief.md` / `decision_rules.md` / `experiment_index.md` にも反映する
- AIがドラフトを書き、ユーザーが確認する。**ユーザーの承認なしにファイルを更新しない**
- 記録は **日本語** で行う（技術用語は英語のまま可）
- スコアや数値は **必ず実際のデータソース（CSV, ログファイル, LB結果）から取得** する。推測で数値を書かない
- `agent_brief.md` と `decision_rules.md` は **長くしすぎない**。次の意思決定に必要な内容だけを残す。古くなった項目は削除・移動する

## モード判定

ユーザーの発言に応じて、以下のいずれかのモードで動作する:

### 記録モード
トリガー: 「実験を記録して」「ログを更新して」「結果をまとめて」「○○の実験を追加して」

### 参照モード
トリガー: 「次何やる？」「実験履歴を見て」「アイデアある？」「振り返って」

---

## 参照モードの手順

### Step 1: 入口ドキュメント読み込み

まず以下の 2 ファイルを読む（必読）。

1. `docs/agent_brief.md` — 現在の戦略・重要知見・禁止事項・未解決の問い
2. `docs/decision_rules.md` — 採用 / 封印 / 条件付き / 運用注意

この時点で多くの質問は答えられる。`docs/experiment_log.md` の全文は **読まない**。

### Step 2: 必要なら個別実験を特定

詳細が要る場合のみ:

1. `docs/experiment_index.md` で関連実験を探す
2. 該当実験の **`docs/experiment_log.md` 内のセクションだけ** を読む（offset/limit で範囲指定）
3. `experiments/{NNN}/SPEC.md` があれば併読

### Step 3: 分析・提案

ユーザーの質問に応じて:

- **「次何やる？」**: `agent_brief.md` の Open Questions と `decision_rules.md` の Conditional / Adopted を起点に、**Do Not Repeat に抵触しない**範囲で次に試すべき実験を提案する。提案には以下を含める:
  - なぜそのアプローチを推奨するか（過去の実験・知見からの根拠）
  - 期待される改善効果
  - リスクや注意点（`decision_rules.md` Operational Pitfalls 参照）

- **「振り返って」**: `experiment_index.md` を時系列で整理し、Phase ごとの成功/失敗パターンを分析

- **「アイデアある？」**: `agent_brief.md` Open Questions + `docs/` 配下のドメイン知識を参照しつつ、Rejected に該当しない案を提示

---

## 記録モードの手順

### Step 1: 現状把握

1. **`docs/agent_brief.md`** と **`docs/decision_rules.md`** を読み、現状の戦略・ルールを把握
2. **`docs/experiment_index.md`** を読み、対象実験の位置付けを確認
3. 対象実験の `experiment_log.md` 既存セクション（あれば）と前後の実験を読む
4. 対象の実験番号を特定する（引数から、または最新の実験を自動検出）

### Step 2: 実験の自動分析

以下のソースから情報を収集する:

```
experiments/{NNN}/config.py     → ハイパーパラメータ、モデル設定
experiments/{NNN}/train.py      → 学習ループ、損失関数
experiments/{NNN}/model.py      → アーキテクチャ
experiments/{NNN}/dataset.py    → データパイプライン
experiments/{NNN}/sweep.py      → ハイパーパラメータ探索（あれば）
experiments/{NNN}/SPEC.md       → 実装仕様書（あれば、ある実験のみ）
experiments/{NNN}/*.py          → その他の実験固有スクリプト

data/output/{NNN}/              → 学習結果（history.csv, config.yaml, train.log）
git log -- experiments/{NNN}/   → 変更履歴
```

### Step 2.5: 不足情報の確認

自動分析で取得できない情報を特定し、**AskUserQuestion ツールを使って** ユーザーに確認する。ドラフト作成前にこのステップを必ず実行すること。

確認が必要になりやすい情報:
- **LBスコア**: Kaggle上でしか確認できない。記録がなければ必ず聞く
- **CVスコア**: history.csv や train.log にない場合は聞く
- **仮説・動機**: コードからは「何をしたか」はわかるが「なぜそうしたか」はわからないことがある
- **没アイデア**: 試そうとしてやめたこと、実装したが効果がなくコードに残っていないもの
- **主観的な学び**: 数値に表れない気づきや直感
- **判断の更新**: 今回の結果で `decision_rules.md` の Adopted / Rejected / Conditional に動きが出るか

### Step 3: ドラフト作成（更新対象は複数ファイル）

#### 3a. `experiments/{NNN}/SPEC.md`（必要な実験のみ）
新規・大きな実験では設計仕様を残す。フォーマットは [assets/template.md](assets/template.md) の `experiments/{NNN}/SPEC.md` セクションを参考に。

#### 3b. `docs/experiment_log.md`（詳細な時系列ログ・必須）

既存実験の追記、または新規 Experiment セクションを追加。フォーマット:

```markdown
### Experiment {NNN}: {タイトル}

#### 仮説
この実験で検証しようとしたこと。なぜこのアプローチを選んだか。

#### アプローチ
使用した手法、モデル、データパイプラインの概要。

#### 前実験からの変更点
直前の実験から何を変えたか。変更の意図も含める（001 の場合は省略）。

#### 結果
- CV: {スコア}
- LB: {スコア}
- 主要な数値結果のテーブル（sweep結果等があれば）

#### 学び・考察
実験から得られた知見。次の実験にどう活かすか。

#### 失敗・没アイデアメモ
試したがうまくいかなかったこと。その理由の仮説。
```

`Current Status` ブロック（ファイル冒頭）の Best LB / Phase / Recent milestones / Next Priority も更新する。

#### 3c. `docs/experiment_index.md`（必須）
新規実験の行を追加、または既存行の LB / Decision を更新する。

#### 3d. `docs/agent_brief.md`（必要に応じて）
**次の意思決定に影響する変化があった場合のみ** 更新:
- Best LB / Current Phase / Active experiments / Next likely moves
- 新たに見えた Strategic Conclusion
- 新たに確定した Do Not Repeat
- Open Questions の追加・解消

ここは **長くなりすぎないように** 古い項目を削除・統合する。実験完了で解消した Open Question は消す。詳細はあくまで `experiment_log.md` 側に書く。

#### 3e. `docs/decision_rules.md`（判断が動いたときのみ）
- 新たに **Adopted** に確定したもの
- 新たに **Rejected**（封印）したもの
- **Conditional** から決着したもの
- 新たに踏んだ **Operational Pitfalls**

「実験ごとに必ず増やす」のではなく、本当に判断ルールに昇格したものだけを足す。

### Step 4: Strategy（大方針）の扱い

`docs/experiment_log.md` の `Strategy` セクションや、`docs/agent_brief.md` の Phase 進行は **AIが勝手に書き換えない**。
フェーズの進行や方針変更が必要そうな場合は、ユーザーに提案して合意を得てから更新する。

### Step 5: ユーザー確認

ドラフトをユーザーに提示し、以下を確認してもらう:
- スコアや数値が正しいか
- 仮説や学びの記述が意図と合っているか
- 追加・修正したい内容があるか
- どのファイルを更新するか（experiment_log.md は基本必須、その他は内容次第）

**ユーザーの承認を得てから各ファイルに書き込む。**

---

## 初回作成フロー

`docs/agent_brief.md` / `docs/decision_rules.md` / `docs/experiment_index.md` がまだ存在しない場合:

1. `docs/experiment_log.md` と各 `experiments/*/SPEC.md` を読み、現状を把握
2. [assets/template.md](assets/template.md) のテンプレートをベースに 4 ファイルのドラフトを作成
3. **Strategy / Phase 進行は、実験履歴の分析結果をもとにAIがたたき台を提案 → ユーザーと合意してから記入**
4. 全体をユーザーに確認してもらい、承認後にファイル作成

---

## Examples

### 例1: 実験完了後に記録
```
ユーザー: 「001 の実験結果を記録して」
→ 記録モード起動
→ agent_brief.md / decision_rules.md / experiment_index.md / experiment_log.md (関連セクション) / experiments/001/ を読む
→ AskUserQuestion で LB / 学び / 没アイデアを確認
→ ドラフト: experiment_log.md (001 結果追記) + experiment_index.md (001 行更新)
        + agent_brief.md (Active experiments / Next moves 更新)
        + 必要なら decision_rules.md (Adopted/Rejected 更新)
→ ユーザー確認 → 承認後に各ファイル更新
```

### 例2: 次の実験を検討
```
ユーザー: 「次何やるべき？」
→ 参照モード起動
→ agent_brief.md と decision_rules.md を読む
→ Open Questions + Conditional + Adopted の組み合わせから候補を提案
→ Do Not Repeat に抵触しないか確認
→ 過去実験を踏まえた具体的な次手を推奨
（experiment_log.md 全文は読まない）
```

### 例3: 知見の振り返り
```
ユーザー: 「これまでの実験を振り返って」
→ 参照モード起動
→ experiment_index.md を時系列で読み、Phase ごとに整理
→ 各 Phase の Best / Closed / 学びを要約
→ 必要な実験だけ experiment_log.md の該当セクションを読む
```

---

## Common Issues

### 実験結果のファイルが見つからない
- `data/output/{NNN}/` が存在しない場合、実験がまだ実行されていない可能性がある
- ユーザーに実行状況を確認する

### LBスコアが不明
- LBスコアはKaggle上でしか確認できない
- ユーザーに聞くか、「LB: 未提出」と記録する

### 既存のドキュメント間で矛盾がある
- `experiment_log.md` を **真実の原本** として扱う
- `agent_brief.md` / `decision_rules.md` / `experiment_index.md` は派生情報なので、矛盾発見時はユーザーに確認の上、原本に合わせて更新する

### `agent_brief.md` / `decision_rules.md` が長くなってきた
- 古くなった Open Question / 解消済みの Conditional は削除する
- 詳細はあくまで `experiment_log.md` に残し、入口 2 ファイルは「今の判断に必要なもの」だけに絞る
- 削減提案はユーザー承認を取る
