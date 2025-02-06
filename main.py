from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits of a number."""
    return sum(int(d) for d in str(n))

async def get_fun_fact(n: int) -> str:
    """Fetch a mathematical fun fact from Numbers API."""
    url = f"http://numbersapi.com/{n}/math"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=2)
            return response.text if response.status_code == 200 else "No fact found."
        except httpx.RequestError:
            return "No fact found."

@app.get("/")
def home():
    """Root endpoint to confirm API is running."""
    return {"message": "API is running!"}

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    """Classifies a given number based on various properties."""
    if not number.lstrip("-").isdigit():
        return {"number": number, "error": True}  # 400 Bad Request response

    number = int(number)
    properties = ["odd" if number % 2 else "even"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")  # Armstrong should be first if applicable

    fun_fact = await get_fun_fact(number)

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": get_digit_sum(number),
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000, configurable via env
    uvicorn.run(app, host="0.0.0.0", port=port)
