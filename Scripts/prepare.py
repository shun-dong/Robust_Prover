from get_answer import get_answer, get_schema_answer

def filter(NLQ: str) -> str:
    return get_answer(f"Filter out any irrelevant information from the following question: {NLQ}\nYou should only output the relevant mathematical question without any additional explanation.")

def pre_answer(NLQ: str) -> str:
    return get_answer(f"solve the following question: {NLQ}")

def prepare(NLQ: str, n_filter: int = 1) -> str:
    for i in range(n_filter):
        NLQ = filter(NLQ)
    filtered_NLQ = get_schema_answer(f"Write the following question in clear mathematical language: {NLQ}\nIn result part, You should only include the mathematical question without any irrelevant information.")["result"]
    NLA = pre_answer(filtered_NLQ)
    return NLA

if __name__ == "__main__":
    NLQ = "x 是偶数, 那么 x^2 是偶数"
    NLA = prepare(NLQ)
    print("NLA:", NLA)