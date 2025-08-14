from get_answer import get_answer
def prepare(NLQ: str) -> str:
    filtered_NLQ = get_answer(f"Write the following question in clear mathematical language: {NLQ}/nYou should only include the mathematical question without any irrelevant information.")
    print(f"Filtered NLQ: {filtered_NLQ}")
    NLA = get_answer(f"solve the following question step by step: {filtered_NLQ}")
    return NLA

if __name__ == "__main__":
    # 示例调用
    NLQ = "For natural number a, b, (a**2 + b**2) is greater than or equal to a*b. fun fact cat sleep in most of their life."
    NLA = prepare(NLQ)
    print(NLA)
    # 示例回答
    print(r"example NLA:通过整理不等式，可以得到：a^2 + 2ab + 1 + b^2 > 0 \implies (a + b)^2 + 1 > 0由于平方数非负，\((a + b)^2 \geq 0\)，因此整个表达式至少为1，显然大于0。")