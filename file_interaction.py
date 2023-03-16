import os
import json
from data_structures import BotConfig
def append_to_file(file_name, text_to_append):
    """Append the given text as a new line at the end of file"""
    # if file does not exist, create it
    if not os.path.exists(file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        file_object.write(text_to_append + '\n')

def save_configs(configs:dict, file_name): #not workin lol
    """Save configs to file"""
    with open(file_name, 'w') as f:
        json.dump(configs, f)

def load_configs(file_name) -> dict:
    """Load configs from file"""
    if not os.path.exists(file_name):
        return {}
    with open(file_name, 'r') as f:
        configs = json.load(f)

    configs_dict = {}
    for key, value in configs.items():
        #value to string
        value = json.dumps(value)
        #string to BotConfig
        value = json.loads(value, object_hook=lambda d: BotConfig(**d))
        configs_dict[int(key)] = value

    return configs_dict