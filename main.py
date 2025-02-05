from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
from typing import List, Union

app = FastAPI()

# Helper functions for classification
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum([d ** len(digits) for d in digits]) == n

def get_fun_fact(n: int) -> str:
    # Add fallback for missing fun facts
    return f"{n} is a narcissistic number."  # A default fallback

# Endpoint to classify number
@app.get("/api/classify-number")
async def classify_number(number: str):
    try:
        # Validate input and parse to integer
        num = int(number)
        
        # Negative number check
        if num < 0:
            raise HTTPException(status_code=400, detail="Invalid input. Please provide a non-negative integer.")
        
        # Classification logic
        result = {
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect(num),
            "properties": [],
            "digit_sum": sum([int(digit) for digit in str(num)]),
            "fun_fact": get_fun_fact(num)
        }

        if is_armstrong(num):
            result["properties"].append("armstrong")
        
        if num % 2 == 0:
            result["properties"].append("even")
        else:
            result["properties"].append("odd")
        
        # Sort properties for consistency
        result["properties"].sort()
        
        return result

    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid input: {number}")
