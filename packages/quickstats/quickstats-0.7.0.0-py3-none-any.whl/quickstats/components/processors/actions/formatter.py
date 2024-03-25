import re

from quickstats.utils.string_utils import split_str

ListRegex = re.compile(r"\[([^\[\]]+)\]")

def ListFormatter(text:str):
    match = ListRegex.match(text)
    if not match:
        return [text]
    return split_str(match.group(1), sep=',', strip=True, remove_empty=True)