import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from tqdm import tqdm

# ===== 配置 =====
INPUT_JSON = "Data\\descriptions.json"
OUTPUT = "Data\\embedded.npy"
MODEL_NAME = "microsoft/codebert-base"
MAX_LENGTH = 512       # CodeBERT 最大输入长度
BATCH_SIZE = 128        # 批大小，可调大到 128 看显存
USE_FP16 = True        # 进半精度模式节省显存

# ===== 加载模型 =====
print(f"加载模型 {MODEL_NAME} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if USE_FP16 and torch.cuda.is_available():
    model = model.to(device).half()
else:
    model = model.to(device)

model.eval()


# ===== 平均池化函数 =====
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state  # (batch, seq, hidden)
    mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * mask_expanded, 1) / torch.clamp(mask_expanded.sum(1), min=1e-9)



# ===== 批量嵌入函数 =====
def embed_batch(texts):
    inputs = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        sentence_embeddings = mean_pooling(outputs, inputs["attention_mask"])
    return sentence_embeddings.cpu().numpy()


# ===== 主处理逻辑 =====
print(f"读取 {INPUT_JSON} ...")
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"共 {len(data)} 条记录，开始生成嵌入向量（batch={BATCH_SIZE}）")

emb_list = []
batch_texts = []

for item in tqdm(data, desc="Processing"):
    batch_texts.append(item)
    # 批处理到上限
    if len(batch_texts) == BATCH_SIZE:
        vectors = embed_batch(batch_texts)
        emb_list.append(vectors)
        batch_texts.clear()

# 处理最后一批
if batch_texts:
    vectors = embed_batch(batch_texts)
    emb_list.append(vectors)

# ===== 保存结果 =====
embeddings = np.vstack(emb_list)
np.save(OUTPUT, embeddings.astype(np.float32))


print("✅ 完成！")