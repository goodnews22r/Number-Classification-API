from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
import uvicorn
import concurrent.futures

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

executor = concurrent.futures.ThreadPoolExecutor() 

def validate_number(number: str):
    if not number.lstrip("-").isdigit():
        return None
    return int(number)

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
    digits = [int(d) for d in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact_sync(n: int) -> str:
    url = f"http://numbersapi.com/{n}"
    try:
        response = httpx.get(url, timeout=0.01)  
        if response.status_code == 200:
            return response.text
    except httpx.TimeoutException:
        return "No fun fact available (timeout)."
    return "No fun fact found."

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/api/classify-number")
async def classify_number(
    number: str = Query(..., description="The number to classify"),
):
    num = validate_number(number)  
    if num is None:
        return JSONResponse(status_code=400, content={"error": True, "number": number})

    properties = ["odd" if num % 2 else "even"]
    if is_armstrong(num):
        properties.append("armstrong")

    response = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": sorted(properties),
        "digit_sum": get_digit_sum(num),
        "fun_fact": "Fetching..."
    }

    executor.submit(lambda: response.update({"fun_fact": get_fun_fact_sync(num)}))

    return response

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
