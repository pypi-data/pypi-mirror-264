import time
import logging
import numpy as np
from ..data.stats import mean_std, normlize
from ..data.utils import odds_avg_max_min, one_hot_encoder
from ...io.utils import make_dir, save_json

logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    encoding="utf8",
)
print = logging.info


def parse_attrs_data(data: dict):
    data = data["titan"]

    keys = [
        "match_id",
        "match_time",
        "match_state",
        "season_name",
        "home_score",
        "visiting_score",
        "home_half_score",
        "visiting_half_score",
        "home_team_name",
        "visiting_team_name",
    ]

    # 10: 10(n-key) * 1(none) + 0(none)
    xs = [data[k] for k in keys]
    return xs


def parse_event_data(data: dict):
    data = data["events"]

    keys = [
        ("goalIn", 0),  # 进球
        ("changePlayer", 1),  # 换人
        ("yellowCard", 2),  # 黄牌
        ("redCard", 3),  # 红牌
        ("ownGoal", 4),  # 乌龙
        ("penaltyKick", 5),  # 点球
        ("penaltyKickMiss", 6),  # 射失点球
        ("doubleYellowToRed", 7),  # 两黄变红
    ]

    xs_home = np.zeros((6, len(keys)), dtype=int)
    xs_away = np.zeros((6, len(keys)), dtype=int)
    for event in data:
        for key, idx in keys:
            if key in event:
                kind = event["kind"].lower()
                cycle = event["time"][:-1].split("+")[0]
                cycle = min(max(0, (int(cycle) - 1) // 15), 5)
                if kind == "home":
                    xs_home[cycle][idx] += 1
                if kind == "away":
                    xs_away[cycle][idx] += 1
                break

    # 96: 8(n-key) * 6(n-cycle) + 8(n-key) * 6(n-cycle)
    xs = xs_home.reshape(-1).tolist() + xs_away.reshape(-1).tolist()
    return xs


def parse_odds_data(data: dict):
    first_1x2 = [v[-1] for v in data["odds_1x2"].values()]
    first_overunder = [v[-1] for v in data["odds_overunder"].values()]
    first_1x2 = odds_avg_max_min(first_1x2)
    first_overunder = odds_avg_max_min(first_overunder)
    # 18: 3(avg-max-min) * 3(1x2) + 3(avg-max-min) * 3(overunder)
    xs = first_1x2 + first_overunder
    return xs


def extract_features(data: dict):
    attrs_data = parse_attrs_data(data["mapping_match"])
    event_data = parse_event_data(data["event_titan"])
    odds_data = parse_odds_data(data["bets_titan"])
    # 124: 10(attrs) + 96(event) + 18(odds)
    xs = attrs_data + event_data + odds_data
    return xs


def check_samples(data: list[list]):
    good_row, bad_row, bad_msg = [], [], []
    for row in data:
        a = int(row[4])  # 主队得分
        b = int(row[5])  # 客队得分
        c = sum([row[i] for i in range(10, 58, 8)])  # 进球
        d = sum([row[i] for i in range(58, 106, 8)])  # 进球
        if a == c and b == d:
            good_row.append(row)
            continue
        bad_row.append(row)
        bad_msg.append([a, b, c, d])
    return good_row, bad_row, bad_msg


def export_samples(data: list[list], encoder: dict, mean: list, std: list, norm: bool, path: str):
    # [0:4] : [比赛ID,比赛时间,比赛状态,联赛名]
    # [4:8] : [主队得分,客队得分,主队半场得分,客队半场得分]
    # [8:10] : [主队名称,客队名称]
    # [10:58] : [进球,换人,黄牌,红牌,乌龙,点球,射失点球,两黄变红]x6
    # [58:106] : [进球,换人,黄牌,红牌,乌龙,点球,射失点球,两黄变红]x6
    # [106:124] : [初赔均值,初赔最大,初赔最小]x[胜平负,进球数]
    scores = []
    team_home = []
    team_away = []
    xfeatures = []
    for row in data:
        scores.append(row[4:6])
        team_home.append(row[8])
        team_away.append(row[9])
        xfeatures.append(row[10:50] + row[58:98] + row[106:124])

    if encoder is None:
        encoder = one_hot_encoder(team_home + team_away)

    X = []
    for _home, _away, _vars in zip(team_home, team_away, xfeatures):
        X.append(encoder[_home] + encoder[_away] + _vars)

    if mean is None or std is None:
        mean, std = mean_std(X, [len(encoder) * 2], [len(X[0])])

    if norm:
        X = normlize(X, mean, std)

    Y = [int(s[0])+int(s[1]) for s in scores]
    Y = [9 if y > 9 else y for y in Y]

    path = make_dir(path)
    ts = time.strftime("%Y%m%d_%H%M%S")

    # .dat: [X, Y]
    # .cfg: [encoder, mean, std]
    save_json(path / f"{ts}.dat", [X, Y])
    save_json(path / f"{ts}.cfg", [encoder, mean, std])
    return X, Y, encoder, mean, std
