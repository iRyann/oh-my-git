from core.tui.colors import blue,green,yellow,red

APP_NAME = "omg"

PROCEED_QUESTION_MESSAGE = "Do you still want to proceed to proceed ? Y/n : "

def MODULE_NOT_FOUND_MESSAGE(module_name : str):    return f"'{module_name}' is not an {APP_NAME} command. See '{APP_NAME} --help'\n\nIt may be because the associated module can not be found"

def MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(module_name : str):    return f"{APP_NAME}: the entrypoint of the module associated to '{module_name}' can not be found."

def ADDING_REPO_TO_REGISTER_MESSAGE(remote_url : str,alias: str, tags : str = None):
    return f'Adding {remote_url} to the repository register as {blue(alias)}{" with the tags " + green(" ".join(tags)) if tags != None else ""}'

def REPOSITORY_NAME_ALREADY_EXISTS_MESSAGE(alias : str):
    return f'An existing repositiory is already named {yellow(alias)}'

def LOG(message : str,color = blue)->None:
    print(f"[{color(APP_NAME)}]: {message}")

def LOG_WARNING(message : str)->None:
    LOG(message,yellow)

def LOG_ERROR(message : str)->None:
    LOG(message,red)

NEW_REPOSITORY_NAME_QUESTION_ALIAS = "Enter a new name for the repository : "