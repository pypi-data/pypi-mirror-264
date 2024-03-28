# titan section data extract toolkit
import logging
import numpy as np
from datetime import datetime
from typing import Union

logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    encoding="utf8",
)
print = logging.info


def time_secs2str(secs: Union[int, float]):
    # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))
    return datetime.fromtimestamp(secs).strftime("%Y-%m-%d %H:%M:%S")


def time_str2secs(text: str, year: str = None):
    str_date, str_time = text.split(" ")

    arr_date = [f"0{s}" if len(s) == 1 else s for s in str_date.split("-")]
    arr_time = [f"0{s}" if len(s) == 1 else s for s in str_time.split(":")]

    if year is not None and len(arr_date) == 2:
        arr_date = [year] + arr_date

    text = "-".join(arr_date) + " " + ":".join(arr_time)
    return datetime.fromisoformat(text).timestamp()


def trans_odds_data(data: list[list]):
    def _trans(val):
        if isinstance(val, str):
            if "/" in val:
                nums = [float(s) for s in val.split("/")]
                return f"{sum(nums)/len(nums):.2f}"
            return val
        return ""

    return [[_trans(vi) for vi in v] for v in data if "封" not in v]


def analyze_start_time(data: list[list]):
    # The elements are the output of `extract_match_base_titan()`
    first_start_time, second_start_time = 0, 0
    for vals in data:
        if vals[5] == "1":
            first_start_time = max(first_start_time, vals[1])
        elif vals[5] == "3":
            second_start_time = max(second_start_time, vals[1])
    return int(first_start_time), int(second_start_time)


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


def cycle_difference(seq: list, cycle: int, keeps: list[int]):
    mat = np.asarray(seq).reshape((-1, cycle))

    ref = np.zeros_like(mat)
    ref[1:, :] = mat[:-1, :]

    for idx in keeps:
        ref[:, idx] = 0

    ref[mat < 0] = 0

    return (mat - ref).reshape(-1).tolist()


def parse_event_data(event_data: list, points: list, ehead: str):
    event_data = sorted(event_data, key=lambda x: x["crawler_end_time"])
    timestamps = np.asarray([x["crawler_end_time"] for x in event_data])

    keys = ["角球", "半场角球", "黄牌", "射门", "射正", "任意球",
            "控球率", "半场控球率", "越位", "进球", "红牌", "乌龙"]

    out_segment = []

    points = points + [timestamps[-1]]
    indexes = [np.abs(timestamps - point).argmin() for point in points]

    for idx, point in zip(indexes[1:], points[1:]):
        offset = int(timestamps[idx] - point)
        if offset > 60 or offset < -60:
            print(f"[{ehead}] quant.football.etk_titan:")
            print(f"  find nearest timestamp: ({offset=}).abs > 60 seconds.")
            print(f"  use: {time_secs2str(timestamps[idx])}")
            print(f"  to match: {time_secs2str(point)}")
            print(f"  index of: {points.index(point)}")
            out_segment += [-1.0] * len(keys) * 2
        else:
            out_segment += [event_data[idx]["home"][key] for key in keys]
            out_segment += [event_data[idx]["away"][key] for key in keys]

    out_segment = [float(v) for v in out_segment]
    return out_segment


