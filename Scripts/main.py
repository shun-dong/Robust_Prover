from prepare import prepare
from translate import translate, inverse_translate
from improve import check, fix, fix_loop

def answer(NLQ: str):
    NLA = prepare(NLQ)
    LL = translate(NLQ, NLA)
    fixcount = 0
    history = []
    feedback, fixed = check(LL)
    while True:
        if fixcount < 5:
            if not fixed:
                history.append(LL)
                LL = fix(LL, feedback)
                fixcount += 1
                if LL in history:
                    loop_index = history.index(LL)
                    # replace loop of history with fixed version
                    history = history[:loop_index - 1] + [fix_loop(history[loop_index:]+[LL])]
                feedback, fixed = check(LL)
            else:
                return inverse_translate(LL), fixcount, LL
        else:
            return inverse_translate(LL), -1, LL

if __name__ == "__main__":
    NLQ = "proof if x is even, then x^2 is even. what's the weather today?"
    NLA, fixcount, LL = answer(NLQ)
    print("answer:", NLA)
    print("fixcount:", fixcount)
    print("Lean code:", LL)
