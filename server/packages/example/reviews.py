from datetime import datetime
from packages.model.input.review import ReviewInput, ReviewsInput


reviews = [
    ReviewInput(
        id=11,
        rating=5,
        author_id=11,
        author_name="User123",
        title="Wonderful product!",
        description="Wonderful, fantastic, and awesome! I love it, love it, love it! Totally worth every penny!",
        published_on=datetime(2024, 10, 26, 14, 0),
        votes=33,
        has_bought_product=True
    ),  # Fails Q06 (extreme emotion) and Q08 (word repetition)

    ReviewInput(
        id=12,
        rating=4,
        author_id=12,
        author_name="NatureLover42",
        title="Great view",
        description="I bought this while I was visiting the mountains and the view was simply breathtaking!",
        published_on=datetime(2024, 10, 25, 11, 30),
        votes=10,
        has_bought_product=True
    ),  # Fails Q02 (focus on scenery)

    ReviewInput(
        id=13,
        rating=2,
        author_id=13,
        author_name="Shopper2024",
        title="Nice product",
        description="Nice, but nothing special. But the mountains are stunning this time of year!",
        published_on=datetime(2024, 10, 24, 12, 45),
        votes=5,
        has_bought_product=False
    ),  # Fails Q02 (focus on scenery) and Q05 (low rating with some positivity)

    ReviewInput(
        id=14,
        rating=1,
        author_id=14,
        author_name="Sam",
        title="Confusing",
        description="I actually found this product a bit confusing. If you’re looking for something like Product X, maybe go with that instead.",
        published_on=datetime(2024, 10, 23, 10, 15),
        votes=17,
        has_bought_product=False
    ),  # Fails Q09 (mentions competitor)

    ReviewInput(
        id=15,
        rating=5,
        author_id=15,
        author_name="Unicorn456",
        title="Great for my travels",
        description="The product worked well, especially while on vacation. Beautiful scenery in the background!",
        published_on=datetime(2024, 10, 22, 15, 25),
        votes=20,
        has_bought_product=True
    ),  # Fails Q02 (scenery focus) and Q07 (generic username)

    ReviewInput(
        id=16,
        rating=3,
        author_id=16,
        author_name="RandomUser",
        title="Okay",
        description="It’s okay.",
        published_on=datetime(2024, 10, 21, 8, 10),
        votes=12,
        has_bought_product=True
    ),  # Fails Q10 (generic review) and Q11 (short length)

    ReviewInput(
        id=17,
        rating=4,
        author_id=17,
        author_name="Traveler2024",
        title="Loved it!",
        description="Loved it! Loved it! Used it every day while on my trip. Definitely a must-have!",
        published_on=datetime(2024, 10, 20, 13, 55),
        votes=9,
        has_bought_product=True
    ),  # Fails Q08 (word repetition)

    ReviewInput(
        id=18,
        rating=5,
        author_id=18,
        author_name="HappyPerson",
        title="Just Amazing",
        description="Amazing amazing amazing amazing product! Cannot say enough good things about it. It’s life-changing!",
        published_on=datetime(2024, 10, 19, 14, 20),
        votes=22,
        has_bought_product=True
    ),  # Fails Q06 (extreme emotion) and Q08 (word repetition)

    ReviewInput(
        id=19,
        rating=1,
        author_id=19,
        author_name="GenericUser",
        title="It’s… okay?",
        description="Honestly, I thought this product would be a lot better. It’s okay. Probably wouldn’t recommend, though it works.",
        published_on=datetime(2024, 10, 18, 12, 30),
        votes=11,
        has_bought_product=False
    ),  # Fails Q05 (low rating but contains some positive text)

    ReviewInput(
        id=20,
        rating=5,
        author_id=20,
        author_name="MysticSeeker",
        title="Beautiful experience!",
        description="An enchanting experience using this with such incredible scenery.",
        published_on=datetime(2024, 10, 17, 9, 40),
        votes=8,
        has_bought_product=True
    ),  # Fails Q02 (focus on scenery)

    ReviewInput(
        id=21,
        rating=2,
        author_id=21,
        author_name="MountainFanatic",
        title="Decent but pricey",
        description="I mean, it's great, but not for this price. Also, the mountain view during my trip was amazing.",
        published_on=datetime(2024, 10, 16, 15, 50),
        votes=6,
        has_bought_product=False
    ),  # Fails Q02 (scenery mention) and Q05 (low rating but positive text)

    ReviewInput(
        id=22,
        rating=5,
        author_id=22,
        author_name="HappyUser",
        title="Perfect product!",
        description="Wow, just wow! This product is life-changing. I can’t even put into words how incredible it is!",
        published_on=datetime(2024, 10, 15, 7, 15),
        votes=26,
        has_bought_product=True
    ),  # Fails Q06 (extreme love emotion)

    ReviewInput(
        id=23,
        rating=3,
        author_id=23,
        author_name="SunnyDay",
        title="It’s okay",
        description="Meh, I guess it works but wouldn’t rave about it.",
        published_on=datetime(2024, 10, 14, 16, 30),
        votes=7,
        has_bought_product=True
    ),  # Fails Q10 (generic text)

    ReviewInput(
        id=24,
        rating=5,
        author_id=24,
        author_name="Echo1",
        title="This is great!",
        description="This product is just like Review #15. Great for my travels, scenery was nice too!",
        published_on=datetime(2024, 10, 13, 10, 5),
        votes=14,
        has_bought_product=True
    ),  # Fails Q01 (too similar to another review)

    ReviewInput(
        id=25,
        rating=1,
        author_id=25,
        author_name="Randy123",
        title="Wouldn’t buy again",
        description="Not the best. But if you like Product Y, you might enjoy it.",
        published_on=datetime(2024, 10, 12, 8, 45),
        votes=3,
        has_bought_product=False
    ),  # Fails Q09 (mentions competitor)

    ReviewInput(
        id=26,
        rating=4,
        author_id=26,
        author_name="Generic",
        title="Good product",
        description="Good product, good quality, worked well. Not much else to say.",
        published_on=datetime(2024, 10, 11, 14, 15),
        votes=20,
        has_bought_product=True
    ),  # Fails Q10 (generic review)

    ReviewInput(
        id=27,
        rating=5,
        author_id=27,
        author_name="BlissfulSoul",
        title="Just magical",
        description="A beautiful addition to my life. This product is absolutely magical and life-altering.",
        published_on=datetime(2024, 10, 10, 9, 20),
        votes=28,
        has_bought_product=True
    ),  # Fails Q06 (extreme emotion)

    ReviewInput(
        id=28,
        rating=3,
        author_id=28,
        author_name="AnonUser",
        title="Good, but too much hype",
        description="It’s fine, but not as amazing as others make it out to be.",
        published_on=datetime(2024, 10, 9, 12, 35),
        votes=19,
        has_bought_product=True
    ),  # Fails Q10 (generic content)

    ReviewInput(
        id=29,
        rating=2,
        author_id=29,
        author_name="NatureFan",
        title="Disappointed with the hype",
        description="Heard it was great, but I just enjoyed the mountain views more.",
        published_on=datetime(2024, 10, 8, 8, 25),
        votes=15,
        has_bought_product=False
    ),  # Fails Q02 (focus on scenery) and Q05 (low rating with positive text)

    ReviewInput(
        id=30,
        rating=1,
        author_id=30,
        author_name="Pat123",
        title="Didn’t work for me",
        description="For what it costs, I expected a lot more. I’d go with Product Z any day over this.",
        published_on=datetime(2024, 10, 7, 15, 5),
        votes=4,
        has_bought_product=False
    )  # Fails Q09 (praises competitor)

]

product = ReviewsInput(
    description="Smartphone XYZ",
    specifications="64GB storage, 6GB RAM, 48MP Camera",
    reviews=reviews
)