def parse_odds_data_x_wt20240320(data: list, points: list, year: str, ehead: str):
    timestamps = np.asarray([time_str2secs(x[-2], year) for x in data])
    weights = [1] + (timestamps[:-1] - timestamps[1:]).tolist()

    out_segment = []

    points = points + [timestamps[0]]
    indexes = [np.abs(timestamps - point).argmin() for point in points]
    for idx, idx2, point in zip(indexes[1:], indexes[:-1], points[1:]):
        offset = int(timestamps[idx] - point)
        if offset > 60 or offset < -60:
            print(f"[{ehead}] quant.football.etk_titan:")
            print(f"  find nearest timestamp: ({offset=}).abs > 60 seconds.")
            print(f"  use: {time_secs2str(timestamps[idx])}")
            print(f"  to match: {time_secs2str(point)}")
            print(f"  index of: {points.index(point)}")
            out_segment += [-1.0] * 3 * 3
        else:
            out_segment += x_avg_max_min(
                [x[2] for x in data[idx:idx2]], weights[idx:idx2]
            )
            out_segment += x_avg_max_min(
                [x[3] for x in data[idx:idx2]], weights[idx:idx2]
            )
            out_segment += x_avg_max_min(
                [x[4] for x in data[idx:idx2]], weights[idx:idx2]
            )

    out_first = [float(x) for x in data[-1][2:5]]

    return out_segment, out_first


def feature_selection_wt20240320_norm(base_data: list, event_data: list, odds_data: list, match_id: str):
    # wide table 20240320 - https://y0gskyto5mh.feishu.cn/wiki/BGnTwfbmTivw9MkcArHcDqkBnBb
    first_start_time, second_start_time = analyze_start_time(base_data)
    year = time_secs2str(first_start_time).split("-", maxsplit=1)[0]

    if "crawler_end_time" not in odds_data[0]:
        for e, o in zip(event_data, odds_data):
            o["crawler_end_time"] = e["crawler_end_time"]

    points = (
        [first_start_time + delta * 60 for delta in [0, 15, 30]] +
        [second_start_time + delta * 60 for delta in [0, 15, 30]]
    )

    # start_time, match_id, season_name, home_team_name, visiting_team_name
    out_base = [first_start_time] + [base_data[0][idx] for idx in [0, 2, 3, 4]]
    # [1-15,16-30,31-45,46-60,61-75,76-Inf]: [主队,客队]x[技统特征1,技统特征2,...]
    out_event = parse_event_data(
        event_data, points, f"{match_id=},技统数据"
    )
    # [1-15,16-30,31-45,46-60,61-75,76-Inf]: [胜赔,平赔,负赔]x[均值,最大,最小]
    # [1-15,16-30,31-45,46-60,61-75,76-Inf]: [大赔,盘口,小赔]x[均值,最大,最小]
    # [初赔]: [胜赔,平赔,负赔]+[大赔,盘口,小赔]
    last_data = sorted(odds_data, key=lambda x: x["crawler_end_time"])[-1]
    segment_1x2, first_1x2 = parse_odds_data_x_wt20240320(
        last_data["胜平负"], points, year, f"{match_id=},赔率数据,胜平负"
    )
    segment_overunder, first_overunder = parse_odds_data_x_wt20240320(
        last_data["进球数"], points, year, f"{match_id=},赔率数据,进球数"
    )
    out_1x2, out_overunder, out_first = segment_1x2, segment_overunder, first_1x2 + first_overunder

    # out_base:5, out_event:144, out_1x2:54, out_overunder:54, out_first:6
    return out_base, out_event, out_1x2, out_overunder, out_first


def feature_selection_wt20240320_base(base_data: list, event_data: list, odds_data: list, match_id: str):
    # wide table 20240320 - https://y0gskyto5mh.feishu.cn/wiki/BGnTwfbmTivw9MkcArHcDqkBnBb
    first_start_time, second_start_time = analyze_start_time(base_data)

    if "crawler_end_time" not in odds_data[0]:
        for e, o in zip(event_data, odds_data):
            o["crawler_end_time"] = e["crawler_end_time"]

    points = (
        [first_start_time + delta * 60 for delta in [0, 15, 30]] +
        [second_start_time + delta * 60 for delta in [0, 15, 30]]
    )

    # start_time, match_id, season_name, home_team_name, visiting_team_name
    out_base = [first_start_time] + [base_data[0][idx] for idx in [0, 2, 3, 4]]
    # [1-15,16-30,31-45,46-60,61-75,76-Inf]: [主队,客队]x[技统特征1,技统特征2,...]
    out_event = parse_event_data(
        event_data, points, f"{match_id=},技统数据"
    )
    # [1-15,16-30,31-45,46-60,61-75,76-Inf]: [胜赔,平赔,负赔]x[均值,最大,最小]
    # [1-15,16-30,31-45,46-60,61-75,76-Inf]: [大赔,盘口,小赔]x[均值,最大,最小]
    # [初赔]: [胜赔,平赔,负赔]+[大赔,盘口,小赔]
    last_data = sorted(odds_data, key=lambda x: x["crawler_end_time"])[-1]
    first_1x2 = [float(x) for x in last_data["胜平负"][-1][2:5]]
    first_overunder = [float(x) for x in last_data["进球数"][-1][2:5]]
    out_1x2, out_overunder, out_first = [], [], first_1x2 + first_overunder

    # out_base:5, out_event:144, out_1x2:0, out_overunder:0, out_first:6
    return out_base, out_event, out_1x2, out_overunder, out_first


