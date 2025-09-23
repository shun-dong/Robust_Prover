import torch
import torch.nn as nn
from torch.utils.data import DataLoader, IterableDataset
import numpy as np

class KatzStreamingDataset(IterableDataset):
    def __init__(self, rows, cols, labels, node_embs, num_samples_per_epoch=None):
        """
        rows, cols, labels: np.array 或 list, 对应样本的节点对与标签
        node_embs: np.ndarray (N, D)
        num_samples_per_epoch: epoch内喂入loader多少个样本（例如10万~100万），None为全部遍历一遍
        """
        self.rows = rows
        self.cols = cols
        self.labels = labels
        self.node_embs = node_embs
        self.total = len(self.rows)
        self.num_samples_per_epoch = num_samples_per_epoch

    def __iter__(self):
        if self.num_samples_per_epoch is None or self.num_samples_per_epoch >= self.total:
            idxs = torch.randperm(self.total)  # 打乱全量样本
        else:
            # 抽一批样本
            idxs = torch.from_numpy(
                np.random.choice(self.total, self.num_samples_per_epoch, replace=False)
            )

        for idx in idxs:
            i, j = self.rows[idx], self.cols[idx]
            x = torch.from_numpy(self.node_embs[i]).float()
            y = torch.from_numpy(self.node_embs[j]).float()
            label = torch.tensor(self.labels[idx], dtype=torch.float)
            yield x, y, label

class FFNConcat(nn.Module):
    def __init__(self, emb_dim, hidden_dim=256):
        super().__init__()
        self.ffn = nn.Sequential(
            nn.Linear(emb_dim*2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    def forward(self, x, y):
        h = torch.cat([x, y], dim=1)
        return self.ffn(h).squeeze(-1)

if __name__ == "__main__":
    pairs = np.load('Data\\train_pairs.npy')  # shape [M, 2]
    labels = np.load('Data\\train_labels.npy')  # shape [M]
    node_embs = np.load('Data\\embedded.npy')  # shape [N, D]
    rows = pairs[:, 0]
    cols = pairs[:, 1]
    print(f"Loaded {len(rows)} training samples, node_embs shape: {node_embs.shape}")
    print("min:", labels.min(), "max:", labels.max())
    print("percentiles:", np.percentile(labels, [0, 10, 50, 90, 99, 100]))
    # 数据集与Loader
    dataset = KatzStreamingDataset(rows, cols, labels, node_embs, num_samples_per_epoch=100000)
    loader = DataLoader(dataset, batch_size=1024, num_workers=0, pin_memory=True)
        
    model = FFNConcat(emb_dim=node_embs.shape[1], hidden_dim=256)
    model.cuda()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()     # Katz为实值回归

    print("Starting training...")
    epochs = 10
    steps_per_epoch = 100000 // 1024  # 例如每次流采样10万，用batch=1024，大约98 steps

    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}")
        model.train()
        total_loss = 0
        for step, (x, y, label) in enumerate(loader):
            if step >= steps_per_epoch:
                break  # 控制一个epoch步数
            x, y, label = x.cuda(), y.cuda(), label.cuda()
            optimizer.zero_grad()
            pred = model(x, y)
            loss = loss_fn(pred, label)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * x.size(0)
        print(f"Avg Loss: {total_loss / (steps_per_epoch * 1024):.6f}")
        torch.save(model.state_dict(), "Data\\ffn_katz.pt")