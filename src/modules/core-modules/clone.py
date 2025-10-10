from core.tui.components import (
                                LOG,
                                LOG_WARNING,
                                ADDING_REPO_TO_REGISTER_MESSAGE,
                                REPOSITORY_NAME_ALREADY_EXISTS_MESSAGE,
                                NEW_REPOSITORY_NAME_QUESTION_ALIAS,
                                PROCEED_QUESTION_MESSAGE)
from core.exceptions import RepositoryAlreadyExistsException
import core.repositories
from typing import List
import core.git
import argparse
import sys

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg-clone',
                        description='omg clone allows you to use basic cloning features of git,\nwhile performing additionnal treatments to include the cloned repository in the oh-my-git workflow',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("remote_url",help="the url of the remote git repository to clone", type=str)
    parser.add_argument("-p","--path",help="set the path where the repository will be cloned",type=str)
    parser.add_argument("-a","--alias",help="set the the name of the repository",type=str)
    parser.add_argument("-t","--tags",help="set tags for the repository",nargs='*',type=str)

    # parse argv
    args = parser.parse_args(argv)
    
    # setting the default values
    if not args.path: args.path = args.remote_url.split("/")[-1].replace(".git","")
    if not args.alias: args.alias = args.remote_url.split("/")[-1].replace(".git","")
    
    # checking if the alias is available, handling the case if not
    proceed = core.repositories.check_repository(args.alias)
    while proceed:
        LOG_WARNING(REPOSITORY_NAME_ALREADY_EXISTS_MESSAGE(args.alias))
        try:
            proceed = input(PROCEED_QUESTION_MESSAGE) == "Y"
            if proceed:
                args.alias = input(NEW_REPOSITORY_NAME_QUESTION_ALIAS)
                proceed = core.repositories.check_repository(args.alias)
            else:
                sys.exit(0)                
        except:
            sys.exit(1)

    # calling git to clone the repo
    error_code,_ = core.git.exec(f"clone {args.remote_url} {args.path}")

    # exit with error 1 if popen.close() returns an error, (meaning 'git clone' failed)
    if(error_code != None): sys.exit(1)

    # adding the repos to the register
    LOG(ADDING_REPO_TO_REGISTER_MESSAGE(args.remote_url, args.alias,args.tags))

    author = core.git.get_author(args.path)
    
    core.repositories.add_repository(args.alias,{
        "author": author,
        "origin": args.remote_url,
        "path" : args.path,
        "tags" : args.tags
    })
    
    core.repositories.save_repositories()
