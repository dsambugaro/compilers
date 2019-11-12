# coding: utf-8

from sys import argv

def find_column(input_str, token):
    line_start = input_str.rfind('\n', 0, token.lexpos) + 1
    aux = input_str.rfind('\t', line_start, token.lexpos)
    if aux != -1:
        return (token.lexpos - line_start) + 5
    else:
        return (token.lexpos - line_start) + 1


def print_usage():
    print("Usage:")
    print("\tpython {} <path to file.tpp>".format(argv[0]))


def print_dictionary(dictionary):
    for ID in dictionary:
        print (ID)
        for att in dictionary[ID]:
            print ('\t{}: {}'.format(att, dictionary[ID][att]))
        print('\n')

def check_exp_node(node):
    if not node.parent:
        return False
    if (': NUM_' in node.name or ': ID' in node.name) and (': expressao' in node.parent.name and ': index' in node.parent.parent.name and ': variavel' in node.parent.parent.parent.name and ': expressao' in node.parent.parent.parent.parent.name):
        return False
    if (': lista_argumentos' in node.name) or (': expressao' in node.name) or (': expressao' in node.parent.name and ': index' not in node.parent.parent.name):
        return True
    if ': chamada_funcao' not in node.name and (': index' in node.parent.name or ': chamada_funcao' in node.parent.name or (': variavel' in node.parent.name and len(node.parent.children) > 1)):
        return False
    return check_exp_node(node.parent)

def get_leaves(initNode):
    leaves = []
    def _get_leaf_nodes(node):
        if node is not None:
            if check_exp_node(node) and (node.is_leaf or ': chamada_funcao' in node.name or (': variavel' in node.name and len(node.children) > 1)):
                leaves.append(node)
            if not (': chamada_funcao' in node.name or (': variavel' in node.name and len(node.children) > 1)):
                for n in node.children:
                    _get_leaf_nodes(n)
    _get_leaf_nodes(initNode)
    return leaves

def get_leaves_index(initNode):
    leaves = []
    def _get_leaf_nodes(node):
        if node is not None:
            if node.is_leaf:
                leaves.append(node)
            for n in node.children:
                _get_leaf_nodes(n)
    _get_leaf_nodes(initNode)
    return leaves