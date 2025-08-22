from prepare import prepare
from translate import translate, inverse_translate
from improve import check, fix

def answer(NLQ: str):
    NLA = prepare(NLQ)
    LL = translate(NLQ,NLA)
    fixcount = 0
    feedback, fixed = check(LL)
    while 1:
        if fixcount < 5:
            if not fixed:
                LL = fix(LL, feedback)
                fixcount += 1
                feedback, fixed = check(LL)
            else:
                return inverse_translate(LL), fixcount, LL
        else:
            return inverse_translate(LL), -1, LL



if __name__ == "__main__":
    NLQ = "proof if x is even, then x^2 is even. what's the weather today?"
    NLA , fixcount, LL = answer(NLQ)
    print("answer:", NLA)
    print("fixcount:", fixcount)
    print("Lean code:", LL)
