import os
import sys
import shlex

from typing import Optional

def add_python_path(path:str):
    """
    Add a path to the Python search path and the PYTHONPATH environment variable if not already present.
    
    Parameters:
    - path (str): Path to add.
    """
    if path not in sys.path:
        sys.path.insert(0, path)
    PYTHONPATH = os.environ.get("PYTHONPATH", "")
    if path not in PYTHONPATH.split(":"):
        os.enviro['PYTHONPATH'] = f"{path}:{PYTHONPATH}"

def remove_python_path(path:str):
    """
    Remove a path from the Python search path and the PYTHONPATH environment variable if present.
    """
    if path in sys.path:
        sys.path.remove(path)
    PYTHONPATHS = os.environ.get("PYTHONPATH", "").split(":")
    if path in PYTHONPATHS:
        PYTHONPATHS.remove(path)
        os.environ["PYTHONPATH"] = ":".join(PYTHONPATHS)

def set_argv(cmd: str, expandvars:bool=True):
    """
    Modifies sys.argv based on a given command line string.

    Parameters:
    - cmd (str): The command line string to parse into sys.argv.
    - expandvars (bool, optional): Whether to expand environment variables in cmd. Defaults to False.
    """
    if expandvars:
        cmd = os.path.expandvars(cmd)
    # Use shlex.split to correctly parse the command line string into arguments,
    # handling cases with quotes and escaped characters appropriately.
    parsed_args = shlex.split(cmd)
    sys.argv = parsed_args