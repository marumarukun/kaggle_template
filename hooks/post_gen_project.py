"""cookiecutter post-generation hook.

Claude Code 用の CLAUDE.md / .claude/skills を OpenAI Codex からも使えるように、
Codex が読み込む AGENTS.md / .agents/skills をシンボリックリンクとして作成する。
実体は CLAUDE.md / .claude/skills 側にあり、リンクにより内容は常に同一になる。

cookiecutter はテンプレート内のシンボリックリンクを保持できない
（ファイルはコピーに実体化、ディレクトリは空になる）ため、
テンプレートにリンクを含めず、生成後にこの hook で作成する。
"""

import shutil
from pathlib import Path


def create_link(link: Path, target: str, is_dir: bool) -> None:
    """link から target へのシンボリックリンクを作成する（再生成にも対応）。"""
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        # ユーザーが独自に作成した実体ファイル/ディレクトリは上書きしない
        print(f"[post_gen] skip: {link.name} は既に存在します（シンボリックリンクではないため保持）")
        return
    try:
        link.symlink_to(target, target_is_directory=is_dir)
        print(f"[post_gen] created: {link.name} -> {target}")
    except OSError:
        # シンボリックリンクが使えない環境（Windows の非開発者モード等）ではコピーで代替
        source = (link.parent / target).resolve()
        if is_dir:
            shutil.copytree(source, link)
        else:
            shutil.copyfile(source, link)
        print(f"[post_gen] symlink 不可のためコピーで代替: {source} -> {link}")
        print("[post_gen] 注意: コピーのため、CLAUDE.md / .claude/skills を編集した際は手動で同期してください")


def main() -> None:
    root = Path.cwd()

    # Codex はプロジェクト指示として AGENTS.md を読む
    create_link(root / "AGENTS.md", "CLAUDE.md", is_dir=False)

    # Codex はスキルを .agents/skills から発見する（SKILL.md 形式は Claude Code と共通）
    agents_dir = root / ".agents"
    agents_dir.mkdir(exist_ok=True)
    create_link(agents_dir / "skills", "../.claude/skills", is_dir=True)


if __name__ == "__main__":
    main()
