from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()  # musí byť nad app.add_middleware!

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         json=payload, headers=headers)







