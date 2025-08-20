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
                return inverse_translate(LL), fixcount
        else:
            return inverse_translate(LL), -1, LL



if __name__ == "__main__":
    NLQ = "proof if x 是偶数, 那么 x^2 是偶数"
    NLA , fixcount, LL = answer(NLQ)
    print("NLA:", NLA)
    print("fixcount:", fixcount)
    print("Lean code:", LL)
