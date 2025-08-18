import requests
import json
from jsonschema import validate, ValidationError
import re

def get_answer(message: str = "", model: str = "deepseek-ai/DeepSeek-V3",  messages: list = [], system_prompt: str = "") -> str:
    '''
    this is a function to get answer from chat model
    '''

    # 设置API端点
    url = "https://api.siliconflow.cn/v1/chat/completions"
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-ytdjrnaeqwohnbzjarpxuafuzfpolqjimwqvyuwdbolgiyvi"  
    }
    
    # 构建请求数据
    if message:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }
    elif messages:
        payload = {
            "model": model,
            "messages": messages
        }
    else:
        raise ValueError("Either message or messages must be provided, but not both.")
    
    # 添加system提示（如果有）
    if system_prompt:
        if "messages" not in payload:
            payload["messages"] = []
        payload["messages"].insert(0, {"role": "system", "content": system_prompt})
    
    # 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # 检查响应状态
    if response.status_code != 200:
        raise Exception(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
    
    # 解析响应
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]

schema = {
    "type": "object",
    "properties": {
        "analysis": {"type": "string"},
        "result": {"type": "string"}
    },
    "required": ["analysis", "result"],
    "additionalProperties": False
}

default_system_prompt = f"""You are a mathematician, and you are tasked with solving complex mathematical problems. Please provide answer in JSON format with 'analysis' and 'result' fields."""

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.S)
    if match:
        return match.group(0)
    return None

def get_schema_answer(message: str = "", model: str = "deepseek-ai/DeepSeek-V3",  messages: list = [], system_prompt: str = default_system_prompt) -> dict:
    '''
    this is a function to get answer from chat model with schema
    '''
    for i in range(3):
        response = get_answer(message, model, messages, system_prompt)
        json_text = extract_json(response)
        if json_text:
            try:
                json_output = json.loads(json_text)
                try:
                    validate(instance=json_output, schema=schema)
                except ValidationError:
                    continue
                return json_output
            except json.JSONDecodeError:
                continue
        else:
            continue
    raise ValueError("Failed to extract valid JSON from the response after multiple attempts.")

if __name__ == "__main__":
    print(get_schema_answer("x 是偶数, 那么 x^2 是偶数"))