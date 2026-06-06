# theses functions colors the text according ANSI escape codes

def blue(string : str):
    return f"\x1b[0;36m{string}\x1b[0;0m"

def green(string : str):
    return f"\x1b[0;32m{string}\x1b[0;0m"

def yellow(string : str):
    return f"\x1b[0;33m{string}\x1b[0;0m"

def red(string : str):
    return f"\x1b[0;31m{string}\x1b[0;0m"