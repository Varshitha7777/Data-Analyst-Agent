from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
import io
import pandas as pd
from dotenv import load_dotenv
import traceback
import re

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
print("🔐 Loaded API Key:", API_KEY)

app = FastAPI()

# Configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001",
    "file://",
    "null",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    url: str
    tasks: list[str]

@app.get("/")
def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Universal Data Analyst Agent using OpenRouter!"}

@app.post("/api/url/")
async def analyze_url_data(request: AnalysisRequest):
    """
    Fetches data from a given URL, sends it along with analysis tasks to the LLM,
    and returns a 4-element JSON array (numeric, string, correlation, PLOTTING_DATA).
    """
    try:
        if not API_KEY:
            raise HTTPException(status_code=500, detail="API key is missing. Check your .env file.")

        # 1. Fetch data from the provided URL
        print(f"Fetching data from: {request.url}")
        data_response = requests.get(request.url)
        data_response.raise_for_status()

        try:
            data_content = io.StringIO(data_response.text)
            df = pd.read_csv(data_content)
            data_preview = df.head().to_string()
            print("Data preview:\n", data_preview)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not parse data from URL as CSV: {e}")

        # 2. Prepare the prompt for the LLM
        # IMPORTANT: Enhanced prompt for LLM to be very specific about plotting data
        user_prompt = f"""
        You are a data analyst. I will provide you with a preview of a dataset and a list of analysis tasks.
        Your response MUST be a JSON array containing exactly four elements in this order:
        1. A numerical result (integer or float) directly answering a numerical question from the tasks. If no numerical question, return 0.
        2. A string summary or textual answer directly addressing a non-numerical question from the tasks. If no string question, return an empty string.
        3. A floating-point number representing a correlation or another relevant numerical value. If no correlation/specific value is requested, return 0.0.
        4. A JSON array of objects, where each object has 'x' and 'y' properties, representing data points for a scatter plot. This array should contain actual numerical values extracted from the dataset preview based on a plotting task. For example: [{{x: 1.4, y: 0.2}}, {{x: 1.5, y: 0.3}}]. If no specific plot is requested, return an empty array [].

        Do not include any other text, conversational elements, or formatting outside of the JSON array.

        Dataset Preview (first 5 rows):
        ```
        {data_preview}
        ```

        Analysis Tasks:
        {'- ' + '\\n- '.join(request.tasks)}

        Example of expected JSON output for Iris dataset with plotting task:
        [5.84, "Average sepal length is 5.84", 0.87, [{{x: 1.4, y: 0.2}}, {{x: 1.4, y: 0.2}}, {{x: 1.3, y: 0.2}}, {{x: 1.5, y: 0.2}}, {{x: 1.4, y: 0.2}}]]

        Example of expected JSON output for Gapminder dataset with plotting task:
        [67.007, "Highest GDP per capita in 2007 is 49357.19 with Switzerland", 0.678, [{{x: 779.44, y: 28.80}}, {{x: 820.85, y: 30.33}}, {{x: 853.10, y: 31.99}}]]
        """

        # 3. Prepare OpenRouter API call
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Universal Data Analyst Agent"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "temperature": 0.0,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful data analyst assistant. Always respond with a JSON array containing exactly four elements: a numerical answer, a string summary, a floating-point value, and a JSON array of objects for plotting data. Do not include any other text or formatting outside the JSON array."
                },
                {"role": "user", "content": user_prompt}
            ]
        }

        openrouter_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        openrouter_response.raise_for_status()
        result = openrouter_response.json()

        if "choices" not in result or not result["choices"]:
            print(f"❌ No valid 'choices' in model response: {result}")
            raise HTTPException(status_code=500, detail="No valid response from model")

        message = result["choices"][0]["message"]["content"]
        print(f"📦 Raw model message received: {repr(message)}")

        # 4. Parse the model's response as JSON
        try:
            parsed = json.loads(message.strip())
            if isinstance(parsed, list) and len(parsed) == 4:
                # Ensure the 4th element is a list/object for plotting data (or None)
                if not (isinstance(parsed[3], list) or isinstance(parsed[3], dict) or parsed[3] is None):
                    raise HTTPException(status_code=500, detail="Model's 4th element (plotting data) is not a valid JSON array, object, or null.")
                return JSONResponse(content=parsed)
            else:
                print(f"⚠️ Parsed content is not a 4-element list: {parsed}")
                raise HTTPException(status_code=500, detail="Model response was not a 4-element JSON array.")
        except json.JSONDecodeError as e:
            print(f"❌ json.loads parsing failed: {e}. Raw response start: {message[:200]}...")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse model response as valid JSON. This might be due to truncation or malformation. Raw response start: {message[:200]}..."
            )
    except requests.exceptions.RequestException as req_err:
        print(f"❌ API request failed: {req_err}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"External API request failed: {req_err}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")
