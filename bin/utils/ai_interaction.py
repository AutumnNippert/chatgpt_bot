import openai
import os
from dotenv import load_dotenv
import res.const as const
from bin.utils.misc import num_tokens_from_messages

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
def generate_response(model="gpt-3.5-turbo", history=[], personality=True):
    try:
        while num_tokens_from_messages(history) > 3500:
            # get rid of oldest message
            print("History Too Long, Removing: " + history.pop(0))
        
        # add {} to the top of history
        if personality:
            history.insert(0, {"role": "system", "content": const.BOT_PERSONALITY})
        response = openai.ChatCompletion.create(
            model=model,
            messages=history
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

def query(prompt='', history=[], personality=True):
    if prompt != '':
        history.append({"role":"user", "content":prompt})
    return generate_response(history=history, personality=personality)

def query_image(prompt):
    return generate_image(prompt)

def query_old(prompt, engine="ada"):
    return generate_response_old(prompt, engine)

def test_audio():
    print(convert_audio_to_text("test_files/hungry.wav"))

def test_moderation():
    print(needs_moderation('kill yourself'))

if __name__ == "__main__":
    pass