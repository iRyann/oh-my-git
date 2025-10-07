from typing import List
from git import Repo
import argparse

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

    # parse argv
    args = parser.parse_args(argv)
    
    # setting the default values
    if not args.path: args.path = args.remote_url.split("/")[-1].replace(".git","")
    if not args.alias: args.alias = args.remote_url.split("/")[-1].replace(".git","")
    
    Repo.clone_from(args.remote_url, args.path)

    