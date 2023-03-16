# bot.py
import os
import const
from file_interaction import *
from tts import tts, tts_watson
from data_structures import BotConfig
from ai_interaction import query, query_old, query_image, needs_moderation

from dotenv import load_dotenv

import discord
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    client.configs = load_configs('data/configs.json')
    if client.configs == {}:
        print('No Configs Found. Creating New Configs...')
        for guild in client.guilds:
            client.configs[guild.id] = BotConfig()
        
        save_configs(client.configs, 'data/configs.json')
        print('Configs Created')

        client.configs = load_configs('data/configs.json')

    print('Configs Loaded')
    
    game = discord.Game("with the API")
    await client.change_presence(activity=game)

    # for guild in client.guilds:
    #     configs[guild.id] = BotConfig()

@client.event
async def on_guild_join(guild):
    client.configs[guild.id] = BotConfig() #create new config for guild
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(const.JOIN_SERVER_NOTIFY)
        break

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if DM
    if not message.guild:
        print('Attempted DM from ' + message.author.name + ': ' + message.content)
        try:
            await message.author.send(const.DM_NOTIFY)
        except Exception as e:
            print('Could not send DM message to user')
            print(e)
        finally:
            return
    
    guild_id = message.guild.id
    # if not a message
    if message.type != discord.MessageType.default and message.type != discord.MessageType.reply:
        return
    
    log_message(message, guild_id)
    
    # Set last_sender to author
    client.configs[guild_id].last_sender = message.author.id

    if client.configs[guild_id].moderation:
        if needs_moderation(message.content):
            await message.delete() # requires manage messages permission
            try:
                await message.author.send(const.MODERATION_NOTIFY)
            except Exception as e:
                print('Could not send moderation message to user')
                print(e)
            finally:
                return

    # Special Commands
    # check if starts with a command header
    if message.content.split(' ')[0] in const.VALID_COMMAND_HEADERS:
        special_command = special_commands(message, guild_id)
        if special_command:
            #if first words are const.ASK_NOTIFY
            if const.ASK_NOTIFY in special_command:
                async with message.channel.typing():
                    question = special_command.replace(const.ASK_NOTIFY, '')
                    response = query(question)
                    response = clean_response(response)
                    await message.channel.send(response)
                    return
            elif special_command == const.JOIN_NOTIFY:
                client.configs[guild_id].voice_client = await message.author.voice.channel.connect()
                await play_audio('res/join.mp3', guild_id)
            elif special_command == const.LEAVE_NOTIFY:
                await client.configs[guild_id].voice_client.disconnect()
            elif special_command == const.SHUTDOWN_NOTIFY:
                await message.channel.send(special_command)
                #if voice client is connected from all servers, disconnect
                for config in client.configs.values():
                    if config.voice_client:
                        await config.voice_client.disconnect()
                        break
                    config.voice_client = None
                await client.close()
                save_configs(client.configs, 'configs.json')
                await client.close()
            elif const.IMAGE_GENERATE_NOTIFY in special_command:
                await message.channel.send(const.IMAGE_GENERATE_NOTIFY)
                async with message.channel.typing():
                    img_query = special_command.replace(const.IMAGE_GENERATE_NOTIFY, '')
                    image = query_image(img_query)
                    if image:
                        special_command = image
                    else:
                        special_command = const.IMAGE_GENERATE_ERROR
            await message.channel.send(special_command)
            return
        else:
            await message.channel.send(const.INVALID_COMMAND_ERROR)
        


    # Check if should respond
    if not should_respond(message):
        client.configs[guild_id].conversee = message.author.id
        client.configs[guild_id].last_sender = client.user.id
        return
    
    # Toggle
    if client.configs[guild_id].current_status == 'Off':
        return

    # Using AI
    async with message.channel.typing():
        # Generate Response
        if client.configs[guild_id].model != 'gpt-3.5-turbo':
            response = query_old(message.content, client.configs[guild_id].model)
        else:
            response = query(message.content)

        response = clean_response(response)

        client.configs[guild_id].last_sender = client.configs[guild_id].conversee
        client.configs[guild_id].conversee = message.author.id
        if client.configs[guild_id].tts:
            if client.configs[guild_id].tts_upgrade:
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
    if client.configs[guild_id].last_sender == client.user.id and client.configs[guild_id].conversee == client.user.id:
        return False
    
    # if bot is mentioned, respond
    if '@' in message.content:
        if client.user in message.mentions:
            client.configs[guild_id].current_status = 'On'
            return True
        else:
            return False
    if message.reference:
        if message.reference.resolved.author == client.user:
            return True
        else:
            return False
    
    return True

