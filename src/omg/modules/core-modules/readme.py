from omg.core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from omg.core.exceptions import RepositoryDoesNotExistsException
import omg.core.repositories
from typing import List
import argparse
import sys
import os

def find_readme(repository_path: str) -> str:
    for name in ["README.md", "README.rst", "README.txt", "README",
                 "readme.md", "readme.rst", "readme.txt", "readme"]:
        candidate = os.path.join(repository_path, name)
        if os.path.isfile(candidate):
            return candidate
    return None


def get_lexer(filename: str):
    from pygments.lexers import get_lexer_for_filename
    from pygments.lexers.markup import MarkdownLexer
    from pygments.util import ClassNotFound

    try:
        return get_lexer_for_filename(filename)
    except ClassNotFound:
        return MarkdownLexer()


def highlight_readme(content: str, filepath: str) -> str:
    from pygments import highlight
    from pygments.formatters import TerminalFormatter

    lexer = get_lexer(os.path.basename(filepath))
    return highlight(content, lexer, TerminalFormatter())


def entrypoint(argv: List[str]) -> None:
    parser = argparse.ArgumentParser(
                        prog='omg readme',
                        description='omg readme displays the README of a repository with syntax highlighting.',
                        epilog="See 'omg --help' to get further help")

    parser.add_argument("repository_alias", help="select the repository by its alias", type=str)

    args = parser.parse_args(argv)

    if not omg.core.repositories.check_repository(args.repository_alias):
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))

    repository = omg.core.repositories.get_repository(args.repository_alias)
    repository_path = repository["path"]

    readme_path = find_readme(repository_path)
    if not readme_path:
        LOG_ERROR(f"No README found in '{args.repository_alias}'")
        sys.exit(1)

    with open(readme_path, "r") as f:
        content = f.read()

    try:
        highlighted = highlight_readme(content, readme_path)
        print(highlighted, end="")
    except ImportError:
        print(content, end="")
