import curses
import os
import json
import omg.core.repositories
from omg.core.git import exec as git_exec
from omg.modules import call_module
from typing import List
import argparse
import sys

OPTIONS = ["run", "edit", "pull", "origin", "rename", "tag", "script", "readme", "rm"]


def safe_addstr(stdscr, y, x, text, attr=curses.A_NORMAL):
    height, width = stdscr.getmaxyx()
    if y < 0 or y >= height or x >= width:
        return
    truncated = text[:width - x]
    try:
        stdscr.addstr(y, x, truncated, attr)
    except curses.error:
        pass


def get_commits_status(repository_path: str) -> str:
    if not repository_path or not os.path.exists(repository_path):
        return "path not found"
    try:
        return_code, branch = git_exec("rev-parse --abbrev-ref HEAD", repository_path, True)
        if return_code is not None:
            return "unknown"
        branch = branch.strip()
        if not branch or branch == "HEAD":
            return "detached HEAD"

        return_code, counts = git_exec(
            f"rev-list --left-right --count origin/{branch}...HEAD",
            repository_path, True,
        )
        if return_code is not None:
            return "no upstream"

        parts = counts.strip().split("\t")
        if len(parts) == 2:
            behind, ahead = int(parts[0]), int(parts[1])
            if behind == 0 and ahead == 0:
                return "up to date"
            status_parts = []
            if behind > 0:
                status_parts.append(f"{behind} behind")
            if ahead > 0:
                status_parts.append(f"{ahead} ahead")
            return ", ".join(status_parts)
        return "unknown"
    except Exception:
        return "unknown"


def draw_list_screen(stdscr, filtered_names, selected_idx, scroll_offset,
                     search_query, search_mode, tag_query, tag_mode):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    safe_addstr(stdscr, 0, 0, "oh-my-git - Repository List", curses.A_BOLD)

    max_display = height - 3
    for i in range(scroll_offset, min(scroll_offset + max_display, len(filtered_names))):
        name = filtered_names[i]
        display = f"  {name}"
        row = i - scroll_offset + 2
        if i == selected_idx:
            safe_addstr(stdscr, row, 0, display, curses.A_REVERSE)
        else:
            safe_addstr(stdscr, row, 0, display)

    if search_mode:
        curses.curs_set(1)
        safe_addstr(stdscr, height - 1, 0, f"/{search_query}")
        try:
            stdscr.move(height - 1, len(search_query) + 1)
        except curses.error:
            pass
    elif tag_mode:
        curses.curs_set(1)
        safe_addstr(stdscr, height - 1, 0, f":{tag_query}")
        try:
            stdscr.move(height - 1, len(tag_query) + 1)
        except curses.error:
            pass
    else:
        curses.curs_set(0)
        status = f"{len(filtered_names)} repos | Up/Down: navigate | Enter: details | /: name filter | : tag filter | q: quit"
        if search_query:
            status = f"Name: '{search_query}' | " + status
        if tag_query:
            status = f"Tags: '{tag_query}' | " + status
        safe_addstr(stdscr, height - 1, 0, status)

    stdscr.refresh()


def draw_detail_screen(stdscr, name, data, selected_option):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = 0
    safe_addstr(stdscr, y, 0, f"Repository: {name}", curses.A_BOLD); y += 1
    safe_addstr(stdscr, y, 0, f"  Author:  {data.get('author', 'N/A')}"); y += 1
    safe_addstr(stdscr, y, 0, f"  Path:    {data.get('path', 'N/A')}"); y += 1
    safe_addstr(stdscr, y, 0, f"  Origin:  {data.get('origin', 'N/A')}"); y += 1
    tags = data.get('tags') or []
    safe_addstr(stdscr, y, 0, f"  Tags:    {', '.join(tags) if tags else 'none'}"); y += 1
    icons = data.get('icons') or []
    safe_addstr(stdscr, y, 0, f"  Icons:   {' '.join(icons) if icons else 'none'}"); y += 1

    behind_ahead = get_commits_status(data.get('path', ''))
    safe_addstr(stdscr, y, 0, f"  Sync:    {behind_ahead}"); y += 2

    safe_addstr(stdscr, y, 0, "Actions:", curses.A_BOLD); y += 1
    for i, option in enumerate(OPTIONS):
        if i == selected_option:
            safe_addstr(stdscr, y + i, 0, f"  > {option}", curses.A_REVERSE)
        else:
            safe_addstr(stdscr, y + i, 0, f"    {option}")

    safe_addstr(stdscr, height - 1, 0, "Up/Down: navigate | Enter: select | Backspace: back | q: quit")
    curses.curs_set(0)
    stdscr.refresh()


