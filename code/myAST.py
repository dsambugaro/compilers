# coding: utf-8

from anytree.exporter import DotExporter
from anytree import Node, RenderTree

class Node_AST(Node):
    def __init__(self, name, parent=None, children=None, **kwargs):
        super().__init__(name, parent=parent, children=children, **kwargs)
        self.data = None