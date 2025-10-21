from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import requests
import os

app = FastAPI()

# ✅ Povolenie CORS, aby HTML frontend mohol volať API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return JSONResponse({"reply": "⚠️ Prázdna správa."}, status_code=400)

        if not API_KEY:
            return JSONResponse({"reply": "❌ GROQ_API_KEY chýba na serveri."}, status_code=500)

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "Si priateľský slovenský chatbot."},
                {"role": "user", "content": user_input}
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # ✅ Opravená URL (odstránené medzery na konci)
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            # 🔍 Detailnejšia chyba
            return JSONResponse({
                "reply": f"⚠️ API chyba: {response.status_code}",
                "details": response.text
            }, status_code=response.status_code)

        result = response.json()
        reply_text = result["choices"][0]["message"]["content"]

        return {"reply": reply_text}

    except Exception as e:
        return JSONResponse({"reply": f"❌ Server error: {str(e)}"}, status_code=500)


@app.get("/")
async def root():
    return FileResponse("index.html")
