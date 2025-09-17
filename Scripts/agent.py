from prepare import prepare_NL
from convert import NLQA_to_LLQA, LLQA_to_NLA
from solve import check, fix, fix_loop, answer_LL, give_lemma


def feedback_loop(LLQA: str, max_fix_attempts = 5) -> tuple[str, int]:
    fixcount = 0
    history = []
    feedback, fixed = check(LLQA)
    while True:
        if fixcount < max_fix_attempts:
            if not fixed:
                history.append(LLQA)
                LLQA = fix(LLQA, feedback)
                fixcount += 1
                if LLQA in history:
                    loop_index = history.index(LLQA)
                    # replace loop of history with fixed version
                    history = history[:loop_index - 1] + [fix_loop(history[loop_index:]+[LLQA])]
                feedback, fixed = check(LLQA)
            else:
                return LLQA, fixcount
        else:
            return LLQA, -1

def answer_full_through_NLA(NLQ: str, n_filter: int = 1, max_fix_attempts:int = 5) -> tuple[str, str, int]:
    NLQA = prepare_NL(NLQ, n_filter)
    LLQA = NLQA_to_LLQA(*NLQA)
    LLQA, fixcount = feedback_loop(LLQA, max_fix_attempts)
    NLA = LLQA_to_NLA(LLQA)
    return NLA, LLQA, fixcount

def answer_core_light(LLQ: str, max_fix_attempts:int = 5) -> tuple[str, int]:
    LLQA = answer_LL(LLQ)
    LLQA, fixcount = feedback_loop(LLQA, max_fix_attempts)
    return LLQA, fixcount

def answer_core_heavy(LLQ: str, max_fix_attempts:int = 5, n_lemmas:int = 3) -> tuple[str, int]:
    lemmas = []
    for i in range(n_lemmas):
        lemma = give_lemma(LLQ)
        lemma_full , lemma_fixcount = answer_core_light(lemma, max_fix_attempts)
        if lemma_fixcount != -1:
            lemmas.append(lemma_full)
    LLQ_with_lemmas = "\n\n".join(lemmas) + "\n\n" + LLQ
    LLQA = answer_LL(LLQ_with_lemmas)
    LLQA, fixcount = feedback_loop(LLQA, max_fix_attempts)
    return LLQA, fixcount

if __name__ == "__main__":
    print(answer_full_through_NLA("there are infinite primes. what's the weather today?"))
    # NLQ = "proof if x is even, then x^2 is even. what's the weather today?"
    # NLA, LL, fixcount = answer_full(NLQ)
    # print("answer:", NLA)
    # print("fixcount:", fixcount)
    # print("Lean code:", LL)
