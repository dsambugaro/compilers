#! /usr/bin/env python3
# coding: utf-8

import logging
from sys import argv, exit

from termcolor import colored
from anytree import PreOrderIter
from anytree.exporter import DotExporter

import parser
from utils import print_dictionary
from MyExceptions import PruningError

has_main = False
symbol_table = parser.ID_table
declarations = []
func_declarations = []
has_semantic_error = False


def remove_node(node):
    for child in node.children:
        child.parent = node.parent
    node.parent = None
    del node


def remove_recursive_node(node):
    if len(node.parent.children) > 1:
        for i in range(len(node.parent.children)):
            if node.parent.children[i].name == node.name:
                aux = list(node.parent.children)
                j = 0
                for c in node.children:
                    c.parent = node.parent
                    aux.insert(i+j, c)
                    j += 1
                node.parent.children = aux
                break
    node.parent = None
    del node


def prune_AST(baseNode):
    try:
        root = baseNode
        queue = list(PreOrderIter(root))
        while queue:
            node = queue.pop(0)
            if not node.is_leaf and ': inicializacao_variaveis' in node.name:
                remove_node(node)
            elif not node.is_leaf and (': expressao_' in node.name or ': operador_' in node.name):
                remove_node(node)
            elif not node.is_leaf and ': acao' in node.name and not 'declaracao' in node.name:
                remove_node(node)
            elif not node.is_leaf and ': lista_variaveis' in node.name and not ': declaracao_variaveis' in node.parent.name:
                remove_recursive_node(node)
            elif not node.is_leaf and ': lista_parametros' in node.name and not ': cabecalho' in node.parent.name:
                remove_recursive_node(node)
            elif not node.is_leaf and ': lista_argumentos' in node.name and not ': chamada_funcao' in node.parent.name:
                remove_recursive_node(node)
            elif not node.is_leaf and ': corpo' in node.name and not (': cabecalho' in node.parent.name or ': se' in node.parent.name or ': repita' in node.parent.name):
                remove_node(node)
            elif not node.is_leaf and ': declaracao' in node.name and not '_' in node.name:
                remove_node(node)
            elif not node.is_leaf and ': expressao' in node.name and ': corpo' in node.parent.name:
                remove_node(node)
            elif not node.is_leaf and ': numero' in node.name:
                remove_node(node)
            elif node.is_leaf and ': vazio' in node.name and (': corpo' in node.parent.parent.name or (': corpo' in node.parent.name and len(node.parent.children) > 1)):
                remove_node(node)
            elif not node.is_leaf and ': lista_declaracoes' in node.name:
                remove_node(node)
            elif node.parent and len(node.children) == 1 and len(node.parent.children) == 1 and not 'declaracao_' in node.name:
                if len(node.children[0].children) != 0:
                    node.parent.children = node.children
                    del node
        return True
    except:
        return False


def get_scope(node, return_node=False):
    scope = None
    scope_node = None
    if ': Programa' in node.parent.name:
        scope = 'global'
    if ': declaracao_funcao' in node.parent.name:
        for child in node.children:
            if ': ID' in child.name:
                scope = child.children[0].name.split(' ')[1]
                scope_node = child
                break
    if scope:
        if return_node:
            return scope, scope_node
        else:
            return scope
    return get_scope(node.parent, return_node)


def has_assignment(node):
    if not symbol_table[node.name]['scope']:
        symbol_table[node.name]['scope'] = get_scope(node)
    for ID in list(symbol_table.keys()):
        if ID != node.name:
            if symbol_table[ID]['ID_type'] == 'assignment':
                if symbol_table[ID]['label'] == symbol_table[node.name]['label']:
                    if symbol_table[ID]['scope'] == symbol_table[node.name]['scope'] or symbol_table[ID]['scope'] == 'global':
                        # symbol_table[node.name]['type'] = symbol_table[ID]['type']
                        return True
    symbol_table[node.name]['value'] = 0
    return False


def get_function_declaration(node):
    if not symbol_table[node.name]['scope']:
        symbol_table[node.name]['scope'] = get_scope(node)
    for ID in list(symbol_table.keys()):
        if ID != node.name:
            if symbol_table[ID]['ID_type'] == 'function_header':
                if symbol_table[ID]['label'] == symbol_table[node.name]['label']:
                    if symbol_table[ID]['scope'] == 'global':
                        return symbol_table[ID]
    return None


