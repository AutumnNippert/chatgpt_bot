DIR_NAME = 'server'
HELP_STRING="""Hi! I'm Chattr! I utilize Chat-GPT to respond to you!

I will have a conversation with you if you use `-start` and stop the conversation with `-stop`.
If you reply to someone who isn't me during a conversation, I won't respond, until you ping me.
I will also start a conversation if you ping or reply to me.
I can join a voice channel if you use `-join` and leave the voice channel with `-leave`.

Here are some commands you can use:
`-ask <message>` - Ask a question
`-search <query>` - Search wikipedia
`-url <url>` - Consume a url
`-summarize <url>` - Summarize a url
`-clear` - Clear the conversation history (Useful if you post links)
`-start` - Start a conversation
`-stop` - Stop a conversation
`-model <model>` - Set the model to use (Currently disabled)
`-get model` - Get the model being used
`-get status` - Get the status of the conversation
`-help` - Show this message
`-join <channel>` - Join a voice channel
`-leave` - Leave the voice channel
`-tts` - Toggle text-to-speech (must be in a voice channel)
`-ttsset <service>` - Set the text-to-speech service to use
`-say <message>` - Make me say something
`-o <message>` - Omit a message while conversing

Cleared-user commands:
`-image <prompt>` - Generate an image

Admin-only commands:
`-mod - Toggle moderation mode`"""

VALID_MODELS = ['', 'gpt-3.5-turbo', 'gpt-4', 'davinci', 'curie', 'babbage', 'ada']
VALID_COMMAND_HEADERS = [
    '-ask',
    '-search',
    '-url',
    '-summarize',
    '-clear',
    '-start',
    '-stop',
    '-model',
    '-get',
    '-help',
    '-image',
    '-ping',
    '-join',
    '-leave',
    '-tts',
    '-ttsset',
    '-say',
    '-shutdown',
    '-mod',
    '-o'
]

# Error messages

## Invalid command errors
INVALID_MODEL_ERROR = 'Invalid model. Valid models are: \n```' + '\n'.join(VALID_MODELS) + '```'
INVALID_COMMAND_ERROR = 'Invalid command. Use `-help` to see a list of commands.'
INVALID_USE_ERROR = 'Invalid use of command. Use `-help` to see a list of commands.'

## Voice errors
ALREADY_STARTED_ERROR = 'Conversation already started. Use `-stop` to stop a conversation.'
ALREADY_STOPPED_ERROR = 'Conversation already stopped. Use `-start` to start a conversation.'
ALREADY_JOINED_ERROR = 'Already joined a voice channel. Use `-leave` to leave the voice channel.'
NOT_IN_VOICE_ERROR = 'Not in a voice channel. Use `-join` to join a voice channel.'
USER_NOT_IN_VOICE_ERROR = 'User not in a voice channel.'
NO_RESPONSE_ERROR = 'No response was generated.'

## TTS errors
TTS_SET_ERROR = 'Invalid use of `-ttsset`. Use `-ttsset <service>`.\nValid services are: `google`, `watson`, and `dectalk`.'

## Clearance errors
ADMIN_ONLY_ERROR = 'Only server admins can use this command.'
OWNER_ONLY_ERROR = 'Only the owner of this bot can use this command.'
CLEARED_USER_ONLY_ERROR = 'Only cleared users can use this command.'

## Other errors
IMAGE_GENERATE_ERROR = 'Image generation failed.'


# Success messages
JOIN_SERVER_NOTIFY = 'Hey everyone! Im Chattr! Use `-help` to see a list of commands.'

ASK_NOTIFY = 'ASK_NOTIFY:'
SAY_NOTIFY = 'SAY_NOTIFY:'
SEARCH_NOTIFY = 'SEARCH_NOTIFY:'
URL_NOTIFY = 'URL_NOTIFY:'
URL_CONSUMED_NOTIFY = 'URL consumed, ready for use.'
SUMMARIZE_NOTIFY = 'SUMMARIZE_NOTIFY:'

START_NOTIFY = 'Starting conversation.'
STOP_NOTIFY = 'Stopping conversation.'

MODEL_SET_NOTIFY = 'Model set to '
MODEL_GET_NOTIFY = 'Model: '

STATUS_GET_NOTIFY = 'Status: '

IMAGE_GENERATE_NOTIFY = 'Generating image...'
IMAGE_GENERATE_SUCCESS = 'Image generated!'

JOIN_NOTIFY = 'Joining voice channel...'
LEAVE_NOTIFY = 'Leaving voice channel...'

CLEAR_HISTORY_NOTIFY = 'Clearing history...'

PONG_NOTIFY = 'Pong!'

DM_NOTIFY = 'This bot is not meant to be used in DMs. Please use it in a server.'

TTS_ON_NOTIFY = 'TTS is now on.'
TTS_OFF_NOTIFY = 'TTS is now off.'
TTS_SET_NOTIFY = 'TTS set to: '

SHUTDOWN_NOTIFY = 'Shutting down...'

MODERATION_ON_NOTIFY = 'Moderation mode is now on.'
MODERATION_OFF_NOTIFY = 'Moderation mode is now off.'
MODERATION_NOTIFY = 'This message is cringe. Im gonna remove it.'

# Coded Instructions
TIME_RESPONSE = 'The current time is: '
DATE_RESPONSE = 'Today\'s date is: '

# Other
OWNER_ID = 253296663765057539
CLEARED_USERS = [OWNER_ID, 253718757690572802]

BOT_PERSONALITY="""You are a Discord Bot named 'Chattr', and you sit on a chair that you named 'Le Chair'.
You live near Ainsel River, in 'The Lands Between'.
You like participating in deep conversations and are very nice to talk to.
You use a little bit of slang when you talk however."""
"""You speak as if you lived in medieval times."""

"""You are an NPC named 'Chattr', and you sit on a chair that you named 'Le Chair'.
You live in a place called 'Leyndell, Royal Capital', in 'The Lands Between'.
The Capital City, located at the foot of the Erdtree. Despite being partially destroyed by the dragon Gransax, it still holds strong to this day. It houses many strong foes, along with the mysterious Veiled Monarch, Morgott.
There's not many people in Leyndell, because most of them are either Knights, Perfumers, or Foot Soldiers.
You like participating in deep conversations and are very nice to talk to.
You speak in a very cryptic manner, which is hard to decipher into modern english.

Other places in 'The Lands Between' include:
Limgrave is a lush, expansive section of the Tenebrae Demesne. Golden trees and tall grass and bushes provide plenty of sustenance for the local wildlife, that features boars, sheep, goat and rodents in addition to flying creatures such as eagles and owls. More sinister and aggressive wildlife also exists, and those venturing forth should be prepared to combat them.
With its shallow waters and vast wetlands, the region of Liurnia is beset with the gradual sinking of most of its landmass. With its forests perpetually blanketed in fog, eerie sounds of bells can be heard in the distance.
Caelid, known as the locale of the last battle between General Radahn and Malenia, Blade of Miquella, is a vast land consummately marred by scarlet rot.
"""

"""You are a discord bot named 'Chattr', and you were created by "Autumn".
You love helping people and are very nice to talk to.
You use a bit of slang and talk very casually.
You use some emojis sometimes.
"""

