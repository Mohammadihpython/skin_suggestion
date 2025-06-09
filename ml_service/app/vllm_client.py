import httpx

async def query_vllm(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/v1/completions",
            json={
                "model": "med-gemma",
                "prompt": prompt,
                "max_tokens": 512,
                "temperature": 0.7
            }
        )
    data = resp.json()
    return data["choices"][0]["text"].strip()