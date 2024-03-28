import pytest
from unittest.mock import patch

with patch('builtins.input', return_value='exit'):
    from src.just4fun import fun

# For 8 Ball Functions
    
def test_response_for_valid_input():
    # Magic_8_ball returns a known response for valid inputs.
    valid_responses = [
        "It is certain.", "As I see it, yes.", "Reply hazy, try again.", "Don't count on it.",
        "It is decidedly so.", "Most likely.", "Ask again later.", "My reply is no.",
        "Yes, definitely.", "Outlook good.", "Better not tell you now.", "Outlook not so good.",
        "Without a doubt.", "Yes.", "Very doubtful.", "The universe says yes.",
        "Yes – in due time.", "Yes, but don't hold your breath.", "You will have to wait.", "I have my doubts.", "The signs suggest no.",
        "The answer lies within yourself.", "Only time will tell.", "The answer is hidden in plain sight."
    ]

    question = "How's it going?"
    for count in range(1, 5):  # Testing for the first four questions
        response = fun.magic_8_ball(question, count)
        assert response in valid_responses, f"Response '{response}' was not in the list of known responses."

def test_tired_response():
    # The function returns the "tired" response at 5 questions
    question = "How's it going?"
    response = fun.magic_8_ball(question, 5) 
    expected_response = "Phew, I'm tired. Let's take a break!"
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'."
    
def test_long_question_response():
    # The function returns the "too long" response when the question has longer than 100 characters.
    question = 'a' * 101
    print(question)
    response = fun.magic_8_ball(question, 1) 
    expected_response = "This question is longer than my memory...try something shorter."
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'."
    
def test_sixth_question_valid_response():
    # The function returns of the 6th response.
    valid_responses = [
        "It is certain.", "As I see it, yes.", "Reply hazy, try again.", "Don't count on it.",
        "It is decidedly so.", "Most likely.", "Ask again later.", "My reply is no.",
        "Yes, definitely.", "Outlook good.", "Better not tell you now.", "Outlook not so good.",
        "Without a doubt.", "Yes.", "Very doubtful.", "The universe says yes.",
        "Yes – in due time.", "Yes, but don't hold your breath.", "You will have to wait.", "I have my doubts.", "The signs suggest no.",
        "The answer lies within yourself.", "Only time will tell.", "The answer is hidden in plain sight."
    ]
    question = "How's it going?"
    response = fun.magic_8_ball(question, 6)  # The 6th question
    assert response in valid_responses, f"Response '{response}' was not in the list of known responses."

def test_affirmation_for_happy_mood():
    happy_responses = [
        "Your joy is contagious.",
        "Happiness looks gorgeous on you.",
        "Continue to shine as you always do."
    ]
    response = fun.affirmations("happy")
    assert response in happy_responses, f"Response '{response}' was not in the list of happy affirmations."

def test_affirmation_for_sad_mood():
    sad_responses = [
        "It's okay to feel sad, growth comes from discomfort.",
        "This is temporary; your strength is permanent.",
        "You are more resilient than you realize."
    ]
    response = fun.affirmations("sad")
    assert response in sad_responses, f"Response '{response}' was not in the list of sad affirmations."

def test_affirmation_for_unrecognized_mood():
    response = fun.affirmations("angry")  # Example of an unrecognized mood
    expected_response = "Mood not recognized. Please enter 'happy' or 'sad'."
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'."


