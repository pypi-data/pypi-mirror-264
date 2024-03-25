import glob

from typing import List, Union
from pathlib import Path

from .string_utils import split_str

def resolve_paths(paths:Union[str, List[str]],
                  sep:str=","):
    if isinstance(paths, str):
        paths = split_str(paths, sep=sep, strip=True, remove_empty=True)
        return resolve_paths(paths, sep=sep)
    resolved_paths = []
    for path in paths:
        if "*" in path:
            resolved_paths.extend(glob.glob(path))
        else:
            resolved_paths.append(path)
    return resolved_paths

