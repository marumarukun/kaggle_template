# Kaggle Template

cookiecutter を使った kaggle code competition 用のテンプレート

## Quickstart

**install cookiecutter**

```bash
pip install cookiecutter
```

**project の作成**

1. project root directory ごと作成する場合

    ```bash
    cookiecutter https://github.com/marumarukun-da/kaggle_template.git
    ```

2. 作成済みの project root directory を使いたい場合 (clone した repository など)

    ```bash
    cd {project_dir}
    cookiecutter https://github.com/marumarukun-da/kaggle_template.git -f -o ../
    ```

    - `project_slug` と `{projet_dir}` が同じ名前であり、それを上書きする形で template を作成する
    - cookicutter の [CL options](https://cookiecutter.readthedocs.io/en/1.7.0/advanced/cli_options.html) を使う

**cookiecutter parameters**

- `competition_name`: Kaggle competition の名前。コンペ URL に含まれる名前、もしくは `kaggle competitions download -c {competition_name}` で指定する名前をここで使用する
- `project_name`: プロジェクトの名前
- `project_slug`: 作成されるディレクトリ名
- `project_description`: プロジェクトの説明
- `kaggle_username`: kaggle に登録してあるユーザー名

**入力例**

例えば、[Titanic - Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic) コンペに参加する場合:

```
competition_name []: titanic
project_name [project_name]: Titanic Survival Prediction
project_slug [titanic_survival_prediction]: titanic
project_description []: Kaggle Titanic competition - predict survival on the Titanic
kaggle_username []: your_kaggle_username
```

- `competition_name` はコンペURLの `https://www.kaggle.com/competitions/titanic` の末尾部分 `titanic` を入力
- `project_slug` は作成されるディレクトリ名になるので、シンプルな名前がおすすめ

## コーディングエージェント対応（Claude Code / Codex）

生成されるプロジェクトは Claude Code と OpenAI Codex の両方に対応しています。
実体（canonical）は Claude Code 用のファイルで、Codex 用の入口は post-generation hook（`hooks/post_gen_project.py`）が生成時にシンボリックリンクとして自動作成します。リンクのため **内容は常に完全に同一** です。

| 実体（編集はこちら） | シンボリックリンク | 読み込むツール |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | Claude Code は `CLAUDE.md`、Codex は `AGENTS.md` を読む |
| `.claude/skills/` | `.agents/skills/` | Claude Code は `.claude/skills`、Codex は `.agents/skills` を読む（SKILL.md 形式は共通） |

このテンプレートから過去に生成した既存プロジェクトへ後付けする場合は、プロジェクトルートで以下を実行してください:

```bash
ln -s CLAUDE.md AGENTS.md
mkdir -p .agents && ln -s ../.claude/skills .agents/skills
```