def select_script(stdscr, alias: str) -> str:
    scripts = omg.core.repositories.get_scripts(alias)
    if not scripts:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        safe_addstr(stdscr, 0, 0, f"No scripts available for '{alias}'", curses.A_BOLD)
        safe_addstr(stdscr, height - 1, 0, "Press any key to go back")
        stdscr.refresh()
        stdscr.getch()
        return None

    selected = 0
    scroll_offset = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        safe_addstr(stdscr, 0, 0, f"Scripts for '{alias}'", curses.A_BOLD)

        max_display = height - 3
        if selected < scroll_offset:
            scroll_offset = selected
        elif selected >= scroll_offset + max_display:
            scroll_offset = selected - max_display + 1

        for i in range(scroll_offset, min(scroll_offset + max_display, len(scripts))):
            row = i - scroll_offset + 2
            if i == selected:
                safe_addstr(stdscr, row, 0, f"  > {scripts[i]}", curses.A_REVERSE)
            else:
                safe_addstr(stdscr, row, 0, f"    {scripts[i]}")

        safe_addstr(stdscr, height - 1, 0, "Up/Down: navigate | Enter: run | Backspace/Esc: cancel")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif key == curses.KEY_DOWN:
            selected = min(len(scripts) - 1, selected + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            return scripts[selected]
        elif key in (curses.KEY_BACKSPACE, 127, 8, 27):
            return None


def call_option(stdscr, option, alias):
    curses.def_prog_mode()
    curses.endwin()
    should_exit = True

    try:
        if option == "rename":
            new_name = input(f"Enter new name for '{alias}': ").strip()
            if new_name:
                mode = input("Mode: (a)lias only [default], (d)irectory only, (f)ull: ").strip().lower()
                args = [alias, new_name]
                if mode == 'd':
                    args.append('-d')
                elif mode == 'f':
                    args.append('-f')
                call_module("rename", args)
        elif option == "tag":
            action = input("Action: (a)dd [default], (r)emove: ").strip().lower()
            tags_input = input("Tags (space-separated): ").strip()
            tags = tags_input.split() if tags_input else []
            if tags:
                args = [alias]
                args.append("--remove" if action == 'r' else "--add")
                args.extend(tags)
                call_module("tag", args)
        elif option == "run":
            script = select_script(stdscr, alias)
            if script:
                try:
                    call_module("run", [alias, script])
                except SystemExit:
                    pass
                except Exception as e:
                    print(f"Error: {e}")
            else:
                should_exit = False
        elif option == "script":
            action = input("Action: (a)dd [default], (r)emove: ").strip().lower()
            global_mode = input("Global script? (y/N): ").strip().lower() == 'y'
            if action == 'r':
                script_name = input("Script name to remove: ").strip()
                if script_name:
                    args = [alias, "--remove", script_name]
                    if global_mode:
                        args.append("-g")
                    call_module("script", args)
            else:
                script_name = input("Script name: ").strip()
                script_command = input("Script command: ").strip()
                if script_name and script_command:
                    args = [alias, "--add", script_name, script_command]
                    if global_mode:
                        args.append("-g")
                    call_module("script", args)
        elif option == "readme":
            call_module("readme", [alias])
        elif option == "origin":
            call_module("origin", [alias])
        elif option == "rm":
            confirm = input(f"Remove '{alias}' from omg? (y/N): ").strip().lower()
            if confirm == 'y':
                call_module("rm", [alias])
        else:
            call_module(option, [alias])
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error: {e}")

    if should_exit:
        curses.reset_prog_mode()
        stdscr.keypad(True)
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        return True

    curses.reset_prog_mode()
    stdscr.keypad(True)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    return False


def tui_main(stdscr, repositories):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    screen = "list"
    selected_idx = 0
    scroll_offset = 0
    selected_option = 0
    search_query = ""
    search_mode = False
    tag_query = ""
    tag_mode = False
    current_repo = None

    while True:
        repositories = omg.core.repositories.get_repositories()

        if screen == "list":
            # filter by name
            filtered_names = [name for name in repositories.keys()
                              if search_query.lower() in name.lower()]

            # filter by tags (repo must have ALL specified tags)
            if tag_query:
                wanted_tags = set(tag_query.split())
                filtered_names = [
                    name for name in filtered_names
                    if wanted_tags <= set(repositories[name].get("tags") or [])
                ]

            if not filtered_names:
                selected_idx = 0
                scroll_offset = 0
            else:
                if selected_idx >= len(filtered_names):
                    selected_idx = len(filtered_names) - 1
                if selected_idx < 0:
                    selected_idx = 0

            height, _ = stdscr.getmaxyx()
            max_display = height - 3
            if selected_idx < scroll_offset:
                scroll_offset = selected_idx
            elif selected_idx >= scroll_offset + max_display:
                scroll_offset = selected_idx - max_display + 1

            draw_list_screen(stdscr, filtered_names, selected_idx, scroll_offset,
                             search_query, search_mode, tag_query, tag_mode)

            key = stdscr.getch()

            if search_mode:
                if key in (curses.KEY_ENTER, 10, 13):
                    search_mode = False
                elif key in (curses.KEY_BACKSPACE, 127, 8):
                    search_query = search_query[:-1]
                elif key == 27:  # Escape
                    search_mode = False
                    search_query = ""
                elif 32 <= key <= 126:
                    search_query += chr(key)
            elif tag_mode:
                if key in (curses.KEY_ENTER, 10, 13):
                    tag_mode = False
                elif key in (curses.KEY_BACKSPACE, 127, 8):
                    tag_query = tag_query[:-1]
                elif key == 27:  # Escape
                    tag_mode = False
                    tag_query = ""
                elif 32 <= key <= 126:
                    tag_query += chr(key)
            else:
                if key == curses.KEY_UP:
                    selected_idx = max(0, selected_idx - 1)
                elif key == curses.KEY_DOWN:
                    selected_idx = min(len(filtered_names) - 1, selected_idx + 1) if filtered_names else 0
                elif key == ord('/'):
                    search_mode = True
                    search_query = ""
                elif key == ord(':'):
                    tag_mode = True
                    tag_query = ""
                elif key in (curses.KEY_BACKSPACE, 127, 8):
                    search_query = ""
                    tag_query = ""
                elif key in (curses.KEY_ENTER, 10, 13):
                    if filtered_names:
                        current_repo = filtered_names[selected_idx]
                        screen = "detail"
                        selected_option = 0
                elif key == ord('q'):
                    break

        elif screen == "detail":
            if current_repo not in repositories:
                screen = "list"
                continue

            data = repositories[current_repo]
            draw_detail_screen(stdscr, current_repo, data, selected_option)

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_option = max(0, selected_option - 1)
            elif key == curses.KEY_DOWN:
                selected_option = min(len(OPTIONS) - 1, selected_option + 1)
            elif key in (curses.KEY_ENTER, 10, 13):
                option = OPTIONS[selected_option]
                should_exit = call_option(stdscr, option, current_repo)
                if should_exit:
                    break
                repositories = omg.core.repositories.get_repositories()
                if current_repo not in repositories:
                    screen = "list"
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                screen = "list"
            elif key == ord('q'):
                break


def entrypoint(argv: List[str]) -> None:
    parser = argparse.ArgumentParser(
                        prog='omg tui',
                        description='omg tui starts a terminal user interface to browse and manage repositories.',
                        epilog="See 'omg --help' to get further help")

    args = parser.parse_args(argv)

    repositories = omg.core.repositories.get_repositories()

    if not repositories:
        print("No repositories registered. Use 'omg clone' or 'omg find' to add repositories.")
        sys.exit(0)

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    try:
        tui_main(stdscr, repositories)
    except KeyboardInterrupt:
        pass
    finally:
        curses.curs_set(1)
        stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
