def prepare(NLQ: str) -> str:
    pass
    return NLA

if __name__ == "__main__":
    # 示例调用
    NLQ = "For natural number a, b, (a**2 + b**2) is greater than or equal to a*b"
    NLA = prepare(NLQ)
    print(NLA)
    # 示例回答
    print("example NLA:通过整理不等式，可以得到：a^2 + 2ab + 1 + b^2 > 0 \implies (a + b)^2 + 1 > 0由于平方数非负，\((a + b)^2 \geq 0\)，因此整个表达式至少为1，显然大于0。")