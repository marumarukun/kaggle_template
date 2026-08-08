# {{ cookiecutter.project_name }}

Kaggle コードコンペティション「{{ cookiecutter.competition_name }}」用プロジェクト。

## 実験ドキュメント（重要）

新しい実験の検討・実装・記録を行う前に、次の2ファイルを読むこと。

1. **`docs/experiments.md`** — 仮説、ベース実験、CV、Public LB、再検討の手がかりを一覧する唯一の実験台帳
2. **`docs/engineering_notes.md`** — 複数実験に影響する実装・運用上の注意事項

詳細な設定とパラメーターは `experiments/{NNN}/` のコードを正とし、ドキュメントへ転記しない。

実験管理では以下を守ること。

- 仮説と変更意図は結果を見る前に `docs/experiments.md` へ記録する
- CVとPublic LBは実データからのみ記録し、推測しない
- スコア記録後の実験フォルダは原則変更せず、条件変更は新しい実験番号で行う
- 過去の結果を恒久的な `Rejected` や「二度と試さない」という判断に変換しない
- 結果は「現条件では」の観測として書き、前提が変わった場合の再検討を妨げない
- 性能と無関係な再発防止事項だけ `docs/engineering_notes.md` に記録する

実験の開始・結果記録・振り返りには `/experiment-log` スキルを使用する。

## 提出コード

推論・提出コードを変更する前に、`docs/engineering_notes.md` の Kaggle Submission を読むこと。実提出はブラックボックスとして扱い、例外を握りつぶすフォールバックを入れず、fail fastにする。

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
- `EXP_VERSION` は同じ条件の再実行や成果物の世代管理に使用する（`next` で新規、`latest` で最新）

## 主要コマンド

```sh
sh scripts/new_exp.sh                  # 新規実験作成
sh scripts/download_competition.sh     # データダウンロード
sh scripts/push_codes.sh               # コードをKaggle Datasetにアップロード
sh scripts/push_artifacts.sh {NNN}     # モデルをKaggle Modelにアップロード
sh scripts/push_deps.sh                # 依存パッケージをアップロード
sh scripts/push_sub.sh                 # 提出カーネルをpush
sh scripts/status.sh                   # 提出状況を確認
```

細かい仕様やオプションは `README.md` を参照。
