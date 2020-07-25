import random

quotes = [
    "It does not matter how slowly you go as long as you do not stop — Confucius",
    "My recovery must com first so that everything I love in life does not come last",
    "Recovery is about progression, not perfection",
    "If you find yourself in a hole, the first thing to do is stop digging",
    "It’s gonna get harder before it gets easier. But it will get better, you just gotta make it through the hard stuff first",
    "Recovery is not for people who need it, it’s for people who want it",
    "You were never created to live depressed, defeated, guilty, condemned, ashamed or unworthy. You were created to be victorious",
    "The best time to plant a tree was 20 years ago. The second best time is now",
    "Believe you can and you’re halfway there — Theodore Roosevelt",
    "It’s no good to be unhappy about the things you can’t change, but also no good to be unhappy about the things you can",
    "You might not be able to change the world, but you can change your corner of it",
    "The greatest gifts you’ll ever open are your eyes and your heart",
    "People often say that motivation doesn’t last. Neither does bathing. That’s why we recommend it daily",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us — Ralph Waldo Emerson",
    "Success is the sum of small efforts, repeated day in and day out — Robert Collier",
    "Our greatest glory is not in never failing, but in rising up every time we fail — Ralph Waldo Emerson",
    "Rock bottom can be the foundation on which you rebuild your life — J.K. Rowling"
]

def random_quote():
    quote = random.choice(quotes)

    if " — " in quote:
        p1, p2 = quote.split(" — ")
        quote = f"“{p1}” — {p2}"

    return quote
