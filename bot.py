import requests
from search import search_top_k
from dotenv import load_dotenv

import os
import json

load_dotenv()

def gemini_response_user_query(context, query):
    GEMINI_API_KEY = os.getenv("GEMINI_KEY")
    GEMINI_MODEL = "gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
        You are a helpful assistant for farmers. Answer the user's question based on query and context.
        Context: {context}
        User Query: {query}
        JUST give answer to the user query, do not include any other information.
        
    """
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    response_json = response.json()

    generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
    generated_text = generated_text.replace("```json", "").replace("```", "").strip()
    return generated_text


while True:
    user_query = input("Enter your query: ")
    if user_query.lower() == "exit":
        break

    # Search for top k documents
    top_k_docs = search_top_k(user_query, k=5)
    
    # Combine the context from the top k documents
    context = "\n".join([doc['text'] for doc in top_k_docs])

    # Get response from Gemini
    response = gemini_response_user_query(context, user_query)
    
    print(f"Response: {response}")


