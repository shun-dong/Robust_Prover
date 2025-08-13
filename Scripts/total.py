from prepare import prepare
from translate import translate
from fix import fix

def total(NLQ: str) -> str:
    NLA = prepare(NLQ)
    LLA = translate(NLA)
    fixed, _ = fix(LLA)
    return fixed