#! /usr/bin/env python3
# coding: utf-8

import logging
from sys import argv, exit
from ply import yacc

from anytree.exporter import DotExporter
from anytree import Node, RenderTree

from utils import find_column, print_usage
from lexer import tokens, ID_list

nodes_count = 0
root = Node('Root')
nodes = []

parser = None
input_text = None


def new_node(nodeName, parent=None, id=None, data=None):
    global nodes_count
    if (id):
        node_ID = id
    else:
        node_ID = str(nodes_count) + ': ' + str(nodeName)
    nodes_count += 1
    if parent:
        node = Node(node_ID, parent)
    else:
        node = Node(node_ID)
    return node


def p_program(p):
    '''
    programa : lista_declaracoes
    '''

    father = new_node('Programa', root)
    p[0] = father
    p[1].parent = father


def p_program_error(p):
    '''
    programa : error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line), root)
    logging.error(
        "Syntax error parsing declaration list at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father


def p_declaration_list(p):
    '''
    lista_declaracoes : lista_declaracoes declaracao
    | declaracao
    '''

    father = new_node('lista_declaracoes')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father


def p_declaration_list_error(p):
    '''
    lista_declaracoes : error declaracao
    | lista_declaracoes error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing declaration list at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father


def p_declaration(p):
    '''
    declaracao : declaracao_variaveis
    | inicializacao_variaveis
    | declaracao_funcao
    '''

    father = new_node('declaracao')
    p[0] = father
    p[1].parent = father


def p_declaration_error(p):
    '''
    declaracao : error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing declaration at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father


def p_variable_declaration(p):
    '''
    declaracao_variaveis : tipo DOISPONTOS lista_variaveis
    '''

    father = new_node('declaracao_variaveis')
    p[0] = father
    p[1].parent = father
    p[2] = new_node('DOISPONTOS', father)
    p[3].parent = father


def p_variable_declaration_error(p):
    '''
    declaracao_variaveis : error DOISPONTOS lista_variaveis
    | tipo DOISPONTOS error
    | error DOISPONTOS error
    '''
    global input_text

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing variable declaration at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father
    p[2] = new_node('DOISPONTOS', father)
    p[3].parent = father


def p_variable_init(p):
    '''
    inicializacao_variaveis : atribuicao
    '''

    father = new_node('inicializacao_variaveis')
    p[0] = father
    p[1].parent = father


def p_variable_init_error(p):
    '''
    inicializacao_variaveis : error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing variable initialization at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father


def p_list_variable_init(p):
    '''
    lista_variaveis : lista_variaveis VIRGULA variavel
    | variavel
    '''

    father = new_node('lista_variaveis')
    p[0] = father
    p[1].parent = father

    if (len(p) > 2):
        p[2] = new_node('VIRGULA', father)
        p[3].parent = father


def p_list_variable_init_error(p):
    '''
    lista_variaveis : error VIRGULA variavel
    | lista_variaveis VIRGULA error
    | error VIRGULA error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing variable list initialization at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if (len(p) > 2):
        p[2] = new_node('VIRGULA', father)
        p[3].parent = father


def p_variable(p):
    '''
    variavel : ID
    | ID index
    '''

    father = new_node('variavel')
    p[0] = father
    aux = new_node('ID', father)
    new_node(p[1], aux)
    if len(p) > 2:
        p[2].parent = father


def p_variable_error(p):
    '''
    variavel : ID error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing variable initialization at line {}".format(error_line))
    parser.errok()
    p[0] = father
    aux = new_node('ID', father)
    new_node(p[1], aux)
    if len(p) > 2:
        p[2].parent = father


def p_index(p):
    '''
    index : index ABRECOLCHETES expressao FECHACOLCHETES
    | ABRECOLCHETES expressao FECHACOLCHETES
    '''

    father = new_node('index')
    p[0] = father
    if len(p) == 4:
        p[1] = new_node('ABRECOLCHETES', father)
        p[2].parent = father
        p[3] = new_node('FECHACOLCHETES', father)
    else:
        p[1].parent = father
        p[2] = new_node('ABRECOLCHETES', father)
        p[3].parent = father
        p[4] = new_node('FECHACOLCHETES', father)


