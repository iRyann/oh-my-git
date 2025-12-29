from core.exceptions import SystemCallErrorException
from typing import List
import json
import os

DEFAUT_CONFIG = {
    "prefered-shell":"/bin/bash"
}

OMG_DATA_PATH = os.path.join(os.path.expanduser("~"), ".omg")
CONFIG_PATH = os.path.join(OMG_DATA_PATH, "config.json")

# creating the ./omg directory if needed
if not os.path.isdir(OMG_DATA_PATH):
    os.mkdir(OMG_DATA_PATH)

# creating the ./omg/config.json if needed
if not os.path.isfile(CONFIG_PATH):
    open(CONFIG_PATH, "a").close()

# opening the file only once
with open(CONFIG_PATH,"r") as CONFIG_FILE: 
    # parsing the json, creating the dict only once
    raw_json = CONFIG_FILE.read()
try:
    CONFIG = json.loads(raw_json)
except:  # avoid crashing when the json is empty or wrong
    CONFIG = DEFAUT_CONFIG
    with open(CONFIG_PATH,"w") as CONFIG_FILE: 
        CONFIG_FILE.write(json.dumps(CONFIG))

def get_config(config_field : str):
    if config_field in CONFIG.keys():
        return CONFIG[config_field]
    else:
        return ""

def save_config() -> None:
    with open(CONFIG_PATH,"w") as CONFIG_FILE: 
        CONFIG_FILE.write(json.dumps(CONFIG))