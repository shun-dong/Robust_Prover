import json
import re
from tqdm import tqdm

# 读取 Lean VSCode 插件的映射（ASCII → 符号）
with open("Data\\abbreviations.json", "r", encoding="utf-8") as f:
    abbrev_map = json.load(f)

# 反转映射 (符号 → ASCII)
reverse_map = {v: k for k, v in abbrev_map.items()}

# 构建正则模式（一次性）
symbol_pattern = re.compile("|".join(re.escape(sym) for sym in reverse_map.keys()))


def bulk_replace(text):
    return symbol_pattern.sub(lambda m: reverse_map[m.group(0)], text)

with open("Data\\merged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []

# 实际上 constType 才是命题
for item in tqdm(data):
    new_item = {}
    new_item["name"] = item["name"]
    new_item["references"] = item["references"]
    new_item["description"] = bulk_replace(f'[name: {item["name"]}] {item["constType"]}')
    new_data.append(new_item)


with open("Data\\merged_ascii.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

