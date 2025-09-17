from LLM import get_answer, get_schema_answer

def filter_NL(NLQ: str) -> str:
    return get_answer(f"Filter out any irrelevant information from the following question: {NLQ}\nYou should only output the relevant mathematical question without any additional explanation.")

def answer_NL(NLQ: str) -> str:
    return get_answer(f"solve the following question: {NLQ}")

def answer_LL(LLQ: str) -> str:
    return get_schema_answer(f"""execute the following lean code and give the whole answer: {LLQ}\n
The necessary imports for the Lean 4 environment have been included at the beginning of the proof, don't include them in your final code.""")["result"]

def prepare_NL(NLQ: str, n_filter: int = 1) -> tuple[str, str]:
    for i in range(n_filter):
        NLQ = filter_NL(NLQ)
    NLA = answer_NL(NLQ)
    return NLQ, NLA

if __name__ == "__main__":
    NLQ = "x 是偶数, 那么 x^2 是偶数"
    filtered_NLQ, NLA = prepare_NL(NLQ)
    print("Filtered NLQ:", filtered_NLQ)
    print("NLA:", NLA)