import copy
import numpy as np
from typing import Union


def mean_std(data: Union[list[list], np.ndarray], start_idxs: list, end_idxs: list):
    assert (
        isinstance(start_idxs, list)
        and isinstance(end_idxs, list)
        and len(start_idxs) == len(end_idxs)
    )

    n_features = len(data[0])
    mean, std = ["none"] * n_features, ["none"] * n_features

    for start_idx, end_idx in zip(start_idxs, end_idxs):
        for idx in range(start_idx, end_idx):
            if isinstance(data, list):
                x = [row[idx] for row in data]
            else:
                x = data[:, idx]

            mean[idx] = np.mean(x).item()
            std[idx] = np.std(x).item()

    return mean, std


def normlize(data: Union[list[list], np.ndarray], mean: list, std: list):
    if isinstance(data, list):
        _data = []
        for row in data:
            _row = []
            for x, x_mean, x_std in zip(row, mean, std):
                if isinstance(x_mean, float) and isinstance(x_std, float):
                    _row.append((x - x_mean) / x_std)
                else:
                    _row.append(x)
            _data.append(_row)
    else:
        _data = copy.deepcopy(data)
        for idx, (x_mean, x_std) in enumerate(zip(mean, std)):
            if isinstance(x_mean, float) and isinstance(x_std, float):
                _data[:, idx] = (data[:, idx] - x_mean) / x_std
    return _data


def test():
    X = [(np.random.normal(size=100000) * 6 + i).tolist()
         for i in range(6)]
    X = np.asarray(X).transpose((1, 0))

    X1 = X.tolist()
    X2 = X.copy()

    def _show_mean_std(*args):
        for v in args:
            print([f"{vi:.2f}" if isinstance(vi, float) else vi for vi in v])

    mean, std = mean_std(X1, [0], [5])
    _show_mean_std(mean, std)

    mean, std = mean_std(X2, [0], [5])
    _show_mean_std(mean, std)

    _mean, _std = mean_std(normlize(X1, mean, std), [0], [6])
    _show_mean_std(_mean, _std)

    _mean, _std = mean_std(normlize(X2, mean, std), [0], [6])
    _show_mean_std(_mean, _std)
