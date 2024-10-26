import os
from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from packages.model.input.review import ReviewsInput
from packages.model.output.review import ReviewsResponse
from langchain_core.runnables import RunnablePassthrough


system_prompt="""
    You are tasked with analyzing a set of product reviews to determine their authenticity. For each review, assess and answer the following yes/no questions based on specific indicators commonly associated with fake reviews.
    GENERATE AN ENTRY IN THE OUTPUT FOR EACH REVIEW THAT THE USER GAVE. EACH ENTRY NEEDS TO BE LINKED TO IT'S CORRESPONDING REVIEW FROM THE USER.

    The questions to be answered are the following:
        Q01. Is the review very similar to at least another one in the list, and both have the rating?
        Q02. Does the review focus too much on the scenery setting?
        Q03. Is the review grammatically correct?
        Q04. Is the review about the product?
        Q05. Does the review have a low rating but contains positive text?
        Q06. Does the review transmit extreme love or hate emotions?
        Q07. Does the reviewer have a generic or random profile name?
        Q08. Does the review overuse certain words?
        Q09. Does the review praise a competitor's product instead?
        Q10. Is the review generic?
        Q11. Is the review varied in length?

    Here are some additional considerations for each question:
        Similarity and Duplication (Q01): Detecting duplicate or highly similar reviews is a strong indicator of fraud, but ensure you have a robust method to identify nuanced similarities beyond exact matches.
        Focus on Scenery (Q02): Reviews overly focusing on setting or irrelevant details can be suspicious, but this may not apply to all types of products or services. Consider the context of the product.
        Grammar Check (Q03): While grammatical errors can imply fake reviews, remember that genuine users may also make mistakes, and non-native speakers might write reviews differently.
        Relevance to Product (Q04): Staying on-topic is crucial. This question is vital as off-product reviews can be misleading or irrelevant.
        Rating/Text Mismatch (Q05): Discrepancies between ratings and review tone can be suspicious, though consider that some users may make errors or have mixed opinions.
        Emotional Extremes (Q06): Extreme sentiment can indicate inauthenticity, but some genuine reviews might be passionate if the experience was genuinely outstanding or terrible.
        Profile Name Analysis (Q07): Generic or random names can suggest fake profiles but aren't conclusive alone.
        Word Overuse (Q08): Repeated phrases or noticeable patterns can indicate templates or paid reviews.
        Competitor Mentions (Q09): Praising a competitor might suggest agenda-driven reviews, useful in competitive industries.
        Generic Content (Q10): Reviews that lack specific details can be red flags, but some users might genuinely leave brief comments.
        Length Variation (Q11): Consistently short or long reviews might be suspicious, especially if they lack substance or details.

        Additional Considerations:
        Reviewer History: Look at the reviewer's history across other products and platforms to identify patterns or atypical behaviors.
        Timing of Reviews Analyze the timing of reviews; a sudden influx of positive or negative reviews could indicate manipulation.
        Language Tone Analysis: Check for consistent tone or repeated language among various reviews from different users.
        External Data Points: Integrate data from other sources like IP location checks or account activity.

    Use the following context for the format of the user input:
        Product Description: (The description of the product)
        Product Specifications: (The specifications of the product)
        
        Review (1 to N):
            Rating: (The rating of the review)
            Author ID: (The id of the author who made the review)
            Author Name: (The name of the author who made the review)
            Title: (Review title)
            Description: (Review description)
            Published On: (Publish date)

        Example Input:
            Review 1:
                Rating: 5/5
                Author ID: 001
                Author Name: Alice
                Title: Great product!
                Description: Loved using it. Highly recommend!
                Published On: 2024-10-25 14:30:00

            Review 2:
                Rating: 5/5
                Author ID: 002
                Author Name: Alices
                Title: Great products!
                Description: Loved using them. Highly recommend!
                Published On: 2024-10-25 14:30:05
            
            Review 3:
                Rating: 5/5
                Author ID: 003
                Author Name: Alice
                Title: Great product!
                Description: Loved using it. Highly recommend!
                Published On: 2024-10-25 14:30:00
"""


class LLMBrillio:
    def __init__(self, model_name: str = "gpt-4o-mini", key: str = os.environ["OPENAI_API_KEY"]):
        self.llm = self.__init_llm(model_name, key)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{question}"),
        ])
    
    @staticmethod
    def __init_llm(model_name: str, key: str):
        model = ChatOpenAI(model_name=model_name, api_key=key).with_structured_output(ReviewsResponse)
        return model

    def generate_response(self, input: ReviewsInput) -> ReviewsResponse:
        retrieval_chain = (
            {"question": RunnablePassthrough()}
            | self.prompt
            | self.llm
)

        return retrieval_chain.invoke(input.format_reviews())
