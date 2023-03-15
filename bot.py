# bot.py
import os
import const
from  file_interaction import *

import asyncio

import discord
from discord import VoiceClient
import shutil
from discord.ext import commands

from dotenv import load_dotenv
#import opus
from ai_interaction import query, query_old, query_image

load_dotenv()
#opus.load_opus()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Global Variables
client.conversee = None
client.last_sender = None
client.current_status = 'Off'
client.model = 'gpt-3.5-turbo'
client.in_voice = False
client.voice_client = None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # if not a message
    if message.type != discord.MessageType.default and message.type != discord.MessageType.reply:
        return
    
    log_message(message)
    
    # Set last_sender to author
    client.last_sender = message.author

    # Special Commands
    # check if starts with a command header
    if message.content.split(' ')[0] in const.VALID_COMMAND_HEADERS:
        parts = message.content.split(' ')
        special_command = special_commands(parts)
        if special_command:
            if special_command == const.JOIN_NOTIFY:
                client.voice_client = await message.author.voice.channel.connect()
                await play_audio('res/join.wav')
            elif special_command == const.LEAVE_NOTIFY:
                await client.voice_client.disconnect()
            await message.channel.send(special_command)
            return
        else:
            return

    # Toggle
    if client.current_status == 'Off':
        return

    # Check if should respond
    if not should_respond(message):
        client.conversee = message.author
        client.last_sender = client.user
        return
    
    # Using AI
    async with message.channel.typing():
        # Generate Response
        if client.model != 'gpt-3.5-turbo':
            response = query_old(message.content, client.model)
        else:
            response = query(message.content)

        response = clean_response(response)

        client.last_sender = client.conversee
        client.conversee = message.author
        await message.channel.send(response)

def should_respond(message) -> bool:
    # if talking to self, stop
    if client.last_sender == client.user and client.conversee == client.user:
        return False
    
    # if bot is mentioned, respond
    if '@' in message.content:
        if client.user in message.mentions:
            return True
        else:
            return False
    if message.reference:
        if message.reference.resolved.author == client.user:
            return True
        else:
            return False

    # if bot is not conversee, don't respond
    if client.conversee != client.user:
        return False
    
    return True

def special_commands(parts:list) -> str:
    if parts[0] == '-start':
        if client.current_status == 'On':
            return const.ALREADY_STARTED_ERROR
        else:
            client.current_status = 'On'
            return const.START_NOTIFY
    elif parts[0] == '-stop':
        if client.current_status == 'Off':
            return const.ALREADY_STOPPED_ERROR
        else:
            client.current_status = 'Off'
            return const.STOP_NOTIFY
    elif parts[0] == '-model':
        if len(parts) == 1:
            return const.INVALID_MODEL_ERROR
        elif parts[1] in const.VALID_MODELS:
            client.model = parts[1]
            return const.MODEL_SET_NOTIFY + parts[1]
        else:
            return const.INVALID_MODEL_ERROR
    elif parts[0] == '-get':
        if len(parts) == 1:
            return const.INVALID_COMMAND_ERROR
        elif parts[1] == 'model':
            return const.MODEL_GET_NOTIFY + client.model
        elif parts[1] == 'status':
            return const.STATUS_GET_NOTIFY + client.current_status
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
            return const.IMAGE_ERROR
    elif parts[0] == '-ping':
        return const.PONG_NOTIFY
    elif parts[0] == '-join':
        if client.in_voice:
            return const.ALREADY_JOINED_ERROR
        client.in_voice = True
        return const.JOIN_NOTIFY
    elif parts[0] == '-leave':
        if not client.in_voice:
            return const.NOT_IN_VOICE_ERROR
        client.in_voice = False
        return const.LEAVE_NOTIFY
    elif parts[0] == '-o':
        return
    else:
        return const.INVALID_COMMAND_ERROR

async def play_audio(file):
    if not client.in_voice:
        return
    voice_client = client.voice_clients[0]
    audio_source = discord.FFmpegPCMAudio(file)
    voice_client.play(audio_source)

def clean_response(response) -> str:
    # if the first characters are "As an AI language model, ", remove them
    if response[:27] == '\n\nAs an AI language model, ':
        response = response[27:]

    if len(response) > 2000:
        response = response[:2000]

    return response

def log_message(message):
    if client.current_status == 'Off':
        return
    
    timestamp = message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    append_to_file('messages.log', str(timestamp) + ":: " + str(client.last_sender) + ' -> ' + str(client.conversee) + ' : ' + str(message.content))

client.run(TOKEN)