def p_index_error(p):
    '''
    index : error ABRECOLCHETES expressao FECHACOLCHETES
    | index ABRECOLCHETES error FECHACOLCHETES
    | ABRECOLCHETES error FECHACOLCHETES
    '''

    error_line = p.lineno(2)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing index rule at line {}".format(error_line))
    parser.errok()
    p[0] = father
    if len(p) == 4:
        p[1] = new_node('ABRECOLCHETES', father)
        p[2].parent = father
        p[3] = new_node('FECHACOLCHETES', father)
    else:
        p[1].parent = father
        p[2] = new_node('ABRECOLCHETES', father)
        p[3].parent = father
        p[4] = new_node('FECHACOLCHETES', father)


def p_function_declaration(p):
    ''' declaracao_funcao : tipo cabecalho
    | cabecalho
    '''

    father = new_node('declaracao_funcao')
    p[0] = father
    p[1].parent = father

    if len(p) == 3:
        p[2].parent = father


def p_function_declaration_error(p):
    ''' declaracao_funcao : error cabecalho
    | tipo error
    | error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing function declaration at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) == 3:
        p[2].parent = father


def p_header(p):
    '''
    cabecalho : ID ABREPARENTESES lista_parametros FECHAPARENTESES corpo FIM
    '''

    father = new_node('cabecalho')
    p[0] = father
    aux = new_node('ID', father)
    new_node(p[1], aux)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)
    p[5].parent = father
    p[6] = new_node('FIM', father)


def p_header_error(p):
    '''
    cabecalho : ID ABREPARENTESES error FECHAPARENTESES corpo FIM
    | ID ABREPARENTESES lista_parametros FECHAPARENTESES error FIM
    | error ABREPARENTESES lista_parametros FECHAPARENTESES corpo FIM
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing function header at line {}".format(error_line))
    parser.errok()
    p[0] = father
    aux = new_node('ID', father)
    new_node(p[1], aux)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)
    p[5].parent = father
    p[6] = new_node('FIM', father)


def p_param_list(p):
    ''' lista_parametros : lista_parametros VIRGULA lista_parametros
    | parametro
    | vazio
    '''

    father = new_node('lista_parametros')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2] = new_node('VIRUGLA', father)
        p[3].parent = father


def p_param_list_error(p):
    ''' lista_parametros : error VIRGULA lista_parametros
    | lista_parametros VIRGULA error
    | error VIRGULA error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing param list at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2] = new_node('VIRUGLA', father)
        p[3].parent = father


def p_param(p):
    '''
    parametro : tipo DOISPONTOS ID
    | parametro ABRECOLCHETES FECHACOLCHETES
    '''

    father = new_node('parametro')
    p[0] = father
    p[1].parent = father

    if p[2] == ':':
        p[2] = new_node('DOISPONTOS', father)
        aux = new_node('ID', father)
        new_node(p[3], aux)
    else:
        p[2] = new_node('ABRECOLCHETES', father)
        p[3] = new_node('FECHACOLCHETES', father)


def p_param_error(p):
    '''
    parametro : error DOISPONTOS ID
    | error ABRECOLCHETES FECHACOLCHETES
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing param at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if p[2] == ':':
        p[2] = new_node('DOISPONTOS', father)
        aux = new_node('ID', father)
        new_node(p[3], aux)
    else:
        p[2] = new_node('ABRECOLCHETES', father)
        p[3] = new_node('FECHACOLCHETES', father)


def p_type(p):
    '''
    tipo : INTEIRO
    | FLUTUANTE
    '''

    father = new_node('tipo')
    p[0] = father
    p[1] = new_node(p[1].upper(), father)


def p_type_error(p):
    '''
    tipo : error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing type at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1] = new_node(p[1].upper(), father)


def p_body(p):
    '''
    corpo : corpo acao
    | vazio
    '''

    father = new_node('corpo')
    p[0] = father
    p[1].parent = father

    if len(p) == 3:
        p[2].parent = father


def p_body_error(p):
    '''
    corpo : error acao
    | corpo error
    | error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing body function at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) == 3:
        p[2].parent = father


