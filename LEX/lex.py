#! /usr/bin/env python3
#coding: utf-8

from sys import argv, exit

from ply import lex

# Reserved words
reserved = {
    'inteiro':'INTEIRO',
    'flutuante':'FLUTUANTE',
    'enquanto':'ENQUANTO',
    'repita':'REPITA',
    'até':'ATE',
    'se':'SE',
    'então':'ENTAO',
    'senão':'SENAO',
    'leia':'LEIA',
    'escreva':'ESCREVA',
    'retorna':'RETORNA',
    'fim':'FIM'
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
t_OPERADOR_SOMA          = r'\+|-'
t_OPERADOR_MULTIPLICACAO = r'\*|/'
t_OPERADOR_RESTO         = r'%'
t_OPERADOR_RELACIONAL    = r'>|<|=|<>|>=|<='
t_OPERADOR_LOGICO        = r'&&|\|\|'
t_OPERADOR_ATRIBUICAO    = r':='
t_OPERADOR_NEGACAO       = r'!'
t_ABREPARENTESES         = r'\('
t_FECHAPARENTESES        = r'\)'
t_ABRECOLCHETES          = r'\['
t_FECHACOLCHETES         = r'\]'
t_DOISPONTOS             = r':'
t_VIRGULA                = r','
t_TEXTO                  = r'\"[\d\D]*?\"'

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
    t.type = reserved.get(t.value,'ID')
    if t.type == 'ID':
        ID_list.append(t)
    return t

# Ignore Comments
def t_COMMENT(t):
     r'{[\d\D]*?}'
     t.lexer.lineno += len(t.value.split('\n')) # Considering the lines of comments in the total number of lines in the input
     pass


# Some rules
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def print_usage():
    print("Usage:")
    print("\tpython {} <path to file.tpp>".format(argv[0]))

def main():
    lexer = lex.lex()
    try:
        data = open(argv[1])
    except IndexError as e:
        print("Error: No source code given!\n")
        print_usage()
        exit(1)
    except IOError as e:
        print("Error: {}".format(str(e)[10:]))
        print("Please give a valid input file")
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
        pos = find_column(text, identifier)
        # Line:LexColumn Type Lexeme
        print("{:02d}:{:02d}\t{} {}".format(identifier.lineno, identifier.lexpos, identifier.type, identifier.value))

if __name__ == "__main__":
    main()