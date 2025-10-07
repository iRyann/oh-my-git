from modules import call_module
import core.exceptions as exceptions
import core.tui.components
from typing import List
import sys

def main(argv : List[str])->None:
    if len(argv) == 1:
        print("display help")
    else:
        try:
            call_module(argv[1],argv[2:])
        except exceptions.ModuleNotFoundException:
            print(core.tui.components.MODULE_NOT_FOUND_MESSAGE(argv[1]))
            sys.exit(1)
        except exceptions.ModuleEntryPointNotFoundException:
            print(core.tui.components.MODULE_ENTRYPOINT_NOT_FOUND_MESSAGE(argv[1]))
            sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)