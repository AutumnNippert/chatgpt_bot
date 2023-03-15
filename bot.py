# bot.py
import os
import const
from wrappers import *
from  file_interaction import *

import discord
from dotenv import load_dotenv
from ai_interaction import query

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Global Variables
client.conversee = None
client.last_sender = None
client.current_status = 'Off'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    client.last_sender = message.author

    # Special Commands
    # if starts with -c, it's a special command
    if message.content[:2] == '-c':
        special_command = special_commands(message)
        if special_command:
            await message.channel.send(special_command)
            return

    # Toggle
    if client.current_status == 'Off':
        return
        
    # Log Message
    timestamp = message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    append_to_file('messages.log', str(timestamp) + ":: " + str(client.last_sender) + ' -> ' + str(client.conversee) + ' : ' + str(message.content))

    if not should_respond(message):
        client.conversee = message.author
        client.last_sender = client.user
        return
    

    # Using AI
    model = 'gpt-3.5-turbo'
    async with message.channel.typing():
        # Model Selection
        if '--model gpt-4' in message.content:
            await message.channel.send('Currently, there is a limited beta for GPT4 that I am not capable of accessing.')
            return

        response = query(message.content, model)
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

def special_commands(message) -> str:
    if '--command help' in message.content or '-c help' in message.content:
        return const.HELP_STRING

    if '--command ping' in message.content or '-c ping' in message.content:
        return 'Pong!'
    
    if '--command ping' in message.content or '-c start' in message.content:
        if client.current_status == 'On':
            return 'Conversation already started. Use `-c stop` to stop a conversation.'
        client.current_status = 'On'
        return 'Starting conversation.'
    
    if '--command stop' in message.content or '-c stop' in message.content:
        if client.current_status == 'Off':
            return 'Conversation already stopped. Use `-c start` to start a conversation.'
        client.current_status = 'Off'
        return 'Stopping conversation.'
    
    if '--command status' in message.content or '-c status' in message.content:
        return 'Status: ' + str(client.current_status)

    return None

def clean_response(response) -> str:
    # if the first characters are "As an AI language model, ", remove them
    if response[:27] == '\n\nAs an AI language model, ':
        response = response[27:]

    if len(response) > 2000:
        response = response[:2000]

    return response

client.run(TOKEN)