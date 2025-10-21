from modules import call_module
import core.exceptions as exceptions
from core.tui.components import LOG_ERROR,MODULE_NOT_FOUND_MESSAGE,MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE
from typing import List
import sys

def main(argv : List[str])->None:
    if len(argv) == 1:
        print("display help")
    else:
        call_module_safely = exceptions.make_safe(call_module)
        call_module_safely(argv[1],argv[2:])

if __name__ == "__main__":
    main(sys.argv)