# Decision Rules — {{ cookiecutter.competition_name }}

> 「知見」ではなく**次の判断に直接使うルール**だけを集めたファイル。
> 詳細な経緯は `docs/experiment_log.md` の該当 Experiment セクション、設計意図は `experiments/{NNN}/SPEC.md`。

最終更新: YYYY-MM-DD

---

## Adopted (採用済み・継続する設計)

実験で有効性が確認され、現行ベースラインに継承している設計。カテゴリ別に箇条書き。

### モデル / 学習
- (例: backbone / 損失 / augmentation / EMA 設定など)

### データ / 教師
- (例: PL の出所、external data の扱い、mixup ポリシーなど)

### パイプライン
- (例: 全データ学習 / fold 戦略 / 推論最適化 / バージョン管理ルール)

---

## Rejected (封印・再検討不要)

明確に失敗してスコアが下がった、または運用上不可だったもの。再試行しない。

### モデル / アーキテクチャ
- (例: 〇〇 backbone は -0.XX で封印)

### データ / 学習
- (例: 〇〇 augmentation は LB 悪化、××パラダイムは構造的に不適合)

### 推論
- (例: 〇〇 TTA は効果なし、××後処理は冗長)

---

## Conditional (条件付き判断 / 未確定)

条件次第で採否が変わるもの、または検証が不十分で結論未確定のもの。次の検証計画と合わせて記載。

- (例: 〇〇 は条件 A では効くが条件 B では効かない、△△は controlled training で再検証要)

---

## Operational Pitfalls (実装/運用で踏みやすい罠)

過去に踏んだ実装ミス・運用事故と回避方法。

- (例: ファイルパスの拡張子固定問題、別実験 config の import 衝突、Kaggle 提出時の code/model 同期など)
