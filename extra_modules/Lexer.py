from extra_modules.position import *
from extra_modules.Tokens import *
import extra_modules.Errors as err

# Lexer

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text + '\n'
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in '\t ':
                self.advance()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char in DIGITS:
                tok, error = self.make_number()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char in LETTERS+'_':
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.current_char == '*':
                tokens.append(self.make_mul())
            elif self.current_char == '@':
                tokens.append(Token(TT_MATMUL, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '.':
                if tokens == []: return [], err.InvalidSyntaxError(self.pos, self.pos, "Expected identifier before '.'")
                toks, error = self.chk_dot(tokens[-1])
                if error: return [], error
                tokens.extend(toks)
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '&':
                tokens.append(Token(TT_BITWISEAND, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '|':
                tokens.append(Token(TT_BITWISEOR, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_BITWISEXOR, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '~':
                tokens.append(Token(TT_COMPLEMENT, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON, pos_start=self.pos.copy()))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], err.IllegalCharError(pos_start, self.pos, "\"" + char + "\"")

        tokens.append(Token(TT_EOF, pos_start=self.pos.copy()))
        return tokens, None
    
    def chk_dot(self, prev_tok: Token):
        dot_tok = Token(TT_DOT, pos_start=self.pos.copy())

        if prev_tok.pos_end.col != dot_tok.pos_start.col or prev_tok.pos_end.ln != dot_tok.pos_start.ln:
            return [], err.InvalidSyntaxError(self.pos, self.pos, "Expected identifier, function call, or member access directly before '.'")
        self.advance()

        if self.current_char not in LETTERS+'_':
            return [], err.InvalidSyntaxError(self.pos, self.pos, "Expected identifier directly after '.'")
        
        nxt_idfr_tok = self.make_identifier()
        if nxt_idfr_tok.type == TT_KEYWORD: 
            return [], err.InvalidSyntaxError(self.pos, self.pos, "Invalid identifier (keyword) directly after '.'")
        
        return [dot_tok, nxt_idfr_tok], None
    
    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            match self.current_char:
                case 'i': # Integer
                    self.advance()
                    return Token(TT_INT, num_str, pos_start, self.pos.copy()), None
                case 'l': # Long
                    self.advance()
                    return Token(TT_LONGINT, num_str, pos_start, self.pos.copy()), None
                case 'b': # BigInt
                    self.advance()
                    return Token(TT_BIGINT, num_str, pos_start, self.pos.copy()), None
                case _:
                    return None, err.InvalidSyntaxError(pos_start, self.pos, "Expected 'i', 'l', or 'b' after integer")
        else:
            #self.advance()
            match self.current_char:
                case 'h': # Half
                    self.advance()
                    return Token(TT_HALF, num_str, pos_start, self.pos.copy()), None
                case 'f': # Float (single)
                    self.advance()
                    return Token(TT_FLOAT, num_str, pos_start, self.pos.copy()), None
                case 'd': # Double
                    self.advance()
                    return Token(TT_DOUBLE, num_str, pos_start, self.pos.copy()), None
                case _:
                    return None, err.InvalidSyntaxError(pos_start, self.pos, "Expected 'f', 'd', 'h', after decimal part of float")

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        ESCAPE_CHARACTERS = {
            'n' : '\n',
            't' : '\t',
            'r' : '\r'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += ESCAPE_CHARACTERS.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
                    escape_character = False
            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos.copy())
    
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER

        return Token(tok_type, id_str, pos_start, self.pos.copy())
    
    def make_minus_or_arrow(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())
    

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None
        
        return None, err.ExpectedCharError(pos_start, self.pos.copy(), "Expected '=' (after '!')")
    
    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())
    
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE
        elif self.current_char == '<':
            self.advance()
            tok_type = TT_LEFTSHIFT
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE
        elif self.current_char == '>':
            self.advance()
            tok_type = TT_RIGHTSHIFT
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())
    
    def make_mul(self):
        tok_type = TT_MUL
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '*':
            self.advance()
            tok_type = TT_POW
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def skip_comment(self):
        self.advance()

        while self.current_char != '\n':
            self.advance()
        
        self.advance()

