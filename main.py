from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import threading
import time
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
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
    abs_n = abs(n)  
    digits = [int(d) for d in str(abs_n)]
    return sum(d ** len(digits) for d in digits) == abs_n

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))  

async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}"
    try:
        async with httpx.AsyncClient(timeout=0.5) as client: 
            response = await client.get(url)
            if response.status_code == 200:
                return response.text
    except httpx.TimeoutException:
        return "No fun fact available (timeout)."
    return "No fun fact found."

async def fetch_fun_fact(number: int, response: dict):
    response["fun_fact"] = await get_fun_fact(number)

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/api/classify-number")
async def classify_number(
    number: str = Query(..., description="The number to classify"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    try:
        num = int(number)
    except ValueError:
        return JSONResponse(status_code=400, content={"error": True, "number": number})

    properties = ["odd" if num % 2 else "even"]

    if num < 0 and is_armstrong(num):
        properties.append("armstrong")

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

    background_tasks.add_task(fetch_fun_fact, num, response)
    
    return response

def keep_alive():
    while True:
        try:
            httpx.get("https://number-classification-api-production-ca7b.up.railway.app/api/classify-number?number=1")
        except:
            pass
        time.sleep(300) 

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
