from LLM import get_answer, get_schema_answer
import re

lean_head = '''import Mathlib
import Aesop
set_option linter.style.setOption false
set_option maxHeartbeats 0
open scoped Affine BigOperators Finset Function EuclideanGeometry Real
open BigOperators Real Nat Topology Rat Affine Finset Set Module Classical Cardinal Polynomial

'''

lean_prompt='''Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.

In the result part, you should only include the Lean code without any additional explanation.
The necessary imports for the Lean 4 environment have been included at the beginning of the proof, don't include them in your final code.'''

def filter_LL(lean_code: str) -> str:
    # Filter the Lean code to only include the relevant parts
    return lean_head + re.sub(r'(?m)^(import|open|set_option).*?\n', '', lean_code)

def NLQA_to_LLQA(NLQ:str, NLA: str) :
    LL = get_schema_answer(f"""translate the following natural language question and answer to lean language:\n Question: {NLQ}\nAnswer: {NLA}
    {lean_prompt}
    """)["result"]
    return filter_LL(LL)

def NLQ_to_LLQ(NLQ: str):
    LLQ = get_schema_answer(f"""translate the following natural language question to lean language question:\n Question: {NLQ}
    """)["result"]
    return filter_LL(LLQ)

def LLQA_to_NLA(LLA: str):
    NLA = get_answer(f"""translate the following lean language to natural language with detailed explanation: {LLA}""")
    return NLA

if __name__ == "__main__":
    lean_code = "import Mathlib\nimport Aesop\nset_option linter.style.setOption false\nset_option maxHeartbeats 0\nopen BigOperators Real Nat Topology Rat\n\ntheorem even_square (x : ℤ) (h : even x) : even (x^2) := by\n  rw [even_iff_exists_two_mul] at h\n  cases h with | intro k hk =>\n  use 2 * k^2\n  rw [hk]\n  ring\n"
    print(filter_LL(lean_code))