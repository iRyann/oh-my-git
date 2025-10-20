from typing import List
from os import environ
from sys import exit as sys_exit
from core.tui.components import LOG_ERROR, LOG_WARNING, LOG_DEV_INFO, LOG_DEV_WARNING
import core.tui.components
from enum import Enum

# log level defined in env variables
LOG_LEVEL = environ["LOG_LEVEL"] if "LOG_LEVEL" in environ else 0

# exception levels
class ExceptionLevel(Enum):
    ERROR = 0
    WARNING = 1
    DEV_WARNING = 2
    DEV_INFO = 3

# function allowing default exception handling
def safe_call(function, args : List[any]) -> any:
    try:
        return function(args)

    except exception:
        if hasattr(exception,"__omg_exception"):
            if exception.error_level <= EX_WARNING or exception.error_level <= LOG_LEVEL:
                match exception.error_level:
                    case ExceptionLevel.ERROR:
                        LOG_ERROR(exception)
                        sys_exit(1)

                    case ExceptionLevel.WARNING:
                        LOG_WARNING(exception)

                    case ExceptionLevel.DEV_WARNING:
                        LOG_DEV_WARNING(exception)

                    case ExceptionLevel.DEV_INFO:
                        LOG_DEV_INFO(exception)

                    case _:
                        LOG_ERROR(exception)
                        sys_exit(1)

        else:
            LOG_ERROR(f"The following error occured : {exception}")
            sys_exit(1)

class __OMG_Exception(Exception):
    def __init__(self : Exception, message : str,error_level : int = 0) -> Exception:
        super().__init__(message)
        self.message = message
        self.__omg_exception = True
        self.error_level = error_level

    def __str__(self) -> str:
        return message

class ModuleNotFoundException(__OMG_Exception):
    def __init__(self,module_name : str):
        super().__init__(core.tui.components.MODULE_NOT_FOUND_MESSAGE(module_name),
                        ExceptionLevel.ERROR)

class ModuleEntryPointNotFoundException(__OMG_Exception):
    def __init__(self,module_name : str):
        super().__init__(core.tui.components.MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(module_name),
                        ExceptionLevel.ERROR)

class RepositoryAlreadyExistsException(__OMG_Exception):
    pass

class InvalidRepositoryDataStructureException(__OMG_Exception):
    pass

class RepositoryDoesNotExistsException(__OMG_Exception):
    pass

class SystemCallErrorException(__OMG_Exception):
    pass

class RepositoryNotFoundException(__OMG_Exception):
    pass
