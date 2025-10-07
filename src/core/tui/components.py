APP_NAME = "omg"

def MODULE_NOT_FOUND_MESSAGE(module_name : str):    return f"{APP_NAME}: '{module_name}' is not an {APP_NAME} command. See '{APP_NAME} --help'\n\nIt may be because the associated module can not be found"
def MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(module_name : str):    return f"{APP_NAME}: the entrypoint of the module associated to '{module_name}' can not be found."