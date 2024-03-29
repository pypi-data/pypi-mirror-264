import torch
import torch.utils.data
from ...io.utils import load_json


class ClassificationDataset(torch.utils.data.Dataset):

    def __init__(self, json_file):
        self.X, self.Y = self._load_data(json_file)

    def _load_data(self, json_file):
        # json_file: list[tuple[list,int]]
        X, Y = [], []

        _X, _Y = load_json(json_file)
        for x, y in zip(_X, _Y):
            X.append(torch.tensor(x, dtype=torch.float))
            Y.append(y)

        return X, Y

    def __getitem__(self, index):
        x, y = self.X[index], self.Y[index]
        return x, y

    def __len__(self):
        return len(self.X)


class RegressionDataset(torch.utils.data.Dataset):

    def __init__(self, json_file):
        self.X, self.Y = self._load_data(json_file)

    def _load_data(self, json_file):
        # json_file: list[tuple[list,list]]
        X, Y = [], []

        _X, _Y = load_json(json_file)
        for x, y in zip(_X, _Y):
            X.append(torch.tensor(x, dtype=torch.float))
            Y.append(torch.tensor(y, dtype=torch.float))

        return X, Y

    def __getitem__(self, index):
        x, y = self.X[index], self.Y[index]
        return x, y

    def __len__(self):
        return len(self.X)


class MultiBranchDataset(torch.utils.data.Dataset):

    def __init__(self, json_file):
        self.X, self.Y = self._load_data(json_file)

    def _load_data(self, json_file):
        raise NotImplementedError("TODO")

    def __getitem__(self, index):
        x, y = self.X[index], self.Y[index]
        return x, y

    def __len__(self):
        return len(self.X)
