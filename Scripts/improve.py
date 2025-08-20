import subprocess
from get_answer import get_schema_answer

lean_head = '''import Mathlib
import Aesop
set_option linter.style.setOption false
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat

'''

def check(LL: str):
    lean_root_path = "C:\\Users\\liuSu\\Projects\\proof"
    with open(lean_root_path+"\\Prover.lean", 'w', encoding='utf-8') as f:
        f.write(lean_head + LL)
    process = subprocess.Popen(
        ["lake", "env", "lean", "Prover.lean"],
        cwd=lean_root_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    fixed = process.returncode == 0
    feedback = out.decode() + err.decode()
    print("Feedback:", feedback)  # 调试输出
    return feedback, fixed

def fix(LL: str, feedback: str):
    result = get_schema_answer(f"""Fix the following proof: the original proof is {LL}, and the feedback from lean is {feedback}. 
                      The necessary imports for the Lean 4 environment have been included at the beginning of the proof, don't include them in your final code.""")["result"]
    return lean_head + result


if __name__ == "__main__":
    LL = "theorem my_thm : 1 + 1 = 2 := "
    result, fixed = check(LL)
    LL = fix(LL, result)
    result, fixed = check(LL)
    print("Result:", result)
    print("Fixed:", fixed)
