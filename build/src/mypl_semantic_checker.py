"""Semantic Checker Visitor for semantically analyzing a MyPL program.

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326

"""
# Homework 4 Time Log
# -----------------------
# 3/18/24, 1 hour
# 3/19/24, 10 minutes
# 3/20/24, 4 hours, 15 minutes
# 3/21/24, 1 hour, 15 minutes
# 3/22/24, 30 minutes
# 3/23/24, 45 minutes
# 3/24/24, 50 minutes
# 3/25/24, 0 minutes
# 3/26/24, 2 hr, 50 minutes
# 3/27/24, 2 hr, 45 minutes
# 4/1/24, 3 hour

# Total: 14 hr, 20 minutes (updated 3/27/24)

from dataclasses import dataclass
from src.mypl_error import *
from src.mypl_token import Token, TokenType
from src.mypl_ast import *
from src.mypl_symbol_table import SymbolTable


BASE_TYPES = ['int', 'double', 'bool', 'string']
BUILT_INS = ['print', 'input', 'itos', 'itod', 'dtos', 'dtoi', 'stoi', 'stod',
             'length', 'get']

TYPE_DIC = {TokenType.INT_TYPE: TokenType.INT_VAL,
                    TokenType.DOUBLE_TYPE: TokenType.DOUBLE_VAL,
                    TokenType.STRING_TYPE: TokenType.STRING_VAL,
                    TokenType.BOOL_TYPE: TokenType.BOOL_VAL}

