import json
import os
from typing import Any, Dict, List, Set

from omg.core.exceptions import (InvalidRepositoryDataStructureException,
                             RepositoryAlreadyExistsException,
                             RepositoryDoesNotExistsException,
                             SystemCallErrorException)

REPOSITORIY_DATA_FIELDS = ["author", "path", "origin", "tags","icons"]

OMG_DATA_PATH = os.path.join(os.path.expanduser("~"), ".omg")
REPOSITORIES_REGISTER_PATH = os.path.join(OMG_DATA_PATH, "repositories.json")
GLOBAL_SCRIPTS_PATH = os.path.join(OMG_DATA_PATH, "scripts.json")

# creating the ./omg directory if needed
if not os.path.isdir(OMG_DATA_PATH):
    os.mkdir(OMG_DATA_PATH)

# creating the ./omg/repositories.json if needed
if not os.path.isfile(REPOSITORIES_REGISTER_PATH):
    open(REPOSITORIES_REGISTER_PATH, "a").close()

# opening the file only once
with open(REPOSITORIES_REGISTER_PATH, "r") as REPOSITORIES_REGISTER_FILE:
    # parsing the json, creating the dict only once
    raw_json = REPOSITORIES_REGISTER_FILE.read()
try:
    REPOSITORIES = json.loads(raw_json)
except:  # avoid crashing when the json is empty or wrong
    REPOSITORIES = {}


def check_repository(repository_proxy: str) -> bool:
    repository_path = os.path.abspath(repository_proxy)

    # check if repository_proxy is known, if yes retrieve path
    if repository_proxy in REPOSITORIES.keys():
        repository_path = REPOSITORIES[repository_proxy]["path"]
    elif repository_path not in [
        repository_data["path"] for repository_data in REPOSITORIES.values()
    ]:
        return ""

    # return repository path if it still exists
    if os.path.exists(repository_path):
        return repository_path
    else:
        return ""


# remove repositories that are no longer on the disk from the register
def clean_repositories() -> None:
    repositories_names = list(REPOSITORIES.keys())
    for repository_name in repositories_names:
        if not os.path.exists(REPOSITORIES[repository_name]["path"]):
            del REPOSITORIES[repository_name]


# add a new repository to the register,
def add_repository(repository_name: str, repository_data: dict) -> dict:
    if repository_name in REPOSITORIES.keys():
        raise RepositoryAlreadyExistsException(repository_name)
    else:
        # check if the data structure has the correct format
        if set(REPOSITORIY_DATA_FIELDS) == set(repository_data.keys()):
            REPOSITORIES[repository_name] = repository_data
            return repository_data
        else:
            raise InvalidRepositoryDataStructureException(repository_data)


# update an already existing repository's data
def update_repository(repository_name: str, repository_data_to_update: dict) -> dict:
    for field in repository_data_to_update.keys():
        if field in REPOSITORIY_DATA_FIELDS:
            REPOSITORIES[repository_name][field] = repository_data_to_update[field]
        else:
            raise InvalidRepositoryDataStructureException(field)

    return REPOSITORIES[repository_name]


# retrive a repository's data from its name
def get_repository(repository_name: str) -> dict:
    return REPOSITORIES[repository_name]

# retrive a repository's data from its name/path
def get_repository_from_proxy(repository_proxy: str) -> dict:
    repository_path = os.path.abspath(repository_proxy)

    # check if repository_proxy is known, if yes retrieve path
    if repository_proxy in REPOSITORIES.keys():
        return REPOSITORIES[repository_proxy]  
    else:
        return next(
            (repository for repository in REPOSITORIES.values() \
            if f"{repository_path}{os.sep}".startswith(f'{repository["path"]}{os.sep}')),
            None)

# retrive all repostories' data
def get_repositories() -> dict:
    return REPOSITORIES


def forget_repositories(repositories_names: List[str]) -> None:
    if not (set(repositories_names) <= set(REPOSITORIES.keys())):
        raise RepositoryDoesNotExistsException(repositories_names)
    else:
        for repository_name in repositories_names:
            del REPOSITORIES[repository_name]


def remove_repositories(repositories_names: List[str]) -> None:
    if not (set(repositories_names) <= set(REPOSITORIES.keys())):
        raise RepositoryDoesNotExistsException(repositories_names)
    else:
        for repository_name in repositories_names:
            try:
                error_code = os.popen(
                    f'rm -Rf {REPOSITORIES[repository_name]["path"]}', "r"
                ).close()
                if error_code != None:
                    raise SystemCallErrorException(f"removal of {repository_name}")
            except exception:
                raise exception


# save the REPOSITORIES object state to the repository.json file
def save_repositories() -> dict:
    with open(REPOSITORIES_REGISTER_PATH, "w") as REPOSITORIES_REGISTER_FILE:
        REPOSITORIES_REGISTER_FILE.write(json.dumps(REPOSITORIES, sort_keys=True))
    return REPOSITORIES


