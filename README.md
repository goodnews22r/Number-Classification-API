# Number Classification API

This is a simple API that classifies numbers based on their properties. It checks if a number is prime, perfect, Armstrong, odd/even, and provides additional fun facts about the number using the Numbers API.

## Features

- Accepts GET requests with a `number` parameter.
- Returns a JSON response with number properties:
  - Whether the number is prime.
  - Whether the number is perfect.
  - Whether the number is Armstrong.
  - The number's digit sum.
  - A fun fact from the Numbers API.

## Endpoint

### GET /api/classify-number

#### Request

- URL: `<your-domain>/api/classify-number?number=<number>`
- Method: `GET`
- Query Parameter: 
  - `number`: The number to classify (integer).

#### Example Request

```bash
GET https://number-classification-api-production-ca7b.up.railway.app/api/classify-number?number=371
Response (200 OK) json

{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is a narcissistic number."
}

Response (400 Bad Request) json
{
    "number": "alphabet",
    "error": true
}

How to Run Locally
Clone the repository:
git clone https://github.com/goodnews22r/Number-Classification-API
cd number-classification-api

Create a virtual environment:
python -m venv .venv

Install dependencies:
pip install -r requirements.txt

Run the application:
uvicorn main:app --reload
Access the API at http://127.0.0.1:8000.

Deployment
This API is deployed and can be accessed publicly. Replace the base URL with your deployment URL when making requests.

Testing the API
You can test the /api/classify-number endpoint using curl or any API testing tool like Postman.
Example using curl:
curl -X GET https://number-classification-api-production-ca7b.up.railway.app/api/classify-number?number=371