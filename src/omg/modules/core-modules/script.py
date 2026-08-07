from omg.core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                LOG_WARNING,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from omg.core.exceptions import RepositoryDoesNotExistsException
import omg.core.repositories
from omg.core.tui.colors import blue,green,yellow,red
from typing import List
import argparse
import sys

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg script',
                        description='omg script allows you to add or remove scripts for repositories.',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="alias of the target repository",type=str)
    parser.add_argument("--add",help="add a script (name and command)",nargs=2,metavar=("NAME","COMMAND"),type=str)
    parser.add_argument("--remove",help="remove a script by name",type=str,metavar="NAME")
    parser.add_argument("-g","--global",help="add or remove a global script available for every repository",action="store_true",dest="is_global")

    # parse argv
    args = parser.parse_args(argv)

    if not args.add and not args.remove:
        LOG_ERROR("You must specify at least one of --add or --remove")
        sys.exit(1)

    if args.add and args.remove:
        LOG_ERROR("Cannot use --add and --remove at the same time")
        sys.exit(1)

    # global scripts don't require a repository alias
    if args.is_global:
        if args.add:
            script_name, script_command = args.add
            omg.core.repositories.add_global_script(script_name, script_command)
            LOG(f"Added global script '{green(script_name)}'")
        elif args.remove:
            if omg.core.repositories.remove_global_script(args.remove):
                LOG(f"Removed global script '{red(args.remove)}'")
            else:
                LOG_WARNING(f"Global script '{yellow(args.remove)}' does not exist")
        return

    # repository-local scripts require a valid repository
    if not omg.core.repositories.check_repository(args.repository_alias):
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))

    if args.add:
        script_name, script_command = args.add
        omg.core.repositories.add_script(args.repository_alias, script_name, script_command)
        LOG(f"Added script '{green(script_name)}' to '{blue(args.repository_alias)}'")
    elif args.remove:
        if omg.core.repositories.remove_script(args.repository_alias, args.remove):
            LOG(f"Removed script '{red(args.remove)}' from '{blue(args.repository_alias)}'")
        else:
            LOG_WARNING(f"Script '{yellow(args.remove)}' does not exist on '{blue(args.repository_alias)}'")
