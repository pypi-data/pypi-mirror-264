from typing import Optional, List, Dict
import os
import re

from quickstats.utils.py_utils import get_required_args

class RooProcBaseAction(object):
    
    NAME = None
    PARAM_FORMATS = {}

    def __init__(self, **params):
        self._params = params
        self.executed = False
        self.status   = None
    
    @staticmethod
    def allow_multiline():
        return False

    @staticmethod
    def has_global_var(text:str):
        return re.search(r"\${(\w+)}", text) is not None
    
    def get_formatted_parameters(self, global_vars:Optional[Dict]=None):
        if global_vars is None:
            global_vars = {}
        formatted_parameters = {}
        for k,v in self._params.items():
            if v is None:
                formatted_parameters[k] = None
                continue
            k_literals = re.findall(r"\${(\w+)}", k)
            is_list = False
            if isinstance(v, list):
                v = '__SEPARATOR__'.join(v)
                is_list = True
            v_literals = re.findall(r"\${(\w+)}", v)
            all_literals = set(k_literals).union(set(v_literals))
            for literal in all_literals:
                if literal not in global_vars:
                    raise RuntimeError(f"the global variable `{literal}` is undefined")
            for literal in k_literals:
                substitute = global_vars[literal]
                k = k.replace("${" + literal + "}", str(substitute))
            for literal in v_literals:
                substitute = global_vars[literal]
                v = v.replace("${" + literal + "}", str(substitute))
            if is_list:
                v = v.split("__SEPARATOR__")
            formatted_parameters[k] = v
        for key, value in formatted_parameters.items():
            if key in self.PARAM_FORMATS:
                formatter = self.PARAM_FORMATS[key]
                formatted_parameters[key] = formatter(value)
        return formatted_parameters
    
    def makedirs(self, filename:str):
        dirname = os.path.dirname(filename)
        if dirname and (not os.path.exists(dirname)):
            os.makedirs(dirname)
    
    def execute(self, **params):
        raise NotImplementedError
    
    @classmethod
    def parse_as_list(cls, text:str):
        match = re.match(r"\[([^\[\]]+)\]", text)
        if not match:
            return [text]
        else:
            return match.group(1).split(",")
    
    @classmethod
    def parse_as_kwargs(cls, text:str):
        kwargs = {}
        text = re.sub(r"\s*", "", text)
        list_attributes = re.findall(r"(\w+)=\[([^\[\]]+)\]", text)
        for attribute in list_attributes:
            kwargs[attribute[0]] = attribute[1].split(",")
            text = text.replace(f"{attribute[0]}=[{attribute[1]}]","")
        attributes = re.findall(r"(\w+)=([^,]+)", text)
        for attribute in attributes:
            kwargs[attribute[0]] = attribute[1]
        for key, value in kwargs.items():
            if (not cls.has_global_var(value)) and (key in cls.PARAM_FORMATS):
                formatter = cls.PARAM_FORMATS[key]
                kwargs[key] = formatter(value)
        return kwargs
    
    @classmethod
    def parse(cls, main_text:str, block_text:Optional[str]=None):
        return cls()
        
    @classmethod
    def _try_create(cls, **kwargs):
        try:
            return cls(**kwargs)
        except Exception:
            argnames = get_required_args(cls)
            missing_argnames = list(set(argnames) - set(kwargs))
            raise ValueError(f'missing keyword argument(s) for the action "{cls.NAME}": '
                             f'{", ".join(missing_argnames)}')