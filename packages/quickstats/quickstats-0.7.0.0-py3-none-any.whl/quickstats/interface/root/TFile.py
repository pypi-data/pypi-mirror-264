from typing import Optional, Union, List, Dict
import os
import re
import glob

import numpy as np

from quickstats import semistaticmethod
from quickstats.utils.path_utils import resolve_paths
from quickstats.utils.root_utils import get_cachedir, set_cachedir, is_corrupt
from .TObject import TObject

class TFile(TObject):

    FILE_PATTERN = re.compile(r"^.+\.root(?:\.\d+)?$")

    def __init__(self, source:Union[str, "ROOT.TFile"],
                 **kwargs):
        super().__init__(source=source, **kwargs)

    def initialize(self, source:Union[str, "ROOT.TFile"]):
        self.obj = self._open(source)
        
    @staticmethod
    def is_corrupt(f:Union["ROOT.TFile", str]):
        return is_corrupt(f)

    @semistaticmethod
    def _is_valid_filename(self, filename:str):
        return self.FILE_PATTERN.match(filename) is not None
    
    @semistaticmethod
    def _requires_protocol(self, filename:str):
        return "://" in filename
    
    @semistaticmethod
    def _resolve_cached_remote_paths(self, paths:List[str]):
        import ROOT
        cachedir = get_cachedir()
        if cachedir is None:
            return list(paths)
        resolved_paths = []
        for path in paths:
            url = ROOT.TUrl(path)
            # skip local file
            if url.GetProtocol() == "file":
                resolved_paths.append(path)
                continue
            filename = url.GetFile().lstrip("/")
            cache_path = os.path.join(cachedir, filename)
            if os.path.exists(cache_path):
                resolved_paths.append(cache_path)
            else:
                resolved_paths.append(path)
        return resolved_paths    

    @semistaticmethod
    def list_files(self, paths:Union[List[str], str],
                   strict_format:Optional[bool]=True,
                   resolve_cache:bool=False):
        paths = resolve_paths(paths)
        filenames = []
        # expand directories if necessary
        for path in paths:
            if os.path.isdir(path):
                filenames.extend(glob.glob(os.path.join(path, "*")))
            else:
                filenames.append(path)
        if strict_format:
            filenames = [filename for filename in filenames if self._is_valid_filename(filename)]
        if not filenames:
            return []
        if resolve_cache:
            filenames = self._resolve_cached_remote_paths(filenames)        
        import ROOT
        invalid_filenames = []
        for filename in filenames:
            if self._requires_protocol(filename):
                continue
            try:
                rfile = ROOT.TFile(filename)
                if self.is_corrupt(rfile):
                    invalid_filenames.append(filename)
            except:
                invalid_filenames.append(filename)
        if invalid_filenames:
            fmt_str = "\n".join(invalid_filenames)
            raise RuntimeError(f'Found empty/currupted file(s):\n{fmt_str}')
        return filenames
    
    @staticmethod
    def _open(source:Union[str, "ROOT.TFile"]):
        # source is path to a root file
        if isinstance(source, str):
            import ROOT
            source = ROOT.TFile(source)
            
        if TFile.is_corrupt(source):
            raise RuntimeError(f'empty or currupted root file: "{source.GetName()}"')
            
        return source
        
    """
    def make_branches(self, branch_data):
        branches = {}
        return branches
    
    def fill_branches(self, treename:str, branch_data):
        if self.obj is None:
            raise RuntimeError("no active ROOT file instance defined")
        tree = self.obj.Get(treename)
        if not tree:
            raise RuntimeError(f"the ROOT file does not contain the tree named \"{treename}\"")
        n_entries = tree.GetEntriesFast()
        
        for i in range(n_entries):
            for branch in branches:
                
        tree.SetDirectory(self.obj)
        # save only the new version of the tree
        tree.GetCurrentFile().Write("", ROOT.TObject.kOverwrite)
    """
    
    def get_tree(self, name:str, strict:bool=True):
        tree = self.obj.Get(name)
        if not tree:
            if strict:
                raise RuntimeError(f'In TFile.Get: Tree "{name}" does not exist')
            return None
        return tree

    @semistaticmethod
    def fetch_remote_file(self, name:str,
                          cachedir:str="/tmp",
                          forcecache:bool=False):
        if not self._requires_protocol(name):
            self.stdout.warning(f"Not a remote file: {name}. Skipping.")
            return None
        import ROOT
        set_cachedir(cachedir, forcecache=True)
        ROOT.TFile.Open(name)
        set_cachedir(cachedir, forcecache=False)
        
    @semistaticmethod
    def fetch_remote_files(self, names:List[str],
                           cachedir:str="/tmp",
                           forcecache:bool=False):
        for name in names:
            self.fetch_remote_file(name, cachedir=cachedir,
                                   forcecache=forcecache)

    def close(self):
        self.obj.Close()
        self.obj = None