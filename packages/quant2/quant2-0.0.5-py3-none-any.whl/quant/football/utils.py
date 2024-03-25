import copy


def filter_values(data, idx, vals, only_matches=True):
    _data = []
    _vals = set(vals)
    for _row in data:
        if only_matches:
            if _row[idx] in _vals:
                _data.append(copy.deepcopy(_row))
        else:
            if _row[idx] not in _vals:
                _data.append(copy.deepcopy(_row))
    return _data


def count_values(data, idx, display=False):
    vals = [row[idx] for row in data]

    keys = sorted(set(vals))
    nums = {key: 0 for key in keys}

    for val in vals:
        nums[val] += 1

    if display:
        print(f"COUNT VALUES:\n{keys=}\n{nums=}")

    return keys, nums