def special_commands(message, guild_id) -> str:
    parts = message.content.split(' ')
    if parts[0] == '-ask':
        if len(parts) == 1:
            return const.INVALID_ASK_ERROR
        return const.ASK_NOTIFY + ' '.join(parts[1:])
    elif parts[0] == '-start':
        if client.configs[guild_id].current_status == 'On':
            return const.ALREADY_STARTED_ERROR
        else:
            client.configs[guild_id].current_status = 'On'
            return const.START_NOTIFY
    elif parts[0] == '-stop':
        if client.configs[guild_id].current_status == 'Off':
            return const.ALREADY_STOPPED_ERROR
        else:
            client.configs[guild_id].current_status = 'Off'
            return const.STOP_NOTIFY
    elif parts[0] == '-model':
        if len(parts) == 1:
            return const.INVALID_MODEL_ERROR
        elif parts[1] in const.VALID_MODELS:
            client.configs[guild_id].model = parts[1]
            return const.MODEL_SET_NOTIFY + parts[1]
        else:
            return const.INVALID_MODEL_ERROR
    elif parts[0] == '-get':
        if len(parts) == 1:
            return const.INVALID_COMMAND_ERROR
        elif parts[1] == 'model':
            return const.MODEL_GET_NOTIFY + client.configs[guild_id].model
        elif parts[1] == 'status':
            return const.STATUS_GET_NOTIFY + client.configs[guild_id].current_status
        else:
            return const.INVALID_COMMAND_ERROR
    elif parts[0] == '-help':
        return const.HELP_STRING
    elif parts[0] == '-image':
        if message.author.id not in const.CLEARED_USERS:
            return const.CLEARED_USER_ONLY_ERROR
        
        if len(parts) == 1:
            return const.INVALID_COMMAND_ERROR
        
        return const.IMAGE_GENERATE_NOTIFY + ' '.join(parts[1:])
    elif parts[0] == '-ping':
        return const.PONG_NOTIFY
    elif parts[0] == '-join':
        if client.configs[guild_id].in_voice:
            return const.ALREADY_JOINED_ERROR
        
        if message.author.voice is None:
            return const.USER_NOT_IN_VOICE_ERROR
        
        client.configs[guild_id].in_voice = True
        #client.configs[guild_id].current_status = 'On'
        client.configs[guild_id].tts = True
        return const.JOIN_NOTIFY
    elif parts[0] == '-leave':
        if not client.configs[guild_id].in_voice:
            return const.NOT_IN_VOICE_ERROR
        client.configs[guild_id].in_voice = False
        client.configs[guild_id].tts = False
        return const.LEAVE_NOTIFY
    elif parts[0] == '-tts':
        if client.configs[guild_id].tts:
            client.configs[guild_id].tts = False
            return const.TTS_OFF_NOTIFY
        else:
            client.configs[guild_id].tts = True
            return const.TTS_ON_NOTIFY
    elif parts[0] == '-tts-upgrade':
        if message.author.id != const.OWNER_ID:
            return const.OWNER_ONLY_ERROR
        if client.configs[guild_id].tts_upgrade:
            client.configs[guild_id].tts_upgrade = False
            return const.TTS_UPGRADE_OFF_NOTIFY
        else:
            client.configs[guild_id].tts_upgrade = True
            return const.TTS_UPGRADE_ON_NOTIFY
    elif parts[0] == '-o':
        return
    elif parts[0] == '-shutdown':
        if message.author.id != const.OWNER_ID:
            return const.OWNER_ONLY_ERROR
        return const.SHUTDOWN_NOTIFY
    elif parts[0] == '-mod':
        # if not message.author.server_permissions.administrator:
        #     return const.ADMIN_ONLY_ERROR
        if client.configs[guild_id].moderation:
            client.configs[guild_id].moderation = False
            return const.MODERATION_OFF_NOTIFY
        else:
            client.configs[guild_id].moderation = True
            return const.MODERATION_ON_NOTIFY
    else:
        return const.INVALID_COMMAND_ERROR

async def play_audio(file, guild_id):
    if not client.configs[guild_id].in_voice:
        return
    voice_client = client.configs[guild_id].voice_client
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
    if client.configs[guild_id].current_status == 'Off':
        return
    
    timestamp = message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    filename = 'logs/' + str(guild_id) + '-messages.log'
    append_to_file(filename, str(timestamp) + ":: " + str(client.configs[guild_id].last_sender) + ' -> ' + str(client.configs[guild_id].conversee) + ' : ' + str(message.content))

client.run(TOKEN)