class SemanticChecker(Visitor):
    """Visitor implementation to semantically check MyPL programs."""

    def __init__(self):
        self.structs = {}
        self.functions = {}
        self.symbol_table = SymbolTable()
        self.curr_type = None


    # Helper Functions

    def error(self, msg, token):
        """Create and raise a Static Error."""
        if token is None:
            raise StaticError(msg)
        else:
            m = f'{msg} near line {token.line}, column {token.column}'
            raise StaticError(m)


    def get_field_type(self, struct_def, field_name):
        """Returns the DataType for the given field name of the struct
        definition.
        Args:
            struct_def: The StructDef object 
            field_name: The name of the field
        Returns: The corresponding DataType or None if the field name
        is not in the struct_def.
        """
        for var_def in struct_def.fields:
            if var_def.var_name.lexeme == field_name:
                return var_def.data_type
        return None


    # Visitor Functions

    def visit_program(self, program):
        # check and record struct defs
        for struct in program.struct_defs:
            struct_name = struct.struct_name.lexeme
            if struct_name in self.structs:
                self.error(f'duplicate {struct_name} definition', struct.struct_name)
            self.structs[struct_name] = struct
        # check and record function defs
        for fun in program.fun_defs:
            fun_name = fun.fun_name.lexeme
            if fun_name in self.functions: 
                self.error(f'duplicate {fun_name} definition', fun.fun_name)
            if fun_name in BUILT_INS:
                self.error(f'redefining built-in function', fun.fun_name)
            if fun_name == 'main' and fun.return_type.type_name.lexeme != 'void':
                self.error('main without void type', fun.return_type.type_name)
            if fun_name == 'main' and fun.params: 
                self.error('main function with parameters', fun.fun_name)
            self.functions[fun_name] = fun
        # check main function
        if 'main' not in self.functions:
            self.error('missing main function', None)
        # check each struct
        
        self.symbol_table.push_environment()
        for struct in list(self.structs.keys()):
            self.symbol_table.add(struct, 'struct')
        
        for struct in self.structs.values():
            struct.accept(self)
        
        # check each function
        for fun in self.functions.values():
            fun.accept(self)
        self.symbol_table.pop_environment()

    def visit_struct_def(self, struct_def):
        
        for var_def in struct_def.fields:
            var_def.accept(self)
            
        
    def visit_fun_def(self, fun_def):
        self.symbol_table.push_environment()
        # getting type for function
        fun_def.return_type.accept(self)
        self.symbol_table.push_environment()
        # getting params from the function
        for i in range(len(fun_def.params)):
            fun_def.params[i].accept(self)
        # checking errors from stmts
        for stmt in fun_def.stmts:
            stmt.accept(self)

        self.symbol_table.pop_environment()
        self.symbol_table.pop_environment()

    def visit_return_stmt(self, return_stmt):
        pass

    def visit_var_decl(self, var_decl):
        var_decl.var_def.accept(self)
        # bad return for built in functions
        var_return = var_decl.var_def.data_type.type_name.lexeme
        if not var_decl.expr == None and type(var_decl.expr.first) == SimpleTerm:
            var_decl.expr.accept(self)   
            # checking return type for built in functions
            if type(var_decl.expr.first.rvalue) == CallExpr:
                fun_name = var_decl.expr.first.rvalue.fun_name.lexeme
                if fun_name in ['itos', 'dtos', 'input', 'get']:
                    if not var_return == 'string':
                        raise MyPLError(f'Static Error: {fun_name}() requires a string return')
                elif fun_name == 'itod':
                    if not var_return == 'double':
                        raise MyPLError(f'Static Error: {fun_name}() requires a double return')
                elif fun_name in ['dtoi', 'length']:
                    if not var_return == 'int':
                        raise MyPLError(f'Static Error: {fun_name}() requires a int return')
            # checking if var declaration assing are the right type
            elif type(var_decl.expr.first.rvalue) == SimpleRValue:
                if not var_decl.expr.first.rvalue.value.token_type == TokenType.NULL_VAL:
                    if var_return == 'int':
                        if not var_decl.expr.first.rvalue.value.token_type == TokenType.INT_VAL:
                            raise MyPLError('Static Error: Var Decl type must be an int')
                    elif var_return == 'double':
                        if not var_decl.expr.first.rvalue.value.token_type == TokenType.DOUBLE_VAL:
                            raise MyPLError('Static Error: Var Decl type must be an double')
                    elif var_return == 'string':
                        if not var_decl.expr.first.rvalue.value.token_type == TokenType.STRING_VAL:
                            raise MyPLError('Static Error: Var Decl type must be an string')
                    elif var_return == 'bool':
                        if not var_decl.expr.first.rvalue.value.token_type in [TokenType.BOOL_VAL, TokenType.INT_VAL]:
                            raise MyPLError('Static Error: Var Decl type must be an bool')
                        
                # mismatched var decl for array types
                if var_decl.var_def.data_type.is_array == True:
                    raise MyPLError('Static Error: Type is currently an array. Definition must be a NewRValue.')
            elif type(var_decl.expr.first.rvalue) == VarRValue:
                var_val = var_decl.expr.first.rvalue.path[0].var_name.lexeme
                # bad assignment with incompatible types
                if self.symbol_table.exists_in_curr_env(var_val):
                    var_val_type = self.symbol_table.get(var_val)
                    if var_val_type in BASE_TYPES:
                        if not var_return == var_val_type:
                            raise MyPLError(f'Static Error: {var_decl.var_def.var_name} is a {var_return} type but {var_val} is a {var_val_type} type')  
                        
                last_val =  var_decl.expr.first.rvalue.path[-1].var_name.lexeme  
                type_last_val = self.symbol_table.get(last_val)
                
                # test bad rvalue path assignment
                if not var_return == type_last_val:
                    raise MyPLError('Static Error: Bad rvalue path assignment')

        
    def visit_assign_stmt(self, assign_stmt):
        pass

    def visit_while_stmt(self, while_stmt):
        pass

    def visit_for_stmt(self, for_stmt):
        pass

    def visit_if_stmt(self, if_stmt):
        pass
    
    def visit_call_expr(self, call_expr):
        # built in functions checking amount of arguments
        if call_expr.fun_name.lexeme in ['itos', 'dtos', 'itod', 'dtoi', 'print', 'length']:
            if not len(call_expr.args) == 1:
                raise MyPLError(f"Static Error: {call_expr.fun_name.lexeme}() requires one argument")
        elif call_expr.fun_name.lexeme == 'get':
            if not len(call_expr.args) == 2:
                raise MyPLError(f"Static Error: {call_expr.fun_name.lexeme}() requires two arguments")
        elif call_expr.fun_name.lexeme == 'input':
            if not len(call_expr.args) == 0:
                raise MyPLError(f"Static Error: {call_expr.fun_name.lexeme}() requires 0 arguments")
            

        # checking valid argument
        if len(call_expr.args) > 0:
            if type(call_expr.args[0].first.rvalue) == SimpleRValue:
                # for single argument built in functions
                token = call_expr.args[0].first.rvalue.value.token_type
                if call_expr.fun_name.lexeme in ['itos', 'itod']:
                    if not token == TokenType.INT_VAL:
                        raise MyPLError(f'Static Error: {call_expr.fun_name.lexeme}() argument requires a int type')
                elif call_expr.fun_name.lexeme in ['dtos', 'dtoi']:
                    if not token == TokenType.DOUBLE_VAL:
                        raise MyPLError(f'Static Error: {call_expr.fun_name.lexeme}() argument requires a double type')
                elif call_expr.fun_name.lexeme in ['length']:
                    if not token == TokenType.STRING_VAL:
                        raise MyPLError(f'Static Error: {call_expr.fun_name.lexeme}() argument requires a string type')
                
                if len(call_expr.args) == 2:
                    # for get function
                    if type(call_expr.args[1].first.rvalue) == NewRValue:
                        raise MyPLError('Static Error: get() argument must not have an array type')
                    token2 = call_expr.args[1].first.rvalue.value.token_type
                    if call_expr.fun_name.lexeme == 'get':
                        if not token == TokenType.INT_VAL:
                            raise MyPLError("Static Error: get() first argument requires a int type")
                        if not token2 == TokenType.STRING_VAL:
                            raise MyPLError('Static Error: get() second argument requires a string type')
            
                    
        for i in range(len(call_expr.args)):
            call_expr.args[i].accept(self)
            
    
    def visit_expr(self, expr):
        expr.first.accept(self)
        
        if not expr.rest == None:
            expr.rest.accept(self)
    
    def visit_data_type(self, data_type):
        # note: allowing void (bad cases of void caught by parser)
        name = data_type.type_name.lexeme
        if name == 'void' or name in BASE_TYPES or name in self.structs:
            self.curr_type = data_type
        else: 
            self.error(f'invalid type "{name}"', data_type.type_name)

    def visit_var_def(self, var_def):
        name_param = var_def.var_name.lexeme
        type_data = var_def.data_type.type_name.lexeme
        
        if not type_data in BASE_TYPES:
            if not self.symbol_table.exists(type_data):
                raise MyPLError(f'Static Error: Struct {type_data} does not exist')
        
        # checking function with two params with same name
        if not self.symbol_table.exists_in_curr_env(name_param):
            self.symbol_table.add(name_param, type_data)
        else:
            raise MyPLError(f'Static Error: {name_param} is already currently defined in file')
            

    def visit_simple_term(self, simple_term):
        simple_term.rvalue.accept(self)

    def visit_complex_term(self, complex_term):
        pass

    def visit_simple_rvalue(self, simple_rvalue):
        value = simple_rvalue.value
        line = simple_rvalue.value.line
        column = simple_rvalue.value.column
        type_token = None 
        if value.token_type == TokenType.INT_VAL:
            type_token = Token(TokenType.INT_TYPE, 'int', line, column)
        elif value.token_type == TokenType.DOUBLE_VAL:
            type_token = Token(TokenType.DOUBLE_TYPE, 'double', line, column)
        elif value.token_type == TokenType.STRING_VAL:
            type_token = Token(TokenType.STRING_TYPE, 'string', line, column)
        elif value.token_type == TokenType.BOOL_VAL:
            type_token = Token(TokenType.BOOL_TYPE, 'bool', line, column)
        elif value.token_type == TokenType.NULL_VAL:
            type_token = Token(TokenType.VOID_TYPE, 'void', line, column)
        self.curr_type = DataType(False, type_token)
    
    def visit_new_rvalue(self, new_rvalue):
        pass

    def visit_var_rvalue(self, var_rvalue):
        pass