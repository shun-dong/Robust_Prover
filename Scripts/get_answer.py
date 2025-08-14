import requests
import json

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


if __name__ == "__main__":
    # 示例调用
    message = "你好，世界！"
    answer = get_answer(message)
    print(answer)