def get_declaration(node):
    scope_node = None
    symbol_table[node.name]['scope'], scope_node = get_scope(node, True)
    if symbol_table[node.name]['scope'] != 'global' and scope_node:
        for param in symbol_table[scope_node.name]['params']:
            if param['label'] == symbol_table[node.name]['label']:
                return param
    for ID in list(symbol_table.keys()):
        if ID != node.name:
            if symbol_table[ID]['ID_type'] == 'declaration':
                if symbol_table[ID]['label'] == symbol_table[node.name]['label']:
                    if symbol_table[ID]['scope'] == symbol_table[node.name]['scope'] or symbol_table[ID]['scope'] == 'global':
                        return symbol_table[ID]
    return None


def get_type(node, show_assigment_warning=False):
    global has_semantic_error
    if ': variavel' in node.name:
        return get_type(node.children[0])
    if ': NUM_INTEIRO' in node.name:
        return 'INTEIRO'
    if ': NUM_PONTO_FLUTUANTE' in node.name:
        return 'FLUTUANTE'
    if ': ID' in node.name:
        declaration = get_declaration(node)
        if declaration:
            if show_assigment_warning and not has_assignment(node):
                logging.warning("Variable {} at line {} was not initialized. Using default value 0".format(
                    colored(symbol_table[node.name]
                            ['label'], 'green', attrs=['bold']),
                    colored(symbol_table[node.name]['line'], 'white', attrs=['bold'])))

            symbol_table[node.name]['type'] = declaration['type']
            return symbol_table[node.name]['type']
        else:
            has_semantic_error = True
            logging.error("Variable {} at line {} was not declared".format(
                colored(symbol_table[node.name]['label'],
                        'green', attrs=['bold']),
                colored(symbol_table[node.name]['line'], 'white', attrs=['bold'])))
    if ': chamada_funcao' in node.name:
        ID_node = node.children[0]
        declaration = get_function_declaration(ID_node)
        if declaration:
            symbol_table[ID_node.name]['type'] = declaration['type']
            return symbol_table[ID_node.name]['type']
        else:
            has_semantic_error = True
            logging.error("Function {} at line {} was not declared".format(
                colored(symbol_table[ID_node.name]
                        ['label'], 'green', attrs=['bold']),
                colored(symbol_table[ID_node.name]['line'], 'white', attrs=['bold'])))
    return None


def check_index_types(node, ID):
    global has_semantic_error
    index_types = []
    for child in node.children:
        if '169: ' in child.name:
            print(node.name)
        if ': index' in child.name:
            check_index_types(child, ID)
        elif ': expressao' in child.name:
            symbol_table[ID.name]['size'] = child
            for item in child.children:
                if ': variavel' in item.name:
                    type_var = get_type(item.children[0])
                    index_types.append(type_var)
                else:
                    type_var = get_type(item)
                    index_types.append(type_var)
                if ': NUM_' in item.name and len(child.children) == 1:
                    symbol_table[ID.name]['size'] = int(
                        item.children[0].name.split(' ')[1])
            for t in index_types:
                if t and t != 'INTEIRO':
                    has_semantic_error = True
                    logging.error('Variable {} at line {} received {} value in the index, but should receive an integer (INTEIRO)'.format(
                        colored(symbol_table[ID.name]
                                ['label'], 'green', attrs=['bold']),
                        colored(symbol_table[ID.name]
                                ['line'], 'white', attrs=['bold']),
                        t
                    ))
                break


def set_variable(ID, tipo, node, index=False):
    global has_semantic_error
    global declarations
    has_been_declared = False
    symbol_table[ID.name]['type'] = tipo
    symbol_table[ID.name]['index'] = index
    symbol_table[ID.name]['ID_type'] = 'declaration'
    symbol_table[ID.name]['value'] = 0
    symbol_table[ID.name]['scope'] = get_scope(node)
    for declaration in declarations:
        if symbol_table[ID.name]['ID_type'] == 'declaration':
            if symbol_table[ID.name]['label'] == symbol_table[declaration]['label']:
                if symbol_table[ID.name]['scope'] == symbol_table[declaration]['scope'] or symbol_table[declaration]['scope'] == 'global':
                    has_semantic_error = True
                    logging.error("Variable {} at line {} already declared at line {}".format(
                        colored(symbol_table[ID.name]
                                ['label'], 'green', attrs=['bold']),
                        colored(symbol_table[ID.name]
                                ['line'], 'white', attrs=['bold']),
                        colored(symbol_table[declaration]
                                ['line'], 'white', attrs=['bold'])
                    ))
                    has_been_declared = True
    if not has_been_declared:
        declarations.append(ID.name)


