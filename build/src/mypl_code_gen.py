"""IR code generator for converting MyPL to VM Instructions. 

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326

"""

from src.mypl_token import *
from src.mypl_ast import *
from src.mypl_var_table import *
from src.mypl_frame import *
from src.mypl_opcode import *
from src.mypl_vm import *


class CodeGenerator (Visitor):

    def __init__(self, vm):
        """Creates a new Code Generator given a VM. 
        
        Args:
            vm -- The target vm.
        """
        # the vm to add frames to
        self.vm = vm
        # the current frame template being generated
        self.curr_template = None
        # for var -> index mappings wrt to environments
        self.var_table = VarTable()
        # struct name -> StructDef for struct field info
        self.struct_defs = {}

    
    def add_instr(self, instr):
        """Helper function to add an instruction to the current template."""
        self.curr_template.instructions.append(instr)

        
    def visit_program(self, program):
        for struct_def in program.struct_defs:
            struct_def.accept(self)
        for fun_def in program.fun_defs:
            fun_def.accept(self)

    
    def visit_struct_def(self, struct_def):
        # remember the struct def for later
        self.struct_defs[struct_def.struct_name.lexeme] = struct_def

        
    def visit_fun_def(self, fun_def):
        self.curr_template = VMFrameTemplate(fun_def.fun_name.lexeme, len(fun_def.params), [])
        self.var_table.push_environment()
        
        # for main function
        if fun_def.fun_name.lexeme == 'main':
            # empty program
            if fun_def.stmts == []:
                self.add_instr(PUSH('null'))
                self.add_instr(RET())
            else:
                for stmt in fun_def.stmts:
                    stmt.accept(self)
                    
                if not self.curr_template.instructions[-1] == RET():
                    self.add_instr(PUSH('null'))
                    self.add_instr(RET())
        # for any other function that is not main 
        else:
            for param in fun_def.params:
                self.var_table.add(param.var_name.lexeme)
                offset = self.var_table.get(param.var_name.lexeme)
                self.add_instr(STORE(offset))
            
            if fun_def.stmts == []:
                self.add_instr(PUSH('null'))
                self.add_instr(RET())
            else:
                for stmt in fun_def.stmts:
                    stmt.accept(self)
            
        self.var_table.push_environment()    
        self.vm.add_frame_template(self.curr_template)

    def visit_return_stmt(self, return_stmt):
        return_stmt.expr.accept(self)
        self.add_instr(RET())   

        
    def visit_var_decl(self, var_decl):
        # nothing to do here
        var_decl.var_def.accept(self)
        
        self.var_table.add(var_decl.var_def.var_name.lexeme)
        
        # simple var declarations
        if not var_decl.expr == None:
            var_decl.expr.accept(self)
            offset = self.var_table.get(var_decl.var_def.var_name.lexeme)
            self.add_instr(STORE(offset))
        # simple variable declaration with no expression
        else:
            self.add_instr(PUSH('null'))
            offset = self.var_table.get(var_decl.var_def.var_name.lexeme)
            self.add_instr(STORE(offset))
    
    def visit_assign_stmt(self, assign_stmt):
        # single lvalue
        if len(assign_stmt.lvalue) == 1:
            # getting value from operand stack
            offset = self.var_table.get(assign_stmt.lvalue[0].var_name.lexeme)
            # for array expressions
            if not assign_stmt.lvalue[0].array_expr == None:
                self.add_instr(LOAD(offset))
                assign_stmt.lvalue[0].array_expr.accept(self)
                assign_stmt.expr.accept(self)
                self.add_instr(SETI())
                
            # simple variable assignments    
            else:
                assign_stmt.expr.accept(self)
                self.add_instr(STORE(offset))
                
        # multiple lvalue
        elif len(assign_stmt.lvalue) > 1:
            if assign_stmt.lvalue[0].array_expr == None:
                offset = self.var_table.get(assign_stmt.lvalue[0].var_name.lexeme)
                self.add_instr(LOAD(offset))
                curr_field = assign_stmt.lvalue[-1].var_name.lexeme
                for i in range(1, len(assign_stmt.lvalue) - 1):
                    field = assign_stmt.lvalue[i].var_name.lexeme
                    self.add_instr(GETF(field))
                assign_stmt.expr.accept(self)
                self.add_instr(SETF(curr_field))
            else:
                offset = self.var_table.get(assign_stmt.lvalue[0].var_name.lexeme)
                self.add_instr(LOAD(offset))
                assign_stmt.lvalue[0].array_expr.accept(self)
                self.add_instr(GETI())
                curr_field = assign_stmt.lvalue[-1].var_name.lexeme
                
                for i in range(1, len(assign_stmt.lvalue) - 1):
                    field = assign_stmt.lvalue[i].var_name.lexeme
                    oid = self.var_table.get(field)
                    self.add_instr(LOAD(oid))
                    self.add_instr(GETF(field))
                    
                assign_stmt.expr.accept(self)
                self.add_instr(SETF(curr_field))
            
            
    def visit_while_stmt(self, while_stmt):
        start_jmp = len(self.curr_template.instructions)
        while_stmt.condition.accept(self)
        
        # creating a filler for JMPF until instructions inside loop are done
        jmp_instr = JMPF(-1)
        self.add_instr(jmp_instr)
        
        # creating new environment
        self.var_table.push_environment()
        for stmt in while_stmt.stmts:
            stmt.accept(self)
        self.var_table.pop_environment()
        
        self.add_instr(JMP(start_jmp))   
        self.add_instr(NOP())
        jmp_instr.operand = len(self.curr_template.instructions) - 1
        
    def visit_for_stmt(self, for_stmt):
        # pushing new environment for the for statment
        self.var_table.push_environment()
        for_stmt.var_decl.accept(self)
        
        # getting the starting index to jump back to
        start_jmp = len(self.curr_template.instructions)
        for_stmt.condition.accept(self)
        
        jmp_instr = JMPF(-1)
        self.add_instr(jmp_instr)
        
        # creating a new environment for inside for loop
        self.var_table.push_environment()
        for stmt in for_stmt.stmts:
            stmt.accept(self)
            
        self.var_table.pop_environment()
        
        for_stmt.assign_stmt.accept(self)
        
        self.add_instr(JMP(start_jmp))
        self.add_instr(NOP())
        jmp_instr.operand = len(self.curr_template.instructions) - 1
        
        # popping the environment once for loop is done
        self.var_table.pop_environment()

    
    def visit_if_stmt(self, if_stmt):
        if_stmt.if_part.condition.accept(self)
        jmp_elseif = JMPF(-1)
        self.add_instr(jmp_elseif)
        
        self.var_table.push_environment()
        for stmt in if_stmt.if_part.stmts:
            stmt.accept(self)
        self.var_table.pop_environment()
        
        jmp_end = JMP(-1)
        self.add_instr(jmp_end)
        
        jmp_end_else_if = JMP(-1)
        
        if not if_stmt.else_ifs == []:
            else_if_index = len(self.curr_template.instructions)
            jmp_elseif.operand = else_if_index
            
            for else_if in if_stmt.else_ifs:
                else_if.condition.accept(self)
                jmp_next_block = JMPF(-1)
                self.add_instr(jmp_next_block)
                
                self.var_table.push_environment()
                for stmt in else_if.stmts:
                    stmt.accept(self)
                self.var_table.pop_environment()
                
                self.add_instr(jmp_end_else_if)
                next_else_if_index = len(self.curr_template.instructions)
                jmp_next_block.operand = next_else_if_index
        else:
            if if_stmt.else_stmts == []:
                # if there is only an if statement
                self.add_instr(NOP())
                jmp_elseif.operand = len(self.curr_template.instructions) - 1
                jmp_end.operand = len(self.curr_template.instructions) - 1
                jmp_end_else_if.operand = len(self.curr_template.instructions) -1
            else:
                # there are no else ifs
                jmp_elseif.operand = len(self.curr_template.instructions)
                jmp_end.operand = len(self.curr_template.instructions)
                jmp_end_else_if.operand = len(self.curr_template.instructions)
            
        if not if_stmt.else_stmts == []:
            else_index = len(self.curr_template.instructions)
            jmp_next_block.operand = else_index
            
            self.var_table.push_environment()
            for stmt in if_stmt.else_stmts:
                stmt.accept(self)
            self.var_table.pop_environment()
            
            jmp_end.operand = len(self.curr_template.instructions)
            jmp_end_else_if = len(self.curr_template.instructions)
                
    
    def visit_call_expr(self, call_expr):
        # simple printing
        if call_expr.fun_name.lexeme == 'print':
            call_expr.args[0].accept(self)
            self.add_instr(WRITE())
        elif call_expr.fun_name.lexeme in ['stoi', 'dtoi']:
            call_expr.args[0].accept(self)
            self.add_instr(TOINT())
        elif call_expr.fun_name.lexeme in ['itos', 'dtos']:
            call_expr.args[0].accept(self)
            self.add_instr(TOSTR())  
        elif call_expr.fun_name.lexeme in ['stod', 'itod']:
            call_expr.args[0].accept(self)
            self.add_instr(TODBL())
        elif call_expr.fun_name.lexeme == 'length':
            call_expr.args[0].accept(self)
            self.add_instr(LEN())   
            
            # making sure that length equals zero
            for i in range(len(self.curr_template.instructions)):
                if self.curr_template.instructions[i] == PUSH(' ') and self.curr_template.instructions[i+1] == LEN(): 
                    self.curr_template.instructions[i] = PUSH("")
        elif call_expr.fun_name.lexeme == 'get':
            call_expr.args[0].accept(self)
            call_expr.args[1].accept(self)
            self.add_instr(GETC())
        elif call_expr.fun_name.lexeme == 'input':
            self.add_instr(READ())
        else:
            function_name = call_expr.fun_name.lexeme
            for arg in call_expr.args:
                arg.accept(self)
            self.add_instr(CALL(function_name))
 

    def visit_expr(self, expr):
        if not expr.op == None and expr.op.lexeme in ['>', '>=']:
            expr.rest.accept(self)
            expr.first.accept(self)
        else:
            expr.first.accept(self)
            
            if expr.not_op == True:
                self.add_instr(NOT())
                
            if not expr.rest == None:
                expr.rest.accept(self)
                
        if not expr.op == None:
            # simple math
            if expr.op.lexeme == '+':
                self.add_instr(ADD())
            elif expr.op.lexeme == '-':
                self.add_instr(SUB())
            elif expr.op.lexeme == '*':
                self.add_instr(MUL())
            elif expr.op.lexeme == '/':
                self.add_instr(DIV())
            # logical expressions
            elif expr.op.lexeme == 'and':
                self.add_instr(AND())
            elif expr.op.lexeme == 'or':
                self.add_instr(OR())
            # comparisions
            elif expr.op.lexeme in ['<', '>']:
                self.add_instr(CMPLT())
            elif expr.op.lexeme in ['<=', '>=']:
                self.add_instr(CMPLE())
            elif expr.op.lexeme == '==':
                self.add_instr(CMPEQ())
            elif expr.op.lexeme == '!=':
                self.add_instr(CMPNE())
                
                
            
    def visit_data_type(self, data_type):
        # nothing to do here
        pass

    
    def visit_var_def(self, var_def):
        # nothing to do here
        pass

    
    def visit_simple_term(self, simple_term):
        simple_term.rvalue.accept(self)

        
    def visit_complex_term(self, complex_term):
        complex_term.expr.accept(self)

        
    def visit_simple_rvalue(self, simple_rvalue):
        val = simple_rvalue.value.lexeme
        if simple_rvalue.value.token_type == TokenType.INT_VAL:
            self.add_instr(PUSH(int(val)))
        elif simple_rvalue.value.token_type == TokenType.DOUBLE_VAL:
            self.add_instr(PUSH(float(val)))
        elif simple_rvalue.value.token_type == TokenType.STRING_VAL:
            if len(val) == 0:
                self.add_instr(PUSH(" "))
            else:
                val = val.replace('\\n', '\n')
                val = val.replace('\\t', '\t')
                self.add_instr(PUSH(val))
        elif val == 'true':
            self.add_instr(PUSH(True))
        elif val == 'false':
            self.add_instr(PUSH(False))
        elif val == 'null':
            self.add_instr(PUSH('null'))

    
    def visit_new_rvalue(self, new_rvalue):
        if new_rvalue.array_expr == None:
            struct_name = new_rvalue.type_name.lexeme
            self.add_instr(ALLOCS())
            
            # seting the field for the struct
            for i in range(len(new_rvalue.struct_params)):
                # getting param and struct name field
                field = self.struct_defs[struct_name].fields[i].var_name.lexeme
                
                # adding struct instructions
                self.add_instr(DUP())
                new_rvalue.struct_params[i].accept(self)
                self.add_instr(SETF(field))
        else:
            new_rvalue.array_expr.accept(self)
            self.add_instr(ALLOCA())
            
    def visit_var_rvalue(self, var_rvalue):
        count = 0
        for var_ref in var_rvalue.path:
            if count == 0:
                index = self.var_table.get(var_ref.var_name.lexeme)
                self.add_instr(LOAD(index))
                if not var_ref.array_expr == None:
                    var_ref.array_expr.accept(self)
                    self.add_instr(GETI())
            else:
                struct_name = var_ref.var_name.lexeme
                if not var_ref.array_expr == None:
                    
                    if self.var_table.get(struct_name) == None and not struct_name in self.struct_defs:
                        self.add_instr(GETF(struct_name))
                    else:
                        index = self.var_table.get(struct_name)
                        self.add_instr(LOAD(index))
                    var_ref.array_expr.accept(self)
                    self.add_instr(GETI())
                else:
                    self.add_instr(GETF(struct_name))
            count = count + 1