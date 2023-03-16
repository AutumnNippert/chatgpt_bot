# bot.py
import os
import const
from file_interaction import *
from tts import tts, tts_watson
from data_structures import BotConfig
from ai_interaction import query, query_old, query_image, needs_moderation

from dotenv import load_dotenv

import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

configs = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # configs = load_configs('configs.json')
    # if configs == {}:
    #     print('No Configs Found. Creating New Configs...')
    #     for guild in client.guilds:
    #         configs[guild.id] = BotConfig()
        
    #     config_json = json.dumps(configs, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    #     save_configs(config_json, 'configs.json')
    #     print('Configs Created')

    #     configs = load_configs('configs.json')
    
    # print(configs[474096541142089728])

    print('Configs Loaded')

    for guild in client.guilds:
        configs[guild.id] = BotConfig()

@client.event
async def on_message(message):
    guild_id = message.guild.id
    # if not a message
    if message.type != discord.MessageType.default and message.type != discord.MessageType.reply:
        return
    
    log_message(message, guild_id)
    
    # Set last_sender to author
    configs[guild_id].last_sender = message.author

    # Special Commands
    # check if starts with a command header
    if message.content.split(' ')[0] in const.VALID_COMMAND_HEADERS:
        special_command = special_commands(message, guild_id)
        if special_command:
            if special_command == const.JOIN_NOTIFY:
                if message.author.voice is None:
                    await message.channel.send(const.USER_NOT_IN_VOICE_ERROR)
                    return
                configs[guild_id].voice_client = await message.author.voice.channel.connect()
                await play_audio('res/join.mp3', guild_id)
            elif special_command == const.LEAVE_NOTIFY:
                await configs[guild_id].voice_client.disconnect()
            elif special_command == const.SHUTDOWN_NOTIFY:
                await message.channel.send(special_command)
                save_configs(configs, 'configs.json')
                await client.close()
            await message.channel.send(special_command)
            return
        else:
            return
        
    
    if needs_moderation(message.content):
        await message.reply(const.MODERATION_NOTIFY)


    # Check if should respond
    if not should_respond(message):
        configs[guild_id].conversee = message.author
        configs[guild_id].last_sender = client.user
        return
    
    # Toggle
    if configs[guild_id].current_status == 'Off':
        return

    # Using AI
    async with message.channel.typing():
        # Generate Response
        if configs[guild_id].model != 'gpt-3.5-turbo':
            response = query_old(message.content, configs[guild_id].model)
        else:
            response = query(message.content)

        response = clean_response(response)

        configs[guild_id].last_sender = configs[guild_id].conversee
        configs[guild_id].conversee = message.author
        if configs[guild_id].tts:
            if configs[guild_id].tts_upgrade:
                tts_watson(response, 'tmp/response.mp3')
            else:
                tts(response, 'tmp/response.mp3')
            await message.channel.send(response)
            await play_audio('tmp/response.mp3', guild_id)
        else:
            await message.channel.send(response)

def should_respond(message) -> bool:
    guild_id = message.guild.id
    # if talking to self, stop
    if configs[guild_id].last_sender == client.user and configs[guild_id].conversee == client.user:
        return False
    
    # if bot is mentioned, respond
    if '@' in message.content:
        if client.user in message.mentions:
            configs[guild_id].current_status = 'On'
            return True
        else:
            return False
    if message.reference:
        if message.reference.resolved.author == client.user:
            return True
        else:
            return False

    # if bot is not conversee, don't respond
    if configs[guild_id].conversee != client.user:
        return False
    
    return True

def special_commands(message, guild_id) -> str:
    parts = message.content.split(' ')
    if parts[0] == '-start':
        if configs[guild_id].current_status == 'On':
            return const.ALREADY_STARTED_ERROR
        else:
            configs[guild_id].current_status = 'On'
            return const.START_NOTIFY
    elif parts[0] == '-stop':
        if configs[guild_id].current_status == 'Off':
            return const.ALREADY_STOPPED_ERROR
        else:
            configs[guild_id].current_status = 'Off'
            return const.STOP_NOTIFY
    elif parts[0] == '-model':
        if len(parts) == 1:
            return const.INVALID_MODEL_ERROR
        elif parts[1] in const.VALID_MODELS:
            configs[guild_id].model = parts[1]
            return const.MODEL_SET_NOTIFY + parts[1]
        else:
            return const.INVALID_MODEL_ERROR
    elif parts[0] == '-get':
        if len(parts) == 1:
            return const.INVALID_COMMAND_ERROR
        elif parts[1] == 'model':
            return const.MODEL_GET_NOTIFY + configs[guild_id].model
        elif parts[1] == 'status':
            return const.STATUS_GET_NOTIFY + configs[guild_id].current_status
        else:
            return const.INVALID_COMMAND_ERROR
    elif parts[0] == '-help':
        return const.HELP_STRING
    elif parts[0] == '-image':
        if len(parts) == 1:
            return const.INVALID_COMMAND_ERROR
        
        query = ' '.join(parts[1:])
        image = query_image(query)
        if image:
            return image
        else:
            return const.IMAGE_GENERATE_ERROR
    elif parts[0] == '-ping':
        return const.PONG_NOTIFY
    elif parts[0] == '-join':
        if configs[guild_id].in_voice:
            return const.ALREADY_JOINED_ERROR
        configs[guild_id].in_voice = True
        #configs[guild_id].current_status = 'On'
        configs[guild_id].tts = True
        return const.JOIN_NOTIFY
    elif parts[0] == '-leave':
        if not configs[guild_id].in_voice:
            return const.NOT_IN_VOICE_ERROR
        configs[guild_id].in_voice = False
        configs[guild_id].tts = False
        return const.LEAVE_NOTIFY
    elif parts[0] == '-tts':
        if configs[guild_id].tts:
            configs[guild_id].tts = False
            return const.TTS_OFF_NOTIFY
        else:
            configs[guild_id].tts = True
            return const.TTS_ON_NOTIFY
    elif parts[0] == '-tts-upgrade':
        if message.author.id != const.OWNER_ID:
            return const.OWNER_ONLY_ERROR
        if configs[guild_id].tts_upgrade:
            configs[guild_id].tts_upgrade = False
            return const.TTS_UPGRADE_OFF_NOTIFY
        else:
            configs[guild_id].tts_upgrade = True
            return const.TTS_UPGRADE_ON_NOTIFY
    elif parts[0] == '-o':
        return
    elif parts[0] == '-shutdown':
        if message.author.id != const.OWNER_ID:
            return const.OWNER_ONLY_ERROR
        return const.SHUTDOWN_NOTIFY
    else:
        return const.INVALID_COMMAND_ERROR

async def play_audio(file, guild_id):
    if not configs[guild_id].in_voice:
        return
    voice_client = configs[guild_id].voice_client
    audio_source = discord.FFmpegPCMAudio(file)
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(audio_source)

def clean_response(response) -> str:
    # if the first characters are "As an AI language model, ", remove them
    if response[:27] == '\n\nAs an AI language model, ':
        response = response[27:]

    if len(response) > 2000:
        response = response[:2000]

    return response

def log_message(message, guild_id):
    if configs[guild_id].current_status == 'Off':
        return
    
    timestamp = message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    filename = 'logs/' + str(guild_id) + '-messages.log'
    append_to_file(filename, str(timestamp) + ":: " + str(configs[guild_id].last_sender) + ' -> ' + str(configs[guild_id].conversee) + ' : ' + str(message.content))

client.run(TOKEN)