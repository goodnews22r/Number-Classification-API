from fastapi import FastAPI, HTTPException, Query
import aiohttp
import math

app = FastAPI()

# Helper functions
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, abs(n)) if abs(n) % i == 0) == abs(n)

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]  # Handle negatives
    return sum(d ** len(digits) for d in digits) == abs(n)

async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("text", f"No fun fact available for {n}.")
        return f"No fun fact available for {n}."
    except Exception:
        return f"Could not fetch a fun fact for {n}."

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="Provide an integer to classify")):
    # Handle missing number parameter
    if number.strip() == "":
        raise HTTPException(status_code=400, detail={"error": True, "number": ""})

    # Validate input
    if not number.lstrip("-").isdigit():
        raise HTTPException(status_code=400, detail={"error": True, "number": number})

    num = int(number)

    result = {
        "error": False,
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": [],
        "digit_sum": sum(int(digit) for digit in str(abs(num))),
        "fun_fact": await get_fun_fact(num),
    }

    if is_armstrong(num):
        result["properties"].append("armstrong")
    if num % 2 == 0:
        result["properties"].append("even")
    else:
        result["properties"].append("odd")

    result["properties"].sort()

    return result
