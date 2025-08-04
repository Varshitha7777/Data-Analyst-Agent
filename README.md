from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import requests
import json
import os
from dotenv import load_dotenv
import traceback
import re
import ast  # ✅ For safely evaluating stringified Python lists

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
print("🔐 Loaded API Key:", API_KEY)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Data Analyst Agent using OpenRouter!"}

@app.post("/api/")
async def analyze_task(file: UploadFile = File(...)):
    try:
        # Step 1: Read question file
        content = await file.read()
        question = content.decode("utf-8")

        if not API_KEY:
            return JSONResponse(status_code=500, content={"error": "API key is missing. Check your .env file."})

        # Step 2: Prepare OpenRouter API call
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Data Analyst Agent"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.0,
            "messages": [{"role": "user", "content": question}]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        if "choices" not in result or not result["choices"]:
            return JSONResponse(status_code=500, content={"error": "No valid response from model", "raw": result})

        message = result["choices"][0]["message"]["content"]
        print("📦 Raw model message:", repr(message))

        # Step 3: Attempt direct JSON or AST parsing
        try:
            parsed = json.loads(message.strip())

            # If response is a stringified list, use ast.literal_eval
            if isinstance(parsed, str):
                parsed = ast.literal_eval(parsed)

            if isinstance(parsed, list) and len(parsed) == 4:
                return JSONResponse(content=parsed)
        except Exception as e:
            print("❌ Direct or AST parsing failed:", e)

        # Step 4: Fallback to regex
        try:
            match = re.search(r"\[\s*[\s\S]*?\]", message)
            if match:
                cleaned = ast.literal_eval(match.group(0))
                if isinstance(cleaned, list) and len(cleaned) == 4:
                    return JSONResponse(content=cleaned)
        except Exception as clean_error:
            print("⚠️ Regex fallback failed:", clean_error)

        # Step 5: Final fallback — return raw response
        return JSONResponse(content={
            "note": "Could not parse model response as 4-element JSON array",
            "raw_response": message
        }, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
