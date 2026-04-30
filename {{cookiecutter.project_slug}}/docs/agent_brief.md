# Agent Brief — {{ cookiecutter.competition_name }}

> 新しい実験の壁打ち・実装前にエージェントが**必ず最初に**読むファイル。
> 詳細を追うときは `docs/experiment_index.md` から該当実験 (`docs/experiment_log.md` または `experiments/{NNN}/SPEC.md`) を引く。
> 採用/封印/条件付きの判断ルールは `docs/decision_rules.md`。

最終更新: YYYY-MM-DD

---

## Current State

- **Best LB**: 現時点のベストスコアと実験番号
- **Current Phase**: 取り組み中のフェーズ・テーマ
- **Active experiments**: 学習中・検証中の実験一覧
- **Next likely moves**: 次に着手予定の動き（候補レベルでもよい）

---

## Must-Know Operational Rules

新規プロジェクトでも共通する運用ルールは最初から記載しておく。プロジェクト固有のルールは適宜追加する。

- Python 実行は **`uv run python`**（uv 経由必須）
- `EXP_VERSION` は `next` 推奨。明示せずに学習を回すと既存出力を上書きする事故あり
- Kaggle 提出時は **code と model をセットで push** する (`push_codes.sh` + `push_artifacts.sh`)
- 提出前に **ローカル擬似テスト必須** (`test_local.py` 等)。Kaggle のエラーログは不親切
- `convert.py` / `inference.py` は **output 側 config (`data/output/{NNN}/{ver}/config.yaml`) を読む**こと。ソース側は新実験で書き換わる
- `--force` 等の **破壊的操作はユーザー承認必須**
- 別実験の `config` を `sys.path` 経由で import しない（sys.modules 衝突で出力破損のリスク）
- ユーザー質問は AskUserQuestion ツールを優先

---

## Strategic Conclusions

現在の実験設計に効く横断知見を箇条書きで記載。経緯は `docs/experiment_log.md` 側。

- (例: 容量帯と pretrain 種別の傾向、有効だった mel 設定、教師 PL の取り扱い等)

---

## Do Not Repeat

過去に明確に失敗したアプローチ。再試行しない（理由とともに 1 行で）。

- (例: 〇〇 backbone は LB -0.XX で封印、××パラダイムは構造的に NG など)

---

## Open Questions

次に検証すべき問い。実験で決着したら削除・移動する。

- (例: 〇〇 を controlled training で検証、××のチューニング)

---

## Where To Look

- **過去実験の索引**: `docs/experiment_index.md`
- **採用/封印/条件付き判断**: `docs/decision_rules.md`
- **詳細な時系列ログ（原本）**: `docs/experiment_log.md`（該当実験セクションのみ）
- **個別実験の設計仕様**: `experiments/{NNN}/SPEC.md`（任意）
- **コンペ情報**: `docs/competition_overview.md` / `docs/dataset_description.md` / `docs/evaluation_metric.md` / `docs/domain_knowledge.md`
