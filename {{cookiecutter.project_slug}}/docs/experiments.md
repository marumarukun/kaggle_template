# Experiments — {{ cookiecutter.competition_name }}

> 実験の仮説とスコアを一覧する唯一の台帳。詳細な設定は `experiments/{NNN}/` のコードを参照する。
> 過去の結果は恒久的な採否ではなく、その時点・条件での観測として扱う。

## Current Context

- **Current baseline**: 001
- **Validation**: 未設定
- **Current focus**: ベースラインとCV/LBの関係を確認する

## Experiment Ledger

| Exp | Base | Hypothesis / Change | CV | Public LB | Observation / Revisit cue |
|---|---|---|---:|---:|---|
| 001 | — | 最小構成のベースラインを作り、以降の比較基準を得る | — | — (未提出) | 未実行 |

## Recording Rules

- 仮説と変更意図は、結果を見る前に簡潔に記録する。
- パラメーターは転記せず、`experiments/{NNN}/` のコードを正とする。
- スコア記録後の実験フォルダは原則変更しない。条件を変える場合は新しい実験番号を作る。
- `EXP_VERSION` は、同じ条件の再実行や成果物の世代管理に使う。特定versionの結果なら `001/v2` のように記録する。
- CV方式が異なるスコアを比較するときは、行内に方式を明記する。
- `Rejected` や「二度と試さない」といった恒久判断は記録しない。結果は「現条件では」の観測として書く。
- スコアはログ、出力ファイル、Kaggle結果などの実データからのみ記録する。推測しない。
