import json
import os
import openai
import re

import openai


# Call openAI APi
def get_chat_completion(prompt: str):
    try:
        # Initialize OpenAI client
        openai.api_key = os.environ["OPENAI_API_KEY"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response
    except Exception as e:
        print(f"Error occurred while fetching chat completion: {e}")
        return None