def s_variable_declaration(node):
    tipo = None
    for i in range(len(node.children)):
        if ': tipo' in node.children[i].name:
            tipo = node.children[i].children[0].name.split(' ')[1]
        if ': lista_variaveis' in node.children[i].name:
            if len(node.children[i].children) == 1 and len(node.children[i].children[0].children) == 1:
                ID = node.children[i].children[0]
                set_variable(ID, tipo, node)
            else:
                for child in node.children[i].children:
                    if ': variavel' in child.name:
                        ID = child.children[0]
                        set_variable(ID, tipo, node)
                        if len(child.children) > 1:
                            symbol_table[ID.name]['index'] = True
                            check_index_types(child, ID)


def s_assignment(node):
    global has_semantic_error
    types = []
    variavel = node.children[0].children[0]
    symbol_table[variavel.name]['ID_type'] = 'assignment'
    symbol_table[variavel.name]['type'] = get_type(variavel)
    expressao = node.children[2].children
    symbol_table[variavel.name]['value'] = expressao

    var_declaration = get_declaration(variavel)

    if len(node.children[0].children) > 1:
        symbol_table[variavel.name]['index'] = True
        check_index_types(node.children[0], variavel)
    else:
        symbol_table[variavel.name]['index'] = False

    if (var_declaration and 'index' in var_declaration) and (var_declaration['index'] and not symbol_table[variavel.name]['index']):
        has_semantic_error = True
        logging.error("Variable {} is an array, provide access indexes".format(
            colored(symbol_table[variavel.name]
                    ['label'], 'green', attrs=['bold'])
        ))

    if len(expressao) == 1:
        types.append(get_type(expressao[0]))
        if ': ID' in expressao[0].name:
            if types and not has_assignment(expressao[0]):
                logging.warning("Variable {} at line {} was not initialized. Using default value 0".format(
                    colored(symbol_table[expressao[0].name]
                            ['label'], 'green', attrs=['bold']),
                    colored(symbol_table[expressao[0].name]['line'], 'white', attrs=['bold'])))
        if ': chamada_funcao' in expressao[0].name:
            s_function_call(expressao[0])
        if ': expressao' in expressao[0].name:
            fix_function_call(expressao[0])
    else:
        for item in expressao:
            item_type = get_type(item)
            if item_type:
                types.append(item_type)
            elif ': OPERADOR_MULTIPLICACAO' in item.name:
                if ': /' in item.children[0].name and symbol_table[variavel.name]['type'] != 'FLUTUANTE':
                    logging.warning('Variable {} at line {} is not of floating type but is receiving division operation.\n\tOnly the integer part will be preserved'.format(
                        colored(symbol_table[variavel.name]
                                ['label'], 'green', attrs=['bold']),
                        colored(symbol_table[variavel.name]['line'], 'white', attrs=['bold'])))
            if ': expressao' in item.name:
                fix_function_call(item)
            if ': chamada_funcao' in item.name:
                s_function_call(item)
    for t in types:
        if t and symbol_table[variavel.name]['type'] and t != symbol_table[variavel.name]['type']:
            if symbol_table[variavel.name]['type'] == 'FLUTUANTE' and not 'FLUTUANTE' in types or symbol_table[variavel.name]['type'] == 'INTEIRO':
                logging.warning('Variable {} at line {} is of type {} but is receiving {}'.format(
                    colored(symbol_table[variavel.name]
                            ['label'], 'green', attrs=['bold']),
                    colored(symbol_table[variavel.name]
                            ['line'], 'white', attrs=['bold']),
                    symbol_table[variavel.name]['type'], t
                ))
            break


def parse_params(node, ID):
    params = []
    for child in node.children:
        param = {}
        if ': parametro' in child.name:
            for p in child.children:
                if ': tipo' in p.name:
                    param['type'] = p.children[0].name.split(' ')[1]
                if ': ID' in p.name:
                    param['label'] = p.children[0].name.split(' ')[1]
            params.append(param)
    symbol_table[ID.name]['params'] = params

def fix_function_call(child):
    for expression in child.children:
        if ': variavel' in expression.name:
            if (symbol_table[expression.children[0].name]['type'] == None):
                get_type(expression)
            if (symbol_table[expression.children[0].name]['scope'] == None):
                symbol_table[expression.children[0].name]['scope'] = get_scope(expression)
            if len(expression.children) > 1:
                symbol_table[expression.children[0].name]['index'] = True
                check_index_types(expression, expression.children[0])
        if ': chamada_funcao' in expression.name:
            s_function_call(expression)
        if ': expressao' in expression.name:
            fix_function_call(expression)

