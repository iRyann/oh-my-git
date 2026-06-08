from omg.modules import call_module
import omg.core.exceptions as exceptions
from omg.core.tui.components import LOG_ERROR,MODULE_NOT_FOUND_MESSAGE,MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE
from typing import List
import sys

def main()->None:
    argv = sys.argv
    
    call_module_safely = exceptions.make_safe(call_module)

    if len(argv) == 1 or argv[1] == "--help":
        call_module_safely("help",[])
    else:
        call_module_safely(argv[1],argv[2:])

if __name__ == "__main__":
    main()