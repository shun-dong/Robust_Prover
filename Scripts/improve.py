import subprocess
from get_answer import get_schema_answer

def check(LL: str):
    lean_file_path = "C:\\Users\\liuSu\\Projects\\proof\\Prover.lean"
    with open(lean_file_path, 'w', encoding='utf-8') as f:
        f.write(LL)
    process = subprocess.Popen(
        ["lean", lean_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    fixed = process.returncode == 0
    return out.decode() + err.decode(), fixed

def fix(LL: str, feedback: str):
    return get_schema_answer(f"""Fix the following proof: the original proof is {LL}, and the feedback from lean is {feedback}. 
                      Remember to include all necessary imports and definitions.
                      In result part, You should only output the fixed lean language translation without any additional explanation. Don't use code blocks to wrap.""")["result"]


if __name__ == "__main__":
    LL = "theorem my_thm : 1 + 1 = 2 := "
    result, fixed = check(LL)
    LL = fix(LL, result)
    result, fixed = check(LL)
    print("Result:", result)
    print("Fixed:", fixed)
