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

def generate_response_old(prompt, engine="ada", temperature=0.5, max_tokens=256, n=1, stop='Q:'):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens, # limit because cringe
        n=n,
        temperature=temperature,
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

def requires_search(prompt) -> bool:
    NEEDS_SEARCH_PROMPT = f"""Q: What is the capital of the United States?
    A: True

    Q: When does this new movie come out?
    A: True

    Q: How are you today?
    A: False

    Q: I think that James isn't alive
    A: False

    Q: You are wrong
    A: False
    
    Q: {prompt}
    A: """
    print(openai.Completion.create(model='davinci', prompt=NEEDS_SEARCH_PROMPT, stop="\n", temperature=0))

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
    print(requires_search('When did george washington die?'))