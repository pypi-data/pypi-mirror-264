import copy
import numpy as np
from datetime import datetime
from typing import Union


def time_secs2str(secs: Union[int, float]):
    return datetime.fromtimestamp(secs).strftime("%Y-%m-%d %H:%M:%S")


def time_str2secs(text: str, year: str = None):
    str_date, str_time = text.split(" ")

    arr_date = [f"0{s}" if len(s) == 1 else s for s in str_date.split("-")]
    arr_time = [f"0{s}" if len(s) == 1 else s for s in str_time.split(":")]

    if year is not None and len(arr_date) == 2:
        arr_date = [year] + arr_date

    text = "-".join(arr_date) + " " + ":".join(arr_time)
    return datetime.fromisoformat(text).timestamp()


def get_start_time(data: list[dict]):
    first_start_time, second_start_time = 0, 0
    for row in data:
        if row["match_state"] == "1":  # 上半场
            first_start_time = max(first_start_time, row["real_start_time"])
        elif row["match_state"] == "3":  # 下半场
            second_start_time = max(second_start_time, row["real_start_time"])
    return int(first_start_time), int(second_start_time)


def trans_odds_data(data: list[list]):
    def _trans(val):
        if isinstance(val, str):
            if "/" in val:  # 2.5/3
                nums = [float(s) for s in val.split("/")]
                return f"{sum(nums)/len(nums):.2f}"
            return val
        return ""

    return [[_trans(vi) for vi in v] for v in data if "封" not in v]


def x_avg_max_min(data: list, weights: list = None):
    if len(data) < 1:
        return [-1.0, -1.0, -1.0]

    if isinstance(data[0], str):
        data = [float(x) for x in data]

    if weights is not None:
        x_avg = sum([x * w for x, w in zip(data, weights)]) / sum(weights)
    else:
        x_avg = sum(data) / len(data)

    x_max = max(data)
    x_min = min(data)

    return [x_avg, x_max, x_min]


def odds_avg_max_min(data: list[list]):
    data = trans_odds_data(data)
    x1 = x_avg_max_min([row[2] for row in data])
    x2 = x_avg_max_min([row[3] for row in data])
    x3 = x_avg_max_min([row[4] for row in data])
    return x1 + x2 + x3


def cycle_difference(seq: list, cycle: int, keeps: list[int]):
    mat = np.asarray(seq).reshape((-1, cycle))

    ref = np.zeros_like(mat)
    ref[1:, :] = mat[:-1, :]

    for idx in keeps:
        ref[:, idx] = 0

    ref[mat < 0] = 0

    return (mat - ref).reshape(-1).tolist()


def train_val(data: list[list], point: str = "2023-12-01 00:00:01"):
    data = copy.deepcopy(data)
    point = time_str2secs(point)

    train_data, val_data = [], []
    for row in data:
        if row[1] < point:  # match_time
            train_data.append(row)
        else:
            val_data.append(row)

    return train_data, val_data


def one_hot_encoder(names: list[str]):
    names = sorted(set(names))
    eye = np.eye(len(names), k=0, dtype=int)
    encoder = {n: v for n, v in zip(names, eye.tolist())}
    return encoder
