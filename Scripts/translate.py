from get_answer import get_answer, get_schema_answer
def translate(NLQ:str, NLA: str) :
    LL = get_schema_answer(f"""translate the following natural language question and answer to lean language:\n Question: {NLQ}\nAnswer: {NLA}
                    Remember to include all necessary imports and definitions.
                    In result part, You should only output the lean language translation without any additional explanation. Don't use code blocks to wrap.""")["result"]
    return LL

def inverse_translate(LL: str) -> str:
    NLA = get_schema_answer(f"""translate the following lean language to natural language: {LL}
                            In result part, You should only output the natural language translation without any additional explanation.""")["result"]
    return NLA


