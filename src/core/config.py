from core.exceptions import SystemCallErrorException
from typing import List
import json
import os

CONFIG_DATA_FIELDS = ["author", "path", "origin", "tags"]

OMG_DATA_PATH = os.path.join(os.path.expanduser("~"), ".omg")
CONFIG_PATH = os.path.join(OMG_DATA_PATH, "repositories.json")

# creating the ./omg directory if needed
if not os.path.isdir(OMG_DATA_PATH):
    os.mkdir(OMG_DATA_PATH)

# creating the ./omg/repositories.json if needed
if not os.path.isfile(REPOSITORIES_REGISTER_PATH):
    open(REPOSITORIES_REGISTER_PATH, "a").close()

# opening the file only once
with open(REPOSITORIES_REGISTER_PATH,"r") as REPOSITORIES_REGISTER_FILE: 
    # parsing the json, creating the dict only once
    raw_json = REPOSITORIES_REGISTER_FILE.read()
try:
    CONFIG = json.loads(raw_json)
except:  # avoid crashing when the json is empty or wrong
    CONFIG = {}

def create_default_config():
    pass

def 