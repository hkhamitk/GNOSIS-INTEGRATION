import json
import os
import openai
import re


def get_question_openai(subject):
    try:
        # Initialize OpenAI client
        openai.api_key = os.environ["OPENAI_API_KEY"]
        prompt = f"Generate an SAT practice question for the subject: {subject}. Provide 4 answer options in the format A), B), C), D)."

        # Create chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )

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
