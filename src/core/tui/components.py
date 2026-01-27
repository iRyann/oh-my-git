from core.tui.colors import blue,green,yellow,red

APP_NAME = "omg"

PROCEED_QUESTION_MESSAGE = "Do you still want to proceed ? Y/n : "

def LOG(message : str,color = blue)->None:
    print(f"[{color(APP_NAME)}]: {message}")

def LOG_WARNING(message : str)->None:
    LOG(message,yellow)

def LOG_ERROR(message : str)->None:
    LOG(message,red)

def LOG_DEV(message : str,color = blue)->None:
    print(f'[{color(APP_NAME)}] <{color("DEV")}> : {message}')

def LOG_DEV_WARNING(message : str) -> None:
    LOG_DEV(message,yellow)

def LOG_DEV_INFO(message : str) -> None:
    LOG_DEV(message,green)

def MODULE_NOT_FOUND_MESSAGE(module_name : str) -> str:
    return f"'{module_name}' is not an {APP_NAME} command. See '{APP_NAME} --help'\n\nIt may be because the associated module can not be found."

def MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(module_name : str) -> str:    return f"{APP_NAME}: the entrypoint of the module associated to '{module_name}' can not be found."

def ADDING_REPO_TO_REGISTER_MESSAGE(remote_url : str,alias: str, tags : str = None) -> str:
    return f'Adding {remote_url} to the repository register as {blue(alias)}{" with the tags " + green(" ".join(tags)) if tags != None else ""}'

def REPOSITORY_NAME_ALREADY_EXISTS_MESSAGE(alias : str) -> str:
    return f'An existing repositiory is already named {yellow(alias)}'

NEW_REPOSITORY_NAME_QUESTION_ALIAS = "Enter a new name for the repository : "

def REPOSITORY_DOES_NOT_EXIST_MESSAGE(alias : str) -> str:
    return f"The repository '{alias}' does not exist."

def REPOSITORY_PULL_MESSAGE(alias: str, origin : str) -> str:
    return f"pulling from origin {origin} into the repository {blue(alias)}."

SYSTEM_CALL_ERROR_MESSAGE = "An error occured during a system call."