from prepare import prepare
from translate import translate, inverse_translate
from improve import check, fix

def answer(NLQ: str):
    NLA = prepare(NLQ)
    print("NLA:", NLA)
    LL = translate(NLQ,NLA)
    print("LL:", LL)
    fixcount = 0
    feedback, fixed = check(LL)
    while 1:
        if fixcount < 90:
            if not fixed:
                LL = fix(LL, feedback)
                fixcount += 1
                feedback, fixed = check(LL)
            else:
                return inverse_translate(LL), fixcount
        else:
            return inverse_translate(LL), -1



if __name__ == "__main__":
    NLQ = "proof if x 是偶数, 那么 x^2 是偶数"
    NLA , fixcount = answer(NLQ)
    print("NLA:", NLA)
    print("fixcount:", fixcount)
