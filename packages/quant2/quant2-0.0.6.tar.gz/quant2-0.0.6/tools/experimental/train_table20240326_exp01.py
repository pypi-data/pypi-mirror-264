import numpy as np
import random
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
from torch.optim.lr_scheduler import StepLR
from quant.football.data.dataset import ClassificationDataset


class Net(nn.Module):

    def __init__(self, in_features, mid_features, out_features):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(in_features, mid_features, bias=True)
        self.fc2 = nn.Linear(mid_features, mid_features, bias=True)
        self.fc3 = nn.Linear(mid_features, mid_features, bias=True)
        self.fc4 = nn.Linear(mid_features, mid_features, bias=True)
        self.fc5 = nn.Linear(mid_features, out_features, bias=True)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc4(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.fc5(x)
        return x


def train(model, device, train_loader, criterion, optimizer, epoch, log_interval, dry_run=False):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print("Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            if dry_run:
                break


def test(model, device, test_loader, criterion):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader)

    print("\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


def main(train_file, test_file, lr, seed=1234, device="cuda", batch_size=128, epochs=100, log_interval=10):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    if device == "cuda" and torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    train_dataset = ClassificationDataset(train_file)
    test_dataset = ClassificationDataset(test_file)

    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1
    )

    model = Net(100, 1024, 4).to(device)
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.SGD(
        model.parameters(), lr, 0.9, weight_decay=0.001)

    scheduler = StepLR(optimizer, step_size=30, gamma=0.1)
    for epoch in range(1, epochs + 1):
        train(model, device, train_loader, criterion,
              optimizer, epoch, log_interval)
        test(model, device, test_loader, criterion)
        scheduler.step()

    tag = time.strftime("%Y%m%d_%H%M%S")
    torch.save(model.state_dict(), f"exp_{tag}.pt")


if __name__ == "__main__":
    main()
