from importlib_resources import files
import tatsu
from tatsu.walkers import NodeWalker
from onemodel.onemodel import OneModel
from onemodel.objects.parameter import Parameter

class OneModelWalker(NodeWalker):

    numberOfUnnamedReactions = 0
    numberOfUnnamedRules = 0
    
    def __init__(self):
        self.onemodel = OneModel()

        grammar = files("onemodel").joinpath("onemodel.ebnf").read_text()
        self.parser = tatsu.compile(grammar, asmodel=True)

    def run(self, onemodel_code):

        ast = self.parser.parse(onemodel_code)
        result = self.walk(ast)

        return result, ast
    
    def walk_Integer(self, node):
        return int(node.value)

    def walk_Float(self, node):
        return float(node.value)

    def walk_Parameter(self, node):
        namespace_list = node.namespace_list
        name = node.name
        value = self.walk(node.value)

        namespace = self.onemodel

        if namespace_list:
            for namespace_name in namespace_list:
                namespace = namespace[namespace_name]

        namespace[name] = Parameter()

        if value:
            namespace[name]["value"] = value

    def walk_AccessIdentifier(self, node):
        namespace_list = node.namespace_list
        name = node.name

        namespace = self.onemodel

        if namespace_list:
            for namespace_name in namespace_list:
                namespace = namespace[namespace_name]

        return namespace[name]

    def walk_list(self, nodes):
        """Walk every object in a list. 
        
        Notes
        -----
        If we don't implement this method, the walker will not
        evaluate list nodes.
        """
        results = []

        for node in nodes:
            results.append(self.walk(node))

        return results

    def walk_tuple(self, nodes):
        return self.walk_list(nodes)