def parse_args(node, ID):
    arg_types = []
    if len(node.children) > 1:
        for child in node.children:
            if ': expressao' in child.name:
                for expression in child.children:
                    arg_types.append(get_type(expression, True))
                    if ': chamada_funcao' in expression.name:
                        s_function_call(expression)
                    if ': expressao' in expression.name:
                        fix_function_call(expression)
            if ': chamada_funcao' in child.name:
                s_function_call(child)
            if ': variavel' in child.name:
                arg_type = get_type(child.children[0], True)
                if arg_type:
                    arg_types.append(arg_type)
    else:
        if ': chamada_funcao' in node.children[0].name:
            s_function_call(node.children[0])
        arg_type = get_type(node.children[0], True)
        if arg_type:
            arg_types.append(arg_type)
    symbol_table[ID.name]['args'] = arg_types


def check_args(ID):
    global has_semantic_error
    declaration = get_function_declaration(ID)
    if declaration:
        if len(symbol_table[ID.name]['args']) != len(declaration['params']):
            has_semantic_error = True
            logging.error("Expected {} arguments in function call '{}' at line {}, but {} are given".format(
                colored(len(declaration['params']), 'white', attrs=['bold']),
                colored(symbol_table[ID.name]['label'],
                        'green', attrs=['bold']),
                colored(symbol_table[ID.name]['line'],
                        'white', attrs=['bold']),
                colored(len(symbol_table[ID.name]
                            ['args']), 'white', attrs=['bold'])
            ))
        else:
            for i in range(len(declaration['params'])):
                if declaration['params'][i]['type'] != symbol_table[ID.name]['args'][i]:
                    has_semantic_error = True
                    logging.error("Function '{}' expected {} in param '{}', but received {}".format(
                        colored(declaration['label'], 'green', attrs=['bold']),
                        colored(declaration['params'][i]
                                ['type'], 'white', attrs=['bold']),
                        colored(declaration['params'][i]
                                ['label'], 'green', attrs=['bold']),
                        colored(symbol_table[ID.name]['args']
                                [i], 'white', attrs=['bold'])
                    ))

def check_repeat(node, func_type, ID):
    for child in node.children:
        if ': expressao' in child.name:
            fix_function_call(child)
        if ': corpo' in child.name:
            check_body(child, func_type, ID, if_body=True)

def check_if(node, func_type, ID):
    for child in node.children:
        if ': expressao' in child.name:
            fix_function_call(child)
        if ': corpo' in child.name:
            check_body(child, func_type, ID, if_body=True)

def check_body(node, func_type, ID, if_body=False):
    global has_semantic_error
    return_types = None
    for child in node.children:
        if ': declaracao_variaveis' in child.name:
            s_variable_declaration(child)
        if ': atribuicao' in child.name:
            s_assignment(child)
        if ': chamada_funcao' in child.name:
            s_function_call(child)
        if ': leia' in child.name:
            s_read(child)
        if ': escreva' in child.name:
            s_write(child)
        if ': se' in child.name:
            check_if(child, func_type, ID)
        if ': repita' in child.name:
            check_repeat(child, func_type, ID)
        if ': retorna' in child.name:
            s_return(child)
            return_types = child.return_type
    if func_type and not return_types and not if_body:
        has_semantic_error = True
        logging.error("Function '{}' should return {} but is returning VOID".format(
            colored(symbol_table[ID.name]['label'], 'green', attrs=['bold']),
            colored(func_type, 'white', attrs=['bold'])
        ))


def s_function_declaration(node):
    global has_semantic_error
    global has_main
    tipo = None
    if len(node.children) > 1:
        if ': tipo' in node.children[0].name:
            tipo = node.children[0].children[0].name.split(' ')[1]
        header = node.children[1]
    else:
        header = node.children[0]
    for i in range(len(header.children)):
        if ': ID' in header.children[i].name:
            ID = header.children[i]
            if tipo:
                symbol_table[ID.name]['type'] = tipo
            else:
                symbol_table[ID.name]['type'] = 'VOID'
            symbol_table[ID.name]['scope'] = get_scope(node)
            if symbol_table[ID.name]['label'] == 'principal':
                has_main = True
            has_declaration = False
            for func in func_declarations:
                if symbol_table[func]['label'] == symbol_table[ID.name]['label']:
                    has_declaration = True
            if has_declaration:
                has_semantic_error = True
                logging.error("Function {} at line {} already declared at line {}".format(
                    colored(symbol_table[ID.name]['label'],
                            'green', attrs=['bold']),
                    colored(symbol_table[ID.name]['line'],
                            'white', attrs=['bold']),
                    colored(symbol_table[func]['line'],
                            'white', attrs=['bold'])
                ))
            else:
                func_declarations.append(ID.name)
        if ': lista_parametros' in header.children[i].name:
            parse_params(header.children[i], ID)
        if ': corpo' in header.children[i].name:
            check_body(header.children[i], tipo, ID)


