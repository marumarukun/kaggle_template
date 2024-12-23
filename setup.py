import json
import os
from pathlib import Path

from dotenv import load_dotenv


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def setup_competition():
    # .envから環境変数を読み込み
    load_dotenv()
    comp_name = os.getenv("COMPETITION_NAME")
    username = os.getenv("KAGGLE_USERNAME")
    project = os.getenv("PROJECT_NAME")

    # データのダウンロード
    os.system(
        f"kaggle competitions download -c {comp_name} -p data && "
        f"unzip data/{comp_name}.zip -d data && "
        f"rm data/{comp_name}.zip"
    )

    # exp/dataset-metadata.jsonの更新
    exp_meta = {"title": f"{project}-codes", "id": f"{username}/{project}-codes", "licenses": [{"name": "CC0-1.0"}]}
    save_json(exp_meta, "exp/dataset-metadata.json")

    # deps/kernel-metadata.jsonの更新
    deps_meta = {
        "id": f"{username}/{project}-deps",
        "title": f"{project}-deps",
        "code_file": "deps.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": "true",
        "enable_gpu": "true",
        "enable_tpu": "false",
        "enable_internet": "true",
        "dataset_sources": [],
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
    }
    save_json(deps_meta, "deps/kernel-metadata.json")

    # sub/kernel-metadata.jsonの更新
    sub_meta = {
        "id": f"{username}/{project}-sub",
        "title": f"{project}-sub",
        "code_file": f"{project}-sub.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": "true",
        "enable_gpu": "true",
        "enable_tpu": "false",
        "enable_internet": "false",
        "dataset_sources": [f"{username}/{project}-codes"],
        "competition_sources": [comp_name],
        "kernel_sources": [f"{username}/{project}-deps"],
        "model_sources": [],
    }
    save_json(sub_meta, "sub/kernel-metadata.json")


if __name__ == "__main__":
    setup_competition()
