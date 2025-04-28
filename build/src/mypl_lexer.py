"""The MyPL Lexer class.

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326

"""

from src.mypl_token import *
from src.mypl_error import *


class Lexer:
    """For obtaining a token stream from a program."""

    def __init__(self, in_stream):
        """Create a Lexer over the given input stream.

        Args:
            in_stream -- The input stream. 

        """
        self.in_stream = in_stream
        self.line = 1
        self.column = 0


    def read(self):
        """Returns and removes one character from the input stream."""
        self.column += 1
        return self.in_stream.read_char()

    
    def peek(self):
        """Returns but doesn't remove one character from the input stream."""
        return self.in_stream.peek_char()

    
    def eof(self, ch):
        """Return true if end-of-file character"""
        return ch == ''

    
    def error(self, message, line, column):
        raise LexerError(f'{message} at line {line}, column {column}')
    
    def move_to_next_line(self):
        if self.peek() == '\n':
            self.read()
            self.column = 1
            self.line += 1
        elif self.eof(self.peek()):
            self.column = 1
        elif self.peek().isspace():
            self.read()

    def next_token(self):
        """Return the next token in the lexer's input stream."""
        # read initial character
        
        ch = self.read()
        while ch == '\n':
            self.line += 1
            self.column = 0
            ch = self.read()
            
        while ch.isspace():
            ch = self.read()
        
        # TODO: Implement the rest of the next_token function
        
        if self.eof(ch):
            return Token(TokenType.EOS, "", self.line, self.column)
        # DOT
        if ch == '.':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.DOT, ch, line, self.column)
        # SEMICOLON
        if ch == ';':
            line = self.line
            if self.peek() == '\n':
                self.read()
                self.column = 1
                self.line += 1
            elif self.peek().isspace():
                self.read()
            return Token(TokenType.SEMICOLON, ch, line, self.column)
        # COMMA
        if ch == ',':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.COMMA, ch, line, self.column)
        # PLUS
        if ch == '+':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.PLUS, ch, self.line, self.column)
        # MINUS
        if ch == '-':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.MINUS, ch, self.line, self.column)
        # TIMES
        if ch == '*':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.TIMES, ch, self.line, self.column)
        # DIVIDE
        if ch == '/':
            # COMMENT
            if self.peek() == '/':
                start_col = self.column
                start_line = self.line
                comment = ''
                while not self.eof(ch) and ch != '\n':
                    ch = self.read()
                    
                    if not ch == '/' and ch != '\n':
                        comment += ch
                    
                    if ch == '\n':
                        self.line += 1
                        self.column = 0

                    if ch == '\n' and not self.peek().isalnum():
                        self.read()
                    
                return Token(TokenType.COMMENT, comment, start_line, start_col)
            
            if self.peek().isspace():
                self.read()
            elif self.peek().isdigit():
                Token(TokenType.INT_VAL, ch, self.line, self.column)
            
            return Token(TokenType.DIVIDE, ch, self.line, self.column)
        # LPAREN
        if ch == '(':     
            line = self.line
            self.move_to_next_line()
                
            return Token(TokenType.LPAREN, ch, line, self.column)
        # RPAREN
        if ch == ')':
            line = self.line
            self.move_to_next_line()
            
            if self.peek().isdigit():
                ch = self.read()
                return Token(TokenType.INT_VAL, ch, line, self.column)
            
            return Token(TokenType.RPAREN, ch, self.line, self.column)
        # LBRACKET
        if ch == '[':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.LBRACKET, ch, self.line, self.column)
        # RBRACKET
        if ch == ']':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.RBRACKET, ch, self.line, self.column)
        # LBRACE
        if ch == '{':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.LBRACE, ch, self.line, self.column)
        # RBRACE
        if ch == '}':
            line = self.line
            self.move_to_next_line()
            return Token(TokenType.RBRACE, ch, self.line, self.column)
        # ASSIGN
        if ch == '=':
            # EQUAL
            if self.peek() == '=':
                ch = self.read()
                self.column -= 0
                if self.peek().isspace():
                    self.read()
                return Token(TokenType.EQUAL, '==', self.line, self.column)

            if self.peek().isspace():
                self.read()
                         
            return Token(TokenType.ASSIGN, ch, self.line, self.column)
        # LESS
        if ch == '<':
            line = self.line
            start_col = self.column
            
            # LESS_EQ
            if self.peek() == '=':
                ch = self.read()
                if self.peek().isspace():
                    self.read()
                return Token(TokenType.LESS_EQ, '<=', self.line, self.column)
    
            self.move_to_next_line()
                
            return Token(TokenType.LESS, ch, line, start_col)
        # GREATER
        if ch == '>':
            # GREATER_EQ
            if self.peek() == '=':
                ch = self.read()
                if self.peek().isspace():
                    self.read()
                return Token(TokenType.GREATER_EQ, '>=', self.line, self.column)
            if self.peek().isspace():
                self.read()
            return Token(TokenType.GREATER, ch, self.line, self.column)
        if ch == '!':
            if self.peek() == '=':
                ch = self.read()
                self.column -= 1
                if self.peek().isspace():
                    self.read()
                return Token(TokenType.NOT_EQUAL, '!=', self.line, self.column)
            elif self.peek() == '>':
                raise MyPLError("Lexer Error: Invalid character")
            elif self.peek() == '!':
                raise MyPLError("Lexer Error: Invalid character")
            raise MyPLError("Lexer Error: Invalid character")
        # STRING_VAL
        if ch == '"':
            start_col = self.column
            string_val = ""
            while not self.eof(self.peek()) and self.peek() != '"':
                string_val += self.read()

            if self.peek() == '"':
                self.read()  # Consume the closing double quote
            
            # Include the spaces within the double quotes
            while not self.eof(self.peek()) and self.peek().isspace():
                string_val += self.read()
                

            return Token(TokenType.STRING_VAL, string_val.strip(), self.line, start_col)
            
        # INT or DOUBLE
        if ch.isdigit():
            start_col = self.column
            # one digit or more
            num_lexeme = ch
            while not self.eof(self.peek()) and not self.peek().isspace() and self.peek() != '.' and not self.peek() == ';' and not self.peek() == ')' and not self.peek() == ',' and not self.peek() == ']' and not self.peek() == '}' and not self.peek() == '-' and not self.peek() == '+' and not self.peek() == '/' and not self.peek() == '*':
                num_lexeme += self.read()

            # Check for leading zeros
            if num_lexeme.startswith('0') and len(num_lexeme) > 1:
                print('in error')
                raise MyPLError("Lexer Error: leading zeros are not allowed")

            # Check for dot in the middle of the number
            if self.peek() == '.':
                num_lexeme += self.read()
                if not self.peek().isdigit():
                    raise MyPLError("Lexer Error: digit expected after dot in a decimal number")
                while not self.eof(self.peek()) and not self.peek().isspace() and self.peek().isdigit():
                    num_lexeme += self.read()

            # Skip any following whitespace
            if self.peek().isspace():
                self.read()

            # Check for invalid characters in the number
            for pos, char in enumerate(num_lexeme):
                
                if not char.isdigit() and char != '.':
                    raise MyPLError(f"Lexer Error: contains invalid character '{char}' at position {pos + 1}")

            if '.' in num_lexeme:
                return Token(TokenType.DOUBLE_VAL, num_lexeme, self.line, start_col)
            else:
                return Token(TokenType.INT_VAL, num_lexeme, self.line, start_col)
        # IDENTIFIERS and KEY WORDS  
        if ch.isalpha():
            start_col = self.column
            type = ch
                
            # Check for keywords
            keyword_mapping = {
                'int': TokenType.INT_TYPE,
                'double': TokenType.DOUBLE_TYPE,
                'string': TokenType.STRING_TYPE,
                'bool': TokenType.BOOL_TYPE,
                'void': TokenType.VOID_TYPE,
                'and': TokenType.AND,
                'or': TokenType.OR,
                'not': TokenType.NOT,
                'if': TokenType.IF,
                'elseif': TokenType.ELSEIF,
                'else': TokenType.ELSE,
                'while': TokenType.WHILE,
                'for': TokenType.FOR,
                'null': TokenType.NULL_VAL,
                'true': TokenType.BOOL_VAL,
                'false': TokenType.BOOL_VAL,
                'return': TokenType.RETURN,
                'struct': TokenType.STRUCT,
                'array': TokenType.ARRAY,
                'new': TokenType.NEW,
                'main': TokenType.ID
            }
            
            while not self.eof(self.peek()) and (self.peek().isalnum() or self.peek() == '_' or (type + self.peek()).isalpha()) and type not in keyword_mapping:
                char = self.read()

                if self.peek() == '_':
                    type += char
                    char = self.read()
                    type += char
                    while self.peek().isalpha():
                        char = self.read()
                        type += char
                elif char.isalnum() or char == '_':
                    type += char
                    # ELSEIF
                    if type == 'else' and self.peek() == 'i':
                        type += self.read()
                        type += self.read()
                elif char == ')':
                    return Token(TokenType.RPAREN, char ,self.line, start_col)
                elif char == '(':
                    return Token(TokenType.LPAREN, char ,self.line, start_col)
                             
            if self.peek().isspace():
                self.read()
                    
            if self.peek() == '\n':
                self.read()
                
            # Check if it's a keyword
            if type in keyword_mapping:
                return Token(keyword_mapping[type], type, self.line, start_col)
            else:
                return Token(TokenType.ID, type, self.line, start_col)
            
        if ch == '#':
            raise MyPLError(f"Lexer Error: contains invalid character")


        # If none of the specific cases match, raise an error
        self.error(f"Unexpected character '{ch}'", self.line, self.column)