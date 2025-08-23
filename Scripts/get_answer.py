import requests
import json
from jsonschema import validate, ValidationError
import re
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

api_key_path = os.path.join(os.path.dirname(__file__), 'api_key.txt')
with open(api_key_path, 'r') as f:
    api_key = f.read().strip()
default_model_id = "chatgpt-4.1"

def get_answer(message: str = "", model_id: str = default_model_id,  messages: list = [], system_prompt: str = "") :
    '''
    this is a function to get answer from chat model
    '''

    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 构建请求数据
    if message:
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": message}]
        }
    elif messages:
        payload = {
            "model": model_id,
            "messages": messages
        }
    else:
        raise ValueError("Either message or messages must be provided, but not both.")
    
    # 添加system提示（如果有）
    if system_prompt:
        if "messages" not in payload:
            payload["messages"] = []
        payload["messages"].insert(0, {"role": "system", "content": system_prompt})
    
    if model_id.endswith("-local"):
        model_id = model_id.replace("-local", "")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
        inputs = tokenizer.apply_chat_template(payload, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)
        outputs = model.generate(inputs, max_new_tokens=8192)
        pattern = r"<｜Assistant｜>(.*?)<｜end▁of▁sentence｜>"# change this for your model
        outputs_text = tokenizer.batch_decode(outputs)
        match = re.search(pattern, outputs_text, re.DOTALL)
        result = match.group(1) if match else ""
        return result.strip()

    else:
        url = "https://sg.uiuiapi.com/v1/chat/completions"
        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # 检查响应状态
        if response.status_code != 200:
            raise Exception(f"API请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
        
        # 解析响应
        response_data = response.json()
        print("Response Data:", response_data["choices"][0]["message"]["content"]+ "\n")  # 调试输出
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

#TD try to use \\n instead of actual newlines in JSON
default_system_prompt = f"""You are a mathematician, and you are tasked with solving complex mathematical problems. Please provide answer in JSON format with 'analysis' and 'result' fields. Note that use \\n instead of actual newlines in JSON.
In the result part, You should output without any additional explanation. Don't use code blocks to wrap.
Each part should be a multi-line plain text without any formatting.
"""

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.S)
    if match:
        return match.group(0)
    else:
        print("Failed to extract JSON")
        return None

def get_schema_answer(message: str = "", model_id: str = default_model_id,  messages: list = [], system_prompt: str = default_system_prompt) -> dict:
    '''
    this is a function to get answer from chat model with schema
    '''
    for i in range(3):
        response = get_answer(message, model_id, messages, system_prompt)
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