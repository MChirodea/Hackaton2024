from pydantic import BaseModel, Field


class AnswerResponse(BaseModel):
    """Represents the answer to one of the questions given in the beginning"""
    answer: bool = Field(..., description='The answer to the corresponding question')
    confidence: float = Field(..., description="The model's confidence on the answer given. It's between 0 and 1.")

class ReviewResponse(BaseModel):
    """Represents the trustworthiness score of a review, based on multiple Answers to the questions and a trustworthiness score given by the model for that review"""

    a01: AnswerResponse = Field(..., description="The answer to question Q01")
    a02: AnswerResponse = Field(..., description="The answer to question Q02")
    a03: AnswerResponse = Field(..., description="The answer to question Q03")
    a04: AnswerResponse = Field(..., description="The answer to question Q04")
    a05: AnswerResponse = Field(..., description="The answer to question Q05")
    a06: AnswerResponse = Field(..., description="The answer to question Q06")
    a07: AnswerResponse = Field(..., description="The answer to question Q07")
    a08: AnswerResponse = Field(..., description="The answer to question Q08")
    a09: AnswerResponse = Field(..., description="The answer to question Q09")
    a10: AnswerResponse = Field(..., description="The answer to question Q10")
    a11: AnswerResponse = Field(..., description="The answer to question Q11")
    score: float = Field(..., description="The trustworthiness score of the review . It's between 0 and 1.")
    
class ReviewsResponse(BaseModel):
    """A list with the trustworthiness score of each review sent by the user"""
    reviews: list[ReviewResponse]