def p_action(p):
    '''
    acao : expressao
    | declaracao_variaveis
    | se
    | repita
    | leia
    | escreva
    | retorna
    '''

    father = new_node('acao')
    p[0] = father
    p[1].parent = father


def p_action_error(p):
    '''
    acao : error
    '''
    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing action at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father


def p_if(p):
    '''
    se : SE expressao ENTAO corpo FIM
    | SE expressao ENTAO corpo SENAO corpo FIM
    '''

    father = new_node('se')
    p[0] = father
    p[1] = new_node('SE', father)
    p[2].parent = father
    p[3] = new_node('ENTAO', father)
    p[4].parent = father

    if len(p) == 8:
        p[5] = new_node('SENAO', father)
        p[6].parent = father
        p[7] = new_node('FIM', father)

    else:
        p[5] = new_node('FIM', father)


def p_if_error(p):
    '''
    se : SE error ENTAO corpo FIM
    | SE error ENTAO corpo SENAO corpo FIM
    | SE expressao ENTAO error FIM
    | SE expressao ENTAO error SENAO corpo FIM
    | SE expressao ENTAO corpo SENAO error FIM
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing if statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1] = new_node('SE', father)
    p[2].parent = father
    p[3] = new_node('ENTAO', father)
    p[4].parent = father

    if len(p) == 8:
        p[5] = new_node('SENAO', father)
        p[6].parent = father
        p[7] = new_node('FIM', father)

    else:
        p[5] = new_node('FIM', father)


def p_while(p):
    '''
    repita : REPITA corpo ATE expressao
    '''

    father = new_node('repita')
    p[0] = father
    p[1] = new_node('REPITA', father)
    p[2].parent = father
    p[3] = new_node('ATE', father)
    p[4].parent = father


def p_while_error(p):
    '''
    repita : REPITA error ATE expressao
    | REPITA corpo ATE error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing while statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1] = new_node('REPITA', father)
    p[2].parent = father
    p[3] = new_node('ATE', father)
    p[4].parent = father


def p_assignment(p):
    '''
    atribuicao : variavel OPERADOR_ATRIBUICAO expressao
    '''

    father = new_node('atribuicao')
    p[0] = father
    p[1].parent = father
    p[2] = new_node('OPERADOR_ATRIBUICAO', father)
    p[3].parent = father


def p_assignment_error(p):
    '''
    atribuicao : error OPERADOR_ATRIBUICAO expressao
    | variavel OPERADOR_ATRIBUICAO error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing variable assignment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father
    p[2] = new_node('OPERADOR_ATRIBUICAO', father)
    p[3].parent = father


def p_read(p):
    '''
    leia : LEIA ABREPARENTESES expressao FECHAPARENTESES
    '''

    father = new_node('leia')
    p[0] = father
    p[1] = new_node('LEIA', father)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_read_error(p):
    '''
    leia : LEIA ABREPARENTESES error FECHAPARENTESES
    '''

    error_line = p.lineno(3)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing read function at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1] = new_node('LEIA', father)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_write(p):
    '''
    escreva : ESCREVA ABREPARENTESES expressao FECHAPARENTESES
    '''

    father = new_node('escreva')
    p[0] = father
    p[1] = new_node('ESCREVA', father)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_write_error(p):
    '''
    escreva : ESCREVA ABREPARENTESES error FECHAPARENTESES
    '''

    error_line = p.lineno(3)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing write function at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[0] = father
    p[1] = new_node('ESCREVA', father)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_return(p):
    '''
    retorna : RETORNA ABREPARENTESES expressao FECHAPARENTESES
    '''

    father = new_node('retorna')
    p[0] = father
    p[1] = new_node('RETORNA', father)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_return_error(p):
    '''
    retorna : RETORNA ABREPARENTESES error FECHAPARENTESES
    '''

    error_line = p.lineno(3)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing return statment at line {}".format(error_line))
    parser.errok()
    father = new_node('retorna')
    p[0] = father
    p[1] = new_node('RETORNA', father)
    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_expression(p):
    '''
    expressao : expressao_logica
    | atribuicao
    '''

    father = new_node('expressao')
    p[0] = father
    p[1].parent = father


def p_expression_error(p):
    '''
    expressao : error
    '''

    error_line = p.lineno(3)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing expression at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father


def p_logical_expression(p):
    '''
    expressao_logica : expressao_simples
    | expressao_logica operador_logico expressao_simples
    '''

    father = new_node('expressao_logica')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_logical_expression_error(p):
    '''
    expressao_logica : error operador_logico expressao_simples
    | expressao_logica error expressao_simples
    | expressao_logica operador_logico error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing logical expression statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_simple_expression(p):
    '''
    expressao_simples : expressao_aditiva
    | expressao_simples operador_relacional expressao_aditiva
    '''

    father = new_node('expressao_simples')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_simple_expression_error(p):
    '''
    expressao_simples : error operador_relacional expressao_aditiva
    | expressao_simples error expressao_aditiva
    | expressao_simples operador_relacional error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing simple expression statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_aditive_expression(p):
    '''
    expressao_aditiva : expressao_multiplicativa
    | expressao_aditiva operador_soma expressao_multiplicativa
    '''

    father = new_node('expressao_aditiva')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_aditive_expression_error(p):
    '''
    expressao_aditiva : error operador_soma expressao_multiplicativa
    | expressao_aditiva error expressao_multiplicativa
    | expressao_aditiva operador_soma error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing aditive expression statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_multiplication_expression(p):
    '''
    expressao_multiplicativa : expressao_unaria
    | expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''

    father = new_node('expressao_multiplicativa')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_multiplication_expression_error(p):
    '''
    expressao_multiplicativa : error operador_multiplicacao expressao_unaria
    | expressao_multiplicativa error expressao_unaria
    | expressao_multiplicativa operador_multiplicacao error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing multiplication expression statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2].parent = father
        p[3].parent = father


