def translate(NLQ:str, NLA: str) :
    pass
    return (LLQ, LLA)

def inverse_translate(LLA: str) -> str:
    pass
    return NLA


if __name__ == "__main__":
    # 示例调用
    NLQ = "For natural number a, b, (a**2 + 2*a*b + 1) is greater than -b**2"
    NLA = "通过整理不等式，可以得到：a^2 + 2ab + 1 + b^2 > 0 \implies (a + b)^2 + 1 > 0由于平方数非负，\((a + b)^2 \geq 0\)，因此整个表达式至少为1，显然大于0。"
    LLQ, LLA = translate(NLQ, NLA)
    print(LLQ, LLA)
    # 示例lean语言
    print('''import data.nat.basic
theorem nat_square_ineq (a b : ℕ) : ((a^2 : ℤ) + 2*a*b + 1) > -(b^2 : ℤ) :=
begin
  have h : ((a+b)^2 : ℤ) + 1 > -((b^2 : ℤ)),
  { linarith [pow_two_nonneg (a+b : ℤ), pow_two_nonneg (b : ℤ)] },
  rw [add_pow_two, ←add_assoc],
  ring_nf,
  exact h,
end
''')

    # 示例逆翻译
    inverse_NLA = inverse_translate(LLA)
    print(inverse_NLA)