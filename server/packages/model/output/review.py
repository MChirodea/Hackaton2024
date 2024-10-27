from pydantic import BaseModel, Field


class AnswerResponse(BaseModel):
    """Represents the answer to one of the questions given in the beginning"""
    answer: bool = Field(..., description='The answer to the corresponding question')
    confidence: float = Field(..., description="The model's confidence on the answer given. It's between 0 and 1.")

class ReviewResponse(BaseModel):
    """Represents the trustworthiness score of one review from the context correlated to the id supplied by the user. It's based on multiple answers to the questions and a trustworthiness score given by the model for that review"""
    id: int = Field(..., description="The id of the review found in the context and the id found in the list supplied by the user")
    a01: AnswerResponse = Field(..., description="The answer to question Q01 for the review found in the context by the id")
    a02: AnswerResponse = Field(..., description="The answer to question Q02 for the review found in the context by the id")
    a03: AnswerResponse = Field(..., description="The answer to question Q03 for the review found in the context by the id")
    a04: AnswerResponse = Field(..., description="The answer to question Q04 for the review found in the context by the id")
    a05: AnswerResponse = Field(..., description="The answer to question Q05 for the review found in the context by the id")
    a06: AnswerResponse = Field(..., description="The answer to question Q06 for the review found in the context by the id")
    a07: AnswerResponse = Field(..., description="The answer to question Q07 for the review found in the context by the id")
    a08: AnswerResponse = Field(..., description="The answer to question Q08 for the review found in the context by the id")
    a09: AnswerResponse = Field(..., description="The answer to question Q09 for the review found in the context by the id")
    a10: AnswerResponse = Field(..., description="The answer to question Q10 for the review found in the context by the id")
    a11: AnswerResponse = Field(..., description="The answer to question Q11 for the review found in the context by the id")
    score: float = Field(..., description="The trustworthiness score of the review found in the context by the id. It's between 0 and 1.")
    
class ReviewsResponse(BaseModel):
    """A list with the analysis results for the reviews found in the context with the id's supplied by the user"""
    reviews: list[ReviewResponse]