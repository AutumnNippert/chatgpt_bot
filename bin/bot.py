# bot.py
import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import res.const as const
from bin.utils.file_interaction import *
from bin.utils.tts import tts_watson, tts_google, tts_dectalk
from bin.utils.ai_interaction import query, query_image, needs_moderation
from bin.classes.data_structures import BotConfig
from bin.utils.wikipedia_interaction import search
from bin.utils.weather_interaction import find_weather
from bin.utils.url_interaction import scrape_site
from bin.utils.misc import num_tokens_from_messages

from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    client.configs = load_configs('configs.json')
    if client.configs == {}:
        print('No Configs Found. Creating New Configs...')
        for guild in client.guilds:
            client.configs[guild.id] = BotConfig()
        
        save_configs(client.configs, 'configs.json')
        print('Configs Created')

        client.configs = load_configs('configs.json')

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
    if const.MAINTENANCE:
        if message.author != client.user:
            await message.channel.send(const.MAINTENANCE_MESSAGE)
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

    # Whiteboard worthy
    # if sender is not set, set sender to author
    # if sender is set, but author is sender, do nothing
    # if sender is set, but author is not sender, set recipient to sender, and sender to author
    if client.configs[guild_id].sender_id == None:
        client.configs[guild_id].sender_id = message.author.id
    elif client.configs[guild_id].sender_id == message.author.id:
        pass
    else:
        client.configs[guild_id].recipient_id = client.configs[guild_id].sender_id
        client.configs[guild_id].sender_id = message.author.id

    log_message(message, guild_id)
    

    # if any user is mentioned
    if message.mentions:
        client.configs[guild_id].done = asyncio.Future()
        client.configs[guild_id].recipient_id = message.mentions[0].id
        #convert mentions to names
        for mention in message.mentions:
            message.content = message.content.replace('<@' + str(mention.id) + '>', mention.name)

    #create memory if not exists
    if not hasattr(client.configs[guild_id], 'message_history'):
        client.configs[guild_id].message_history = []
    # keep track of memory
    if message.author == client.user:
        client.configs[guild_id].message_history.append({"role":"assistant", "content":message.content})
        if num_tokens_from_messages(client.configs[guild_id].message_history) > 4000:
            client.configs[guild_id].message_history.pop(0)
        return
    
    client.configs[guild_id].message_history.append({"role":"user", "content":'From ' + message.author.display_name + ': ' + message.content})
    if num_tokens_from_messages(client.configs[guild_id].message_history) > 4000:
        client.configs[guild_id].message_history.pop(0)

    # if not a message
    if message.type != discord.MessageType.default and message.type != discord.MessageType.reply:
        return

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
    possible_command = message.content.split(' ')[0]
    if possible_command in const.VALID_COMMAND_HEADERS:
        if possible_command == '-o':
            return
        special_command = special_commands(message, guild_id)
        if special_command:
            print('Special Command: ' + message.content)
            #if first words are const.ASK_NOTIFY
            if const.ASK_NOTIFY in special_command:
                async with message.channel.typing():
                    question = special_command.replace(const.ASK_NOTIFY, '')
                    response = query(question, personality=False)
                    response = clean_response(response)
                    await message.channel.send(response)
                    return
            if const.URL_NOTIFY in special_command:
                async with message.channel.typing():
                    url = special_command.replace(const.URL_NOTIFY, '')
                    site_contents = scrape_site(url)
                    if site_contents == None:
                        await message.channel.send(const.URL_ERROR)
                        return
                    client.configs[guild_id].message_history += site_contents
                    await message.channel.send(const.URL_CONSUMED_NOTIFY)
                    return
            elif const.SEARCH_NOTIFY in special_command:
                async with message.channel.typing():
                    question = special_command.replace(const.SEARCH_NOTIFY, '')
                    response = search(q=question)
                    await message.channel.send(response)
                    return
            elif const.SUMMARIZE_NOTIFY in special_command:
                async with message.channel.typing():
                    url = special_command.replace(const.SUMMARIZE_NOTIFY, '')
                    site_contents = scrape_site(url)
                    if site_contents == None:
                        await message.channel.send(const.URL_ERROR)
                        return
                    response = query(history=(site_contents + [{"role":"user", "content":"Summarize the information."}]), personality=False)
                    response = clean_response(response)
                    await message.channel.send(response)
                    return
            elif const.SAY_NOTIFY in special_command:
                if client.configs[guild_id].voice_client:
                    async with message.channel.typing():
                        text = special_command.replace(const.SAY_NOTIFY, '')
                        filename = str(guild_id) + '_say_request.mp3'
                        if client.configs[guild_id].tts_service == 'watson':
                            tts_watson(text, filename)
                        elif client.configs[guild_id].tts_service == 'google':
                            tts_google(text, filename)
                        elif client.configs[guild_id].tts_service == 'dectalk':
                            tts_dectalk(text, filename)
                    await message.channel.send(message.author.name + ' told me to say: ' + text)
                    await play_audio(filename, guild_id)
                    await remove_audio_file_when_done(filename, guild_id)
                    return
                else:
                    try:
                        async with message.channel.typing():
                            text = special_command.replace(const.SAY_NOTIFY, '')
                            filename = str(guild_id) + '_say_request.mp3'
                            if client.configs[guild_id].tts_service == 'watson':
                                tts_watson(text, filename)
                            elif client.configs[guild_id].tts_service == 'google':
                                tts_google(text, filename)
                            elif client.configs[guild_id].tts_service == 'dectalk':
                                tts_dectalk(text, filename)
                            
                            #join
                            client.configs[guild_id].voice_client = await message.author.voice.channel.connect()
                            client.configs[guild_id].in_voice = True
                            await message.channel.send(message.author.name + ' told me to say: ' + text)
                            await play_audio(filename, guild_id)
                            await remove_audio_file_when_done(filename, guild_id)
                            await disconnect_when_done(guild_id)
                            client.configs[guild_id].voice_client = None
                            client.configs[guild_id].in_voice = False
                            return
                    except Exception as e:
                        await message.channel.send(const.USER_NOT_IN_VOICE_ERROR)
                        return
            elif special_command == const.JOIN_NOTIFY:
                client.configs[guild_id].voice_client = await message.author.voice.channel.connect()
                await play_audio('join.mp3', guild_id)
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
            return
        


    # Check if should respond
    # if bot is mentioned, respond
    if message.mentions != None:
        if client.user in message.mentions:
            client.configs[guild_id].current_status = 'On'
    
    if message.reference:
        if message.reference.resolved.author == client.user:
            client.configs[guild_id].current_status = 'On'
            #get reference message
            reference_message = message.reference.resolved
            #add to history
            client.configs[guild_id].message_history.append({"role":"system", "content":"Refering to: " + reference_message.content})
    
    # Toggle
    if client.configs[guild_id].current_status == 'Off':
        return
    
    # if is_question(message.content):
    #     response = coded_instructions(message.content)
    #     if response:
    #         await message.channel.send(response)
    #         return
    #     async with message.channel.typing():
    #         response = search(q=message.content, history=client.configs[guild_id].message_history)
    #         print(response)
    #         await message.channel.send(response)
    #         return

    # contains url
    url = get_url(message.content)
    if url != '':
        print('url found: ' + url)
        async with message.channel.typing():
            site_contents = scrape_site(url)
            if site_contents != None:
                client.configs[guild_id].message_history += site_contents
                client.configs[guild_id].message_history.append({"role":"user", "content":message.content})
                while num_tokens_from_messages(client.configs[guild_id].message_history) > 4000:
                    client.configs[guild_id].message_history.pop(0)
                # await message.channel.send(const.URL_CONSUMED_NOTIFY)
            else:
                await message.channel.send(const.URL_ERROR)
                return

    # Using AI
    async with message.channel.typing():
        # Generate Response
        print('generating response...')
        response = query(history=client.configs[guild_id].message_history)
        print('response generated')

        response = clean_response(response)
        if response == '':
            response = const.NO_RESPONSE_ERROR

        if client.configs[guild_id].tts:
            filename = str(guild_id) + '_tts_response.mp3'
            if client.configs[guild_id].tts_service == 'watson':
                tts_watson(response, filename)
            elif client.configs[guild_id].tts_service == 'google':
                tts_google(response, filename)
            elif client.configs[guild_id].tts_service == 'dectalk':
                tts_dectalk(response, filename)
            await message.channel.send(response)
            await play_audio(filename, guild_id)
            await remove_audio_file_when_done(filename, guild_id)
        else:
            await message.channel.send(response)

