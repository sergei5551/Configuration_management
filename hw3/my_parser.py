import ply.yacc as yacc
from lexer import tokens

# Правила грамматики

def p_config(p):
    '''config : server_block
              | setlist'''
    p[0] = p[1]

def p_setlist(p):
    '''setlist : set
               | set setlist'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_set(p):
    '''set : NAME EQUALS value SEMI'''
    p[0] = ('SET', p[1], p[3])

def p_value(p):
    '''value : NUMBER
             | STRING
             | array
             | dict
             | dollar_expr'''
    p[0] = p[1]

def p_array(p):
    '''array : LSQUARE values RSQUARE'''
    p[0] = ('ARRAY', p[2])

def p_values(p):
    '''values : value
              | value COMMA values'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_dict(p):
    '''dict : LBRACE pairs RBRACE'''
    p[0] = ('DICT', p[2])

def p_pairs(p):
    '''pairs : pair
             | pair COMMA pairs'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_pair(p):
    '''pair : NAME MINUS GREATER value'''
    p[0] = (p[1], p[4])

def p_dollar_expr(p):
    '''dollar_expr : DOLLAR LPAREN NAME RPAREN'''
    p[0] = ('DOLLAR', p[3])

def p_semi(p):
    '''SEMI : '''
    pass

def p_minus(p):
    '''MINUS : '-' '''
    pass

def p_greater(p):
    '''GREATER : '>' '''
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}({p.value})")
    else:
        print("Syntax error at EOF")

# Функция для запуска парсера
def parse(data):
    parser = yacc.yacc()
    return parser.parse(data)

def p_server_block(p):
    '''server_block : SERVER LBRACE server_options RBRACE'''
    p[0] = ('SERVER_BLOCK', p[3])  # Сохранить опции сервера

def p_server_options(p):
    '''server_options : option
                      | option server_options'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_option(p):
    '''option : NAME EQUALS value SEMI'''
    p[0] = (p[1], p[3])
# Создание глобального парсера (можно убрать, если он не используется вне функции parse())
parser = yacc.yacc()