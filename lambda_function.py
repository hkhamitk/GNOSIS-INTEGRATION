import sys
import os

# Add the 'lib' directory to Python's path
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import json
from utils import get_intent, get_session_attributes, get_slots
from ask_practice_questions import handle_ask_practice_questions


# Lambda handler using modular functions
def lambda_handler(event, context):
    # Extract intent, session attributes, and slots
    intent_name = get_intent(event)
    session_attributes = get_session_attributes(event)
    slots = get_slots(event)

    # Check if the intent is "AskPracticeQuestions"
    if intent_name == "AskPracticeQuestions":
        return handle_ask_practice_questions(intent_name, event, session_attributes)
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
