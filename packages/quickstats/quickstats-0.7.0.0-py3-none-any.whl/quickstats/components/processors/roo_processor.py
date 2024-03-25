from typing import Optional, List, Dict, Union
import os
import glob
import json
import time
import ROOT

from .builtin_methods import BUILTIN_METHODS
from .actions import *
from .roo_process_config import RooProcessConfig

from quickstats import Timer, AbstractObject, PathManager
from quickstats.interface.root import TFile, RDataFrame, RDataFrameBackend
from quickstats.utils.root_utils import declare_expression, close_all_root_files, set_cachedir

class RooProcessor(AbstractObject):

    @property
    def distributed(self):
        return self.backend != RDataFrameBackend.DEFAULT
        
    def __init__(self, config_source:Optional[Union[RooProcessConfig, str]]=None,
                 config_text:Optional[str]=None,
                 flags:Optional[List[str]]=None,
                 backend:Optional[str]=None,
                 backend_options:Optional[Dict]=None,
                 multithread:bool=True,
                 cache:bool=False,
                 use_template:bool=False,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        self.cache = cache
        self.action_tree = None
        if flags is not None:
            self.flags = list(flags)
        else:
            self.flags = []
        self.rdf_frames = {}
        self.rdf = None
        self.global_variables = {}
        self.external_variables = {}
        self.default_treename = None
        self.use_template = use_template
        self.multithread = multithread
        if backend is None:
            self.backend = RDataFrameBackend.DEFAULT
        else:
            self.backend = RDataFrameBackend.parse(backend)
        self.backend_options = backend_options
        
        self.load_buildin_functions()
        
        if multithread:
            ROOT.EnableImplicitMT()
        
        if config_source is not None:
            self.load_config(config_source)
            
    def set_cache(self, cache:bool=True):
        self.cache = cache
        
    def set_remote_cachedir(self, cachedir:Optional[str]=None):
        self.set_cachedir(cachedir, forcecache=True)
            
    def load_buildin_functions(self):
        # bug of redefining module from ROOT
        try:
            import ROOT
            Internal = ROOT.Internal
        except:
            Internal = None
        distributed = self.distributed
        for name, definition in BUILTIN_METHODS.items():
            declare_expression(definition, name, distributed=distributed)
        if Internal is not None:
            if Internal != ROOT.Internal:
                ROOT.Internal = Internal
    
    def load_config(self, config_source:Union[RooProcessConfig, str]):
        if isinstance(config_source, RooProcessConfig):
            config = config_source
        else:
            config = RooProcessConfig.open(config_source)
        self.config = config
        action_tree = config.get_action_tree()
        action_tree.construct_actions(rdf_backend=self.backend)
        if not action_tree.root_node.has_child:
            raise RuntimeError("no actions found in the process card")
        first_action = action_tree.root_node.first_child.action
        if isinstance(first_action, RooProcTreeName):
            self.default_treename = first_action._params['treename']
        else:
            self.default_treename = None
        self.action_tree = action_tree
        
    def set_global_variables(self, **kwargs):
        self.global_variables.update(kwargs)
        
    def clear_global_variables(self):
        self.global_variables = {}
    
    def add_flags(self, flags:List[str]):
        self.flags += list(flags)
        
    def set_flags(self, flags:List[str]):
        self.flags = list(flags)        
        
    def cleanup(self, deepclean:bool=True):
        close_all_root_files()
        if deepclean:
            self.rdf_frames = {}
            self.rdf = None
            
    def shallow_cleanup(self):
        self.cleanup(deepclean=False)
    
    def run_action(self, action:RooProcBaseAction):
        if not self.rdf:
            raise RuntimeError("RDataFrame instance not initialized")
        if isinstance(action, RooProcRDFAction):
            self.rdf = action.execute(self.rdf, self.global_variables)
        elif isinstance(action, RooProcHelperAction):
            action.execute(self, self.global_variables)
        elif isinstance(action, RooProcHybridAction):
            self.rdf, _ = action.execute(self.rdf, self, self.global_variables)
        elif isinstance(action, RooProcNestedAction):
            return_code = action.execute(self, self.global_variables)
            return return_code
        else:
            raise RuntimeError("unknown action type")
        return RooProcReturnCode.NORMAL
            
    def run_all_actions(self, consider_child:bool=True):
        if not self.action_tree:
            raise RuntimeError("action tree not initialized")
        node = self.action_tree.get_next(consider_child=consider_child)
        if node is not None:
            self.stdout.debug(f'Executing node "{node.name}" defined at line {node.data["start_line_number"]}')
            action = node.action
            return_code = self.run_action(action)
            if return_code == RooProcReturnCode.NORMAL:
                self.run_all_actions()
            elif return_code == RooProcReturnCode.SKIP_CHILD:
                self.run_all_actions(consider_child=False)
            else:
                raise RuntimeError("unknown return code")
        else:
            self.stdout.debug('All node executed')
            
    def sanity_check(self):
        if not self.action_tree:
            raise RuntimeError("action tree not initialized")        
        if not self.action_tree.root_node.has_child:
            self.stdout.warning("No actions to be performed.")
            return None

    def load_rdataframe(self,
                        filenames:Union[List[str], str],
                        treename:Optional[str]=None):
        if treename is None:
            treename = self.default_treename
        if treename is None:
            raise RuntimeError("treename is undefined")
        filenames = TFile.list_files(filenames, resolve_cache=True)
        if not filenames:
            self.stdout.info('No files to be processed. Skipped.')
            return None
        if len(filenames) == 1:
            self.stdout.info(f'Processing file "{filenames[0]}".')
        else:
            self.stdout.info("Professing files")
            for filename in filenames:
                self.stdout.info(f'  "{filename}"', bare=True)
        rdf = RDataFrame.from_files(filenames, treename=treename,
                                    backend=self.backend,
                                    backend_options=self.backend_options,
                                    multithread_safe=self.multithread)
        self.rdf = rdf
        return self
    
    def run(self, filenames:Optional[Union[List[str], str]]=None):
        self.sanity_check()
        with Timer() as t:
            if filenames is not None:
                self.load_rdataframe(filenames)
            self.action_tree.reset()
            self.run_all_actions()
            self.shallow_cleanup()
        self.stdout.info(f"Task finished. Total time taken: {t.interval:.3f} s.")
        return self
        
    def awkward_array(self, frame:Optional[str]=None,
                       columns:Optional[List[str]]=None):
        if frame is None:
            rdf = self.rdf
        else:
            rdf = self.rdf_frames.get(frame, None)
        if rdf is None:
            raise RuntimeError('RDataFrame instance not initialized')
        return RDataFrame._awkward_array(rdf, columns=columns)