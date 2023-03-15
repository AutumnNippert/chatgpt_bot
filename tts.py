from gtts import gTTS
def tts(text, filename="output.mp3"):
    """Convert text to speech and save as mp3 file"""
    obj = gTTS(text=text, lang='en', tld='com.au', slow=False)
    obj.save(filename)