HELP_STRING="""Hi! I'm Chattr! I utilize Chat-GPT to respond to you!

I will have a conversation with you if you use `-start` and stop the conversation with `-stop`.
If you reply to someone who isn't me during a conversation, I won't respond, until you ping me.
I will also start a conversation if you ping or reply to me.
I can join a voice channel if you use `-join` and leave the voice channel with `-leave`.

Here are some commands you can use:
`-ask <message>` - Ask a question
`-start` - Start a conversation
`-stop` - Stop a conversation
`-model <model>` - Set the model to use (Currently disabled)
`-get model` - Get the model being used
`-get status` - Get the status of the conversation
`-help` - Show this message
`-join <channel>` - Join a voice channel
`-leave` - Leave the voice channel
`-tts` - Toggle text-to-speech (must be in a voice channel)
`-o <message>` - Omit a message while conversing

Cleared-user commands:
`-image <prompt>` - Generate an image

Admin-only commands:
`-mod - Toggle moderation mode`"""

VALID_MODELS = ['', 'gpt-3.5-turbo', 'gpt-4', 'davinci', 'curie', 'babbage', 'ada']
VALID_COMMAND_HEADERS = [
    '-ask',
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
    '-tts-upgrade',
    '-shutdown',
    '-mod',
    '-o'
]

# Error messages

## Invalid command errors
INVALID_ASK_ERROR = 'Invalid use of `-ask`. Use `-ask <message>`.'
INVALID_MODEL_ERROR = 'Invalid model. Valid models are: \n```' + '\n'.join(VALID_MODELS) + '```'
INVALID_COMMAND_ERROR = 'Invalid command. Use `-help` to see a list of commands.'

## Voice errors
ALREADY_STARTED_ERROR = 'Conversation already started. Use `-stop` to stop a conversation.'
ALREADY_STOPPED_ERROR = 'Conversation already stopped. Use `-start` to start a conversation.'
ALREADY_JOINED_ERROR = 'Already joined a voice channel. Use `-leave` to leave the voice channel.'
NOT_IN_VOICE_ERROR = 'Not in a voice channel. Use `-join` to join a voice channel.'
USER_NOT_IN_VOICE_ERROR = 'User not in a voice channel.'

## Clearance errors
ADMIN_ONLY_ERROR = 'Only server admins can use this command.'
OWNER_ONLY_ERROR = 'Only the owner of this bot can use this command.'
CLEARED_USER_ONLY_ERROR = 'Only cleared users can use this command.'

## Other errors
IMAGE_GENERATE_ERROR = 'Image generation failed.'


# Success messages
JOIN_SERVER_NOTIFY = 'Hey everyone! Im Chattr! Use `-help` to see a list of commands.'

ASK_NOTIFY = 'ASK_NOTIFY:'

START_NOTIFY = 'Starting conversation.'
STOP_NOTIFY = 'Stopping conversation.'

MODEL_SET_NOTIFY = 'Model set to '
MODEL_GET_NOTIFY = 'Model: '

STATUS_GET_NOTIFY = 'Status: '

IMAGE_GENERATE_NOTIFY = 'Generating image...'
IMAGE_GENERATE_SUCCESS = 'Image generated!'

JOIN_NOTIFY = 'Joining voice channel...'
LEAVE_NOTIFY = 'Leaving voice channel...'

PONG_NOTIFY = 'Pong!'

DM_NOTIFY = 'This bot is not meant to be used in DMs. Please use it in a server.'

TTS_ON_NOTIFY = 'TTS is now on.'
TTS_OFF_NOTIFY = 'TTS is now off.'
TTS_UPGRADE_ON_NOTIFY = 'TTS has been upgraded.'
TTS_UPGRADE_OFF_NOTIFY =  'TTS has been downgraded.'

SHUTDOWN_NOTIFY = 'Shutting down...'

MODERATION_ON_NOTIFY = 'Moderation mode is now on.'
MODERATION_OFF_NOTIFY = 'Moderation mode is now off.'
MODERATION_NOTIFY = 'This message is cringe. Im gonna remove it.'

# Other
OWNER_ID = 253296663765057539
CLEARED_USERS = [OWNER_ID]