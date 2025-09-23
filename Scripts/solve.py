import subprocess
from LLM import get_schema_answer
from convert import filter_LL, lean_head

def answer_LL(LLQ: str):
    LLQA= get_schema_answer(f"""complete the following lean code without sorry: {LLQ}\n {lean_head}""")["result"]
    return filter_LL(LLQA)

def give_lemma(LLQ: str):
    lemma= get_schema_answer(f"""give useful new lemma for the following lean code: {LLQ}\n In your code, do not include the original theorem statement, only include the lemma statement.\n{lean_head}""")["result"]
    return filter_LL(lemma)

def check(LL: str):
    #TD 这个要改, 没法并行
    lean_root_path = "C:\\Users\\liuSu\\Projects\\proof"
    with open(lean_root_path+"\\Prover.lean", 'w', encoding='utf-8') as f:
        f.write(LL)
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
    return filter_LL(result)

def fix_loop(loop_history: list):
    loop_history_str = "\n---\n".join(loop_history)
    result = get_schema_answer(f"""The following Lean proof code has entered a loop during the fixing process. They all have some mistakes. The history of the code is as follows:
    {loop_history_str}
    Please provide a new version of the Lean proof code that breaks this loop and solves the problem.
    The necessary imports for the Lean 4 environment have been included at the beginning of the proof, don't include them in your final code.""")["result"]
    return filter_LL(result)


if __name__ == "__main__":
    pass

    print(fix_loop(["theorem my_thm : 1 + 1 = 2 := sorry", "theorem my_thm : 1 + 1 = 2 := by refl", "theorem my_thm : 1 + 1 = 2 := sorry"]))