def p_unary_expression(p):
    '''
    expressao_unaria : fator
    | operador_soma fator
    | operador_negacao fator
    '''

    father = new_node('expressao_unaria')
    p[0] = father
    if p[1] == '!':
        p[1] = new_node('OPERADOR_NEGACAO', father)
    else:
        p[1].parent = father

    if len(p) > 2:
        p[2].parent = father


def p_unary_expression_error(p):
    '''
    expressao_unaria : error fator
    | operador_soma error
    | operador_negacao error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing unary expression statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    if p[1] == '!':
        p[1] = new_node('OPERADOR_NEGACAO', father)
    else:
        p[1].parent = father

    if len(p) > 2:
        p[2].parent = father


def p_relational_operator(p):
    '''
    operador_relacional : OPERADOR_RELACIONAL
    '''
    father = new_node('operador_relacional')
    p[0] = father
    p[1] = new_node('OPERADOR_RELACIONAL', father)


def p_sum_operator(p):
    '''
    operador_soma : OPERADOR_SOMA
    '''
    father = new_node('operador_soma')
    p[0] = father
    p[1] = new_node('OPERADOR_SOMA', father)


def p_logical_operator(p):
    '''
    operador_logico : OPERADOR_LOGICO
    '''
    father = new_node('operador_logico')
    p[0] = father
    p[1] = new_node('OPERADOR_LOGICO', father)


def p_not_operator(p):
    '''
    operador_negacao : OPERADOR_NEGACAO
    '''
    father = new_node('operador_negacao')
    p[0] = father
    p[1] = new_node('OPERADOR_NEGACAO', father)


def p_multiplication_operator(p):
    '''
    operador_multiplicacao : OPERADOR_MULTIPLICACAO
    '''
    father = new_node('operador_multiplicacao')
    p[0] = father
    p[1] = new_node('OPERADOR_MULTIPLICACAO', father)


def p_factor(p):
    '''
    fator : ABREPARENTESES expressao FECHAPARENTESES
    | variavel
    | chamada_funcao
    | numero
    '''

    father = new_node('operador_soma')
    p[0] = father
    if len(p) > 2:
        p[1] = new_node('ABREPARENTESES', father)
        p[2].parent = father

        p[3] = new_node('FECHAPARENTESES', father)
    else:
        p[1].parent = father


def p_factor_error(p):
    '''
    fator : ABREPARENTESES error FECHAPARENTESES
    | error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing factor statment at line {}".format(error_line))
    parser.errok()
    p[0] = father
    if len(p) > 2:
        p[1] = new_node('ABREPARENTESES', father)
        p[2].parent = father

        p[3] = new_node('FECHAPARENTESES', father)
    else:
        p[1].parent = father


