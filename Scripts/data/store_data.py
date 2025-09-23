import json
import numpy as np
from scipy import sparse

with open('Data\\merged_ascii.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

name_to_index = {item['name']: idx for idx, item in enumerate(new_data)}


with open('Data\\index.json', 'w', encoding='utf-8') as f:
    json.dump(name_to_index, f, ensure_ascii=False, indent=2)

rows = []
cols = []
descriptions = []

for item in new_data:
    if item['name'] not in name_to_index:
        continue
    src_idx = name_to_index[item['name']]
    for ref in item['references']:
        if ref in name_to_index:
            tgt_idx = name_to_index[ref]
            rows.append(src_idx)
            cols.append(tgt_idx)
    descriptions.append(item['description'])

N = len(new_data)
data = np.ones(len(rows), dtype=np.float32)
S_coo = sparse.coo_matrix((data, (rows, cols)), shape=(N, N), dtype=np.float32)

sparse.save_npz('Data\\adjacency_matrix.npz', S_coo)

with open('Data\\descriptions.json', 'w', encoding='utf-8') as f:
    json.dump(descriptions, f, ensure_ascii=False, indent=2)