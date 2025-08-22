from get_answer import get_answer, get_schema_answer
import re

lean_head = '''import Mathlib
import Aesop
set_option linter.style.setOption false
set_option maxHeartbeats 0
open BigOperators Real Nat Topology Rat

'''
def head_filter(lean_code: str) -> str:
    # Filter the Lean code to only include the relevant parts
    return lean_head + re.sub(r'(?m)^(import|open|set_option).*?\n', '', lean_code)

def translate(NLQ:str, NLA: str) :
    LL = get_schema_answer(f"""translate the following natural language question and answer to lean language:\n Question: {NLQ}\nAnswer: {NLA}
    
    Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
    The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.

    In the result part, you should only include the Lean code without any additional explanation.
    The necessary imports for the Lean 4 environment have been included at the beginning of the proof, don't include them in your final code.
    """)["result"]
    return head_filter(LL)

def inverse_translate(LL: str):
    NLA = get_answer(f"""translate the following lean language to natural language with detailed explanation: {LL}""")
    return NLA

if __name__ == "__main__":
    lean_code = "import Mathlib\nimport Aesop\nset_option linter.style.setOption false\nset_option maxHeartbeats 0\nopen BigOperators Real Nat Topology Rat\n\ntheorem even_square (x : ℤ) (h : even x) : even (x^2) := by\n  rw [even_iff_exists_two_mul] at h\n  cases h with | intro k hk =>\n  use 2 * k^2\n  rw [hk]\n  ring\n"
    print(head_filter(lean_code))