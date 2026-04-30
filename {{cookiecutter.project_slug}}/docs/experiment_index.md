# Experiment Index — {{ cookiecutter.competition_name }}

> 全実験の索引。詳細は `docs/experiment_log.md` の該当 Experiment セクションを参照。
> 設計仕様 (SPEC.md) があるものは `experiments/{NNN}/SPEC.md` も参照。

最終更新: YYYY-MM-DD

---

## Legend

- **LB**: 単体スコア。複数 version は最良値、レンジは最低-最高
- **Decision**: `adopted` (現行に継承) / `closed` (失敗確定) / `superseded` (後続実験で置換) / `current` (進行中)
- **Links**: `log` = `docs/experiment_log.md` 内のセクション、`spec` = `experiments/{NNN}/SPEC.md`

---

## Phase 1: (フェーズ名・テーマ)

| Exp | Theme | LB | Decision | Links |
|---|---|---:|---|---|
| 001 | (タイトル) | 0.XXX | (adopted/closed/superseded/current) | log |

<!-- フェーズが進んだら追加していく -->
<!--
## Phase 2: (フェーズ名)

| Exp | Theme | LB | Decision | Links |
|---|---|---:|---|---|
| 002 | (タイトル) | 0.XXX | adopted | log, spec |
-->

---

## Quick lookup

実験が増えてきたら、参照しやすいベースラインや代表的な失敗例をここに列挙する。

- **現 TOP**: 実験番号 — 構成サマリ
- **旧 TOP / superseded baseline**: 実験番号
- **失敗で学んだ大きな実験**: 実験番号
