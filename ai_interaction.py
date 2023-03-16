import openai
import os
from dotenv import load_dotenv

# Set your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def convert_audio_to_text(audio_file_path) -> str:
    audio_file= open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def generate_response_old(prompt, engine="ada"):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=256, # limit because cringe
        n=1,
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
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(e)

def needs_moderation(message) -> bool:
    if 'dumbass' in message: # fun little ee
        return True
    response = openai.Moderation.create(
        model="text-moderation-stable",
        input=message
    )
    return response['results'][0]['flagged']

# Define function to run the chatbot

def query(prompt):
    return generate_response(prompt)

def query_image(prompt):
    return generate_image(prompt)

def query_old(prompt, engine="ada"):
    return generate_response_old(prompt, engine)

def test_audio():
    print(convert_audio_to_text("test_files/hungry.wav"))

def test_moderation():
    print(needs_moderation('kill yourself'))

if __name__ == "__main__":
    test_moderation()