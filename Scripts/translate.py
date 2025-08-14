<<<<<<< HEAD
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
=======
def translate(NLA: str) -> str:
"""
    将自然语言推理（NLA）转换为Lean代码（LLA）
    
    参数:
        NLA: 字符串类型，包含分步骤的自然语言推理（如判断17是否为质数的推理）
    
    返回:
        str: 对应的Lean代码字符串
    """
    # 调用模型将自然语言推理转写为Lean代码
    completion_lean = client.chat.completions.create(
        model="ep-20250809224204-vxlgq",
        messages=[
            {"role": "system", "content": """
            请将以下自然语言推理转写成严格的Lean 4代码，需满足：
            1. 包含必要的库导入（如判断质数需import Mathlib.Data.Nat.Prime）；
            2. 用example定义待证明命题（如example : Prime 17 := by ...）；
            3. 每一步推导用rw、intro、norm_num等战术，对应自然语言中的推理步骤；
            4. 明确引用相关数学定义（如质数定义Prime.def）；
            5. 代码必须可被Lean验证（无语法错误）。
            """},
            {"role": "user", "content": NLA}  # 传入自然语言推理
        ]
    )
    # 返回生成的Lean代码
    return completion_lean.choices[0].message.content

# 示例使用
if __name__ == "__main__":
    # 示例自然语言推理（判断17是否为质数）
    sample_NLA = """
    1. 质数定义：大于1的自然数，除1和自身外无其他因数。
    2. 17是大于1的自然数，满足质数定义的第一个条件。
    3. 检查17的因数：需验证2到16之间是否有能整除17的数。
    4. 2不能整除17（17÷2=8余1）；3不能整除17（17÷3=5余2）；
       4不能整除17（17÷4=4余1）；5到16同理，均不能整除17。
    5. 因此17除1和自身外无其他因数，符合质数定义，故17是质数。
    """
    
    # 调用translate函数生成Lean代码
    lean_code = translate(sample_NLA)
    print("生成的Lean代码：")
    print(lean_code)

def inverse_translate(lean_code: str) -> str:
    """将Lean代码转换为对应的自然语言解释"""
    print("\n----- Lean代码转自然语言 -----")
    # 调用模型解析Lean代码，生成自然语言说明
    completion = client.chat.completions.create(
        model="ep-20250809224204-vxlgq",
        messages=[
            {"role": "system", "content": """
            你是数学形式化解释助手，请将以下Lean代码转换为自然语言推理步骤：
            1. 先说明代码要证明的命题（如“证明17是质数”）；
            2. 逐句解释代码中的战术（如rw、intro、norm_num等）对应的数学逻辑；
            3. 关联代码步骤与数学定义（如质数定义、整除规则等）；
            4. 用“1. 2. 3. ”分点说明，保持与代码步骤的对应关系。
            """},
            {"role": "user", "content": f"请解释以下Lean代码的推理逻辑：\n{lean_code}"}
        ]
    )
    return completion.choices[0].message.content

# 示例：使用上述函数转换质数判断的Lean代码
if __name__ == "__main__":
    # 假设这是新的Lean代码（例如判断17是质数的证明）
    sample_lean_code = """
import Mathlib.Data.Nat.Prime

example : Prime 17 := by
  rw Prime.def  -- 展开质数定义
  split         -- 分解为两个条件：17 > 1 和 无其他因数
  -- 证明17 > 1
  norm_num
  -- 证明除1和自身外无其他因数
  intro m h_div
  have h_le : m ≤ 17 := Nat.le_of_dvd (Nat.pos_of_prime this) h_div
  interval_cases m with m  -- 枚举可能的因数范围
  · exact Or.inl rfl       -- m=1的情况
  · norm_num; contradiction -- m=2到16的情况（均不能整除17）
  · exact Or.inr rfl       -- m=17的情况
    """
    
    # 调用函数转换为自然语言
    natural_explanation = lean_to_natural(sample_lean_code)
    print("自然语言解释：")
    print(natural_explanation)
>>>>>>> 364786b26cf619373342c109bbd3cfb402991092
