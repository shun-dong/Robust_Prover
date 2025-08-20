from get_answer import get_answer, get_schema_answer



def translate(NLQ:str, NLA: str) :
    LL = get_schema_answer(f"""translate the following natural language question and answer to lean language:\n Question: {NLQ}\nAnswer: {NLA}
    
    Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof plan outlining the main proof steps and strategies.
    The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide the construction of the final formal proof.

    In the result part, you should only include the Lean code without any additional explanation.
    The necessary imports for the Lean 4 environment have been included at the beginning of the proof, don't include them in your final code.
    """)["result"]
    return LL

def inverse_translate(LL: str):
    NLA = get_answer(f"""translate the following lean language to natural language with detailed explanation: {LL}""")
    return NLA

if __name__ == "__main__":
    NLQ = "What is the sum of the angles in a triangle?"
    NLA = "The sum of the angles in a triangle is 180 degrees."
    LL = translate(NLQ, NLA)