def special_commands(message, guild_id) -> str:
    parts = message.content.split(' ')
    if parts[0] == '-ask':
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        return const.ASK_NOTIFY + ' '.join(parts[1:])
    elif parts[0] == '-search':
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        return const.SEARCH_NOTIFY + ' '.join(parts[1:])
    elif parts[0] == '-url':
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        return const.URL_NOTIFY + ' '.join(parts[1:])
    elif parts[0] == '-summarize':
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        return const.SUMMARIZE_NOTIFY + ' '.join(parts[1:])
    elif parts[0] == '-clear':
        #clear history
        client.configs[guild_id].message_history = []
        return const.CLEAR_HISTORY_NOTIFY
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
    elif parts[0] == '-get':
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        elif parts[1] == 'status':
            return const.STATUS_GET_NOTIFY + client.configs[guild_id].current_status
        else:
            return const.INVALID_USE_ERROR
    elif parts[0] == '-help':
        return const.HELP_STRING
    elif parts[0] == '-image':
        if message.author.id not in const.CLEARED_USERS:
            return const.CLEARED_USER_ONLY_ERROR
        
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        
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
    elif parts[0] == '-ttsset':
        if len(parts) == 1:
            return const.TTS_SET_ERROR
        elif parts[1] == 'google':
            client.configs[guild_id].tts_service = 'google'
            return const.TTS_SET_NOTIFY + 'Google'
        elif parts[1] == 'watson':
            if message.author.id != const.OWNER_ID:
                return const.OWNER_ONLY_ERROR
            client.configs[guild_id].tts_service = 'watson'
            return const.TTS_SET_NOTIFY + 'Watson'
        elif parts[1] == 'dectalk':
            client.configs[guild_id].tts_service = 'dectalk'
            return const.TTS_SET_NOTIFY + 'Dectalk'
        else:
            return const.TTS_SET_ERROR
        
    elif parts[0] == '-say':
        if len(parts) == 1:
            return const.INVALID_USE_ERROR
        return const.SAY_NOTIFY + ' '.join(parts[1:])
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
    file = 'res/' + file
    print('playing audio file: ' + file)
    voice_client = client.configs[guild_id].voice_client
    audio_source = discord.FFmpegPCMAudio(file)
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(audio_source)

