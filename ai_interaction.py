import openai
import os
from dotenv import load_dotenv

# Set your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response_old(prompt, engine="ada"):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

# Define function to generate response
def generate_response(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        response = response["choices"][0]["message"]["content"]
        return response
    except Exception as e:
        return "Im having some issues:\n```" + str(e) + "```"
    
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

# Define function to run the chatbot
def query(prompt):
    return generate_response(prompt)

def query_image(prompt):
    return generate_image(prompt)

def query_old(prompt, engine="ada"):
    return generate_response_old(prompt, engine)


if __name__ == "__main__":
    print(query("Hello, how are you?"))