def test_text_copypasta():
    valid_text_copypastas = [
        """I like to creep around my home and act like a goblin. I don’t know why but I just enjoy doing this. Maybe it’s my way of dealing with stress or something but I just do it about once every week. Generally I’ll carry around a sack and creep around in a sort of crouch-walking position making goblin noises, then I’ll walk around my house and pick up various different “trinkets” and put them in my bag while saying stuff like “I’ll be having that” and laughing maniacally in my goblin voice (“trinkets” can include anything from shit I find on the ground to cutlery or other utensils). The other day I was talking with my neighbours and they mentioned hearing weird noises like what I wrote about and I was just internally screaming the entire conversation. I’m 99% sure they don’t know it’s me but god that 1% chance is seriously weighing on my mind.""",
        """Imagine a world where your code never bugs and every function call returns the expected result. 🌈 In this utopia, null pointers are mythical creatures, and segfaults are just stories we tell to scare junior developers. 🎃 Here, every loop terminates, every exception is caught, and variables name themselves in a self-documenting symphony of clarity. 🎶 In this realm, your favorite snack is always within reach, and coffee refills itself, perpetually warm. ☕ Welcome to Devtopia, the land where debugging is a hobby, not a necessity, and your IDE writes half your code, whispering sweet nothings of optimization as you sleep. 💻🛌 Remember, in Devtopia, the only infinite loop is the one that leads to endless creativity. 🌀 Let's code happily ever after. 🚀""",
        """Don't even ask the question. The answer is yes, it's priced in. Think Amazon will beat the next earnings? That's already been priced in. You work at the drive thru for Mickey D's and found out that the burgers are made of human meat? Priced in. You think insiders don't already know that? The market is an all powerful, all encompassing being that knows the very inner workings of your subconscious before you were even born. Your very existence was priced in decades ago when the market was valuing Standard Oil's expected future earnings based on population growth that would lead to your birth, what age you would get a car, how many times you would drive your car every week, how many times you take the bus/train, etc. Anything you can think of has already been priced in, even the things you aren't thinking of. You have no original thoughts. Your consciousness is just an illusion, a product of the omniscent market. Free will is a myth. The market sees all, knows all and will be there from the beginning of time until the end of the universe (the market has already priced in the heat death of the universe). So please, before you make a post on wsb asking whether AAPL has priced in earpods 11 sales or whatever, know that it has already been priced in and don't ask such a dumb fucking question again.""",
        """You are my sunshine. Boy oh boy where do I even begin. Lebron... honey, my pookie bear. I have loved you ever since I first laid eyes on you. The way you drive into the paint and strike fear into your enemies eyes. Your silky smooth touch around the rim, and that gorgeous jumpshot. I would do anything for you. I wish it were possible to freeze time so I would never have to watch you retire. You had a rough childhood, but you never gave up hope. You are even amazing off the court, you're a great husband and father, sometimes I even call you dad. I forvever dread and weep, thinking of the day you will one day retire. I would give you my newborn it were the only thing that could put a smile on your beautiful face. You have given me so much joy, and heartbreak over the years. I remember when you first left cleveland and its like my heart got broken into a million pieces. But a tear still fell from my right eye when I watched you win your first ring in miami, because deep down, my glorious king deserved it. I just wanted you to return home. Then allas, you did, my sweet baby boy came home and I rejoiced. 2015 was a hard year for us baby, but in 2016 you made history happen. You came back from 3-1 and I couldn't believe it. I was crying, bawling even, and I heard my glorious king exclaim these words, "CLEVELAND, THIS IS FOR YOU!" Not only have you changed the game of basketball and the world forever, but you've eternally changed my world. And now you're getting older, but still the goat, my goat. I love you pookie bear, my glorious king, Lebron""",
        """I have an unhealthy addiction to problem sets. So the other day at school (specifically, Biology class), we got assigned a gel electrophoresis problem set. I was initially indifferent, but as I worked through the problems, I realized that the arc and satisfaction of problem-solving transcended the excitement that any sexual encounter could bring. I'll admit, I got a little too excited and I did some things I'm not proud of. But it didn't stop there. It was like a switch had been flipped within me; I just couldn't resist the (borderline sexual) urge to complete problem sets. My lust for problem sets has driven me to worrying extremes, and now I'm seeking out online PSETs as well. I'm afraid that my newfound addiction will deteriorate my study habits and social connections. What should I do??"""        
    ]
    response = fun.copypasta("text")
    assert response in valid_text_copypastas, f"Response '{response}' was not in the list of valid text copypastas."

