from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import requests
import os

app = FastAPI()

API_KEY = os.getenv("GROQ_API_KEY")

# 👉 Route na zobrazenie tvojej webovej stránky
@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("index.html")

# 👉 Chat endpoint
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
    response = requests.post("https://api.groq.com/openai/v1/chat/completions


