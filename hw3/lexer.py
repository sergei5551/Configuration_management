import ply.lex as lex

tokens = (
    'NAME', 'NUMBER', 'STRING',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'EQUALS', 'ARROW',
    'DOLLAR', 'LSQUARE', 'RSQUARE', 'SET', 'SERVER'
)

literals = ['(', ')', '{', '}', ',', '=', '-', '>']
def t_NAME(t):
    r'[a-z][a-z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Удаляем кавычки
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()