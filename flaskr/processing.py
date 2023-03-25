import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from bin.utils.misc import num_tokens_from_messages
from bin.utils.url_interaction import scrape_site
from bin.utils.ai_interaction import query

message_history = []

def process_message(message):
    global message_history
    message_history.append({"role":"user", "content": message})
    if num_tokens_from_messages(message_history) > 4000:
        message_history.pop(0)
    
    # if is_question(message.content):
    #     response = coded_instructions(message.content)
    #     if response:
    #         await message.channel.send(response)
    #         return
    #     async with message.channel.typing():
    #         response = search(q=message.content, history=message_history)
    #         print(response)
    #         await message.channel.send(response)
    #         return

    # contains url
    url = get_url(message)
    if url != '':
        print('url found: ' + url)
        site_contents = scrape_site(url)
        if site_contents != None:
            message_history += site_contents
            message_history.append({"role":"user", "content":message})
            while num_tokens_from_messages(message_history) > 4000:
                message_history.pop(0)
            # await message.channel.send(const.URL_CONSUMED_NOTIFY)
        else:
            print("Error scraping site")
            return

    # Using AI
    # Generate Response
    print('generating response...')
    response = query(history=message_history)
    print('response generated')

    response = clean_response(response)
    if response == '':
        response = "I'm sorry, I don't understand."
    
    message_history.append({"role":"assistant", "content": response})
    if num_tokens_from_messages(message_history) > 4000:
        message_history.pop(0)

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

def is_question(message) -> bool:
    question_words = ["what", "why", "when", "where", "how", "which", "whom", "whose", "who"]

    question = message
    question = question.lower()

    if any(word in question for word in question_words):
        return True
    else:
        return False

def get_url(message) -> str:
    import re
    url = re.compile(r'https?://\S+|www\.\S+')
    if url.search(message):
        return url.search(message).group()
    
    return ''

def get_message_history():
    return message_history