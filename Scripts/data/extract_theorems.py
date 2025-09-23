import re
import json
from typing import List, Dict, Any
import os

def extract_block_theorems(lean_code: str, source: str) -> List[Dict[str, Any]]:
    theorems = []
    # 用非贪婪匹配提取每个 theorem/lemma ... begin ... end 块
    pattern = re.compile(r'(theorem|lemma)\s+([a-zA-Z0-9_]+)([\s\S]+?)begin([\s\S]+?)end', re.MULTILINE)
    for match in pattern.finditer(lean_code):
        kind, thm_name, thm_decl, proof = match.groups()
        statement = f"{kind} {thm_name}{thm_decl}begin\n  sorry\nend"
        full_statement = f"{kind} {thm_name}{thm_decl}begin{proof}end"
        if re.search(r'\bsorry\b', proof):
            solution = None
        else:
            # solution是原始块
            solution = full_statement.strip()
        theorems.append({
            "id": thm_name,
            "statement": statement.strip(),
            "solution": solution,
            "source": source
        })
    return theorems

def extract_file_theorem(lean_code: str, source: str) -> Dict[str, Any]:
    pattern = re.compile(r'namespace\s+(\S+)([\s\S]+)end', re.MULTILINE)
    match = pattern.search(lean_code)
    if match:
        thm_name, statement = match.groups()
        statement = statement.replace("result", thm_name).strip()
        if re.search(r'\bsorry\b', statement):
            solution = None
        else:
            solution = statement
        return ({
            "id": thm_name,
            "statement": statement.strip(),
            "solution": solution,
            "source": source
        })
    else:
        raise LookupError("fail to find thoerem")

def extract_file_theorems(path:str, source:str) -> List[Dict[str, Any]]:
    theorems = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lean_code = f.read()
            theorems.append(extract_file_theorem(lean_code, source))
    return theorems

if __name__ == "__main__":
    # 读取输入 lean 文件
    with open('Data\\problems.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = extract_file_theorems('Data\\IMO\\IMO', source="IMO")

    # 写入 json 文件
    with open('Data\\problems.json', 'w', encoding='utf-8') as f:
        json.dump(data + results, f, ensure_ascii=False, indent=2)