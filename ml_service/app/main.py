import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

VLLM_API_URL = "http://localhost:8000/v1/completions"

app = FastAPI()

class PromptRequest(BaseModel):
    user_id: int
    features: dict  # مثال: {"acne": "moderate", "wrinkles": "mild"}

@app.post("/generate-report")
async def generate_report(data: PromptRequest):
    prompt = f"User has these skin features: {data.features}. Provide a skincare routine."

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            VLLM_API_URL,
            json={
                "model": "med-gemma",
                "prompt": prompt,
                "max_tokens": 512,
                "temperature": 0.7
            }
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    result = resp.json()["choices"][0]["text"]
    return {"user_id": data.user_id, "recommendation": result}


import asyncio
from app.kafka.consumer import consume_messages

if __name__ == "__main__":
    asyncio.run(consume_messages())