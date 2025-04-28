"""IR code generator for converting MyPL to VM Instructions. 

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326

"""

from mypl_token import *
from mypl_ast import *
from mypl_var_table import *
from mypl_frame import *
from mypl_opcode import *
from mypl_vm import *


class PythonConverter(Visitor):
    def __init__(self):
        self.indent = 0
        self.output_file = open('output.py', 'w')  # Open file for writing

    # Helper Functions
        
    def output(self, msg):
        """Prints message without ending newline.

        Args:
           msg -- The string to print.

        """
        self.output_file.write(msg)

        
    def output_indent(self):
        """Prints an initial indent string."""
        self.output_file.write('    ')
        
    def close_output_file(self):
        """Closes the output file."""
        self.output_file.close()
        
# Visitor Functions
        
    def visit_program(self, program):
        for struct in program.struct_defs:
            struct.accept(self)
            self.output('\n')
        for fun in program.fun_defs:
            fun.accept(self)
            self.output('\n')
        self.output('main()')

    def visit_struct_def(self, struct_def):
        pass

    def visit_fun_def(self, fun_def):
        self.output('def ' + fun_def.fun_name.lexeme + '(')
        for i in range(len(fun_def.params)):
            fun_def.params[i].accept(self)
            
            if i < len(fun_def.params) - 1:
                self.output(', ')
        self.output('):\n')
        
        for stmt in fun_def.stmts:
            self.output_indent()
            stmt.accept(self)
            self.output('\n')
        

    def visit_return_stmt(self, return_stmt):
        self.output('return ')
        return_stmt.expr.accept(self)

    def visit_var_decl(self, var_decl):
        pass

    def visit_assign_stmt(self, assign_stmt):
        pass

    def visit_while_stmt(self, while_stmt):
        pass

    def visit_for_stmt(self, for_stmt):
        pass

    def visit_if_stmt(self, if_stmt):
        pass
    
    def visit_call_expr(self, call_expr):
        self.output(call_expr.fun_name.lexeme + '(')
        for arg in call_expr.args:
            arg.accept(self)
            if not arg == call_expr.args[-1]:
                self.output(', ')
        self.output(')')
    
    def visit_expr(self, expr):
        if expr.not_op == True:
            self.output('not ')
        expr.first.accept(self)
        
        if not expr.op == None:
            self.output(' ')
            self.output(expr.op.lexeme + ' ')
            
        if not expr.rest == None:
            expr.rest.accept(self)
    
    def visit_data_type(self, data_type):
        pass

    def visit_var_def(self, var_def):
        self.output(var_def.var_name.lexeme)

    def visit_simple_term(self, simple_term):
        simple_term.rvalue.accept(self)

    def visit_complex_term(self, complex_term):
        pass

    def visit_simple_rvalue(self, simple_rvalue):
        if simple_rvalue.value.token_type == TokenType.STRING_VAL:
            self.output('"')
        self.output(simple_rvalue.value.lexeme)
        if simple_rvalue.value.token_type == TokenType.STRING_VAL:
            self.output('"')
    
    def visit_new_rvalue(self, new_rvalue):
        pass

    def visit_var_rvalue(self, var_rvalue):
        for i in range(len(var_rvalue.path)):
            self.output(var_rvalue.path[i].var_name.lexeme)