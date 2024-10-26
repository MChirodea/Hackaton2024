from datetime import datetime
from packages.model.input.review import ReviewInput, ReviewsInput


reviews = [
    ReviewInput(
        rating=5,
        author_id="001",
        author_name="Alice",
        title="Great product!",
        description="Loved using it. Highly recommend!",
        published_on=datetime(2024, 10, 25, 14, 30)
    ),
    ReviewInput(
        rating=5,
        author_id="002",
        author_name="Bob",
        title="Great product!",
        description="Loved using it. Highly recommend!",
        published_on=datetime(2024, 10, 24, 11, 45)
    ),  # Q01: Similar review, same rating
    ReviewInput(
        rating=4,
        author_id="003",
        author_name="Traveler42",
        title="Beautiful setting, good product",
        description="The scenery around while using it was fantastic! Helps elevate the entire experience.",
        published_on=datetime(2024, 10, 23, 9, 20)
    ),  # Q02: Focus on setting
    ReviewInput(
        rating=4,
        author_id="004",
        author_name="Diana",
        title="Impresed",
        description="Works as expected!",
        published_on=datetime(2024, 10, 22, 16, 50)
    ),  # Q03: Grammar mistake in title
    ReviewInput(
        rating=3,
        author_id="005",
        author_name="User987",
        title="Interesting buy!",
        description="Bought it because everyone recommended it... so far, so good?",
        published_on=datetime(2024, 10, 21, 10, 15)
    ),  # Q10: Generic review
    ReviewInput(
        rating=1,
        author_id="006",
        author_name="UnhappyCustomer",
        title="Worst ever",
        description="I absolutely hate it. Nothing works as advertised!",
        published_on=datetime(2024, 10, 20, 8, 30)
    ),  # Q06: Extreme hate
    ReviewInput(
        rating=5,
        author_id="007",
        author_name="TravelFan",
        title="Best phone for travel!",
        description="Took it with me across the country, and the phone and camera worked perfectly at every scenic location.",
        published_on=datetime(2024, 10, 19, 17, 45)
    ),  # Q02: Focus on scenery
    ReviewInput(
        rating=2,
        author_id="008",
        author_name="Sammy99",
        title="Could be better",
        description="Honestly, it’s decent, but nothing special. Battery dies fast.",
        published_on=datetime(2024, 10, 18, 12, 30)
    ),  # Q05: Low rating, slightly positive text
    ReviewInput(
        rating=5,
        author_id="009",
        author_name="TechLover",
        title="Best on the market!",
        description="Why buy anything else? This is the BEST phone out there!",
        published_on=datetime(2024, 10, 17, 15, 10)
    ),  # Q06: Extreme love
    ReviewInput(
        rating=1,
        author_id="010",
        author_name="Casey",
        title="Not great",
        description="Was expecting something like the SuperPhone model from Competitor, but this didn’t measure up.",
        published_on=datetime(2024, 10, 16, 19, 20)
    ),  # Q09: Mentions competitor product
    ReviewInput(
        rating=5,
        author_id="011",
        author_name="Chris",
        title="Excellent!",
        description="Fantastic camera, fantastic battery, fantastic performance. Fantastic overall.",
        published_on=datetime(2024, 10, 15, 13, 5)
    ),  # Q08: Overuse of "fantastic"
    ReviewInput(
        rating=4,
        author_id="012",
        author_name="GamerGuy",
        title="Good for gaming",
        description="Handles my mobile games well, doesn’t lag. Battery could last longer, though.",
        published_on=datetime(2024, 10, 14, 11, 30)
    ),  # Q04: About the product
    ReviewInput(
        rating=3,
        author_id="013",
        author_name="AvidConsumer",
        title="Just alright",
        description="Not very different from other phones in this price range.",
        published_on=datetime(2024, 10, 13, 18, 45)
    ),  # Q10: Generic review
    ReviewInput(
        rating=5,
        author_id="014",
        author_name="Shopper1",
        title="Love it so much!",
        description="Best thing I've ever purchased. This product is life-changing!",
        published_on=datetime(2024, 10, 12, 9, 40)
    ),  # Q06: Extreme love
    ReviewInput(
        rating=3,
        author_id="015",
        author_name="PhoneFanatic",
        title="Just okay",
        description="Nothing really stands out. Not bad, but there are better options.",
        published_on=datetime(2024, 10, 11, 14, 25)
    ),  # Q09: Mentions potential for other options
    ReviewInput(
        rating=2,
        author_id="016",
        author_name="Alex",
        title="Mediocre",
        description="It’s a smartphone. Does the usual things, but nothing extraordinary.",
        published_on=datetime(2024, 10, 10, 16, 55)
    ),  # Q10: Generic review
    ReviewInput(
        rating=5,
        author_id="017",
        author_name="CameraLover",
        title="Perfect for photos!",
        description="The camera is unbelievable. Perfect for capturing all my travels.",
        published_on=datetime(2024, 10, 9, 20, 10)
    ),  # Q02: Mentions scenery while traveling
    ReviewInput(
        rating=4,
        author_id="018",
        author_name="Randy",
        title="Nice phone",
        description="Pretty good features overall. I would buy it again.",
        published_on=datetime(2024, 10, 8, 11, 35)
    ),  # Q11: Shorter review
    ReviewInput(
        rating=2,
        author_id="019",
        author_name="TechFanatic",
        title="Didn’t meet expectations",
        description="Great battery life, but really expected better performance.",
        published_on=datetime(2024, 10, 7, 8, 50)
    ),  # Q05: Positive text with a low rating
    ReviewInput(
        rating=4,
        author_id="020",
        author_name="MobileEnthusiast",
        title="Good enough",
        description="This phone is okay, not amazing, but okay. Okay battery, okay screen, okay everything.",
        published_on=datetime(2024, 10, 6, 15, 20)
    )  # Q08: Repeats "okay"
]

product = ReviewsInput(
    description="Smartphone XYZ",
    specifications="64GB storage, 6GB RAM, 48MP Camera",
    reviews=reviews
)