from dotenv import load_dotenv
from fastapi import FastAPI
import requests
import time

from packages.model.input.review import ReviewsInput
from packages.model.model import LLMBrillio
from packages.example.reviews import product

load_dotenv()

app = FastAPI()
model = LLMBrillio()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

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


@app.get("/review/example")
async def calculate_review_trustworthiness():
    response = model.generate_response(product)
    return response

@app.get("/review")
async def calculate_review_trustworthiness(input: ReviewsInput):
    response = model.generate_response(input)
    return response

def convert_api_response_to_api_input(response):
    formatted_reviews = []
    for review in response:
        formatted_reviews.append(ReviewsInput.ReviewInput(
            rating=review["rating"],
            author_id=str(review["author_id"]),
            author_name=review["author_name"],
            title=review["title"],
            description=review["description"],
            published_on=review["published_on"]
        ))

    input_data = ReviewsInput(
        description="PlayStation 5 Digital Edition",
        specifications="1TB SSD, D-Chassis",
        reviews=formatted_reviews
    )

    return input_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
