# coding: utf-8

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