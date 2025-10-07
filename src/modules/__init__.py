from os.path import dirname, basename, isfile, join
import core.exceptions as exceptions
from typing import List
import importlib
import glob
import sys

# updating the program's path
sys.path.append(dirname(__file__))
sys.path.append(join(dirname(__file__),"core-modules"))

# registering core modules files, then custom modules files
modules = glob.glob(join(dirname(__file__), "core-modules/*.py"))
modules += glob.glob(join(dirname(__file__), "*.py"))

# formating the data, removing .py suffix,  directories and __init__.py
modules = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


# call a module with arguments
def call_module(module_name : str,argv : List[str])->None:
    if module_name in modules:
        module = importlib.import_module(module_name)
        if "entrypoint" in dir(module):
            getattr(module,"entrypoint")(argv)
        else : raise exceptions.ModuleEntryPointNotFoundException(module_name)
    else:   raise exceptions.ModuleNotFoundException(module_name)

# retrieve the list of all modules
def list_modules()->List[str]:
    return modules