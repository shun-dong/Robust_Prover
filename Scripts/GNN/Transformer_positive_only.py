import torch
import torch.nn as nn
from torch.utils.data import DataLoader, IterableDataset
import numpy as np

class KatzStreamingDataset(IterableDataset):
    def __init__(self, rows, cols, labels, node_embs, num_samples_per_epoch,
                 hard_rate=0.5, hard_thresh=None):
        '''
        hard_rate: 每个epoch里 hard（高Katz）样本占比
        hard_thresh: Katz >= hard_thresh 的都视为 hard，默认按99分位数自动统计
        '''
        self.rows = rows
        self.cols = cols
        self.labels = labels
        self.node_embs = node_embs
        self.total = len(rows)

        # Katz阈值分层
        if hard_thresh is None:
            self.hard_thresh = np.percentile(labels, 99)
        else:
            self.hard_thresh = hard_thresh

        self.hard_rate = hard_rate
        self.num_samples_per_epoch = num_samples_per_epoch

        self.hard_idx = np.where(labels >= self.hard_thresh)[0]
        self.easy_idx = np.where(labels < self.hard_thresh)[0]

    def __iter__(self):
        n_hard = int(self.num_samples_per_epoch * self.hard_rate)
        n_easy = self.num_samples_per_epoch - n_hard

        hard_indices = np.random.choice(self.hard_idx, n_hard, replace=(n_hard>len(self.hard_idx)))
        easy_indices = np.random.choice(self.easy_idx, n_easy, replace=(n_easy>len(self.easy_idx)))

        all_indices = np.concatenate([hard_indices, easy_indices])
        np.random.shuffle(all_indices)

        for idx in all_indices:
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
    from scipy import sparse
    adj = sparse.load_npz("Data\\Katz_index0.1.npz")  # 读取邻接矩阵，检查文件是否存在
    adj = adj.tocoo()
    rows, cols, labels = adj.row, adj.col, np.log1p(adj.data)
    node_embs = np.load('Data\\embedded.npy')  # shape [N, D]
    print(f"Loaded {len(rows)} training samples, node_embs shape: {node_embs.shape}")
    print("min:", labels.min(), "max:", labels.max())
    print("percentiles:", np.percentile(labels, [0, 10, 50, 90, 99, 100]))
    # 数据集与Loader
    dataset = KatzStreamingDataset(rows, cols, labels, node_embs, num_samples_per_epoch=100000)
    loader = DataLoader(dataset, batch_size=1024, num_workers=0, pin_memory=True)
        
    model = FFNConcat(emb_dim=node_embs.shape[1], hidden_dim=256)
    model.cuda()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    loss_fn = nn.MSELoss()     # Katz为实值回归

    print("Starting training...")
    epochs = 1000
    steps_per_epoch = 100000 // 1024  # 例如每次流采样10万，用batch=1024，大约98 steps

    loss_list = []
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
        loss_list.append(total_loss / (steps_per_epoch * 1024))
        print(f"Avg Loss: {total_loss / (steps_per_epoch * 1024):.6f}")
        torch.save(model.state_dict(), "Data\\ffn_katz_log1p.pt")