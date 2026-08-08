# Engineering Notes

> モデル性能の良し悪しではなく、複数の実験に影響する実装・運用上の注意事項だけを残す。

## Experiment Execution

- ローカルでのPython実行には `uv run python` を使う。
- 学習時は `EXP_VERSION=next` を指定し、既存の成果物を上書きしない。
- スコア記録後の実験コードは原則固定し、条件変更は新しい実験番号で行う。
- 別実験の `config` を `sys.path` の変更でimportしない。モジュール衝突や出力先の取り違えにつながる。

## Training / Inference Consistency

- 学習と推論で、特徴量、前処理、列順、モデル設定が一致していることを提出前に確認する。
- 推論で読み込む実験番号と、アップロードしたartifactの実験番号・versionを一致させる。

## Kaggle Submission

- codeとmodel artifactは対応する組み合わせでpushする。
- 提出前にローカルまたはKaggle Notebookの手動実行で疑似testを検証する。
- 実提出はブラックボックスとして扱い、例外を握りつぶす処理や定数予測へのフォールバックを入れない。想定外の状態ではfail fastにする。
- 実提出の失敗原因は、ローカルまたはKaggle Notebookの手動実行で再現して調べる。
- `model_sources` にはKaggle上の最新model versionだけを指定できる。ローカルのversion番号とKaggleのversion番号を混同しない。

## Maintenance Policy

- この文書へ追加するのは、複数実験に影響し、再発すると結果や提出を壊す、現在も有効な事実だけにする。
- 特定手法の性能評価、アイデア、実験固有のメモは記載しない。
- 注意事項が不要になった場合は履歴として残さず、削除または現在の仕様に書き換える。
