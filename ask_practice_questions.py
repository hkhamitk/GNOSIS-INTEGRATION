import json
import os
import re
from openai_integration import get_chat_completion
from utils import get_slot_value


# Format question opetions
def format_options(options):
    formatted_options = "\n".join([f"{key} {value}" for key, value in options.items()])
    return formatted_options


# Ask a question to openAI
def get_question_openai(subject):
    try:
        prompt = f"Generate an SAT practice question for the subject: {subject}. Provide 4 answer options in the format A), B), C), D)."

        # Create chat completion
        response = get_chat_completion(prompt)

        # Extract the assistant's response
        assistant_response = response["choices"][0]["message"]["content"]

        # Use regular expressions to split the question and options
        # Assuming the format is: Question\nA) Option1\nB) Option2\nC) Option3\nD) Option4
        question_match = re.match(r"(.*?)(?=\n[A-D]\))", assistant_response, re.DOTALL)
        options_match = re.findall(r"([A-D]\))\s*(.*)", assistant_response)

        if question_match:
            question = question_match.group(0).strip()
        else:
            question = "No question found"

        options = {option[0]: option[1] for option in options_match}

        # Return the question and options in a simplified format
        return question, options

    except Exception as e:
        return json.dumps({"error": str(e)})


import json


# Handle AskPracticeQuestion intent
def handle_ask_practice_questions(intent_name, event, session_attributes):
    """
    Handles the 'AskPracticeQuestions' intent, extracts the subject, calls OpenAI to get a question,
    and formats the response.

    Args:
    - intent_name (str): The name of the intent.
    - event (dict): The event object containing slot values.
    - session_attributes (dict): The current session attributes.

    Returns:
    - dict: The formatted response to send back.
    """
    # Extract the subject from the event slots
    subject = get_slot_value(event, "Subject")

    # Call OpenAI API to get SAT practice question
    question, options = get_question_openai(subject)

    # Log the extracted values for debugging
    print(f"Intent Name: {intent_name}")
    print(f"Session Attributes: {json.dumps(session_attributes, indent=2)}")
    print(f"Subject: {subject}")
    print(f"Question: {question}")
    print(f"Options: {json.dumps(options, indent=2)}")

    # Format the response with the question and options
    response = {
        "sessionState": {
            "dialogAction": {"type": "ElicitIntent"},  # Keeps the conversation going
            "intent": {
                "name": intent_name,
                "state": "InProgress",  # Marks the intent as in progress
            },
            "sessionAttributes": session_attributes,  # Retain session attributes
        },
        "messages": [
            {
                "contentType": "PlainText",  # Response type (PlainText)
                "content": f"Here is your question for {subject}:\n\n{question}\n\nOptions:\n\n"
                + f"\n{format_options(options)}",
            }
        ],
    }

    # Log the response for debugging
    print(f"Lambda Response: {json.dumps(response, indent=2)}")

    return response
