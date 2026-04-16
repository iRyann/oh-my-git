import argparse
import os
import sys
from typing import List

import core.repositories
from core.tui.colors import blue, green, yellow
from core.tui.components import LOG, LOG_WARNING


def entrypoint(argv: List[str]) -> None:
    # init parser
    parser = argparse.ArgumentParser(
        prog="omg-list",
        description="omg list allows you to list all the repositories registered in omg",
        epilog="See 'omg --help' to get further help",
    )

    # add arguments
    parser.add_argument(
        "-l",
        "--inline",
        help="display the repositories inline, with minimal informations",
        action="store_true",
    )
    parser.add_argument(
        "-n", "--names", help="filters the repositories by name", nargs="*", type=str
    )
    parser.add_argument(
        "-p", "--paths", help="filters the repositories by path", nargs="*", type=str
    )
    parser.add_argument(
        "-a",
        "--authors",
        help="filters the repositories by author",
        nargs="*",
        type=str,
    )
    parser.add_argument(
        "-t", "--tags", help="filters the repositories by tags", nargs="*", type=str
    )
    parser.add_argument(
        "-o",
        "--origins",
        help="filters the repositories by origin",
        nargs="*",
        type=str,
    )

    # parse argv
    args = parser.parse_args()

    # fetch repositories data
    repositories = core.repositories.get_repositories()

    if (
        args.names is None
        and args.authors is None
        and args.origin is None
        and args.tags is None
        and args.paths is None
    ):
        repositories_names = list(repositories.keys())
    else:
        repositories_names = core.repositories.get_repositories_filtered(
            args.names, args.authors, args.paths, args.origins, args.tags
        )
    # init buffer
    buffer = ""

    # format output -> inline
    if args.inline:
        for repository_name in repositories_names:
            tags = (
                ""
                if repositories[repository_name]["tags"] == None
                else f'\n\ttags: {" ".join(repositories[repository_name]["tags"])}'
            )
            buffer += f'{blue(repository_name)}\n\torigin: {repositories[repository_name]["origin"]}\n\tpath: {repositories[repository_name]["path"]}\n\tauthor: {repositories[repository_name]["author"]}{tags}\n'

    # format output -> ls style
    elif len(repositories_names):
        terminal_width, _ = os.get_terminal_size()
        max_len = max([len(repository_name) for repository_name in repositories_names])
        formatted_repositories_names = [
            (repository_name + " " * (4 + max_len - len(repository_name)))
            for repository_name in repositories_names
        ]

        number_of_records_per_line = terminal_width // (max_len + 4)
        number_of_lines = (
            1 + (len(formatted_repositories_names) * (max_len + 4)) // terminal_width
        )
        for i in range(1, number_of_lines):
            formatted_repositories_names[i * number_of_records_per_line - 1] += "\n"
        buffer = "".join(formatted_repositories_names)

    print(buffer + "\n")
    LOG(f"Displaying {len(repositories_names)} repositories")
