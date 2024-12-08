import sys
import os

# Add the 'lib' directory to Python's path
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import json
from utils import get_intent, get_session_attributes, get_slots, get_slot_value
from openai_integration import get_question_openai


def format_options(options):
    formatted_options = "\r\n".join(
        [f"{key} {value}" for key, value in options.items()]
    )
    return formatted_options


# Lambda handler using modular functions
def lambda_handler(event, context):
    # Extract intent, session attributes, and slots
    intent_name = get_intent(event)
    session_attributes = get_session_attributes(event)
    slots = get_slots(event)

    # Check if the intent is "AskPracticeQuestions"
    if intent_name == "AskPracticeQuestions":
        # Get the value of the 'Subject' slot
        subject = get_slot_value(event, "Subject")  # Replace with your slot name

        # Call OpenAI API to get SAT practice question
        question, options = get_question_openai(subject)

        # Log the extracted values for debugging
        print(f"Intent Name: {intent_name}")
        print(f"Session Attributes: {json.dumps(session_attributes, indent=2)}")
        print(f"Subject: {subject}")
        print(f"Question: {question}")
        print(f"Options: {json.dumps(options, indent=2)}")

        # Respond with the question and options
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitIntent"  # Keeps the conversation going
                },
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
    else:
        # Handle other intents (default)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitIntent"},
                "intent": {"name": intent_name, "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I didn't understand that. Can you please clarify?",
                }
            ],
        }