def s_function_call(node):
    for child in node.children:
        if ': ID' in child.name:
            ID = node.children[0]
            get_type(node)
            if symbol_table[ID.name]['label'] == 'principal':
                if symbol_table[ID.name]['scope'] == 'principal':
                    logging.warning("Found loope with main function '{}' at line {}".format(
                        colored('principal', 'green', attrs=['bold']),
                        colored(symbol_table[ID.name]['line'], 'white', attrs=['bold'])))
        if ': lista_argumentos' in child.name:
            symbol_table[ID.name]['args_node'] = child
            parse_args(child, ID)
    check_args(ID)


def s_read(node):
    node.scope = get_scope(node)
    types = []
    expressao = node.children[2].children
    if len(expressao) == 1:
        types.append(get_type(expressao[0]))
        if ': ID' in expressao[0].name:
            if types and not has_assignment(expressao[0]):
                logging.warning("Variable {} at line {} was not initialized. Using default value 0".format(
                    colored(symbol_table[expressao[0].name]
                            ['label'], 'green', attrs=['bold']),
                    colored(symbol_table[expressao[0].name]['line'], 'white', attrs=['bold'])))
        if ': chamada_funcao' in expressao[0].name:
            s_function_call(expressao[0])
    else:
        for item in expressao:
            item_type = get_type(item)
            if item_type:
                types.append(item_type)


def s_write(node):
    node.scope = get_scope(node)
    types = []
    expressao = node.children[2].children
    if len(expressao) == 1:
        types.append(get_type(expressao[0]))
        if ': ID' in expressao[0].name:
            if types and not has_assignment(expressao[0]):
                logging.warning("Variable {} at line {} was not initialized. Using default value 0".format(
                    colored(symbol_table[expressao[0].name]
                            ['label'], 'green', attrs=['bold']),
                    colored(symbol_table[expressao[0].name]['line'], 'white', attrs=['bold'])))
        if ': chamada_funcao' in expressao[0].name:
            s_function_call(expressao[0])
    else:
        for item in expressao:
            item_type = get_type(item)
            if item_type:
                types.append(item_type)


def s_return(node):
    global has_semantic_error
    node.scope = get_scope(node)
    func_return_type = None
    for ID in list(symbol_table.keys()):
        if symbol_table[ID]['ID_type'] == 'function_header':
            if symbol_table[ID]['label'] == node.scope:
                func_return_type = symbol_table[ID]['type']
    types = []
    expressao = node.children[2].children
    if len(expressao) == 1:
        types.append(get_type(expressao[0]))
        if ': ID' in expressao[0].name:
            if types and not has_assignment(expressao[0]):
                logging.warning("Variable {} at line {} was not initialized. Using default value 0".format(
                    colored(symbol_table[expressao[0].name]
                            ['label'], 'green', attrs=['bold']),
                    colored(symbol_table[expressao[0].name]['line'], 'white', attrs=['bold'])))
        if ': chamada_funcao' in expressao[0].name:
            s_function_call(expressao[0])
    else:
        for item in expressao:
            
            if ': chamada_funcao' in item.name:
                s_function_call(item)
            
            item_type = get_type(item)
            if item_type:
                types.append(item_type)
            elif ': OPERADOR_MULTIPLICACAO' in item.name:
                if ': /' in item.children[0].name and func_return_type != 'FLUTUANTE':
                    has_semantic_error = True
                    logging.error("Function '{}' is not of floating type but is receiving division operation in return at line {}.\n\tOnly the integer part will be preserved".format(
                        colored(node.scope, 'green', attrs=['bold']), colored(
                            node.line, 'white', attrs=['bold'])
                    ))
    node.return_type = types
    for t in node.return_type:
        if t and t != func_return_type:
            logging.warning('Function {} is of type {} but is returning {} at line {}'.format(
                colored(node.scope, 'green', attrs=['bold']),
                func_return_type, t,
                colored(node.line, 'white', attrs=['bold'])
            ))
            break


