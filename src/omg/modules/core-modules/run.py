from omg.core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                LOG_WARNING,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from omg.core.tui.colors import blue,green,yellow,red
from omg.core.exceptions import RepositoryDoesNotExistsException,__OMG_Exception
import omg.core.repositories
from typing import List
import omg.core.config
import argparse
import json
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg run',
                        description="omg run allows you to run scripts in a repository.",
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="select the repository by its alias",type=str,default=None)
    parser.add_argument("script",help="select the script you want to run",type=str,default=None)
    parser.add_argument("-G","--global",help="use a global script",action="store_true")

    # parse argv
    args = parser.parse_args(argv)

    # check if repository exists
    if omg.core.repositories.check_repository(args.repository_alias):
        repository = omg.core.repositories.get_repository(args.repository_alias)
        scripts_file_path = os.path.join(repository["path"],".omg/scripts.json")
        
        # check if the script file exists
        if os.path.isfile(scripts_file_path):
            with open(scripts_file_path,"r") as f:
                raw_content = f.read()
                scripts_dict = json.loads(raw_content)

                # check if the requested script exists 
                if args.script in scripts_dict:
                    os.chdir(repository["path"])
                    command = scripts_dict[args.script]
                    os.system(command)

                else:
                    raise __OMG_Exception(f"There are no script named '{args.script}' available for the repository '{args.repository_alias}'")
                    
        else:
            raise __OMG_Exception(f"There are no scripts available for the repository '{args.repository_alias}'")

    else:
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))