def get_repositories_filtered(
    names: List[str],
    authors: List[str],
    paths: List[str],
    origins: List[str],
    tags: List[str],
) -> List[str]:
    repositories = get_repositories()
    names_set = set(names or [])
    authors_set = set(authors or [])
    tags_set = set(tags or [])
    paths_set = set(paths or [])
    origins_set = set(origins or [])

    def matches(name: str, repo: dict) -> bool:
        repo_author = repo.get("author", "")
        repo_tags = set(repo.get("tags") or [])
        repo_path = repo.get("path", "")
        repo_origin = repo.get("origin", "")

        if names_set and not any(n in name for n in names_set):
            return False
        if authors_set and not any(a in repo_author for a in authors_set):
            return False
        if tags_set and repo_tags.isdisjoint(tags_set):
            return False
        if paths_set and not any(p in repo_path for p in paths_set):
            return False
        if origins_set and not any(o in repo_origin for o in origins_set):
            return False
        return True

    return [name for name, repo in repositories.items() if matches(name, repo)]


clean_repositories()


# retrieve the list of script names available for a repository (local + global)
def get_scripts(repository_name: str) -> List[str]:
    scripts = {}

    # global scripts
    if os.path.isfile(GLOBAL_SCRIPTS_PATH):
        try:
            with open(GLOBAL_SCRIPTS_PATH, "r") as f:
                scripts.update(json.loads(f.read()))
        except Exception:
            pass

    # repository-local scripts
    try:
        repository = get_repository(repository_name)
    except KeyError:
        return list(scripts.keys())

    scripts_file_path = os.path.join(repository["path"], ".omg/scripts.json")
    if os.path.isfile(scripts_file_path):
        try:
            with open(scripts_file_path, "r") as f:
                scripts.update(json.loads(f.read()))
        except Exception:
            pass

    return list(scripts.keys())


# retrieve the command for a given script name (local takes priority over global)
def get_script_command(repository_name: str, script_name: str) -> str:
    # repository-local scripts take priority
    try:
        repository = get_repository(repository_name)
        scripts_file_path = os.path.join(repository["path"], ".omg/scripts.json")
        if os.path.isfile(scripts_file_path):
            with open(scripts_file_path, "r") as f:
                scripts_dict = json.loads(f.read())
                if script_name in scripts_dict:
                    return scripts_dict[script_name]
    except KeyError:
        pass

    # fall back to global scripts
    if os.path.isfile(GLOBAL_SCRIPTS_PATH):
        with open(GLOBAL_SCRIPTS_PATH, "r") as f:
            scripts_dict = json.loads(f.read())
            if script_name in scripts_dict:
                return scripts_dict[script_name]

    return None


# add a script to a repository's local scripts file
def add_script(repository_name: str, script_name: str, script_command: str) -> None:
    repository = get_repository(repository_name)
    scripts_dir = os.path.join(repository["path"], ".omg")
    scripts_file_path = os.path.join(scripts_dir, "scripts.json")

    if not os.path.isdir(scripts_dir):
        os.makedirs(scripts_dir)

    if os.path.isfile(scripts_file_path):
        with open(scripts_file_path, "r") as f:
            scripts_dict = json.loads(f.read())
    else:
        scripts_dict = {}

    scripts_dict[script_name] = script_command

    with open(scripts_file_path, "w") as f:
        f.write(json.dumps(scripts_dict, indent=4))


# remove a script from a repository's local scripts file
def remove_script(repository_name: str, script_name: str) -> bool:
    repository = get_repository(repository_name)
    scripts_file_path = os.path.join(repository["path"], ".omg/scripts.json")

    if not os.path.isfile(scripts_file_path):
        return False

    with open(scripts_file_path, "r") as f:
        scripts_dict = json.loads(f.read())

    if script_name not in scripts_dict:
        return False

    del scripts_dict[script_name]

    with open(scripts_file_path, "w") as f:
        f.write(json.dumps(scripts_dict, indent=4))

    return True


# add a global script available for every repository
def add_global_script(script_name: str, script_command: str) -> None:
    if not os.path.isfile(GLOBAL_SCRIPTS_PATH):
        scripts_dict = {}
    else:
        with open(GLOBAL_SCRIPTS_PATH, "r") as f:
            scripts_dict = json.loads(f.read())

    scripts_dict[script_name] = script_command

    with open(GLOBAL_SCRIPTS_PATH, "w") as f:
        f.write(json.dumps(scripts_dict, indent=4))


# remove a global script
def remove_global_script(script_name: str) -> bool:
    if not os.path.isfile(GLOBAL_SCRIPTS_PATH):
        return False

    with open(GLOBAL_SCRIPTS_PATH, "r") as f:
        scripts_dict = json.loads(f.read())

    if script_name not in scripts_dict:
        return False

    del scripts_dict[script_name]

    with open(GLOBAL_SCRIPTS_PATH, "w") as f:
        f.write(json.dumps(scripts_dict, indent=4))

    return True
