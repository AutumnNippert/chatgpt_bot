import os
import json
from bin.classes.data_structures import BotConfig
def append_to_file(file_name, text_to_append):
    """Append the given text as a new line at the end of file"""
    # if file does not exist, create it
    if not os.path.exists(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        file_object.write(text_to_append + '\n')

def log(filename, text_to_append):
    """Append the given text as a new line at the end of log file"""
    append_to_file(f'logs/{filename}', text_to_append)

def save_configs(configs:dict, file_name): #not workin lol
    """Save configs to file"""
    #for each value in configs, convert to dict
    for key, value in configs.items():
        configs[key] = value.__dict__()

    file_name = f'res/{file_name}'
    if not os.path.exists(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, 'w') as f:
        dumps = json.dumps(configs, indent=4)
        f.write(dumps)

def load_configs(file_name) -> dict:
    """Load configs from file"""
    file_name = f'res/{file_name}'

    if not os.path.exists(file_name):
        return {}
    with open(file_name, 'r') as f:
        configs = json.load(f)

    configs_dict = {}
    for key, value in configs.items():
        configs_dict[int(key)] = BotConfig.create_from_dict(value)

    return configs_dict