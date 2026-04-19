import glob
import sys
from os.path import basename, dirname, isfile, join

# updating the program's path
sys.path.append(dirname(__file__))

modules = glob.glob(join(dirname(__file__), "*.py"))

# formating the data, removing .py suffix,  directories and __init__.py
modules = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]
