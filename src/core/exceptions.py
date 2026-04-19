from typing import List
from os import environ
from sys import exit as sys_exit
from core.tui.components import LOG_ERROR, LOG_WARNING, LOG_DEV_WARNING
import core.tui.components
from enum import Enum

# exception types
class ExceptionType(Enum):
    ERROR = 0
    WARNING = 1

# function allowing default exception handling
def make_safe(function : callable, resolve : callable = None) -> callable:
    def safe_function(*args : any):
        try:
            return function(*args)

        except __OMG_Exception as exception:
            match exception.exception_type:
                case ExceptionType.ERROR:
                    LOG_ERROR(exception)

                case ExceptionType.WARNING:
                    LOG_WARNING(exception)

                case _:
                    LOG_DEV_WARNING(exception)
                    sys_exit(1)
                
            if exception.is_fatal:
                sys_exit(1)
            elif resolve != None:
                return resolve(exception)

        except Exception as exception: 
            LOG_ERROR(f"The following error occured : {exception}")
            sys_exit(1)

    return safe_function

class __OMG_Exception(Exception):
    def __init__(self : Exception, message : str,exception_type = ExceptionType.ERROR, is_fatal: bool = True) -> Exception:
        super().__init__(message)
        self.message = message
        self.exception_type = exception_type
        self.is_fatal = is_fatal

    def __str__(self) -> str:
        return self.message

class ModuleNotFoundException(__OMG_Exception):
    def __init__(self,module_name : str):
        super().__init__(core.tui.components.MODULE_NOT_FOUND_MESSAGE(module_name),
                        ExceptionType.ERROR)
        self.module_name = module_name

class ModuleEntryPointNotFoundException(__OMG_Exception):
    def __init__(self,module_name : str):
        super().__init__(core.tui.components.MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(module_name),
                        ExceptionType.ERROR)

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

class PathDoesNotExistException(__OMG_Exception):
    def __init__(self,path : str):
        super().__init__(core.tui.components.PATH_DOES_NOT_EXIST_MESSAGE(path),
                        ExceptionType.ERROR)