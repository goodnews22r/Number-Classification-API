from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

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
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))

async def get_fun_fact(n: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://numbersapi.com/{n}")
        return response.text if response.status_code == 200 else "No fact found."

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    print(f"Received number: {number}")  # Debugging line
    try:
        fun_fact = await get_fun_fact(number)
        properties = ["odd" if number % 2 else "even"]
        if is_armstrong(number):
            properties.append("armstrong")
        response = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": get_digit_sum(number),
            "fun_fact": fun_fact
        }
        print(response)  # Debugging line
        return response
    except Exception as e:
        print(f"Error: {e}")  # Debugging line
        return {"number": str(number), "error": True}

@app.get("/api/test-httpx")
async def test_httpx():
    return await get_fun_fact(371)