def check_unused_functions():
    for declaration in func_declarations:
        has_use = False
        for ID in list(symbol_table.keys()):
            if ID != declaration:
                if symbol_table[ID]['ID_type'] == 'function_call':
                    if symbol_table[ID]['label'] == symbol_table[declaration]['label']:
                        if symbol_table[ID]['scope'] == symbol_table[declaration]['scope'] or symbol_table[declaration]['scope'] == 'global':
                            has_use = True
        if not has_use and symbol_table[declaration]['label'] != 'principal':
            logging.warning("Function {} was declared at line {}, but never used".format(
                colored(symbol_table[declaration]
                        ['label'], 'green', attrs=['bold']),
                colored(symbol_table[declaration]['line'], 'white', attrs=['bold'])))


def check_unused_variables():
    for declaration in declarations:
        has_use = False
        for ID in list(symbol_table.keys()):
            if ID != declaration:
                if symbol_table[ID]['ID_type'] == 'variable':
                    if symbol_table[ID]['label'] == symbol_table[declaration]['label']:
                        if symbol_table[ID]['scope'] == symbol_table[declaration]['scope'] or symbol_table[declaration]['scope'] == 'global':
                            has_use = True
        if not has_use:
            logging.warning("Variable {} was declared at line {}, but never used".format(
                colored(symbol_table[declaration]
                        ['label'], 'green', attrs=['bold']),
                colored(symbol_table[declaration]['line'], 'white', attrs=['bold'])))


def semantic_check(root):
    global has_semantic_error
    queue = list(PreOrderIter(root))
    while queue:
        node = queue.pop(0)
        if not node.is_leaf and node.parent:
            scope = get_scope(node)
            if ': declaracao_variaveis' in node.name:
                if scope == 'global':
                    s_variable_declaration(node)
            if ': atribuicao' in node.name:
                if scope == 'global':
                    s_assignment(node)
            if ': declaracao_funcao' in node.name:
                s_function_declaration(node)

    if not has_main:
        has_semantic_error = True
        logging.error("Main function '{}' was not declared".format(
            colored('principal', 'green', attrs=['bold'])))

    check_unused_functions()
    check_unused_variables()


def main(logging_level, export_AST=False):
    global has_semantic_error
    pruned_tree_file = 'pruned_tree.png'
    try:
        root, hasError = parser.main(logging_level, True)
        if hasError:
            raise SyntaxError("Syntax Errors found")
        if not root:
            raise PruningError("The AST don't has nodes")
        if root and not root.is_leaf:
            if export_AST:
                print('\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n')
                print("Pruning the AST, please wait...")
                if(prune_AST(root)):
                    DotExporter(root).to_picture(pruned_tree_file)
                    print("AST was successfully proned.\nOutput file: '{}'".format(
                        pruned_tree_file))
                    print(
                        '\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n')
            else:
                raise PruningError("Error while prunning the AST")
        else:
            raise PruningError("The AST has only root node")
    except PruningError as e:
        has_semantic_error = True
        logging.error("Unable to prune the AST")
        print(e)
        exit(1)
    except SyntaxError as e:
        has_semantic_error = True
        logging.error("Unable to check semantic -- Fix Syntax Errors")
        exit(1)

    semantic_check(root)
    
    queue = list(PreOrderIter(root))
    while queue:
        node = queue.pop(0)
        if ': ID' in node.name:
            if (symbol_table[node.name]['type'] == None):
                get_type(node)
            if (symbol_table[node.name]['scope'] == None):
                symbol_table[node.name]['scope'] = get_scope(node)
            if len(node.parent.children) > 1:
                symbol_table[node.name]['index'] = True
                check_index_types(node.parent, node)
        if ': variavel' in node.name:
                if (symbol_table[node.children[0].name]['type'] == None):
                    get_type(node)
                if (symbol_table[node.children[0].name]['scope'] == None):
                    symbol_table[node.children[0].name]['scope'] = get_scope(node)
                if len(node.children) > 1:
                    symbol_table[node.children[0].name]['index'] = True
                    check_index_types(node, node.children[0])

    print('\n==============================================')
    print('================ Symbol Table ================\n')
    print_dictionary(symbol_table)

    return root, symbol_table, has_semantic_error


if __name__ == '__main__':
    main(logging.WARNING, True)
