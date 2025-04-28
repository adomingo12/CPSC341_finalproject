"""MyPL simple syntax checker (parser) implementation.

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326
"""

from mypl_error import *
from mypl_token import *
from mypl_lexer import *

class SimpleParser:

    def __init__(self, lexer):
        """Create a MyPL syntax checker (parser). 
        
        Args:
            lexer -- The lexer to use in the parser.

        """
        self.lexer = lexer
        self.curr_token = None

        
    def parse(self):
        """Start the parser."""
        self.advance()
        while not self.match(TokenType.EOS):
            if self.match(TokenType.STRUCT):
                self.struct_def()
            else:
                self.fun_def()
        self.eat(TokenType.EOS, 'expecting EOF')

        
    #----------------------------------------------------------------------
    # Helper functions
    #----------------------------------------------------------------------

    def error(self, message):
        """Raises a formatted parser error.

        Args:
            message -- The basic message (expectation)

        """
        lexeme = self.curr_token.lexeme
        line = self.curr_token.line
        column = self.curr_token.column
        err_msg = f'{message} found "{lexeme}" at line {line}, column {column}'
        raise ParserError(err_msg)


    def advance(self):
        """Moves to the next token of the lexer."""
        self.curr_token = self.lexer.next_token()
        # skip comments
        while self.match(TokenType.COMMENT):
            self.curr_token = self.lexer.next_token()

            
    def match(self, token_type):
        """True if the current token type matches the given one.

        Args:
            token_type -- The token type to match on.

        """
        return self.curr_token.token_type == token_type

    
    def match_any(self, token_types):
        """True if current token type matches on of the given ones.

        Args:
            token_types -- Collection of token types to check against.

        """
        for token_type in token_types:
            if self.match(token_type):
                return True
        return False

    
    def eat(self, token_type, message):
        """Advances to next token if current tokey type matches given one,
        otherwise produces and error with the given message.

        Args: 
            token_type -- The totken type to match on.
            message -- Error message if types don't match.

        """
        if not self.match(token_type):
            self.error(message)
        self.advance()

        
    def is_bin_op(self):
        """Returns true if the current token is a binary operation token."""
        ts = [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE,
              TokenType.AND, TokenType.OR, TokenType.EQUAL, TokenType.LESS,
              TokenType.GREATER, TokenType.LESS_EQ, TokenType.GREATER_EQ,
              TokenType.NOT_EQUAL]
        return self.match_any(ts)

    
    #----------------------------------------------------------------------
    # Recursive descent functions
    #----------------------------------------------------------------------
        
    def struct_def(self):
        self.eat(TokenType.STRUCT, 'expecting STRUCT token type')
        self.eat(TokenType.ID, 'expecting ID token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        self.fields()
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        
    def fields(self):
        while not self.match(TokenType.RBRACE):
            self.data_type()
            self.eat(TokenType.ID, 'expecting ID token type')
            self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
            
    def fun_def(self):
        if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.ID, TokenType.ARRAY]):
            self.data_type()
        elif self.match(TokenType.VOID_TYPE):
            self.eat(TokenType.VOID_TYPE, 'expecting VOID_TYPE token type')
        else:
            self.error('invalid token type')

        self.eat(TokenType.ID, 'expecting ID token type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        self.params()
        if not self.match(TokenType.RPAREN):
            self.error('missing closing parenthesis for function parameters')
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOS):
            self.stmt()        
        if not self.match(TokenType.RBRACE):
            self.error('missing closing brace for function body')
                
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
 
        
    def params(self):
        if self.match(TokenType.RPAREN):
            return
        
        self.data_type()
        self.eat(TokenType.ID, 'expecting ID token type')
        
        if not self.match(TokenType.COMMA):
            return
        
        while self.match(TokenType.COMMA):
            self.eat(TokenType.COMMA, 'expecting COMMA token type')
            self.data_type()
            self.eat(TokenType.ID, 'expecting ID token type')
    
    def data_type(self):
        if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE]):
            self.base_type()
        elif self.match(TokenType.ID):
            self.eat(TokenType.ID, 'expecting ID token type')
        elif self.match(TokenType.ARRAY):
            self.eat(TokenType.ARRAY, 'expecting ARRAY token type')
            self.data_type()
        else:
            self.var_rvalue()

    def base_type(self):
        if self.match(TokenType.INT_TYPE):
            self.eat(TokenType.INT_TYPE, 'expecting INT_TYPE token type')
        elif self.match(TokenType.DOUBLE_TYPE):
            self.eat(TokenType.DOUBLE_TYPE, 'expecting DOUBLE_TYPE token type')
        elif self.match(TokenType.BOOL_TYPE):
            self.eat(TokenType.BOOL_TYPE, 'expecting BOOL_TYPE token type')
        elif self.match(TokenType.STRING_TYPE):
            self.eat(TokenType.STRING_TYPE, 'expecting STRING_TYPE token type')
            
    def stmt(self):
        if self.match(TokenType.WHILE):
            self.while_stmt()
        elif self.match(TokenType.ELSEIF):
            self.error('missing IF keyword before ELSEIF statement') 
        elif self.match(TokenType.ELSE):
            self.error('missing IF keyword before ELSEIF statement') 
        elif self.match(TokenType.IF):
            self.if_stmt()
        elif self.match(TokenType.FOR):
            self.for_stmt()
        elif self.match(TokenType.RETURN):
            self.return_stmt()
            self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        elif self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.ARRAY]):            
            self.vdecl_stmt()
            self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        elif self.match(TokenType.ID):
            self.eat(TokenType.ID, 'expecting ID token type')
            if self.match(TokenType.LPAREN):
                self.call_expr()
                self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
            elif self.match_any([TokenType.LBRACE, TokenType.DOT, TokenType.ASSIGN]):
                self.assign_stmt()
                self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
            else:  
                self.vdecl_stmt()
                self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        else:
            self.error('invalid stmt token type')
            
    def vdecl_stmt(self):
        if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.ARRAY]):
            self.data_type()
            self.eat(TokenType.ID, 'expecting ID token type')
        else:
            self.data_type()
        
        if self.match(TokenType.ASSIGN):
            self.eat(TokenType.ASSIGN, 'expecting ASSIGN token type')
            self.expr()
        else:
            pass
        
    def assign_stmt(self):
        self.lvalue()
        self.eat(TokenType.ASSIGN, 'expecting ASSIGN token type')
        self.expr()
        
    def lvalue(self):
        if self.match(TokenType.ASSIGN):
            pass
        if self.match(TokenType.ID):
            self.eat(TokenType.ID, 'expecting ID token type')
        else:
            pass
            
        if self.match(TokenType.LBRACKET):
            self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
            self.expr()
            self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
        else:
            pass
        
        if self.match(TokenType.DOT):
            while self.match(TokenType.DOT):
                self.eat(TokenType.DOT, 'expecting DOT token type')
                self.eat(TokenType.ID, 'expecting ID token type')
                if self.match(TokenType.LBRACKET):
                    self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
                    self.expr()
                    self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
                else:
                    pass
        else:
            pass
        
     
    def if_stmt(self):
        self.eat(TokenType.IF, 'expecting IF token type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        if self.match(TokenType.RPAREN):
            self.error('must have expression in IF statement')
        self.expr()
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE):
            self.stmt()
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        self.if_stmt_t() 
        
    def if_stmt_t(self):
        if self.match(TokenType.ELSEIF):    
            self.eat(TokenType.ELSEIF, 'expecting ELSEIF token type')
            self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
            self.expr()
            self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
            self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
            while not self.match(TokenType.RBRACE):
                self.stmt()
            self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
            self.if_stmt_t()   
        elif self.match(TokenType.ELSE):
            self.eat(TokenType.ELSE, 'expecting ELSE token type')
            self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
            while not self.match(TokenType.RBRACE):
                self.stmt()
            self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        else:
            pass
    
    def while_stmt(self):
        self.eat(TokenType.WHILE, 'expecting WHILE toke type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        if self.match(TokenType.RPAREN):
            self.error('must have expression in WHILE loop statement')
        self.expr()
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE):
            self.stmt()
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
    
    def for_stmt(self):
        self.eat(TokenType.FOR, 'expecting FOR token type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        self.vdecl_stmt()
        self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        self.expr()
        self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        self.assign_stmt()
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE):
            self.stmt()
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
    
    def call_expr(self):
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        if self.match(TokenType.RPAREN):
            self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
            return
        self.expr()
        while self.match(TokenType.COMMA):
            self.eat(TokenType.COMMA, 'expecting COMMA token type')
            self.expr()
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        
    def return_stmt(self):
        self.eat(TokenType.RETURN, 'expecting RETURN token type')
        self.expr() 
        
    def expr(self):
        if self.match_any([TokenType.INT_VAL, TokenType.DOUBLE_VAL, TokenType.BOOL_VAL, TokenType.STRING_VAL, TokenType.NULL_VAL, TokenType.NEW, TokenType.ID]):
            self.rvalue()
        elif self.match(TokenType.NOT):
            self.eat(TokenType.NOT, 'expecting NOT token type')
            self.expr()
        elif self.match(TokenType.LPAREN):
            self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
            self.expr()
            self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        elif self.match(TokenType.RPAREN):
            pass
        else:
            self.error('must have an expression')
            
        if self.is_bin_op():
            self.bin_op()
            self.expr()
        else:
            pass
    
    def bin_op(self):
        if self.match(TokenType.PLUS):
            self.eat(TokenType.PLUS, 'expecting PLUS token type')
        elif self.match(TokenType.MINUS):
            self.eat(TokenType.MINUS, 'expecting MINUS token type')
        elif self.match(TokenType.TIMES):
            self.eat(TokenType.TIMES, 'expecting MINUS token type')
        elif self.match(TokenType.DIVIDE):
            self.eat(TokenType.DIVIDE, 'expecting MINUS token type')
        elif self.match(TokenType.AND):
            self.eat(TokenType.AND, 'expecting MINUS token type')
        elif self.match(TokenType.OR):
            self.eat(TokenType.OR, 'expecting MINUS token type')
        elif self.match(TokenType.EQUAL):
            self.eat(TokenType.EQUAL, 'expecting MINUS token type')
        elif self.match(TokenType.LESS):
            self.eat(TokenType.LESS, 'expecting MINUS token type')
        elif self.match(TokenType.GREATER):
            self.eat(TokenType.GREATER, 'expecting MINUS token type')
        elif self.match(TokenType.LESS_EQ):
            self.eat(TokenType.LESS_EQ, 'expecting MINUS token type')
        elif self.match(TokenType.GREATER_EQ):
            self.eat(TokenType.GREATER_EQ, 'expecting MINUS token type')
        elif self.match(TokenType.NOT_EQUAL):
            self.eat(TokenType.NOT_EQUAL, 'expecting MINUS token type')
    
    def rvalue(self):
        if self.match_any([TokenType.INT_VAL, TokenType.DOUBLE_VAL, TokenType.BOOL_VAL, TokenType.STRING_VAL]):
            self.base_rvalue()
        elif self.match(TokenType.NULL_VAL):
            self.eat(TokenType.NULL_VAL, 'expecting NULL_VAL token type')
        elif self.match(TokenType.NEW):
            self.new_rvalue()
        elif self.match(TokenType.ID):
            self.eat(TokenType.ID, 'expecting ID token type')
            if self.match_any([TokenType.LBRACKET, TokenType.DOT]):
                self.var_rvalue()
            elif self.match(TokenType.LPAREN):
                self.call_expr()
    
    def new_rvalue(self):
        self.eat(TokenType.NEW, 'expecting NEW token type')
        
        if self.match(TokenType.ID):
            self.eat(TokenType.ID, 'expecting ID token type')
        else:
            self.base_type()
            
        if self.match(TokenType.LPAREN):
            self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
            self.expr()
            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA, 'expecting COMMA token type')
                self.expr()
            self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        elif self.match(TokenType.LBRACKET):  
            self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
            self.expr()
            self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')

    def base_rvalue(self):
        if self.match(TokenType.INT_VAL):
            self.eat(TokenType.INT_VAL, 'expecting INT_VAL token type')
        elif self.match(TokenType.DOUBLE_VAL):
            self.eat(TokenType.DOUBLE_VAL, 'expecting DOUBLE_VAL token type')
        elif self.match(TokenType.BOOL_VAL):
            self.eat(TokenType.BOOL_VAL, 'expecting BOOL_VAL token type')
        elif self.match(TokenType.STRING_VAL):
            self.eat(TokenType.STRING_VAL, 'expecting STRING_VAL token type')
    
    def var_rvalue(self):
        if self.match(TokenType.LBRACKET):
            self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
            self.expr()
            self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
        else:
            pass
         
        if self.match(TokenType.DOT):
            while self.match(TokenType.DOT):
                self.eat(TokenType.DOT, 'expecting DOT token type')
                self.eat(TokenType.ID, 'expecting ID token type')
                if self.match(TokenType.LBRACKET):
                    self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
                    self.expr()
                    self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
                else:
                    pass
        else:
            pass           