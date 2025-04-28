"""MyPL AST parser implementation.

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326
"""

from src.mypl_error import *
from src.mypl_token import *
from src.mypl_lexer import *
from src.mypl_ast import *

BUILT_INS = ['print', 'input', 'itos', 'itod', 'dtos', 'dtoi', 'stoi', 'stod',
             'length', 'get']

class ASTParser:

    def __init__(self, lexer):
        """Create a MyPL syntax checker (parser). 
        
        Args:
            lexer -- The lexer to use in the parser.

        """
        self.lexer = lexer
        self.curr_token = None

        
    def parse(self):
        """Start the , returning a Program AST node."""
        program_node = Program([], [])
        self.advance()
        while not self.match(TokenType.EOS):
            if self.match(TokenType.STRUCT):
                self.struct_def(program_node)
            else:
                self.fun_def(program_node)
        self.eat(TokenType.EOS, 'expecting EOF')
        return program_node

        
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
        """Returns true if the current token is a binary operator."""
        ts = [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE,
              TokenType.AND, TokenType.OR, TokenType.EQUAL, TokenType.LESS,
              TokenType.GREATER, TokenType.LESS_EQ, TokenType.GREATER_EQ,
              TokenType.NOT_EQUAL]
        return self.match_any(ts)


    #----------------------------------------------------------------------
    # Recursive descent functions
    #----------------------------------------------------------------------


    # TODO: Finish the recursive descent functions below. Note that
    # you should copy in your functions from HW-2 and then instrument
    # them to build the corresponding AST objects.
    
    def struct_def(self, program_node):
        struct_def_node = StructDef(None, None)
        self.eat(TokenType.STRUCT, 'expecting STRUCT token type')
        struct_def_node.struct_name = self.curr_token
        self.eat(TokenType.ID, 'expecting ID token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        fields_node = self.fields()
        struct_def_node.fields = fields_node
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        
        program_node.struct_defs.append(struct_def_node)
        
    def fields(self):
        fields_list = []
        while not self.match(TokenType.RBRACE):
            var_def_node = VarDef(None, None)
            data_type_node = self.data_type()
            var_def_node.data_type = data_type_node
            var_def_node.var_name = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
            self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
            
            fields_list.append(var_def_node)
            
        return fields_list
            
    def fun_def(self, program_node):
        fun_def_node = FunDef(None, None, [], [])
        
        # return type
        if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.ID, TokenType.ARRAY]):
            data_type_node = self.data_type()
            fun_def_node.return_type = data_type_node
        elif self.match(TokenType.VOID_TYPE):
            fun_def_node.return_type = self.data_type()
            self.eat(TokenType.VOID_TYPE, 'expecting VOID_TYPE token type')
        else:
            self.error('invalid token type')

        # fun_name
        fun_def_node.fun_name = self.curr_token
        self.eat(TokenType.ID, 'expecting ID token type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        
        # params
        param_node = self.params()
        fun_def_node.params = param_node
        
        if not self.match(TokenType.RPAREN):
            self.error('missing closing parenthesis for function parameters')
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOS):
            stmt_result = self.stmt() 
            fun_def_node.stmts.append(stmt_result)  
            
        if not self.match(TokenType.RBRACE):
            self.error('missing closing brace for function body')
                
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        
        program_node.fun_defs.append(fun_def_node)
 
        
    def params(self):
        var_def_node_list = []
        var_def_node = VarDef(None, None)
        if self.match(TokenType.RPAREN):
            return var_def_node_list
        
        var_def_node.data_type = self.data_type()
        var_def_node.var_name = self.curr_token
        self.eat(TokenType.ID, 'expecting ID token type')
        
        var_def_node_list.append(var_def_node)
        if not self.match(TokenType.COMMA):
            return var_def_node_list
        
        while self.match(TokenType.COMMA):
            var_def_node2 = VarDef(None, None)
            self.eat(TokenType.COMMA, 'expecting COMMA token type')
            var_def_node2.data_type = self.data_type()
            var_def_node2.var_name = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
            var_def_node_list.append(var_def_node2)
    
        return var_def_node_list
            
    def data_type(self):
        data_type_node = DataType(False, None)
        if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.VOID_TYPE]):
            data_type_node.type_name = self.base_type()
        elif self.match(TokenType.ID):
            data_type_node.type_name = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
        elif self.match(TokenType.ARRAY):
            data_type_node.is_array = True
            self.eat(TokenType.ARRAY, 'expecting ARRAY token type')
            if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE]):
                data_type_node.type_name = self.base_type()
            elif self.match(TokenType.ID):
                data_type_node.type_name = self.curr_token
                self.eat(TokenType.ID, 'expecting ID token type')
        else:
            self.var_rvalue()
          
        return data_type_node

    def base_type(self):
        if self.match(TokenType.INT_TYPE):
            base_type_node = self.curr_token
            self.eat(TokenType.INT_TYPE, 'expecting INT_TYPE token type')
        elif self.match(TokenType.DOUBLE_TYPE):
            base_type_node = self.curr_token
            self.eat(TokenType.DOUBLE_TYPE, 'expecting DOUBLE_TYPE token type')
        elif self.match(TokenType.BOOL_TYPE):
            base_type_node = self.curr_token
            self.eat(TokenType.BOOL_TYPE, 'expecting BOOL_TYPE token type')
        elif self.match(TokenType.STRING_TYPE):
            base_type_node = self.curr_token
            self.eat(TokenType.STRING_TYPE, 'expecting STRING_TYPE token type')
        else:
            base_type_node = self.curr_token
            
        return base_type_node
            
    def stmt(self):
        if self.match(TokenType.WHILE):
            while_result = self.while_stmt()
            return while_result
        elif self.match(TokenType.ELSEIF):
            self.error('missing IF keyword before ELSEIF statement') 
        elif self.match(TokenType.ELSE):
            self.error('missing IF keyword before ELSEIF statement') 
        elif self.match(TokenType.IF):
            if_result = self.if_stmt()
            return if_result
        elif self.match(TokenType.FOR):
            for_results = self.for_stmt()
            return for_results
        elif self.match(TokenType.RETURN):
            return_result = self.return_stmt()
            self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
            return return_result
    
        elif self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.ARRAY]):            
            vdecl_result = self.vdecl_stmt(None)
            self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
            return vdecl_result
        
        elif self.match(TokenType.ID):
            id_result = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
            if self.match(TokenType.LPAREN):
                call_result = self.call_expr(id_result)
                self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
                return call_result
            elif self.match_any([TokenType.LBRACE, TokenType.DOT, TokenType.ASSIGN, TokenType.LBRACKET]):
                assign_result = self.assign_stmt(id_result)
                self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
                return assign_result
            else:  
                vdecl_result = self.vdecl_stmt(id_result)
                self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
                return vdecl_result
        else:
            self.error('invalid stmt token type')
            
    def vdecl_stmt(self, id_type):
        var_decl_node = VarDecl(None, None)
        var_def_node = VarDef(None, None)
        if self.match_any([TokenType.INT_TYPE, TokenType.DOUBLE_TYPE, TokenType.BOOL_TYPE, TokenType.STRING_TYPE, TokenType.ARRAY]):
            data_type_result = self.data_type()
            var_def_node.data_type = data_type_result
            var_def_node.var_name = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
            
        elif self.match(TokenType.ID):
            data_type_node = DataType(False, None)
            data_type_node.type_name = id_type
            var_def_node.var_name = self.curr_token
            var_def_node.data_type = data_type_node
            self.eat(TokenType.ID, 'expecting ID token type')
        
        var_decl_node.var_def = var_def_node
        
        if self.match(TokenType.ASSIGN):
            self.eat(TokenType.ASSIGN, 'expecting ASSIGN token type')
            expr_result = self.expr()
            if self.match(TokenType.LPAREN):
                fun_name = expr_result.first.rvalue.path[0].var_name
                call_result = self.call_expr(fun_name)
                expr_result.first = SimpleTerm(call_result)
            var_decl_node.expr = expr_result

        return var_decl_node
        
    def assign_stmt(self, id_name):
        
        assign_stmt_node = AssignStmt(None, None)
        lvalue_result = self.lvalue(id_name)
        assign_stmt_node.lvalue = lvalue_result
        self.eat(TokenType.ASSIGN, 'expecting ASSIGN token type')
        expr_results = self.expr()
        assign_stmt_node.expr = expr_results
        
        return assign_stmt_node
        
    def lvalue(self, id_name):
        lvalue_list = []
        var_ref_node = VarRef(None, None)
        if not id_name == None:
            var_ref_node.var_name = id_name
        else:
            var_ref_node.var_name = self.curr_token
            self.advance()
        
        if self.match(TokenType.LBRACKET):
            self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
            expr_results = self.expr()
            var_ref_node.array_expr = expr_results
            self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
        
        lvalue_list.append(var_ref_node)
        
        if self.match(TokenType.DOT):
            while self.match(TokenType.DOT):
                var_ref_node2 = VarRef(None, None)
                self.eat(TokenType.DOT, 'expecting DOT token type')
                var_ref_node2.var_name = self.curr_token
                self.eat(TokenType.ID, 'expecting ID token type')
                if self.match(TokenType.LBRACKET):
                    self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
                    expr_results2 = self.expr()
                    var_ref_node2.array_expr = expr_results2
                    self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
                lvalue_list.append(var_ref_node2)
            return lvalue_list
        else:
            return lvalue_list
        
    def if_stmt(self):
        if_stmt_node = IfStmt(None, [], [])
        basic_if_node = BasicIf(None, [])
        self.eat(TokenType.IF, 'expecting IF token type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        if self.match(TokenType.RPAREN):
            self.error('must have expression in IF statement')
        expr_results = self.expr()
        basic_if_node.condition = expr_results
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE):
            stmt_result = self.stmt()
            basic_if_node.stmts.append(stmt_result)
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        if_stmt_node.if_part = basic_if_node
        self.if_stmt_t(if_stmt_node) 
        
        return if_stmt_node
        
    def if_stmt_t(self, if_stmt_node):
        basic_if_node = BasicIf(None, [])
        if self.match(TokenType.ELSEIF):    
            self.eat(TokenType.ELSEIF, 'expecting ELSEIF token type')
            self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
            expr_results = self.expr()
            basic_if_node.condition = expr_results
            self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
            self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
            while not self.match(TokenType.RBRACE):
                stmt_result = self.stmt()
                if type(stmt_result) == CallExpr:
                    expr_node = Expr(None, SimpleTerm(stmt_result), None, None)
                    basic_if_node.stmts.append(expr_node)
                basic_if_node.stmts.append(stmt_result)
            self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
            if_stmt_node.else_ifs.append(basic_if_node)
            self.if_stmt_t(if_stmt_node)   
        elif self.match(TokenType.ELSE):
            self.eat(TokenType.ELSE, 'expecting ELSE token type')
            self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
            while not self.match(TokenType.RBRACE):
                stmt_result = self.stmt()
                if type(stmt_result) == CallExpr:
                    expr_node = Expr(None, SimpleTerm(stmt_result), None, None)
                    if_stmt_node.else_stmts.append(expr_node)
                if_stmt_node.else_stmts.append(stmt_result)
            self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
    
    def while_stmt(self):
        while_stmt_node = WhileStmt(None, [])
        self.eat(TokenType.WHILE, 'expecting WHILE toke type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        if self.match(TokenType.RPAREN):
            self.error('must have expression in WHILE loop statement')
        expr_results = self.expr()
        while_stmt_node.condition = expr_results
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        while not self.match(TokenType.RBRACE):
            stmt_result = self.stmt()
            while_stmt_node.stmts.append(stmt_result)
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        
        return while_stmt_node
    
    def for_stmt(self):
        for_stmt_node = ForStmt(None, None, None, [])
        
        self.eat(TokenType.FOR, 'expecting FOR token type')
        self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
        vdecl_results = self.vdecl_stmt(None)
        for_stmt_node.var_decl = vdecl_results
        self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        expr_results = self.expr()
        
        if self.match(TokenType.LPAREN) and expr_results.op == None:
            fun_name = expr_results.first.rvalue.path[0].var_name
            call_result = self.call_expr(fun_name)
            expr_results.first = SimpleTerm(call_result)
        elif self.match(TokenType.LPAREN) and not expr_results.op == None:
            fun_name = expr_results.rest.first.rvalue.path[0].var_name
            call_result = self.call_expr(fun_name)
            expr_results.rest = Expr(False, SimpleTerm(call_result), None, None)

        for_stmt_node.condition = expr_results
        self.eat(TokenType.SEMICOLON, 'expecting SEMICOLON token type')
        assign_results = self.assign_stmt(None)
        for_stmt_node.assign_stmt = assign_results
        self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        self.eat(TokenType.LBRACE, 'expecting LBRACE token type')
        
        while not self.match(TokenType.RBRACE):
            stmt_result = self.stmt()
            for_stmt_node.stmts.append(stmt_result)
        self.eat(TokenType.RBRACE, 'expecting RBRACE token type')
        
        return for_stmt_node
    
    def call_expr(self, id_node):
            # creating node from the CallExpr class
            call_expr_node = CallExpr(None, None)

            # using passed in saved ID, set fun_name param to it
            call_expr_node.fun_name = id_node

            # looking for start to call
            if(self.match(TokenType.LPAREN)):
                self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
                # list to hold expr nodes
                expr_list = []
                if(self.match(TokenType.PLUS) or self.match(TokenType.MINUS) or self.match(TokenType.TIMES)
                    or self.match(TokenType.DIVIDE) or self.match(TokenType.AND) or self.match(TokenType.OR)
                    or self.match(TokenType.EQUAL) or self.match(TokenType.LESS) or self.match(TokenType.GREATER)
                    or self.match(TokenType.LESS_EQ) or self.match(TokenType.GREATER_EQ) or self.match(TokenType.NOT_EQUAL)
                    or self.match(TokenType.LPAREN) or self.match(TokenType.NOT) or self.match(TokenType.INT_VAL) or self.match(TokenType.DOUBLE_VAL) or self.match(TokenType.BOOL_VAL)
                    or self.match(TokenType.STRING_VAL) or self.match(TokenType.NULL_VAL) or self.match(TokenType.ID)
                    or self.match(TokenType.NEW)):
                    # setting local nodes to expression found
                    expr_node = self.expr()
                    if self.match(TokenType.LPAREN):
                        fun_name = expr_node.first.rvalue.path[0].var_name
                        call_result = self.call_expr(fun_name)
                        expr_node.first = SimpleTerm(call_result)
                        expr_list.append(expr_node)
                    else:
                        # appending node to list
                        expr_list.append(expr_node)

                        # if there is multiple params
                        while(self.match(TokenType.COMMA)):
                            self.eat(TokenType.COMMA, 'expecting COMMA token type')

                            # finding next param
                            expr_node = self.expr()
                            expr_list.append(expr_node)
                # setting built expr list to args param
                call_expr_node.args = expr_list
                self.eat(TokenType.RPAREN, 'Expecting RPAREN token type')
            return call_expr_node
        
    def return_stmt(self):
        return_stmt_node = ReturnStmt(None)
        self.eat(TokenType.RETURN, 'expecting RETURN token type')
        expr_results = self.expr()
        if type(expr_results.first) == SimpleTerm and type(expr_results.first.rvalue) == VarRValue:
            fun_name = expr_results.first.rvalue.path[0].var_name
            if self.match(TokenType.LPAREN) and expr_results.op == None:
                call_result = self.call_expr(fun_name)
                expr_results.first = SimpleTerm(call_result)
                while self.is_bin_op():
                    expr_results.op = self.curr_token
                    self.advance()
                    fun_name = self.curr_token
                    self.advance()
                    call_result2 = self.call_expr(fun_name)
                    expr_results.rest = Expr(False, SimpleTerm(call_result2), None, None)
            elif self.match(TokenType.LPAREN) and not expr_results.op == None:
                fun_name = expr_results.rest.first.rvalue.path[0].var_name
                call_result = self.call_expr(fun_name)
                expr_results.rest = Expr(False, SimpleTerm(call_result), None, None)
 
        return_stmt_node.expr = expr_results
        
        return return_stmt_node
    
    def expr(self, expr_node = None):
        # creating node from the Expr class
        expr_node = Expr(None, None, None, None)

        # looking for basic r -values (simple terms)
        if(self.match(TokenType.INT_VAL) or self.match(TokenType.DOUBLE_VAL) or self.match(TokenType.BOOL_VAL)
             or self.match(TokenType.STRING_VAL) or self.match(TokenType.NULL_VAL) or self.match(TokenType.ID)
             or self.match(TokenType.NEW)):
            if(expr_node.not_op != True):
                expr_node.not_op = False

            # setting r_value_node to found rhs
            r_value_node = self.rvalue()

            # setting the first of the expr_node(ExprTerm) to found r -value
            expr_node.first = SimpleTerm(r_value_node)

        # finding NOT expr case
        elif(self.match(TokenType.NOT)):
            self.advance()

            # finding the expression after the NOT
            expr_node = self.expr()

            # setting not_op to true since it has a NOT
            expr_node.not_op = True

        # looking for complex expressions
        elif(self.match(TokenType.LPAREN)):
            # creating new expr node
            expr_node = Expr(False, None, None, None)

            # creating node from ComplexTerm class
            complex_term_node = ComplexTerm(None)
            self.advance()

            # setting expr param in complex node to the found expr
            complex_term_node.expr = self.expr()

            # setting the first param(ExprTerm) to the complex node
            expr_node.first = complex_term_node
            self.eat(TokenType.RPAREN, 'Expecting )')
        else:
            self.error('Improper expression syntax')
       
        # looking for binary operators
        if self.match_any([TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE
                        ,TokenType.AND, TokenType.OR, TokenType.EQUAL, TokenType.LESS, TokenType.GREATER
                        , TokenType.LESS_EQ, TokenType.GREATER_EQ, TokenType.NOT_EQUAL]):
                        # determining bin operator to expr param
                        expr_node.op = self.bin_op()

                        # finding the rest of the expression
                        expr_results = self.expr()

                        # setting the results of expr param to the rest of the expr
                        expr_node.rest = expr_results
                       
                        return expr_node
        return expr_node

              
    def bin_op(self):
        if self.match(TokenType.PLUS):
            bin_op_token = self.curr_token
            self.eat(TokenType.PLUS, 'expecting PLUS token type')
        elif self.match(TokenType.MINUS):
            bin_op_token = self.curr_token
            self.eat(TokenType.MINUS, 'expecting MINUS token type')
        elif self.match(TokenType.TIMES):
            bin_op_token = self.curr_token
            self.eat(TokenType.TIMES, 'expecting MINUS token type')
        elif self.match(TokenType.DIVIDE):
            bin_op_token = self.curr_token
            self.eat(TokenType.DIVIDE, 'expecting MINUS token type')
        elif self.match(TokenType.AND):
            bin_op_token = self.curr_token
            self.eat(TokenType.AND, 'expecting MINUS token type')
        elif self.match(TokenType.OR):
            bin_op_token = self.curr_token
            self.eat(TokenType.OR, 'expecting MINUS token type')
        elif self.match(TokenType.EQUAL):
            bin_op_token = self.curr_token
            self.eat(TokenType.EQUAL, 'expecting MINUS token type')
        elif self.match(TokenType.LESS):
            bin_op_token = self.curr_token
            self.eat(TokenType.LESS, 'expecting MINUS token type')
        elif self.match(TokenType.GREATER):
            bin_op_token = self.curr_token
            self.eat(TokenType.GREATER, 'expecting MINUS token type')
        elif self.match(TokenType.LESS_EQ):
            bin_op_token = self.curr_token
            self.eat(TokenType.LESS_EQ, 'expecting MINUS token type')
        elif self.match(TokenType.GREATER_EQ):
            bin_op_token = self.curr_token
            self.eat(TokenType.GREATER_EQ, 'expecting MINUS token type')
        elif self.match(TokenType.NOT_EQUAL):
            bin_op_token = self.curr_token
            self.eat(TokenType.NOT_EQUAL, 'expecting MINUS token type')
          
        return bin_op_token
    
    def rvalue(self):
        if self.match_any([TokenType.INT_VAL, TokenType.DOUBLE_VAL, TokenType.BOOL_VAL, TokenType.STRING_VAL]):
            simple_rvalue_node = SimpleRValue(None)
            base_rvalue_result = self.base_rvalue()
            simple_rvalue_node.value = base_rvalue_result
            return simple_rvalue_node
        elif self.match(TokenType.NULL_VAL):
            simple_rvalue_node = SimpleRValue(None)
            simple_rvalue_node.value = self.curr_token
            self.eat(TokenType.NULL_VAL, 'expecting NULL_VAL token type')
            return simple_rvalue_node
        elif self.match(TokenType.NEW):
            new_result = self.new_rvalue()
            return new_result
        elif self.match(TokenType.ID):
            var_rvalue_node = VarRValue([])
            var_ref_node = VarRef(None, None)
            var_ref_node.var_name = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
            var_rvalue_node.path.append(var_ref_node)
            if self.match_any([TokenType.LBRACKET, TokenType.DOT]):
                self.var_rvalue(var_ref_node, var_rvalue_node)
    
            return var_rvalue_node
    
    def new_rvalue(self):
        new_rvalue_node = NewRValue(None, None, [])
        self.eat(TokenType.NEW, 'expecting NEW token type')
        
        
        if self.match(TokenType.ID):
            new_rvalue_node.type_name = self.curr_token
            self.eat(TokenType.ID, 'expecting ID token type')
        else:
            base_result = self.base_type()
            new_rvalue_node.type_name = base_result
            
        if self.match(TokenType.LPAREN):
            self.eat(TokenType.LPAREN, 'expecting LPAREN token type')
            if self.match(TokenType.RPAREN):
                self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
                return new_rvalue_node
            expr_results = self.expr()
            new_rvalue_node.struct_params.append(expr_results)
            while self.match(TokenType.COMMA):
                self.eat(TokenType.COMMA, 'expecting COMMA token type')
                expr_results = self.expr()
                new_rvalue_node.struct_params.append(expr_results)
            self.eat(TokenType.RPAREN, 'expecting RPAREN token type')
        elif self.match(TokenType.LBRACKET):  
            self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
            expr_results = self.expr()
            new_rvalue_node.array_expr = expr_results
            new_rvalue_node.struct_params = None
            self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
        
        return new_rvalue_node

    def base_rvalue(self):
        if self.match(TokenType.INT_VAL):
            base_value = self.curr_token
            self.eat(TokenType.INT_VAL, 'expecting INT_VAL token type')
        elif self.match(TokenType.DOUBLE_VAL):
            base_value = self.curr_token
            self.eat(TokenType.DOUBLE_VAL, 'expecting DOUBLE_VAL token type')
        elif self.match(TokenType.BOOL_VAL):
            base_value = self.curr_token
            self.eat(TokenType.BOOL_VAL, 'expecting BOOL_VAL token type')
        elif self.match(TokenType.STRING_VAL):
            base_value = self.curr_token
            self.eat(TokenType.STRING_VAL, 'expecting STRING_VAL token type')
            
        return base_value
    
    def var_rvalue(self, var_ref_node, var_rvalue_node):
        if self.match(TokenType.LBRACKET):
            self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
            expr_result = self.expr()
            var_ref_node.array_expr = expr_result
            self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type')
         
        if self.match(TokenType.DOT):
            while self.match(TokenType.DOT):
                var_ref_node2 = VarRef(None, None)
                self.eat(TokenType.DOT, 'expecting DOT token type')
                var_ref_node2.var_name = self.curr_token
                self.eat(TokenType.ID, 'expecting ID token type')
                if self.match(TokenType.LBRACKET):
                    self.eat(TokenType.LBRACKET, 'expecting LBRACKET token type')
                    expr_result = self.expr()
                    var_ref_node2.array_expr = expr_result
                    self.eat(TokenType.RBRACKET, 'expecting RBRACKET token type') 
                var_rvalue_node.path.append(var_ref_node2)