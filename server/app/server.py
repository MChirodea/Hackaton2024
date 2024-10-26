import ast
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import time
import re
import os
from upstash_redis import Redis
from packages.model.input.review import ReviewsInput
from packages.model.input.review import ReviewInput, ReviewsInput
from packages.model.model import LLMBrillio
from packages.example.reviews import product

load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = LLMBrillio()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.post("/analyze")
async def analyze(data: dict):
    redis = Redis(url="https://correct-mullet-20638.upstash.io", token=os.environ["REDIS_TOKEN"])

    base_url = get_url(data['url'])

    redis_product_reviews_key = f"reviews:{base_url}"
    redis_product_review_count_key = f"review-count:{base_url}"

    number_of_reviews = data['total_reviews']
    number_of_cached_reviews = -1
    if redis.exists(redis_product_review_count_key):
        number_of_cached_reviews = int(redis.get(redis_product_review_count_key))
    else:
        redis.set(redis_product_review_count_key, number_of_reviews)

    if number_of_reviews != number_of_cached_reviews:
        # Fetch all reviews
        reviews = await get_reviews(base_url)
        redis.set(redis_product_reviews_key, str(reviews))
    else:
        # Fetch cached reviews
        reviews = ast.literal_eval(redis.get(redis_product_reviews_key))

    formatted_reviews = convert_api_response_to_api_input(reviews, data['description'], data['specifications'])
    response = model.generate_response(formatted_reviews)
    return response

def get_url(url: str):
    start_pattern = "^https://www.emag.ro/"
    url = re.sub(start_pattern, 'https://www.emag.ro/product-feedback/', url)
    end_pattern = "(\\?(.*))|(#(.*))"
    x = re.search(end_pattern, url)
    if x is not None:
        result = re.sub(end_pattern, 'reviews/list', url)
    else:
        result = url + 'reviews/list'
    
    return result 


async def get_reviews(base_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    # Parameters for pagination
    limit = 20  # Number of reviews per page
    offset = 0

    # List to store all reviews
    all_reviews = []

    def fetch_reviews(offset):
        params = {
            "page[limit]": limit,
            "page[offset]": offset,
        }
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()

    while True:
        data = fetch_reviews(offset)
        # Access the reviews data from the JSON response
        reviews = data.get("reviews", []).get("items", [])

        # If there are no reviews, stop the loop
        if not reviews:
            print("No reviews found")
            break

        # Process each review
        for review in reviews:
            # If the review has no author, skip it
            if not review.get("user"):
                continue

            if not review.get("user").get("id"):
                continue

            all_reviews.append({
                "id": int(review.get("id")),
                "author_id": int(review.get("user").get("id")),
                "author_name": review.get("user").get("name"),
                "title": review.get("title", ""),
                "description": review.get("content_no_tags"),
                "rating": int(review.get("rating")),
                "votes": int(review.get("votes")),
                "published_on": review.get("published"),
                "has_bought_product": review.get("is_bought"),
            })

        offset = offset + limit
        time.sleep(1)  # Add a delay to avoid hitting the API rate limit

    return all_reviews

@app.get("/review/example")
async def calculate_review_trustworthiness():
    response = model.generate_response(product)
    return response

@app.post("/review")
async def calculate_review_trustworthiness_with_input(input: ReviewsInput):
    response = model.generate_response(input)
    return response

def convert_api_response_to_api_input(reviews, product_description, product_specifications):
    formatted_reviews = []
    for review in reviews:
        formatted_reviews.append(ReviewInput(
            id=review["id"],
            author_id=review["author_id"],
            author_name=review["author_name"],
            title=review["title"],
            description=review["description"],
            rating=review["rating"],
            votes=review["votes"],
            published_on=review["published_on"],
            has_bought_product=review["has_bought_product"]
        ))

    input_data = ReviewsInput(
        description=product_description,
        specifications=product_specifications,
        reviews=formatted_reviews
    )

    return input_data


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
