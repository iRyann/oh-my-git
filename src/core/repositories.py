import json
from core.exceptions import RepositoryAlreadyExistsException, InvalidRepositoryDataStructureException
import os

REPOSITORIY_DATA_FIELDS = ["author","path", "origin", "tags"]

OMG_DATA_PATH = os.path.join(os.path.expanduser("~"),".omg")
REPOSITORIES_REGISTER_PATH =  os.path.join(OMG_DATA_PATH,"repositories.json")

# creating the ./omg directory if needed
if not os.path.isdir(OMG_DATA_PATH):
    os.mkdir(OMG_DATA_PATH)

# creating the ./omg/repositories.json if needed
if not os.path.isfile(REPOSITORIES_REGISTER_PATH):
    open(REPOSITORIES_REGISTER_PATH,"a").close()

# opening the file only once
REPOSITORIES_REGISTER_FILE = open(REPOSITORIES_REGISTER_PATH,"r+")

# parsing the json, creating the dict only once
raw_json = REPOSITORIES_REGISTER_FILE.read()
try:
    REPOSITORIES = json.loads(raw_json)
except: # avoid crashing when the json is empty or wrong
    REPOSITORIES = {}


# check if a repository name is known by omg, and if it is, check if the repository is still actually installed
def check_repository(repository_name: str)->bool:
    if repository_name in REPOSITORIES.keys():
        return os.path.exists(REPOSITORIES[repository_name]["path"])
    else:
        return False

# remove repositories that are no longer on the disk from the register
def clean_repositories()->None:
    repositories_names = list(REPOSITORIES.keys())
    for repository_name in repositories_names:
        if not os.path.exists(REPOSITORIES[repository_name]["path"]):
            del REPOSITORIES[repository_name]

# add a new repository to the register,
def add_repository(repository_name: str,repository_data : dict)->dict:
    if repository_name in REPOSITORIES.keys():
        raise RepositoryAlreadyExistsException(repository_name)
    else:
        # check if the data structure has the correct format
        if set(REPOSITORIY_DATA_FIELDS) == set(repository_data.keys()):
            REPOSITORIES[repository_name] = repository_data
            return repository_data
        else:   raise InvalidRepositoryDataStructureException(repository_data)
    

# update an already existing repository's data
def update_repository(repository_name: str,repository_data_to_update : dict)->dict:
    for field in repository_data_to_update.keys():
        if field in REPOSITORIY_DATA_FIELDS:
            REPOSITORIES[repository_name][field] = repository_data_to_update[field]
        else:   raise InvalidRepositoryDataStructureException(field)

    return REPOSITORIES[repository_name]

# retrive a repository's data from its name
def get_repository(repository_name : str)->dict:
    return REPOSITORIES[repository_name]

# retrive all repostories' data
def get_repositories()->dict:
    return REPOSITORIES

# save the REPOSITORIES object state to the repository.json file
def save_repositories()->dict:
    REPOSITORIES_REGISTER_FILE.seek(0)
    REPOSITORIES_REGISTER_FILE.write(json.dumps(REPOSITORIES,sort_keys=True))
    return REPOSITORIES

clean_repositories()