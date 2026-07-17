# {{ cookiecutter.project_name }}

Kaggle コードコンペティション「{{ cookiecutter.competition_name }}」用プロジェクト。

## 提出コードの鉄則（最重要・常に意識すること）

実提出（隠し test データでの再実行）は**完全なブラックボックス**である。成功してもログ・print 出力は一切見られず、失敗してもエラー内容は取得できない。Kaggle 上で Notebook を手動実行して見えるのは疑似 test データへの推論結果だけである。この前提から、以下を厳守すること:

- **「提出を失敗させないためのフォールバック」を入れてはならない**（例外を握りつぶす try/except、データ仕様が想定外の場合に定数予測へ切り替える等）。フォールバックが発動したかどうかを観測する手段がないため、「モデルの性能が悪い」のか「フォールバックが発動してスコアが下がった」のかが切り分け不能になる。これはデバッグ不能な状態を自ら作る行為であり、**有害**である
- 提出失敗時に「ログを仕込んで原因を調べましょう」と提案してはならない。そのログは実提出環境では**誰も見られない**ため無意味である
- 方針は **fail fast**。想定外の状態では黙って継続せず、明示的に失敗させる。「エラーで落ちた」という事実自体が、実提出環境から得られる唯一の観測可能なシグナルであり、スコアの解釈を汚染しない
- 原因調査は、ローカルおよび Kaggle Notebook の手動実行（疑似 test）での再現・検証によって行う

## 実験ログ（重要）

実験ログは用途別に **4 つのファイル** に分担して管理する。
新しい実験を考える・実装する前は **以下の順** で読むこと。

1. **`docs/agent_brief.md`** — 必読。Current State / Must-Know Rules / Strategic Conclusions / Do Not Repeat / Open Questions
2. **`docs/decision_rules.md`** — 必読。Adopted / Rejected / Conditional / Operational Pitfalls
3. **`docs/experiment_index.md`** — 過去実験の索引。関連実験を特定する
4. **`docs/experiment_log.md`** — 詳細な時系列ログ（原本）。**該当実験のセクションだけ** を読む（全文は読まない）

個別実験の設計仕様は `experiments/{NNN}/SPEC.md` も参照可能（任意、大きな実験で推奨）。

実験完了時は `/experiment-log` スキルで上記 4 ファイル + `experiments/{NNN}/SPEC.md` を更新する。

## コンペ情報

詳細は `docs/` 配下を参照:

- `docs/competition_overview.md` — コンペ概要・ルール・制約
- `docs/dataset_description.md` — データセットの詳細
- `docs/evaluation_metric.md` — 評価指標の解説
- `docs/domain_knowledge.md` — ドメイン知識・有効なアプローチ

## プロジェクト構造

- `experiments/{NNN}/` — 実験フォルダ（config.py / train.py / inference.py）
- `src/kaggle_utils/` — Kaggle APIラッパー（upload/download）
- `data/input/` — コンペデータ、`data/output/` — 学習成果物
- `sub/` — 提出用カーネル、`deps/` — 依存パッケージ用カーネル
- `scripts/` — ワークフロー用シェルスクリプト

## 実験の仕組み

- 各実験の `config.py` が `IS_KAGGLE_ENV` でローカル/Kaggle環境を自動判別しパスを切り替える
- `EXP_NAME` は `Path(__file__).parent.name` から自動取得（フォルダ名 = 実験名）
- `EXP_VERSION` 環境変数でバージョン管理（`next` で新規、`latest` で最新）

## 主要コマンド

```sh
sh scripts/new_exp.sh                  # 新規実験作成
sh scripts/download_competition.sh     # データダウンロード
sh scripts/push_codes.sh              # コードをKaggle Datasetにアップロード
sh scripts/push_artifacts.sh {NNN}    # モデルをKaggle Modelにアップロード
sh scripts/push_deps.sh              # 依存パッケージをアップロード
sh scripts/push_sub.sh               # 提出カーネルをpush
sh scripts/status.sh                 # 提出状況を確認
```

細かい仕様やオプションは `README.md` を参照。
