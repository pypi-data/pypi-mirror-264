import json
import shutil
from pathlib import Path


def make_dir(path, exist_ok=True):
    path = Path(path)

    if not exist_ok:
        shutil.rmtree(path, ignore_errors=True)

    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(file):
    with open(file, "r", encoding="utf8") as f:
        data = json.load(f)
    return data


def save_json(file, data):
    with open(file, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
    return file
