import numpy as np
from scipy import sparse
import random

node_embs = np.load('Data\\embedded.npy')  # shape [N, D]
katz = sparse.load_npz('Data\\katz_index.npz')   # shape [N, N]



katz = katz.tocoo()
rows = katz.row.astype(np.int32)
cols = katz.col.astype(np.int32)
values = katz.data.astype(np.float32)
print("正样本对数:", len(values))   # 非零Katz数目

#TD 事先抽负样本
# ---可选：采样负样本（Katz为0的节点对）---
# 数量可等于正样本或更少，否则训练效率较低
N = node_embs.shape[0]
negative_num = len(values)   # 负样本数
neg_pairs, neg_labels = [], []
existing_pairs_set = set((r, c) for r, c in zip(rows, cols))
while len(neg_pairs) < negative_num:
    i = random.randrange(N)
    j = random.randrange(N)
    if i == j: continue
    if (i, j) in existing_pairs_set: continue
    neg_pairs.append((i, j))
# ---构造总训练集---
pairs = np.concatenate([np.column_stack((rows, cols)), np.array(neg_pairs)])
labels = np.concatenate([values, np.zeros(negative_num, dtype=np.float32)])
print("总训练对数:", len(labels))

np.save('Data\\train_pairs.npy', pairs)
np.save('Data\\train_labels.npy', labels)