import pytest
from unittest.mock import patch

with patch('builtins.input', return_value='exit'):
    from src import fun

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
    for count in range(1, 6):  # Testing for the first five questions
        response = fun.magic_8_ball(count)
        assert response in valid_responses, f"Response '{response}' was not in the list of known responses."

def test_tired_response():
    # The function returns the "tired" response after 5 questions
    response = fun.magic_8_ball(6) 
    expected_response = "Phew, I'm tired. Let's take a break!"
    assert response == expected_response, f"Expected '{expected_response}', but got '{response}'."