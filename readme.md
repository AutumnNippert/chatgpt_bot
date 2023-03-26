# Chattr
Hi there! I am Chattr, a Discord bot that can participate in deep conversations, provide information on various topics, summarize articles, generate images, and much more.

# [Invite Me](https://discord.com/api/oauth2/authorize?client_id=1085319165650411570&permissions=3147776&scope=bot)

# Usage
To start a conversation with me, you can use the -start command, and to stop the conversation, use -stop. You can also ask me to answer a question with the -ask command, search for information on a topic with -search, consume a URL with -url, or summarize an article with -summarize. If you want me to say something, use -say. To get the latest news, use -news.

If you want me to generate an image, use the -image prompt command. If you want me to join a voice channel, use the -join channel_name command, and to leave it, use -leave. You can also toggle text-to-speech with -tts (must be in a voice channel) and set the service to use with -ttsset.

As an admin, you can use -mod to toggle moderation mode. It lets me delete messages containing invalid URLs or explicit content.

# Commands
```
- -start: Start a conversation with me.
- -stop: Stop the current conversation with me.
- -ask <message>: Ask me a question and I'll do my best to answer it.
- -search <query>: Search for information on a topic in Wikipedia.
- -url <url>: Consume a URL and get information about it.
- -summarize <url>: Summarize an article from the given URL.
- -clear: Clear the conversation history.
- -say <message>: Make me speak out loud what you say.
- -news: Get the latest news from multiple sources.
- -image <prompt>: Generate an image from the prompt message.
- -join <channel>: Make me join a voice channel.
- -leave: Let me leave a voice channel (if I'm in one).
- -tts: Toggle text-to-speech.
- -ttsset <service>: Set a text-to-speech service.
- -mod: Toggle moderation mode.
```
# Bugs

# Setup
Create a `.env` file in the root directory with the following contents:
```
OPENAI_API_KEY=<Your OpenAI API Key>
DISCORD_TOKEN=<Your Bot's Token>
```
Optionally, you can add the following to enable the Watson TTS service:
```
WATSON_API_KEY=<Your Watson API Key>
```

Run setup.sh and this should install everything you need to run the bot (Assuming apt, python3, and pip are installed)

Run start_bot.sh to start the bot

# Requirements
## Python
```
python version >= 3.8
```

## Pip
```
discord.py[voice]
openai
wikipedia
tiktoken
python-dotenv
ibm_watson
gtts
requests
pyTesseract
nltk
numpy
```

## Apt
```
sudo apt-get install ffmpeg
sudo apt-get install tesseract-ocr
```

## run setup_nltk.py for nltk punkt
or run the following in a python shell
```
import nltk
nltk.download('punkt')
```

# Licence
This project is licensed under the MIT License - see the LICENSE file for details