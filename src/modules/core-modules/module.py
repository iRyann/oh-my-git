from core.exceptions import ModuleNotFoundException
from modules import call_module, list_modules, list_core_modules
from core.tui.colors import blue, green, red, yellow
from typing import List
import argparse

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg module',
                        description='omg module allows you to manage omg modules')

    # add arguments
    parser.add_argument("modules",
                        help="select target modules",
                        nargs="*",
                        type=str,
                        default=None)
    

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-l","--list",
                        help="list modules",
                        action="store_true",
                        default=False)

    group.add_argument("-U","--update",
                        help="update target modules",
                        action="store_true",
                        default=False)

    group.add_argument("-D","--delete",
                        help="delete target modules",
                        action="store_true",
                        default=False)

    group.add_argument("-I","--install",
                        help="install module from git url",
                        type=str,
                        default=None)
    
    group.add_argument("-i","--info",
                        help="check informations about target modules",
                        action="store_true",
                        default=None)


    # parse argv
    args = parser.parse_args(argv)

    # retrieving the modules
    modules_list = list_modules()
    core_modules_list = list_core_modules()
    target_modules_list = modules_list

    # listing the modules
    if args.list:
        for module in modules_list:
            if module in core_modules_list:
                print(f'\t{module} ({blue("core")})')
            else:
                print(f"\t{module}")

    # target modules mode
    elif args.modules:
        target_modules_list = []

        # check if all modules exist
        for module in args.modules:
            target_modules_list.append(module)
            if module not in modules_list:
                raise ModuleNotFoundException(module)

        for module in target_modules_list:
            if args.info:
                print(module)