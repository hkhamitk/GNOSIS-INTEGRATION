import json
import os
from openai import OpenAI


def lambda_handler(event, context):
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        # Parse the incoming event body
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        clea
        if not user_message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No message provided"}),
            }

        # Create chat completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150,
            temperature=0.7,
        )

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": assistant_response}),
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