def test_image_copypasta():
    valid_image_copypastas = [
        "Sample Text",
        "👉🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👇🏿👈🏿\n👉🏿👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👇🏾👈🏿\n👉🏿👉🏾👇🏽👇🏽👇🏽👇🏽👇🏽👇🏽👇🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👇🏼👇🏼👇🏼👇🏼👇🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👉🏼👇🏻👇🏻👇🏻👈🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👉🏼👉🏻 ඞ 👈🏻👈🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👉🏼👆🏻👆🏻👆🏻👈🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👉🏽👆🏼👆🏼👆🏼👆🏼👆🏼👈🏽👈🏾👈🏿\n👉🏿👉🏾👆🏽👆🏽👆🏽👆🏽👆🏽👆🏽👆🏽👈🏾👈🏿\n👉🏿👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👆🏾👈🏿\n👉🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👆🏿👈🏿\n",
        """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣤⣤⣄⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠖⠊⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠲⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡤⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢢⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⡀⠈⠀⡀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠘⡆⡜⠁⠀⠀⠀⠀⢧⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠀⣀⣤⡂⠀⠇⠱⠀⡀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠈⢄⡀⢠⣟⢭⣥⣤⠽⡆⠀⡶⣊⣉⣲⣤⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⡀⠀⠐⠂⠘⠄⣈⣙⡡⡴⠀⠀⠙⣄⠙⣛⠜⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⢦⡀⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⠄⠊⠀⠀⠀⠀⡸⠛⠀⠀⠀⢸⠆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠦⢄⣘⣄⠀⠀⠀⠀⠀⠀⠀⡠⠀⠀⠀⠀⣇⡀⠀⠀⣠⠎⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠈⡟⠒⠲⣄⠀⠀⡰⠇⠖⢄⠀⠀⡹⡇⢀⠎⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⡇⠀⠀⠹⠀⡞⠀⠀⢀⠤⣍⠭⡀⢱⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⠞⠀⠀⢠⡇⠀⠀⠀⠀⠁⠀⢴⠥⠤⠦⠦⡼⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣀⣤⣴⣶⣿⣿⡟⠁⠀⠋⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⠀⠑⣠⢤⠐⠁⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠬⠥⣄⠀⠀⠈⠲⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⠀⠀⢀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠒⠦⠤⢤⣄⣀⣠⠤⢿⣶⣶⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠁⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣀⣀⣀⣀⣀⣀⣀⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀""",
        """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀
⠀⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀
⠀⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⠀
⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀
⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇⠀⠀
⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀
⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀
⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀
⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀
⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀
⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⠀⢠⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""",
        """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀⠀
⠀⠀⠀⣴⠿⠏⠀⠀⠀⠀⠀⠀⢳⡀⠀⡏⠀⠀⠀⠀⠀⢷
⠀⠀⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀⠀⠀ ⡇
⠀⠀⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿⠀⣸⠀⠀OK⠀ ⡇
⠀⠀⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀⣿⠀⢹⠀⠀⠀⠀⠀ ⡇
⠀⠀⠙⢿⣯⠄⠀⠀⠀⢀⡀⠀⠀⡿⠀⠀⡇⠀⠀⠀⠀⡼
⠀⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀⠀⠘⠤⣄⣠⠞⠀
⠀⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀⠀⠀⠀⠀⠀
⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿⠀⠀⠀⠀⠀⠀
⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀⠀⣄⢸⠀⠀⠀⠀⠀⠀
⣿⣿⣧⣀⣿.........⣀⣰⣏⣘⣆⣀⠀⠀"""
    ]
    response = fun.copypasta("image")
    assert response in valid_image_copypastas, f"Response '{response}' was not in the list of valid image copypastas."

def test_invalid_input_copypasta():
    invalid_response = ["Invalid Type."]
    response = fun.copypasta("googoogaga")
    assert response in invalid_response, f"Response '{response}' was not a valid response to an invalid input."

def test_fun_fact():
    valid_fun_facts = [
        "Octopuses have three hearts.",
        "Butterflies can taste with their feet.",
        "The inventor of the frisbee was turned into a frisbee after he died.",
        "Honey never spoils."
    ]
    response = fun.make_me_laugh("fun fact")
    assert response in valid_fun_facts, f"Response '{response}' was not in the list of valid fun facts."

    
def test_joke():
    
    valid_jokes = [
        "Why don't scientists trust atoms? Because they make up everything.",
        "What do you call fake spaghetti? An impasta.",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
        "What's orange and sounds like a parrot? A carrot."
    ]
    response = fun.make_me_laugh("joke")
    assert response in valid_jokes, f"Response '{response}' was not in the list of valid jokes."

def test_invalid_choice_laugh():
        invalid_response = ["Please choose either 'fun fact' or 'joke'."]
        response = fun.make_me_laugh("quack")
        assert response in invalid_response, f"Response '{response}' was not a valid response to an invalid input."

    
