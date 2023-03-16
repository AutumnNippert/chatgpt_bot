from gtts import gTTS
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import os

load_dotenv()
WATSON_API_KEY=os.getenv('WATSON_API_KEY')

def tts(text, filename="output.mp3"):
    """Convert text to speech and save as mp3 file"""
    obj = gTTS(text=text, lang='en', tld='com.au', slow=False)
    obj.save(filename)

def tts_watson(text, filename="output.mp3"):
    url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/3e1ca206-c17b-4799-981f-12fed394264f"

    authenticator = IAMAuthenticator(WATSON_API_KEY)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(url)

    with open(filename,'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(text,voice='en-AU_JackExpressive',accept='audio/mp3').get_result().content)

if __name__ == "__main__":
    tts_watson("""Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.""", "tmp/temp.mp3")