async def remove_audio_file_when_done(file, guild_id):
    file = 'res/' + file
    from asyncio import sleep
    while client.configs[guild_id].voice_client.is_playing():
        await sleep(1)
    os.remove(file)

async def disconnect_when_done(guild_id):
    from asyncio import sleep
    while client.configs[guild_id].voice_client.is_playing():
        await sleep(1)
    await client.configs[guild_id].voice_client.disconnect()

def clean_response(response) -> str:
    if response[:2] == '\n\n':
        response = response[2:]
    if response[:3] == 'AI:':
        response = response[3:]
    # if the first characters are "As an AI language model, ", remove them
    if response[:27] == '\n\nAs an AI language model, ':
        response = response[27:]

    if len(response) > 2000:
        response = response[:2000]

    return response

def log_message(message, guild_id):
    # if client.configs[guild_id].current_status == 'Off':
    #     return
    
    timestamp = message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    filename = str(guild_id) + '-messages.log'
    sender = message.guild.get_member(client.configs[guild_id].sender_id)
    recipient = message.guild.get_member(client.configs[guild_id].recipient_id)
    if sender is None:
        sender = 'Unknown'
    else:
        sender = sender.name
    if recipient is None:
        recipient = 'Unknown'
    else:
        recipient = recipient.name
    text = str(timestamp) + ":: " + sender + ' -> ' + recipient + ' : ' + str(message.content)
    log(filename, text)

def is_question(message) -> bool:
    question_words = ["what", "why", "when", "where", "how", "which", "whom", "whose", "who"]

    question = message
    question = question.lower()

    if any(word in question for word in question_words):
        return True
    else:
        return False
    
def coded_instructions(message) -> str:
    import datetime
    import time
    message = message.lower()
    if 'time' in message and 'what' in message:
        date_time = datetime.datetime.now()
        timestamp = int(time.mktime(date_time.timetuple()))
        return f'<t:{timestamp}:t>'
    elif 'date' in message and 'what' in message:
        date_time = datetime.datetime.now()
        timestamp = int(time.mktime(date_time.timetuple()))
        return f'<t:{timestamp}:F>'
    elif 'weather' in message and 'what' in message:
        return find_weather(message)
    
async def send_pulse(x):
    import asyncio
    for i in range(0, x):
        client.ws.ping()
        await asyncio.sleep(10)

def get_url(message) -> str:
    import re
    url = re.compile(r'https?://\S+|www\.\S+')
    if url.search(message):
        return url.search(message).group()
    
    return ''
    
client.run(TOKEN)