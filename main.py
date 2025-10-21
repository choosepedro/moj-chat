from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 200
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                             json=payload, headers=headers)

    result = response.json()
    return {"reply": result["choices"][0]["message"]["content"]}

@app.get("/")
async def root():
    return {"message": "Chat API is running. Send POST requests to /chat endpoint."}
