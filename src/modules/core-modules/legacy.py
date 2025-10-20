import argparse
from os import getcwd
from sys import exit
from typing import List

from core.exceptions import RepositoryNotFoundException
from core.git import exec
from core.repositories import check_repository, get_repositories
from core.tui.components import LOG_ERROR


def check_args(args: argparse.Namespace) -> str:
    repository_proxy = (
        args.alias
        if args.alias != None
        else args.path if args.path != None else getcwd()
    )

    repository_path = check_repository(repository_proxy)
    if repository_path:
        return repository_path
    else:
        raise RepositoryNotFoundException(repository_proxy)


def execute(cmd: str,path : str) -> None:
    error_code, _ = exec(f"{cmd}",path)
    exit(error_code != None)


def entrypoint(argv: List[str]) -> None:
    # init parser
    parser = argparse.ArgumentParser(
        prog="omg-legacy",
        description="omg legacy enables you to execute a git command on a certain repository",
        epilog="See 'omg --help' to get further help",
    )
    location_group = parser.add_mutually_exclusive_group()

    location_group.add_argument(
        "-a",
        "--alias",
        help="select the target repository from its alias",
        type=str,
    )
    location_group.add_argument(
        "-p",
        "--path",
        help="select the target repository from its path",
        type=str,
    )
    parser.add_argument(
        "command",
        help="the git command to execute",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="disable verbose"
    )

    # parsing the arguments
    args = parser.parse_args(argv)

    try:
        repository_path = check_args(args)
        execute(args.command,repository_path)
    except RepositoryNotFoundException as e:
        LOG_ERROR("The repository identified by " + e.args[0] + " is not found.")
        exit(1)
