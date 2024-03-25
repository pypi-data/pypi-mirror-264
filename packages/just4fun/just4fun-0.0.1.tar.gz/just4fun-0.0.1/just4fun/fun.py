import random

def magic_8_ball(question_count):
    responses = [
        "It is certain.", "As I see it, yes.", "Reply hazy, try again.", "Don't count on it.",
        "It is decidedly so.", "Most likely.", "Ask again later.", "My reply is no.",
        "Yes, definitely.", "Outlook good.", "Better not tell you now.", "Outlook not so good.",
        "Without a doubt.", "Yes.", "Very doubtful.", "The universe says yes.",
        "Yes – in due time.", "Yes, but don't hold your breath.", "You will have to wait.", "I have my doubts.", "The signs suggest no.",
        "The answer lies within yourself.", "Only time will tell.", "The answer is hidden in plain sight."
    ]
    
    if question_count > 5: 
        return "Phew, I'm tired. Let's take a break!"
    
    if len(question) > 100:
        return "This question is longer than my memory...try something shorter."
    
    return random.choice(responses)

question_count = 0
while True:
    question = input("Ask the Magic 8 Ball a question (or type 'exit' to stop): ")
    if question == 'exit':
        break
    question_count += 1
    print(magic_8_ball(question_count))
