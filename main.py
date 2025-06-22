from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from pymongo import MongoClient
import re
import os
from dotenv import load_dotenv

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

# Function to split text into paragraphs
def split_into_paragraphs(text):
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]

# E5 embedding function (with prefix)
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

# Function to embed and store paragraphs
def embed_and_store_paragraphs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    paragraphs = split_into_paragraphs(text)

    for para in paragraphs:
        vector = get_embedding(para, prefix="passage: ")
        doc = {
            "text": para,
            "embedding": vector
        }
        collection.insert_one(doc)

    print(f"Inserted {len(paragraphs)} paragraphs into MongoDB.")


embed_and_store_paragraphs("rice.txt")