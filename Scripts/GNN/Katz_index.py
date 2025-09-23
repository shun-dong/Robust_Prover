from scipy import sparse
import numpy as np

A = sparse.load_npz('Data\\adjacency_matrix.npz')
beta = 0.1

K_est = beta * A.copy()
Ak = A.copy()
for k in range(2, 6):  # 路径长度6以内
    print(k)
    Ak = Ak.dot(A)
    K_est += (beta**k) * Ak

sparse.save_npz(f'Data\\katz_index{beta}.npz', K_est)