def p_number(p):
    '''
    numero : NUM_INTEIRO
    | NUM_PONTO_FLUTUANTE
    | NUM_NOTACAO_CIENTIFICA
    '''

    father = new_node('numero')
    p[0] = father
    if str(p[1]).find('.') == -1:
        aux = new_node('NUM_INTEIRO', father)
        new_node(p[1], aux)
    elif str(p[1]).find('e') >= 0:
        aux = new_node('NUM_NOTACAO_CIENTIFICA', father)
        new_node(p[1], aux)
    else:
        aux = new_node('NUM_PONTO_FLUTUANTE', father)
        new_node(p[1], aux)


def p_function_call(p):
    '''
    chamada_funcao : ID ABREPARENTESES lista_argumentos FECHAPARENTESES
    '''

    father = new_node('chamada_funcao')
    p[0] = father
    aux = new_node('ID', father)
    new_node(p[1], aux)

    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_function_call_error(p):
    '''
    chamada_funcao : ID ABREPARENTESES error FECHAPARENTESES
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing function call at line {}".format(error_line))
    parser.errok()
    p[0] = father
    aux = new_node('ID', father)
    new_node(p[1], aux)

    p[2] = new_node('ABREPARENTESES', father)
    p[3].parent = father
    p[4] = new_node('FECHAPARENTESES', father)


def p_arguments_list(p):
    ''' lista_argumentos : lista_argumentos VIRGULA expressao
    | expressao
    | vazio
    '''

    father = new_node('lista_argumentos')
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2] = new_node('VIRGULA', father)
        p[3].parent = father


def p_arguments_list_error(p):
    ''' lista_argumentos : error VIRGULA expressao
    | lista_argumentos VIRGULA error
    '''

    error_line = p.lineno(1)
    father = new_node('ERROR::{}'.format(error_line))
    logging.error(
        "Syntax error parsing arguments list at line {}".format(error_line))
    parser.errok()
    p[0] = father
    p[1].parent = father

    if len(p) > 2:
        p[2] = new_node('VIRGULA', father)
        p[3].parent = father


def p_empty(p):
    ''' vazio : '''
    father = new_node('vazio')
    p[0] = father


def p_error(p):
    global input_text
    if p:
        logging.error("Unexpected token '{}' at '{}:{}' (line:column)".format(
            p.value, p.lineno, find_column(input_text, p)))
    else:
        logging.critical(
            "EOF error -- Syntax error found at end of file\n\t Possible end token (fim) missing\n\t Please review your syntax.")


def main():
    global input_text
    global parser
    parser = yacc.yacc(optimize=True)
    print_tree = False
    try:
        if len(argv) > 1:
            aux = argv[1].split('.')
            if aux[-1] != 'tpp':
                raise IOError("Not a .tpp file!")
            input_file = open(argv[1])
            input_text = input_file.read()
        else:
            raise IndexError
    except IndexError as e:
        print("Error: No source code provided!\n")
        print_usage()
        exit(1)
    except IOError as e:
        print("Error: {}".format(str(e)))
        print("Please give a valid input file\n\n")
        exit(1)

    print('\n\n')
    parser.parse(input_text)

    if print_tree:
        for pre, fill, node in RenderTree(root):
            print("{}{}".format(pre, node.name))

        print('===================================  \n')

        # for pre, fill, node in RenderTree(root):
        #     if node.children == ():
        #         print("{}".format(node.name.split(' ')[-1]), end=' ')
    print('\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n')
    print("Generating AST, please wait...")
    if root.children != ():
        DotExporter(root).to_picture("tree.png")
        print("AST was successfully generated.\nOutput file: 'tree.png'")
    else:
        logging.error("Unable to generate AST -- Syntax nodes not found")
    print('\n\n')


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.WARNING)
    main()