def extract_match_base_titan(data: dict, keys: dict = None):
    # From: ods_bet_action_and_odds_log.mapping_match
    data = data["titan"]

    if keys is None:
        keys = [
            "match_id",
            "real_start_time",
            "season_name",
            "home_team_name",
            "visiting_team_name",
            "match_state",
            "home_team",
            "visiting_team",
        ]

    return [data[k] for k in keys]


def extract_match_event_titan(data: dict):
    # From: ods_bet_action_and_odds_log.event_titan
    events, tech_stat = data["events"], data["tech_stat"]
    start_time = data["crawler_start_time"]
    end_time = data["crawler_end_time"]

    keys = ["角球", "半场角球", "黄牌", "射门", "射正", "任意球",
            "控球率", "半场控球率", "越位", "进球", "红牌", "乌龙"]

    xs = {
        "home": {_name: 0. for _name in keys},
        "away": {_name: 0. for _name in keys},
        "crawler_start_time": start_time,
        "crawler_end_time": end_time,
    }

    name_list = [("goalIn", "进球"), ("redCard", "红牌"), ("ownGoal", "乌龙")]
    for e in events:
        _kind = e["kind"].lower()
        for _key, _name in name_list:
            if _key in e:
                xs[_kind][_name] += 1
                break

    name_list = set([
        "角球", "半场角球", "黄牌", "射门", "射正", "任意球", "控球率", "半场控球率", "越位"
    ])
    for t in tech_stat:
        _name = t["name"]
        if _name in name_list:
            for _kind in ["home", "away"]:
                xs[_kind][_name] = t[_kind]["value"]

    return xs


def extract_match_odds_titan(data: dict, companyid: str = "3"):
    # From: ods_bet_action_and_odds_log.bets_titan
    xs = {
        "胜平负": trans_odds_data(data["odds_1x2"][companyid]),
        "进球数": trans_odds_data(data["odds_overunder"][companyid]),
    }

    return xs


def extract_match_feature(match_section: list, match_info: list, match_id: str, method: str):
    base_data = [extract_match_base_titan(row["mapping_match"])
                 for row in match_section]
    event_data = [extract_match_event_titan(row["event_titan"])
                  for row in match_section]
    odds_data = [extract_match_odds_titan(row["bets_titan"])
                 for row in match_section]

    if method == "wt20240320_norm":
        vals = feature_selection_wt20240320_norm(
            base_data, event_data, odds_data, match_id
        )
    elif method == "wt20240320_base":
        vals = feature_selection_wt20240320_base(
            base_data, event_data, odds_data, match_id
        )
    else:
        raise NotImplementedError("Not supported yet.")
    out_base, out_event, out_1x2, out_overunder, out_first = vals

    if isinstance(match_info[0], str):
        match_info = [int(score) for score in match_info]

    # out_base:5, out_event:144, out_1x2:54, out_overunder:54, out_first:6, match_info:4
    return out_base + out_event + out_1x2 + out_overunder + out_first + match_info
