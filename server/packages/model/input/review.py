from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field

class ReviewInput(BaseModel):
    id: int = Field(..., description="ID of the review")
    author_id: Union[int,str,None] = Field(..., description="ID of the author")
    author_name: Optional[str] = Field(..., description="Name of the author")
    title: Optional[str] = Field(..., description="Title of the review")
    description: Optional[str] = Field(..., description="Description of the review")
    rating: Optional[int] = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    votes: Optional[int] = Field(..., ge=0, description="Votes on the review")
    published_on: Optional[datetime] = Field(..., description="Date and time of publishing")
    has_bought_product: Optional[bool] = Field(..., description="True if the review is verified as bought")

    def format_review(self, index: int) -> str:
        return (
            f"Review {index + 1}:\n"
            f"  Rating: {self.rating}/5\n"
            f"  Author ID: {self.author_id}\n"
            f"  Author Name: {self.author_name}\n"
            f"  Title: {self.title}\n"
            f"  Description: {self.description}\n"
            f"  Published On: {self.published_on.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        

class ReviewsInput(BaseModel):
    description: str = Field(..., description="Product description")
    specifications: str = Field(..., description="Product specifications")
    reviews: list[ReviewInput] = Field(..., description="List of reviews for the product")

    def format_reviews(self) -> str:
        result = f"Product Description: {self.description}\nProduct Specifications: {self.specifications}\n\n"
        for i, review in enumerate(self.reviews):
            result += review.format_review(i) + "\n"
        return result

