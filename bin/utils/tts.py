from gtts import gTTS
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import requests
import os

load_dotenv()
WATSON_API_KEY=os.getenv('WATSON_API_KEY')

def tts_dectalk(text, filename="output.mp3"):
    url = 'https://tts.cyzon.us/tts?text='
    url += text
    #This url when doing a get request will return a wav file
    response = requests.get(url)
    filename = "res/" + filename
    with open(filename, 'wb') as f:
        f.write(response.content)


def tts_google(text, filename="output.mp3"):
    """Convert text to speech and save as mp3 file"""
    obj = gTTS(text=text, lang='en', tld='com.au', slow=False)
    filename = "res/" + filename
    obj.save(filename)

def tts_watson(text, filename="output.mp3"):
    url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/3e1ca206-c17b-4799-981f-12fed394264f"

    authenticator = IAMAuthenticator(WATSON_API_KEY)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(url)

    filename = "res/" + filename

    with open(filename,'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(text,voice='en-AU_JackExpressive',accept='audio/mp3').get_result().content)

if __name__ == "__main__":
    tts_dectalk("Hello world", "hello.wav")