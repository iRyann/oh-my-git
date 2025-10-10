from typing import Tuple
import os

def exec(command: str, repository_path: str = None, capture: bool = False)->Tuple[int,str]:
    if repository_path:
        command = f'cd {repository_path}; git {command}'
    else:
        command = f'git {command}'
    
    if capture:
        pipe = os.popen(command,"r")
        buffer = pipe._stream.read()
        return_code = pipe.close()
    else:
        return_code = os.popen(command,"w").close()
        buffer = ""

    return return_code,buffer

def get_author(repository_path: str)->str:
    return_code, author = exec("show | grep Author",repository_path,True)
    author = author.split(": ")[1].split(" <")[0]
    return author