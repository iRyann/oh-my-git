import argparse
from os import getcwd
from sys import exit
from typing import List

from core.exceptions import RepositoryNotFoundException
from core.git import exec
from core.repositories import check_repository
from core.tui.components import LOG_ERROR


def entrypoint(argv: List[str]) -> None:
    # init parser
    parser = argparse.ArgumentParser(
        prog="omg-legacy",
        description="omg legacy enable to execute a git legacy command",
        epilog="See 'omg --help' to get further help",
    )
    location_group = parser.add_mutually_exclusive_group()

    location_group.add_argument(
        "-a",
        "--alias",
        help="set the alias of the target repository",
        type=str,
    )
    location_group.add_argument(
        "-p",
        "--path",
        help="set the path of the target repository",
        type=str,
    )
    parser.add_argument(
        "command",
        help="name of the legacy git command to execute",
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )

    args = parser.parse_args(argv)
    try:
        check_args(args)
        execute(args.command)
    except Exception :
        LOG_ERROR("Repository not found")
        exit(1)

def check_args(args: argparse.Namespace) -> bool:
    repository_proxy = (
        args.alias
        if args.alias != None
        else args.path if args.path != None else getcwd()
    )
    if check_repository(repository_proxy):
        return True
    else:
        raise RepositoryNotFoundException()


def execute(cmd: str) -> None:
    error_code, _ = exec(f"{cmd}")
    exit(error_code != None)
