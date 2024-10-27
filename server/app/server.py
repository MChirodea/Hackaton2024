import ast
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import time
import re
import os
from upstash_redis import Redis
from packages.llm_model.input.review import ReviewInput, ReviewsInput
from packages.llm_model.model import LLMBrillio
from packages.example.reviews import product
from packages.llm_model.output.review import ReviewsResponse
import pickle
import pandas as pd
import sklearn
from pydantic.dataclasses import dataclass
from dataclasses import asdict
import json
from pydantic.tools import parse_obj_as

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
    redis_product_llm_feedback_key = f"llm-feedback:{base_url}"

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

    llm_answers: ReviewsResponse
    # If the LLM feedback is cached, return it
    if redis.exists(redis_product_llm_feedback_key):
        llm_feedback_json = json.loads(redis.get(redis_product_llm_feedback_key))
        llm_feedback_obj = parse_obj_as(ReviewsInput, llm_feedback_json)
        llm_answers = llm_feedback_obj
    else:
        formatted_reviews = convert_api_response_to_api_input(reviews, data['description'], data['specifications'])
        llm_answers = model.generate_response(formatted_reviews)

        # Cache the LLM feedback
        llm_answers_dict = llm_answers.model_dump()
        llm_answers_json = json.dumps(llm_answers_dict)
        redis.set(redis_product_llm_feedback_key, llm_answers_json)

    prediction = calculate_final_score(llm_answers)

    response = []
    for index, llm_answer in enumerate(llm_answers.reviews):
        response.append({
            "id": llm_answer.id,
            "score": prediction[index],
            "summary": llm_answer.summary,
        })

    return response

def calculate_final_score(llm_answers: ReviewsResponse):
    data: dict = {
        "a01_answer": [],
        "a01_confidence": [],
        "a02_answer": [],
        "a02_confidence": [],
        "a03_answer": [],
        "a03_confidence": [],
        "a04_answer": [],
        "a04_confidence": [],
        "a05_answer": [],
        "a05_confidence": [],
        "a06_answer": [],
        "a06_confidence": [],
        "a07_answer": [],
        "a07_confidence": [],
        "a08_answer": [],
        "a08_confidence": [],
        "a09_answer": [],
        "a09_confidence": [],
        "a10_answer": [],
        "a10_confidence": [],
        "a11_answer": [],
        "a11_confidence": [],
    }

    for llm_answer in llm_answers.reviews:
        data['a01_answer'].append(llm_answer.a01.answer)
        data['a01_confidence'].append(llm_answer.a01.confidence)
        data['a02_answer'].append(llm_answer.a02.answer)
        data['a02_confidence'].append(llm_answer.a02.confidence)
        data['a03_answer'].append(llm_answer.a03.answer)
        data['a03_confidence'].append(llm_answer.a03.confidence)
        data['a04_answer'].append(llm_answer.a04.answer)
        data['a04_confidence'].append(llm_answer.a04.confidence)
        data['a05_answer'].append(llm_answer.a05.answer)
        data['a05_confidence'].append(llm_answer.a05.confidence)
        data['a06_answer'].append(llm_answer.a06.answer)
        data['a06_confidence'].append(llm_answer.a06.confidence)
        data['a07_answer'].append(llm_answer.a07.answer)
        data['a07_confidence'].append(llm_answer.a07.confidence)
        data['a08_answer'].append(llm_answer.a08.answer)
        data['a08_confidence'].append(llm_answer.a08.confidence)
        data['a09_answer'].append(llm_answer.a09.answer)
        data['a09_confidence'].append(llm_answer.a09.confidence)
        data['a10_answer'].append(llm_answer.a10.answer)
        data['a10_confidence'].append(llm_answer.a10.confidence)
        data['a11_answer'].append(llm_answer.a11.answer)
        data['a11_confidence'].append(llm_answer.a11.confidence)

    multiple_records_df = pd.DataFrame({
        'a01_answer': data['a01_answer'],
        'a01_confidence': data['a01_confidence'],
        'a02_answer': data['a02_answer'],
        'a02_confidence': data['a02_confidence'],
        'a03_answer': data['a03_answer'],
        'a03_confidence': data['a03_confidence'],
        'a04_answer': data['a04_answer'],
        'a04_confidence': data['a04_confidence'],
        'a05_answer': data['a05_answer'],
        'a05_confidence': data['a05_confidence'],
        'a06_answer': data['a06_answer'],
        'a06_confidence': data['a06_confidence'],
        'a07_answer': data['a07_answer'],
        'a07_confidence': data['a07_confidence'],
        'a08_answer': data['a08_answer'],
        'a08_confidence': data['a08_confidence'],
        'a09_answer': data['a09_answer'],
        'a09_confidence': data['a09_confidence'],
        'a10_answer': data['a10_answer'],
        'a10_confidence': data['a10_confidence'],
        'a11_answer': data['a11_answer'],
        'a11_confidence': data['a11_confidence'],
    })
    return predict_final_score(multiple_records_df)


def predict_final_score(df):
    model_path = '../packages/ml_model/random_forest_model.pkl'
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)
        # Make sure the features columns order is the same as in the training dataset
        columns = ['a01_answer', 'a01_confidence', 'a02_answer', 'a02_confidence',
                   'a03_answer', 'a03_confidence', 'a04_answer', 'a04_confidence',
                   'a05_answer', 'a05_confidence', 'a06_answer', 'a06_confidence',
                   'a07_answer', 'a07_confidence', 'a08_answer', 'a08_confidence',
                   'a09_answer', 'a09_confidence', 'a10_answer', 'a10_confidence',
                   'a11_answer', 'a11_confidence']
        df = df[columns]

        predictions = loaded_model.predict(df)
        return predictions

@app.get("/review/example")
async def calculate_review_trustworthiness():
    response = model.generate_response(product)
    return response

@app.post("/review")
async def calculate_review_trustworthiness_with_input(input: ReviewsInput):
    response = model.generate_response(input)
    return {"request":input, "response":response}


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
