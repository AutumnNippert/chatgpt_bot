HELP_STRING="""Hi! I'm Chattr! I utilize Chat-GPT to respond to you!
I will respond to any message that does not contain a ping or mention of another user, unless that user is myself.
Here are some commands you can use:
`-start` - Start a conversation
`-stop` - Stop a conversation
`-model <model>` - Set the model to use
`-get model` - Get the model being used
`-get status` - Get the status of the conversation
`-help` - Show this message
`-image <prompt>` - Generate an image
`-join <channel>` - Join a voice channel
`-leave` - Leave the voice channel"""

VALID_MODELS = ['', 'gpt-3.5-turbo', 'gpt-4', 'davinci', 'curie', 'babbage', 'ada']
VALID_COMMAND_HEADERS = [
    '-start',
    '-stop',
    '-model',
    '-get',
    '-help',
    '-image',
    '-ping',
    '-join',
    '-leave',
    '-o'
]

# Error messages
INVALID_MODEL_ERROR = 'Invalid model. Valid models are: \n```' + '\n'.join(VALID_MODELS) + '```'
INVALID_COMMAND_ERROR = 'Invalid command. Use `-help` to see a list of commands.'
ALREADY_STARTED_ERROR = 'Conversation already started. Use `-stop` to stop a conversation.'
ALREADY_STOPPED_ERROR = 'Conversation already stopped. Use `-start` to start a conversation.'
ALREADY_JOINED_ERROR = 'Already joined a voice channel. Use `-leave` to leave the voice channel.'
NOT_IN_VOICE_ERROR = 'Not in a voice channel. Use `-join` to join a voice channel.'

# Success messages
START_NOTIFY = 'Starting conversation.'
STOP_NOTIFY = 'Stopping conversation.'
MODEL_SET_NOTIFY = 'Model set to '
MODEL_GET_NOTIFY = 'Model: '
STATUS_GET_NOTIFY = 'Status: '
IMAGE_GENERATE_NOTIFY = 'Generating image...'
IMAGE_GENERATE_SUCCESS = 'Image generated!'
IMAGE_GENERATE_FAIL = 'Image generation failed.'
JOIN_NOTIFY = 'Joining voice channel...'
LEAVE_NOTIFY = 'Leaving voice channel...'
PONG_NOTIFY = 'Pong!'