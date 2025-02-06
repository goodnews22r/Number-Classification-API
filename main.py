from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
import httpx
import asyncio
import os
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    abs_n = abs(n)  # Use absolute value for negative numbers
    digits = [int(d) for d in str(abs_n)]
    return sum(d ** len(digits) for d in digits) == abs_n

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))  # Use absolute value


async def fetch_fun_fact(number: int, response: dict):
    response["fun_fact"] = await get_fun_fact(number)

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        num = int(number)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": True, "number": number})

    properties = ["odd" if num % 2 else "even"]
    if num >= 0 and is_armstrong(num):
        properties.append("armstrong")

    response = {
        "number": num,
        "is_prime": is_prime(num) if num >= 2 else False,
        "is_perfect": is_perfect(num) if num >= 2 else False,
        "properties": sorted(properties),
        "digit_sum": get_digit_sum(abs(num)),
        "fun_fact": "Fetching..."
    }

    # Fetch fun fact in the background
    background_tasks.add_task(fetch_fun_fact, num, response)
    
    return response

@app.get("/api/test-httpx")
async def test_httpx():
    return await get_fun_fact(371)

# Run the API with dynamic port binding for Railway
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
