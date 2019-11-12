#! /usr/bin/env python3
# coding: utf-8

from sys import argv, exit
from ply import lex

from utils import find_column, print_usage
from MyExceptions import CommentInvalidSyntax, IllegalCharacter

last_comment = None

# Reserved words
reserved = {
    'inteiro': 'INTEIRO',
    'flutuante': 'FLUTUANTE',
    'enquanto': 'ENQUANTO',
    'repita': 'REPITA',
    'até': 'ATE',
    'se': 'SE',
    'então': 'ENTAO',
    'senão': 'SENAO',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'retorna': 'RETORNA',
    'fim': 'FIM'
}

# List of token names
tokens = [
    'ID',
    'NUM_INTEIRO',
    'NUM_PONTO_FLUTUANTE',
    'NUM_NOTACAO_CIENTIFICA',
    'OPERADOR_SOMA',
    'OPERADOR_MULTIPLICACAO',
    'OPERADOR_RESTO',
    'OPERADOR_RELACIONAL',
    'OPERADOR_LOGICO',
    'OPERADOR_ATRIBUICAO',
    'OPERADOR_NEGACAO',
    'ABREPARENTESES',
    'FECHAPARENTESES',
    'ABRECOLCHETES',
    'FECHACOLCHETES',
    'DOISPONTOS',
    'VIRGULA',
    'COMMENT',
    'TEXTO'
]

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_OPERADOR_SOMA = r'\+|-'
t_OPERADOR_MULTIPLICACAO = r'\*|/'
t_OPERADOR_RESTO = r'%'
t_OPERADOR_RELACIONAL = r'>=|<=|<>|>|<|='
t_OPERADOR_LOGICO = r'&&|\|\|'
t_OPERADOR_ATRIBUICAO = r':='
t_OPERADOR_NEGACAO = r'!'
t_ABREPARENTESES = r'\('
t_FECHAPARENTESES = r'\)'
t_ABRECOLCHETES = r'\['
t_FECHACOLCHETES = r'\]'
t_DOISPONTOS = r':'
t_VIRGULA = r','
t_TEXTO = r'\"[\d\D]*?\"'

ID_list = []


def t_NUM_NOTACAO_CIENTIFICA(t):
    r'\d+(\.\d+)?e\d*'
    if t.value[-1] == 'e':
        t.value = float(t.value[:-1])*10
    elif t.value[0] == 'e':
        t.value = 10**float(t.value[1:])
    else:
        t.value = float(t.value)
    return t


def t_NUM_PONTO_FLUTUANTE(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t


def t_NUM_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_]+\w*'
    t.type = reserved.get(t.value, 'ID')
    if t.type == 'ID':
        ID_list.append(
            {t.value: {'token': t, 'column': None, 'type': None, 'value': None}})
    return t


# Ignore Comments
def t_COMMENT(t):
    r'{[\d\D]*?}'
    global last_comment
    last_comment = (t.value, t.lineno)
    # Considering the lines of comments in the total number of lines in the input
    t.lexer.lineno += len(t.value.split('\n'))-1
    pass


# Some rules
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    try:
        if t.value[0] == '{' or t.value[0] == '}':
            raise CommentInvalidSyntax(
                "Comment with invalid syntax at line {}".format(t.lineno))
        else:
            raise IllegalCharacter(
                "Illegal character '{}' found at line {}".format(t.value[0], t.lineno))
    except CommentInvalidSyntax as error:
        print("Error: {}\n".format(error))
        print(
            "Comment example:\n\t{Hi! I'm a comment}\nComments are always between { }\n")
        print("Please fix it\n")
        exit(1)
    except IllegalCharacter as error:
        print("Error: {}\n".format(error))
        print("Please review yout code syntax \n")
        exit(1)


def main():
    # lexer = lex.lex()
    try:
        aux = argv[1].split('.')
        if aux[-1] != 'tpp':
            raise IOError("Not a .tpp file!")
        data = open(argv[1])
    except IndexError as e:
        print("Error: No source code provided!\n")
        print_usage()
        exit(1)
    except IOError as e:
        print("Error: {}".format(str(e)))
        print("Please give a valid input file\n\n")
        exit(1)

    text = data.read()
    lexer.input(text)

    print('\n==========================================')
    print('============== Tokens Table ==============\n')

    for tok in lexer:
        pos = find_column(text, tok)

        # print format
        # Line:Column Type
        print("{:02d}:{:02d}\t{}".format(tok.lineno, pos, tok.type))

    print('\n==========================================')
    print('================ ID Table ================\n')
    for identifier in ID_list:
        key = list(identifier.keys())[0]
        token = identifier[key]['token']
        pos = find_column(text, token)
        identifier[key]['column'] = pos

        # print format
        # Line:LexColumn Type Lexeme
        print("{:02d}:{:02d}\t{} {}".format(token.lineno,
                                            identifier[key]['column'], token.type, token.value))


lexer = lex.lex(optimize=True)

if __name__ == "__main__":
    main()
