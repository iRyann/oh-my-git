from omg.core.exceptions import ModuleNotFoundException
from omg.modules import call_module, list_modules
from omg.core.tui.colors import blue
from typing import List
import argparse

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg help',
                        description='omg help allows you display specific help about omg modules')

    # add arguments
    parser.add_argument("modules",
                        help="choose the starting paths of the research",
                        nargs="*",
                        type=str,
                        default=None)
    
    # parse argv
    args = parser.parse_args(argv)

    modules_list = list_modules()
    target_modules_list = modules_list

    # target modules mode
    if args.modules:
        target_modules_list = []

        # check if all modules exist
        for module in args.modules:
            target_modules_list.append(module)
            if module not in modules_list:
                raise ModuleNotFoundException(module)

    for module in target_modules_list:
        print(f'\nomg {blue(module)}\n')
        try:
            call_module(module,["--help"])
        except SystemExit:
            pass
        print("-"*20)