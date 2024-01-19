# Imports
from extra_modules.execution_components.position import Position
from string import ascii_letters

# Constants

DIGITS = '0123456789'
LETTERS = ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

# Tokens

TT_BIGINT               = 'BIGINT'
TT_INT                  = 'INT'
TT_LONGINT              = 'LONGINT'
TT_UINT                 = 'UINT'
TT_ULONGINT             = 'ULONGINT'
TT_HALF                 = 'HALF'
TT_FLOAT                = 'FLOAT'
TT_DOUBLE               = 'DOUBLE'
TT_STRING               = 'STRING'
TT_IDENTIFIER           = 'IDENTIFIER'
TT_KEYWORD              = 'KEYWORD'
TT_PLUS                 = 'PLUS'
TT_MINUS                = 'MINUS'
TT_MUL                  = 'MUL'
TT_MATMUL               = 'MATMUL'
TT_DIV                  = 'DIV'
TT_POW                  = 'POW'
TT_EQ                   = 'EQ'
TT_DOT                  = 'DOT'
TT_LPAREN               = 'LPAREN'
TT_RPAREN               = 'RPAREN'
TT_LSQUARE              = 'LSQUARE'
TT_RSQUARE              = 'RSQUARE'
TT_LBRACE               = 'LBRACE'
TT_RBRACE               = 'RBRACE'
TT_EE                   = 'EE'
TT_NE                   = 'NE'
TT_LT                   = 'LT'
TT_GT                   = 'GT'
TT_LTE                  = 'LTE'
TT_GTE                  = 'GTE'
TT_BITWISEAND           = 'BITWISEAND'
TT_BITWISEOR            = 'BITWISEOR'
TT_BITWISEXOR           = 'BITWISEXOR'
TT_LEFTSHIFT            = 'LEFTSHIFT'
TT_RIGHTSHIFT           = 'RIGHTSHIFT'
TT_COMPLEMENT           = 'COMPLEMENT'
TT_COMMA                = 'COMMA'
TT_COLON                = 'COLON'
TT_ARROW                = 'ARROW'
TT_NEWLINE              = 'NEWLINE'
TT_EOF                  = 'EOF'

TOKEN_TYPE_TO_STRING = {
    TT_BIGINT       : 'bigint',
    TT_INT          : 'int',
    TT_LONGINT      : 'longint',
    TT_UINT         : 'uint',
    TT_ULONGINT     : 'ulongint',
    TT_HALF         : 'half',
    TT_FLOAT        : 'float',
    TT_DOUBLE       : 'double',
    TT_STRING       : 'string',
    TT_IDENTIFIER   : 'identifier',
    TT_KEYWORD      : 'keyword',
    TT_PLUS         : '\'+\'',
    TT_MINUS        : '\'-\'',
    TT_MUL          : '\'*\'',
    TT_MATMUL       : '\'@\'',
    TT_DIV          : '\'/\'',
    TT_POW          : '\'**\'',
    TT_EQ           : '\'=\'',
    TT_DOT          : '\'.\'',
    TT_LPAREN       : '\'(\'',
    TT_RPAREN       : '\')\'',
    TT_LSQUARE      : '\'[\'',
    TT_RSQUARE      : '\']\'',
    TT_LBRACE       : '\'{\'',
    TT_RBRACE       : '\'}\'',
    TT_EE           : '\'==\'',
    TT_NE           : '\'!=\'',
    TT_LT           : '\'<\'',
    TT_GT           : '\'>\'',
    TT_LTE          : '\'<=\'',
    TT_GTE          : '\'>=\'',
    TT_BITWISEAND   : '\'&\'',
    TT_BITWISEOR    : '\'|\'',
    TT_BITWISEXOR   : '\'^\'',
    TT_COMPLEMENT   : '\'~\'',
}

KEYWORDS = [
    'var',
    'mut',
    'const',
    'struct',
    'class',
    'and',
    'or',
    'not',
    'if',
    'then',
    'elif',
    'else',
    'del',
    'for',
    'to',
    'step',
    'while',
    'func',
    'mthd',
    'end',
    'return',
    'continue',
    'break',
    'protect',
    'typeof',
    'copy',
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start: 
            self.pos_start = pos_start.copy()
            self.pos_end = self.pos_start.copy()
            self.pos_end.advance()
        if pos_end: self.pos_end = pos_end
    
    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

    def __hash__(self):
        return hash((self.type, self.value, self.pos_start, self.pos_end))