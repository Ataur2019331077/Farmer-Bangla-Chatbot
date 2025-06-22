from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from pymongo import MongoClient
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load multilingual E5 model
model_name = "intfloat/multilingual-e5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bengali_texts"]
collection = db["paragraphs"]

def get_embedding(text, prefix="passage: "):
    text = prefix + text.strip()
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        model_output = model(**encoded)
    embeddings = model_output.last_hidden_state
    attention_mask = encoded["attention_mask"]
    mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    summed = torch.sum(embeddings * mask_expanded, 1)
    counted = torch.clamp(mask_expanded.sum(1), min=1e-9)
    mean_pooled = summed / counted
    return F.normalize(mean_pooled, p=2, dim=1)[0].tolist()

def search_top_k(query, k=5):
    query_vector = get_embedding(query, prefix="query: ")

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_vector,
                "path": "embedding",
                "numCandidates": 100,
                "limit": k,
                "index": "embedding_knn_index"
            }
        },
        {
            "$project": {
                "text": 1,
                "_id": 0
            }
        }
    ])

    return list(results)


