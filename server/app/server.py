from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain_openai import ChatOpenAI
import json
import uvicorn
import requests
import pandas as pd
import time

load_dotenv()

app = FastAPI()
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.put("/send-ext-data")
async def send_data(jsonstring):
    data = json.load(jsonstring)

    # for k, v in data.items():
    #     print(k, v)
    return {"message": data}

def send_data_to_openai(data):
    llm = ChatOpenAI(model="gpt-4o-mini")

@app.get("/emag")
async def emag():
    # Base URL for the API endpoint
    base_url = "https://www.emag.ro/product-feedback/consola-playstation-5-digital-edition-ps5-slim-1tb-ssd-d-chassis-1000040668/pd/D1NVNKYBM/reviews/list"
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
