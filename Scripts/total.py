from prepare import prepare
from translate import translate
from fix import fix

def total(NLQ: str):
    NLA = prepare(NLQ)
    LLA, _ = translate(NLQ,NLA)
    fixcount = 0
    fixed, LLA = fix(LLA)
    if fixcount < 90:
        if not fixed:
            fixcount += 1
            fixed, LLA = fix(LLA)
    else:
        return LLA, -1
    return LLA, fixcount