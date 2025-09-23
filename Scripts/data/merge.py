import os
import json

input_folder = "C:\\Users\\liuSu\\Projects\\proof\\data"  # 你的所有json文件的文件夹
output_file = "C:\\Users\\liuSu\\Projects\\Robust_Prover\\Data\\merged.json"

merged = []

for fname in os.listdir(input_folder):
    if not fname.endswith(".json"):
        continue
    fpath = os.path.join(input_folder, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        items = json.load(f)
        # 假设每个文件都是一个list
        # 从文件名中提取namespace
        namespace = fname[:-5] # 去掉 .json
        for obj in items:
            try:
                obj["namespace"] = namespace
                merged.append(obj)
            except TypeError:
                print(namespace, obj)

with open(output_file, "w", encoding="utf-8") as out:
    json.dump(merged, out, ensure_ascii=False, indent=2)