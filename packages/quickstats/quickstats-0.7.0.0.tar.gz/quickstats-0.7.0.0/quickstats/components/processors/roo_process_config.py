from typing import List, Optional
import os
import re

from quickstats import semistaticmethod, TVirtualNode, TVirtualTree, stdout
from quickstats.utils.string_utils import split_lines, split_str
from quickstats.interface.root import RDataFrameBackend

from .actions import RooProcBaseAction, RooProcNestedAction, get_action

def _get_action(name:str, rdf_backend:Optional[str]=None):
    if name.lower() == "alias":
        backend = RDataFrameBackend.parse(rdf_backend)
        if backend in [RDataFrameBackend.DASK, RDataFrameBackend.SPARK]:
            stdout.warning(f'{backend.name.title()} backend does not support the '
                           f'"{name.title()}" action. The "Define" action will be used instead.')
            name = "DEFINE"
    return get_action(name)

class ActionNode(TVirtualNode):
    
    def __init__(self, name:Optional[str]=None, level:Optional[int]=0,
                 parent:Optional["DomainNode"]=None,
                 **data):
        super().__init__(name=name, level=level,
                         parent=parent, **data)
        self.action = None
        
    def get_context(self):
        source = self.try_get_data("source", None)
        line_number = self.try_get_data("start_line_number", None)
        if source and line_number:
            context = f" (Line {line_number}, Source {source})"
        else:
            context = ""
        return context
        
    def construct_action(self, rdf_backend:Optional[str]=None):
        action_cls = _get_action(self.name, rdf_backend=rdf_backend)
        if action_cls is None:
            context = self.get_context()
            raise RuntimeError(f'Unknown action "{self.name}"{context}. '
                               f'Make sure to use start and end tags <Action> </Action> '
                               'to enclose a multiline block.')
        main_text  = self.get_data("main_text")
        block_text = self.get_data("block_text")
        action = action_cls.parse(main_text=main_text, block_text=block_text)
        self.action = action        
        
class ActionTree(TVirtualTree):
    
    NodeClass = ActionNode
    
    def construct_actions(self, rdf_backend:Optional[str]=None):
        self.reset()
        node = self.get_next()
        while node is not None:
            try:
                node.construct_action(rdf_backend=rdf_backend)
            except Exception as e:
                context = node.get_context()
                raise RuntimeError("failed to construct action for the instruction "
                                   f"{node.name}{context}. Error message: {e}") from e
            node = self.get_next()
        self.reset()

class RooConfigLine(object):
    
    def __init__(self, text:str, line_number:int):
        self.text = text
        self.line_number = line_number
        self.start_tag = self.get_start_tag()
        if self.start_tag:
            self.end_tag = None
        else:
            self.end_tag = self.get_end_tag()
    
    def get_start_tag(self):
        result = re.search(r"^\s*<(?!/)([^>]+)>\s*$", self.text)
        if result:
            return result.group(1)
        return result
    
    def get_end_tag(self):
        result = re.search(r"^\s*</([^>]+)>\s*$", self.text)
        if result:
            if not re.search(r"^\s*</(\w+)>\s*$", self.text):
                raise ValueError(f'Line {self.line_number}: invalid end tag syntax "{self.text}"')
            return result.group(1)
        return result
    
class RooProcessConfig(object):
    
    def __init__(self, content:Optional[str]=None, file:Optional[str]=None):
        self.initialize(content=content, file=file)

    @classmethod
    def open(cls, filename:str):
        return cls(file=filename)

    def initialize(self, content:Optional[str]=None, file:Optional[str]=None):
        if (content is not None) and (file is not None):
            raise ValueError('either "content" or "file" should be specified')
        if file is not None:
            with open(file, "r") as f:
                content = f.read()
            source = file
        else:
            source = "text"
        self.content = content
        self.source = source

    @staticmethod
    def _get_iterlines(text:str):
        numbered_lines = split_lines(text, comment_string="#", remove_blank=True, with_line_number=True)
        clines = [RooConfigLine(line, line_number) for line, line_number in numbered_lines]
        clines_iter = iter(clines)
        return clines_iter

    def get_iterlines(self):
        return self._get_iterlines(self.content)

    @semistaticmethod
    def _get_action_tree(self, clines_iter, action_tree:Optional[ActionTree]=None, source:Optional[str]=None):
        if action_tree is None:
            action_tree = ActionTree()
        cline = next(clines_iter, None)
        if cline is None:
            current_node = action_tree.current_node
            if current_node.name is not None:
                if current_node.data["end_line_number"] == -1:
                    raise RuntimeError(f'unterminated start tag "{current_node.data["raw_text"]}" '
                                       f'at Line {current_node.data["start_line_number"]}')
            return action_tree
        if cline.start_tag:
            current_node = action_tree.current_node
            if current_node.name is not None:
                action = get_action(current_node.name)
                if not issubclass(action, RooProcNestedAction):
                    raise RuntimeError(f'Line {cline.line_number}: can not create action block within an unnestable '
                                       f'action block "{current_node.name}" '
                                       f'(Line {current_node.data["start_line_number"]})')
            tokens = split_str(cline.start_tag)
            action_name = tokens[0]
            if len(tokens) > 1:
                block_text = " ".join(tokens[1:])
            else:
                block_text = None
            child_node = action_tree.add_child(action_name,
                                               raw_text=cline.text,
                                               start_line_number=cline.line_number,
                                               end_line_number=-1,
                                               block_text=block_text,
                                               main_text="",
                                               source=source)
            action_tree.current_node = child_node
        elif cline.end_tag:
            current_node = action_tree.current_node
            if current_node.name is None:
                raise RuntimeError(f'Line {cline.line_number}: found close tag '
                                   f'"{cline.text}" without a start tag')
            if current_node.name != cline.end_tag:
                raise RuntimeError(f'Line {cline.line_number}: close tag '
                                   f'"{cline.text}" does not match the start tag '
                                   f'"{current_node.data["raw_text"]}" '
                                   f'(Line {current_node.data["start_line_number"]}, '
                                   f'Source {current_node.data["source"]})')
            current_node.data["end_line_number"] = cline.line_number
            action_tree.current_node = current_node.parent
        else:
            current_node = action_tree.current_node
            action = None
            if current_node.name is not None:
                action = get_action(current_node.name)
            if action and not issubclass(action, RooProcNestedAction):
                if action.allow_multiline():
                    current_node.data["main_text"] += f'\n{cline.text}'
                else:
                    current_node.data["main_text"] += cline.text
            else:
                tokens = split_str(cline.text)
                action_name = tokens[0]
                if len(tokens) > 1:
                    main_text = " ".join(tokens[1:])
                else:
                    main_text = None
                if action_name.lower() != "include":
                    child_node = action_tree.add_child(action_name,
                                                       raw_text=cline.text,
                                                       start_line_number=cline.line_number,
                                                       end_line_number=cline.line_number,
                                                       main_text=main_text,
                                                       block_text=None,
                                                       source=source)
                else:
                    basedir = os.path.dirname(source)
                    path = os.path.join(basedir, main_text.strip())
                    subtree = RooProcessConfig.open(path).get_action_tree()
                    action_tree.merge(subtree)
        return self._get_action_tree(clines_iter, action_tree, source=source)
       
    def get_action_tree(self):
        iterlines = self.get_iterlines()
        action_tree = self._get_action_tree(iterlines, source=self.source)
        return action_tree