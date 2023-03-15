import openai
import os
from dotenv import load_dotenv

# Set your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function to generate response
def generate_response(prompt, model_engine="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}]
        )
        response = response["choices"][0]["message"]["content"]
        return response
    except Exception as e:
        return "Im having some issues:\n```" + str(e) + "```"

# Define function to run the chatbot
def query(prompt, model_engine="gpt-3.5-turbo"):
    return generate_response(prompt, model_engine)

if __name__ == "__main__":
    print(query("Hello, how are you?"))