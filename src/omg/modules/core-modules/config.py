from omg.core.tui.components import LOG, LOG_ERROR, LOG_WARNING
from omg.core.tui.colors import blue, green, yellow, red
import omg.core.config
from typing import List
import argparse
import sys


def entrypoint(argv: List[str]) -> None:
    parser = argparse.ArgumentParser(
                        prog='omg config',
                        description='omg config allows you to view and manage oh-my-git configuration.',
                        epilog="See 'omg --help' to get further help")

    parser.add_argument("--get", help="get the value of a config attribute", type=str)
    parser.add_argument("--set", help="set a config attribute", nargs=2, metavar=("KEY", "VALUE"))
    parser.add_argument("-l", "--list", help="list all config attributes", action="store_true")

    args = parser.parse_args(argv)

    if args.list:
        config = omg.core.config.CONFIG
        if not config:
            LOG_WARNING("Configuration is empty")
            return
        for key in sorted(config.keys()):
            print(f"{blue(key)} = {green(config[key])}")
        return

    if args.get:
        value = omg.core.config.get_config(args.get)
        if value == "":
            LOG_ERROR(f"Config attribute '{args.get}' does not exist")
            sys.exit(1)
        print(value)
        return

    if args.set:
        key, value = args.set
        omg.core.config.CONFIG[key] = value
        omg.core.config.save_config()
        LOG(f"Set {blue(key)} = {green(value)}")
        return

    # default: show all config
    config = omg.core.config.CONFIG
    if not config:
        LOG_WARNING("Configuration is empty")
        return
    for key in sorted(config.keys()):
        print(f"{blue(key)} = {green(config[key])}")
