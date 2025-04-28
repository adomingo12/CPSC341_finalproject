import pytest
import io

from src.mypl_error import *
from src.mypl_iowrapper import *
from src.mypl_token import *
from src.mypl_lexer import *
from src.mypl_ast_parser import *


#----------------------------------------------------------------------
# Basic Function Definitions
#----------------------------------------------------------------------

def test_empty_input():
    in_stream = FileWrapper(io.StringIO(''))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 0

def test_empty_fun():
    in_stream = FileWrapper(io.StringIO('int f() {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert len(p.struct_defs) == 0
    assert p.fun_defs[0].return_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].return_type.is_array == False
    assert p.fun_defs[0].fun_name.lexeme == 'f'
    assert len(p.fun_defs[0].params) == 0
    assert len(p.fun_defs[0].stmts) == 0

def test_empty_fun_array_return():
    in_stream = FileWrapper(io.StringIO('array int f() {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert p.fun_defs[0].return_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].return_type.is_array == True
    assert p.fun_defs[0].fun_name.lexeme == 'f'
    assert len(p.fun_defs[0].params) == 0
    assert len(p.fun_defs[0].stmts) == 0

def test_empty_fun_one_param():
    in_stream = FileWrapper(io.StringIO('int f(string x) {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert len(p.fun_defs[0].params) == 1
    assert p.fun_defs[0].params[0].data_type.is_array == False
    assert p.fun_defs[0].params[0].data_type.type_name.lexeme == 'string'
    assert p.fun_defs[0].params[0].var_name.lexeme == 'x'    

def test_empty_fun_one_id_param():
    in_stream = FileWrapper(io.StringIO('int f(S s1) {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert len(p.fun_defs[0].params) == 1
    assert p.fun_defs[0].params[0].data_type.is_array == False
    assert p.fun_defs[0].params[0].data_type.type_name.lexeme == 'S'
    assert p.fun_defs[0].params[0].var_name.lexeme == 's1'    

def test_empty_fun_one_array_param():
    in_stream = FileWrapper(io.StringIO('int f(array int ys) {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert len(p.fun_defs[0].params) == 1
    assert p.fun_defs[0].params[0].data_type.is_array == True
    assert p.fun_defs[0].params[0].data_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].params[0].var_name.lexeme == 'ys'    

def test_empty_fun_two_params():
    in_stream = FileWrapper(io.StringIO('int f(bool x, int y) {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert len(p.fun_defs[0].params) == 2
    assert p.fun_defs[0].params[0].data_type.is_array == False
    assert p.fun_defs[0].params[0].data_type.type_name.lexeme == 'bool'
    assert p.fun_defs[0].params[0].var_name.lexeme == 'x'    
    assert p.fun_defs[0].params[1].data_type.is_array == False
    assert p.fun_defs[0].params[1].data_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].params[1].var_name.lexeme == 'y'    

def test_empty_fun_three_params():
    in_stream = FileWrapper(io.StringIO('int f(bool x, int y, array string z) {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 1
    assert len(p.fun_defs[0].params) == 3
    assert p.fun_defs[0].params[0].data_type.is_array == False
    assert p.fun_defs[0].params[0].data_type.type_name.lexeme == 'bool'
    assert p.fun_defs[0].params[0].var_name.lexeme == 'x'    
    assert p.fun_defs[0].params[1].data_type.is_array == False
    assert p.fun_defs[0].params[1].data_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].params[1].var_name.lexeme == 'y'    
    assert p.fun_defs[0].params[2].data_type.is_array == True
    assert p.fun_defs[0].params[2].data_type.type_name.lexeme == 'string'
    assert p.fun_defs[0].params[2].var_name.lexeme == 'z'    

def test_multiple_empty_funs():
    in_stream = FileWrapper(io.StringIO(
        'void f() {}\n'
        'int g() {}\n'
        ''
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 2
    assert len(p.struct_defs) == 0
    
    
#----------------------------------------------------------------------
# Basic Struct Definitions
#----------------------------------------------------------------------

def test_empty_struct():
    in_stream = FileWrapper(io.StringIO('struct S {}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 1
    assert p.struct_defs[0].struct_name.lexeme == 'S'
    assert len(p.struct_defs[0].fields) == 0

def test_one_base_type_field_struct():
    in_stream = FileWrapper(io.StringIO('struct S {int x;}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 1
    assert p.struct_defs[0].struct_name.lexeme == 'S'
    assert len(p.struct_defs[0].fields) == 1
    assert p.struct_defs[0].fields[0].data_type.is_array == False
    assert p.struct_defs[0].fields[0].data_type.type_name.lexeme == 'int'
    assert p.struct_defs[0].fields[0].var_name.lexeme == 'x'

def test_one_id_field_struct():
    in_stream = FileWrapper(io.StringIO('struct S {S s1;}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 1
    assert p.struct_defs[0].struct_name.lexeme == 'S'
    assert len(p.struct_defs[0].fields) == 1
    assert p.struct_defs[0].fields[0].data_type.is_array == False
    assert p.struct_defs[0].fields[0].data_type.type_name.lexeme == 'S'
    assert p.struct_defs[0].fields[0].var_name.lexeme == 's1'

def test_one_array_field_struct():
    in_stream = FileWrapper(io.StringIO('struct S {array int x1;}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 1
    assert p.struct_defs[0].struct_name.lexeme == 'S'
    assert len(p.struct_defs[0].fields) == 1
    assert p.struct_defs[0].fields[0].data_type.is_array == True
    assert p.struct_defs[0].fields[0].data_type.type_name.lexeme == 'int'
    assert p.struct_defs[0].fields[0].var_name.lexeme == 'x1'

def test_two_field_struct():
    in_stream = FileWrapper(io.StringIO('struct S {int x1; bool x2;}'))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 1
    assert p.struct_defs[0].struct_name.lexeme == 'S'
    assert len(p.struct_defs[0].fields) == 2
    assert p.struct_defs[0].fields[0].data_type.is_array == False
    assert p.struct_defs[0].fields[0].data_type.type_name.lexeme == 'int'
    assert p.struct_defs[0].fields[0].var_name.lexeme == 'x1'
    assert p.struct_defs[0].fields[1].data_type.is_array == False
    assert p.struct_defs[0].fields[1].data_type.type_name.lexeme == 'bool'
    assert p.struct_defs[0].fields[1].var_name.lexeme == 'x2'

def test_three_field_struct():
    in_stream = FileWrapper(io.StringIO(
        'struct S {int x1; bool x2; array S x3;}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 0
    assert len(p.struct_defs) == 1
    assert p.struct_defs[0].struct_name.lexeme == 'S'
    assert len(p.struct_defs[0].fields) == 3
    assert p.struct_defs[0].fields[0].data_type.is_array == False
    assert p.struct_defs[0].fields[0].data_type.type_name.lexeme == 'int'
    assert p.struct_defs[0].fields[0].var_name.lexeme == 'x1'
    assert p.struct_defs[0].fields[1].data_type.is_array == False
    assert p.struct_defs[0].fields[1].data_type.type_name.lexeme == 'bool'
    assert p.struct_defs[0].fields[1].var_name.lexeme == 'x2'
    assert p.struct_defs[0].fields[2].data_type.is_array == True
    assert p.struct_defs[0].fields[2].data_type.type_name.lexeme == 'S'
    assert p.struct_defs[0].fields[2].var_name.lexeme == 'x3'

def test_empty_struct_and_fun():
    in_stream = FileWrapper(io.StringIO(
        'struct S1 {} \n'
        'int f() {} \n'
        'struct S2 {} \n'
        'int g() {} \n'
        'struct S3 {} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs) == 2
    assert len(p.struct_defs) == 3
    assert p.fun_defs[0].fun_name.lexeme == 'f'
    assert p.fun_defs[1].fun_name.lexeme == 'g'
    assert p.struct_defs[0].struct_name.lexeme == 'S1'
    assert p.struct_defs[1].struct_name.lexeme == 'S2'    
    assert p.struct_defs[2].struct_name.lexeme == 'S3'    

    
#----------------------------------------------------------------------
# Variable Declaration Statements
#----------------------------------------------------------------------

def test_var_base_type_var_decls():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  int x1; \n'
        '  double x2; \n'
        '  bool x3; \n'
        '  string x4; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 4
    assert p.fun_defs[0].stmts[0].var_def.data_type.is_array == False
    assert p.fun_defs[0].stmts[1].var_def.data_type.is_array == False
    assert p.fun_defs[0].stmts[2].var_def.data_type.is_array == False
    assert p.fun_defs[0].stmts[3].var_def.data_type.is_array == False    
    assert p.fun_defs[0].stmts[0].var_def.data_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].stmts[1].var_def.data_type.type_name.lexeme == 'double'
    assert p.fun_defs[0].stmts[2].var_def.data_type.type_name.lexeme == 'bool'
    assert p.fun_defs[0].stmts[3].var_def.data_type.type_name.lexeme == 'string'
    assert p.fun_defs[0].stmts[0].var_def.var_name.lexeme == 'x1'
    assert p.fun_defs[0].stmts[1].var_def.var_name.lexeme == 'x2'
    assert p.fun_defs[0].stmts[2].var_def.var_name.lexeme == 'x3'
    assert p.fun_defs[0].stmts[3].var_def.var_name.lexeme == 'x4'

def test_array_var_decl():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  array int x1; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].var_def.data_type.is_array == True
    assert p.fun_defs[0].stmts[0].var_def.data_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].stmts[0].var_def.var_name.lexeme == 'x1'    

def test_id_var_decl():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  S s1; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].var_def.data_type.is_array == False
    assert p.fun_defs[0].stmts[0].var_def.data_type.type_name.lexeme == 'S'
    assert p.fun_defs[0].stmts[0].var_def.var_name.lexeme == 's1'    
    

def test_base_type_var_def():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  int x1 = 0; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].var_def.data_type.is_array == False
    assert p.fun_defs[0].stmts[0].var_def.data_type.type_name.lexeme == 'int'
    assert p.fun_defs[0].stmts[0].var_def.var_name.lexeme == 'x1'
    print(p.fun_defs[0].stmts[0].expr)
    assert p.fun_defs[0].stmts[0].expr.not_op == False
    assert p.fun_defs[0].stmts[0].expr.first.rvalue.value.lexeme == '0'

def test_id_var_def():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  Node my_node = null; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].var_def.data_type.is_array == False
    assert p.fun_defs[0].stmts[0].var_def.data_type.type_name.lexeme == 'Node'
    assert p.fun_defs[0].stmts[0].var_def.var_name.lexeme == 'my_node'
    assert p.fun_defs[0].stmts[0].expr.not_op == False
    assert p.fun_defs[0].stmts[0].expr.first.rvalue.value.lexeme == 'null'
    
def test_array_var_def():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  array bool my_bools = null; \n'
        '  array Node my_nodes = null; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 2
    assert p.fun_defs[0].stmts[0].var_def.data_type.is_array == True
    assert p.fun_defs[0].stmts[0].var_def.data_type.type_name.lexeme == 'bool'
    assert p.fun_defs[0].stmts[0].var_def.var_name.lexeme == 'my_bools'
    assert p.fun_defs[0].stmts[0].expr.not_op == False
    assert p.fun_defs[0].stmts[0].expr.first.rvalue.value.lexeme == 'null'
    assert p.fun_defs[0].stmts[1].var_def.data_type.is_array == True
    assert p.fun_defs[0].stmts[1].var_def.data_type.type_name.lexeme == 'Node'
    assert p.fun_defs[0].stmts[1].var_def.var_name.lexeme == 'my_nodes'
    assert p.fun_defs[0].stmts[1].expr.not_op == False
    assert p.fun_defs[0].stmts[1].expr.first.rvalue.value.lexeme == 'null'

    
#----------------------------------------------------------------------
# Assignment Statements
#----------------------------------------------------------------------

def test_simple_assignment():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = null; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].lvalue[0].var_name.lexeme == 'x'
    assert p.fun_defs[0].stmts[0].lvalue[0].array_expr == None
    assert p.fun_defs[0].stmts[0].expr.not_op == False
    assert p.fun_defs[0].stmts[0].expr.first.rvalue.value.lexeme == 'null'
    assert p.fun_defs[0].stmts[0].expr.rest == None

def test_simple_path_assignment():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x.y = null; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].lvalue[0].var_name.lexeme == 'x'
    assert p.fun_defs[0].stmts[0].lvalue[0].array_expr == None
    assert p.fun_defs[0].stmts[0].lvalue[1].var_name.lexeme == 'y'
    assert p.fun_defs[0].stmts[0].lvalue[1].array_expr == None
    assert p.fun_defs[0].stmts[0].expr.not_op == False
    assert p.fun_defs[0].stmts[0].expr.first.rvalue.value.lexeme == 'null'
    assert p.fun_defs[0].stmts[0].expr.rest == None

def test_simple_array_assignment():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x[0] = null; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.lvalue[0].var_name.lexeme == 'x'
    assert stmt.lvalue[0].array_expr.not_op == False
    assert stmt.lvalue[0].array_expr.first.rvalue.value.lexeme == '0'
    assert stmt.lvalue[0].array_expr.rest == None
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.value.lexeme == 'null'
    assert stmt.expr.rest == None

def test_multiple_path_assignment():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x1.x2[0].x3.x4[1] = null; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert len(stmt.lvalue) == 4
    assert stmt.lvalue[0].var_name.lexeme == 'x1'
    assert stmt.lvalue[0].array_expr == None
    assert stmt.lvalue[1].var_name.lexeme == 'x2'    
    assert stmt.lvalue[1].array_expr.not_op == False
    assert stmt.lvalue[1].array_expr.first.rvalue.value.lexeme == '0'
    assert stmt.lvalue[2].var_name.lexeme == 'x3'
    assert stmt.lvalue[2].array_expr == None
    assert stmt.lvalue[3].var_name.lexeme == 'x4'
    assert stmt.lvalue[3].array_expr.not_op == False
    assert stmt.lvalue[3].array_expr.first.rvalue.value.lexeme == '1'

    
#----------------------------------------------------------------------
# If Statements
#----------------------------------------------------------------------

def test_single_if_statement():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 0
    assert len(stmt.else_ifs) == 0
    assert len(stmt.else_stmts) == 0
    
def test_if_statement_with_body():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {int x = 0;} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 1
    assert len(stmt.else_ifs) == 0
    assert len(stmt.else_stmts) == 0

def test_if_statement_with_one_else_if():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {} \n'
        '  elseif (false) {} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 0
    assert len(stmt.else_ifs) == 1
    assert stmt.else_ifs[0].condition.first.rvalue.value.lexeme == 'false'
    assert len(stmt.else_ifs[0].stmts) == 0

    
def test_if_statement_with_two_else_ifs():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {} \n'
        '  elseif (false) {} \n'
        '  elseif (true) {} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 0
    assert len(stmt.else_ifs) == 2
    assert stmt.else_ifs[0].condition.first.rvalue.value.lexeme == 'false'
    assert len(stmt.else_ifs[0].stmts) == 0
    assert stmt.else_ifs[1].condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.else_ifs[1].stmts) == 0
    assert len(stmt.else_stmts) == 0

def test_if_statement_with_empty_else():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {} \n'
        '  else {} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 0
    assert len(stmt.else_ifs) == 0
    assert len(stmt.else_stmts) == 0

def test_if_statement_with_non_empty_else():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {} \n'
        '  else {x = 5;} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 0
    assert len(stmt.else_ifs) == 0
    assert len(stmt.else_stmts) == 1

def test_full_if_statement():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  if (true) {x = 5;} \n'
        '  elseif (false) {x = 6;} \n'
        '  else {x = 7;} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.if_part.stmts) == 1
    assert len(stmt.else_ifs) == 1
    assert stmt.else_ifs[0].condition.first.rvalue.value.lexeme == 'false'
    assert len(stmt.else_ifs[0].stmts) == 1
    assert len(stmt.else_stmts) == 1

    
#----------------------------------------------------------------------
# While Statements
#----------------------------------------------------------------------

def test_empty_while_statement():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  while (true) {} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.stmts) == 0

def test_while_statement_with_body():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  while (true) {x = 5;} \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.condition.first.rvalue.value.lexeme == 'true'
    assert len(stmt.stmts) == 1

    
#----------------------------------------------------------------------
# Expressions
#----------------------------------------------------------------------

def test_literals():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = true; \n'
        '  x = false; \n'        
        '  x = 0; \n'
        '  x = 0.0; \n'
        '  x = "a"; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 5
    assert p.fun_defs[0].stmts[0].expr.first.rvalue.value.lexeme == 'true'
    assert p.fun_defs[0].stmts[1].expr.first.rvalue.value.lexeme == 'false'
    assert p.fun_defs[0].stmts[2].expr.first.rvalue.value.lexeme == '0'    
    assert p.fun_defs[0].stmts[3].expr.first.rvalue.value.lexeme == '0.0'    
    assert p.fun_defs[0].stmts[4].expr.first.rvalue.value.lexeme == 'a'        
    assert p.fun_defs[0].stmts[0].expr.not_op == False
    assert p.fun_defs[0].stmts[1].expr.not_op == False
    assert p.fun_defs[0].stmts[2].expr.not_op == False
    assert p.fun_defs[0].stmts[3].expr.not_op == False
    assert p.fun_defs[0].stmts[4].expr.not_op == False

def test_simple_bool_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = true and false; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.value.lexeme == 'true'
    assert stmt.expr.op.lexeme == 'and'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.rvalue.value.lexeme == 'false'
    assert stmt.expr.rest.op == None
    assert stmt.expr.rest.rest == None    

def test_simple_not_bool_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = not true and false; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == True
    assert stmt.expr.first.rvalue.value.lexeme == 'true'
    assert stmt.expr.op.lexeme == 'and'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.rvalue.value.lexeme == 'false'
    assert stmt.expr.rest.op == None
    assert stmt.expr.rest.rest == None    

def test_simple_paren_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = (1 + 2); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.expr.first.rvalue.value.lexeme == '1'
    assert stmt.expr.first.expr.op.lexeme == '+'
    assert stmt.expr.first.expr.rest.not_op == False
    assert stmt.expr.first.expr.rest.first.rvalue.value.lexeme == '2'
    assert stmt.expr.first.expr.rest.op == None
    assert stmt.expr.first.expr.rest.rest == None    

def test_expr_after_paren_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = (1 + 2) - 3; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.expr.first.rvalue.value.lexeme == '1'
    assert stmt.expr.first.expr.op.lexeme == '+'
    assert stmt.expr.first.expr.rest.not_op == False
    assert stmt.expr.first.expr.rest.first.rvalue.value.lexeme == '2'
    assert stmt.expr.first.expr.rest.op == None
    assert stmt.expr.first.expr.rest.rest == None    
    assert stmt.expr.op.lexeme == '-'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.rvalue.value.lexeme == '3'
    assert stmt.expr.rest.op == None
    assert stmt.expr.rest.rest == None

def test_expr_before_paren_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = 3 * (1 + 2); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.value.lexeme == '3'
    assert stmt.expr.op.lexeme == '*'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.first.rvalue.value.lexeme == '1'
    assert stmt.expr.rest.first.expr.op.lexeme == '+'
    assert stmt.expr.rest.first.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.rest.first.rvalue.value.lexeme == '2'
    assert stmt.expr.rest.first.expr.rest.op == None
    assert stmt.expr.rest.first.expr.rest.rest == None
    assert stmt.expr.rest.op == None
    assert stmt.expr.rest.rest == None

def test_expr_with_two_ops():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = 1 / 2 * 3; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.value.lexeme == '1'
    assert stmt.expr.op.lexeme == '/'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.rvalue.value.lexeme == '2'
    assert stmt.expr.rest.op.lexeme == '*'
    assert stmt.expr.rest.rest.not_op == False
    assert stmt.expr.rest.rest.first.rvalue.value.lexeme == '3'
    assert stmt.expr.rest.rest.op == None
    assert stmt.expr.rest.rest.rest == None    

def test_empty_call_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  f(); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.fun_name.lexeme == 'f'
    assert len(stmt.args) == 0

def test_one_arg_call_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  f(3); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.fun_name.lexeme == 'f'
    assert len(stmt.args) == 1
    assert stmt.args[0].not_op == False
    assert stmt.args[0].first.rvalue.value.lexeme == '3'
    assert stmt.args[0].op == None
    assert stmt.args[0].rest == None    

def test_two_arg_call_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  f(3, 4); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.fun_name.lexeme == 'f'
    assert len(stmt.args) == 2
    assert stmt.args[0].not_op == False
    assert stmt.args[0].first.rvalue.value.lexeme == '3'
    assert stmt.args[0].op == None
    assert stmt.args[0].rest == None    
    assert stmt.args[1].not_op == False
    assert stmt.args[1].first.rvalue.value.lexeme == '4'
    assert stmt.args[1].op == None
    assert stmt.args[1].rest == None    
    
def test_simple_struct_new_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = new S(); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.type_name.lexeme == 'S'
    assert stmt.expr.first.rvalue.array_expr == None
    assert len(stmt.expr.first.rvalue.struct_params) == 0

def test_two_arg_struct_new_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = new S(3, 4); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.type_name.lexeme == 'S'
    assert stmt.expr.first.rvalue.array_expr == None
    assert len(stmt.expr.first.rvalue.struct_params) == 2
    assert stmt.expr.first.rvalue.struct_params[0].first.rvalue.value.lexeme == '3'
    assert stmt.expr.first.rvalue.struct_params[1].first.rvalue.value.lexeme == '4'

def test_base_type_array_new_expr():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = new int[10]; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.type_name.lexeme == 'int'
    assert stmt.expr.first.rvalue.array_expr.first.rvalue.value.lexeme == '10'
    assert stmt.expr.first.rvalue.struct_params == None

def test_simple_var_rvalue():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = y; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert len(stmt.expr.first.rvalue.path) == 1
    assert stmt.expr.first.rvalue.path[0].var_name.lexeme == 'y'
    assert stmt.expr.first.rvalue.path[0].array_expr == None

def test_simple_array_var_rvalue():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = y[0]; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert len(stmt.expr.first.rvalue.path) == 1
    assert stmt.expr.first.rvalue.path[0].var_name.lexeme == 'y'
    assert stmt.expr.first.rvalue.path[0].array_expr.not_op == False
    assert stmt.expr.first.rvalue.path[0].array_expr.first.rvalue.value.lexeme == '0'
    assert stmt.expr.first.rvalue.path[0].array_expr.op == None
    assert stmt.expr.first.rvalue.path[0].array_expr.rest == None

def test_two_path_var_rvalue():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = y.z; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert len(stmt.expr.first.rvalue.path) == 2
    assert stmt.expr.first.rvalue.path[0].var_name.lexeme == 'y'
    assert stmt.expr.first.rvalue.path[0].array_expr == None
    assert stmt.expr.first.rvalue.path[1].var_name.lexeme == 'z'
    assert stmt.expr.first.rvalue.path[1].array_expr == None


def test_mixed_path_var_rvalue():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = u[2].v.w[1].y; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert len(stmt.expr.first.rvalue.path) == 4
    assert stmt.expr.not_op == False
    assert stmt.expr.op == None
    assert stmt.expr.rest == None
    path = stmt.expr.first.rvalue.path
    assert path[0].var_name.lexeme == 'u'
    assert path[0].array_expr.not_op == False
    assert path[0].array_expr.first.rvalue.value.lexeme == '2'
    assert path[0].array_expr.op == None
    assert path[0].array_expr.rest == None
    assert path[1].var_name.lexeme == 'v'
    assert path[1].array_expr == None
    assert path[2].var_name.lexeme == 'w'
    assert path[2].array_expr.not_op == False
    assert path[2].array_expr.first.rvalue.value.lexeme == '1'
    assert path[2].array_expr.op == None
    assert path[2].array_expr.rest == None
    assert path[3].var_name.lexeme == 'y'
    assert path[3].array_expr == None


#----------------------------------------------------------------------
# TODO: Add at least 10 of your own tests below. Define at least two
# tests for statements, one test for return statements, five tests
# for expressions, and two tests that are more involved combining
# multiple constructs.
#----------------------------------------------------------------------

# Two for statement tests

# TEST 1
def test_for_empty():
    in_stream = FileWrapper(io.StringIO(
        'void f() {'
        '  for (int i = 10; i > 0; i = i - 2) {}'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.var_decl.var_def.data_type.is_array == False
    assert stmt.var_decl.var_def.data_type.type_name.lexeme == 'int'
    assert stmt.var_decl.var_def.var_name.lexeme == 'i'
    assert stmt.var_decl.expr.first.rvalue.value.lexeme == '10'
    assert stmt.condition.not_op == False
    assert stmt.condition.first.rvalue.path[0].var_name.lexeme == 'i'
    assert stmt.condition.op.lexeme == '>'
    assert stmt.condition.rest.not_op == False
    assert stmt.condition.rest.first.rvalue.value.lexeme == '0'
    assert stmt.assign_stmt.lvalue[0].var_name.lexeme == 'i'
    assert stmt.assign_stmt.lvalue[0].array_expr == None
    assert stmt.assign_stmt.expr.not_op == False
    assert stmt.assign_stmt.expr.first.rvalue.path[0].var_name.lexeme == 'i'
    assert stmt.assign_stmt.expr.rest.not_op == False
    assert stmt.assign_stmt.expr.rest.first.rvalue.value.lexeme == '2'
    assert stmt.assign_stmt.expr.rest.op == None
    assert stmt.assign_stmt.expr.rest.rest == None
    assert stmt.stmts == []

# TEST 2
def test_for_simple():
    in_stream = FileWrapper(io.StringIO(
        'void f() {'
        '  for (int i = 0; i < 10; i = i + 1) {'
        '    x = x + 1;'
        '  }'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.var_decl.var_def.data_type.is_array == False
    assert stmt.var_decl.var_def.data_type.type_name.lexeme == 'int'
    assert stmt.var_decl.var_def.var_name.lexeme == 'i'
    assert stmt.var_decl.expr.first.rvalue.value.lexeme == '0'
    assert stmt.condition.not_op == False
    assert stmt.condition.first.rvalue.path[0].var_name.lexeme == 'i'
    assert stmt.condition.op.lexeme == '<'
    assert stmt.condition.rest.not_op == False
    assert stmt.condition.rest.first.rvalue.value.lexeme == '10'
    assert stmt.assign_stmt.lvalue[0].var_name.lexeme == 'i'
    assert stmt.assign_stmt.lvalue[0].array_expr == None
    assert stmt.assign_stmt.expr.not_op == False
    assert stmt.assign_stmt.expr.first.rvalue.path[0].var_name.lexeme == 'i'
    assert stmt.assign_stmt.expr.rest.not_op == False
    assert stmt.assign_stmt.expr.rest.first.rvalue.value.lexeme == '1'
    assert stmt.assign_stmt.expr.rest.op == None
    assert stmt.stmts[0].lvalue[0].var_name.lexeme == 'x'
    assert stmt.stmts[0].expr.not_op == False
    assert stmt.stmts[0].expr.first.rvalue.path[0].var_name.lexeme == 'x'
    assert stmt.stmts[0].expr.op.lexeme == '+'
    assert stmt.stmts[0].expr.rest.not_op == False
    assert stmt.stmts[0].expr.rest.first.rvalue.value.lexeme == '1'
    assert stmt.stmts[0].expr.rest.op == None
    
# One return statement test

# TEST 3
def test_return():
    in_stream = FileWrapper(io.StringIO(
        'void f() {'
        '  return 10;'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.value.lexeme == '10'
    assert stmt.expr.rest == None
    
# Five expression tests

# TEST 4
def test_two_paren():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = (1 + 2) - (3 + 4); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.expr.first.rvalue.value.lexeme == '1'
    assert stmt.expr.first.expr.op.lexeme == '+'
    assert stmt.expr.first.expr.rest.not_op == False
    assert stmt.expr.first.expr.rest.first.rvalue.value.lexeme == '2'
    assert stmt.expr.first.expr.rest.op == None
    assert stmt.expr.first.expr.rest.rest == None    
    assert stmt.expr.op.lexeme == '-'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.first.rvalue.value.lexeme == '3'
    assert stmt.expr.rest.op == None
    assert stmt.expr.rest.rest == None
    assert stmt.expr.rest.first.expr.op.lexeme == '+'
    assert stmt.expr.rest.first.expr.rest.first.rvalue.value.lexeme == '4'
 
# TEST 5   
def test_two_paren_with_variables():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = (a * b) - (c / d) + e; \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == False
    assert stmt.expr.first.expr.first.rvalue.path[0].var_name.lexeme == 'a'
    assert stmt.expr.first.expr.op.lexeme == '*'
    assert stmt.expr.first.expr.not_op == False
    assert stmt.expr.first.expr.rest.first.rvalue.path[0].var_name.lexeme == 'b'
    assert stmt.expr.op.lexeme == '-'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.first.rvalue.path[0].var_name.lexeme == 'c'
    assert stmt.expr.rest.first.expr.op.lexeme == '/'
    assert stmt.expr.rest.first.expr.not_op == False
    assert stmt.expr.rest.first.expr.rest.first.rvalue.path[0].var_name.lexeme == 'd'
    assert stmt.expr.rest.op.lexeme == '+'
    assert stmt.expr.rest.rest.first.rvalue.path[0].var_name.lexeme == 'e'
    assert stmt.expr.rest.rest.op == None
    assert stmt.expr.rest.rest.rest == None
    
# TEST 6
def test_bool_variable_assignment_with_logical_operators():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  var2 = not (x and y) or (z and w); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    assert p.fun_defs[0].stmts[0].lvalue[0].var_name.lexeme == 'var2'
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.expr.not_op == True
    assert stmt.expr.first.expr.not_op == False
    assert stmt.expr.first.expr.first.rvalue.path[0].var_name.lexeme == 'x'
    assert stmt.expr.first.expr.op.lexeme == 'and'
    assert stmt.expr.first.expr.rest.not_op == False
    assert stmt.expr.first.expr.rest.first.rvalue.path[0].var_name.lexeme == 'y'
    assert stmt.expr.op.lexeme == 'or'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.not_op == False
    assert stmt.expr.rest.first.expr.first.rvalue.path[0].var_name.lexeme == 'z'
    assert stmt.expr.rest.first.expr.op.lexeme == 'and'
    assert stmt.expr.rest.first.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.rest.first.rvalue.path[0].var_name.lexeme == 'w'
    assert stmt.expr.rest.first.expr.rest.op == None
    assert stmt.expr.rest.first.expr.rest.rest == None
    assert stmt.expr.rest.op == None
    assert stmt.expr.rest.rest == None
  
# TEST 7
def test_more_assign_variables_with_doubles():
    in_stream = FileWrapper(io.StringIO(
        'int main() {'
        '    double f = (10.0 / 2.0) - (3.0 + 1.14159);'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.var_def.data_type.is_array == False
    assert stmt.var_def.data_type.type_name.lexeme == 'double'
    assert stmt.var_def.var_name.lexeme == 'f'
    assert stmt.expr.not_op == False
    assert stmt.expr.first.expr.not_op == False
    assert stmt.expr.first.expr.first.rvalue.value.lexeme == '10.0'
    assert stmt.expr.first.expr.op.lexeme == '/'
    assert stmt.expr.first.expr.rest.not_op == False
    assert stmt.expr.first.expr.rest.first.rvalue.value.lexeme == '2.0'
    assert stmt.expr.op.lexeme == '-'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.not_op == False
    assert stmt.expr.rest.first.expr.first.rvalue.value.lexeme == '3.0'
    assert stmt.expr.rest.first.expr.op.lexeme == '+'
    assert stmt.expr.rest.first.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.rest.first.rvalue.value.lexeme == '1.14159'
    assert stmt.expr.rest.first.expr.rest.op == None
    assert stmt.expr.rest.first.expr.rest.rest == None
    
    
def test_complex_at_end():
    in_stream = FileWrapper(io.StringIO(
        'void main() { \n'
        '  x = e * (a * b) - (c / d); \n'
        '} \n'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.lvalue[0].var_name.lexeme == 'x'
    assert stmt.lvalue[0].array_expr == None
    assert stmt.expr.not_op == False
    assert stmt.expr.first.rvalue.path[0].var_name.lexeme == 'e'
    assert stmt.expr.first.rvalue.path[0].array_expr == None
    assert stmt.expr.op.lexeme == '*'
    assert stmt.expr.rest.not_op == False
    assert stmt.expr.rest.first.expr.not_op == False
    assert stmt.expr.rest.first.expr.first.rvalue.path[0].var_name.lexeme == 'c'
    assert stmt.expr.rest.first.expr.first.rvalue.path[0].array_expr == None
    

# TEST 8

# Three more involved tests that involve multiple constructs
    
# TEST 9
def test_nested_statetements(): 
    in_stream = FileWrapper(io.StringIO(
        'void f() {'
        '  if (x) {'
        '    while (true) {'
        '      for (int i = 0; i < x; i = i + 1) {'
        '        x = x + 2 + (x + z);'
        '      }'
        '    }'
        '  }'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 1
    stmt = p.fun_defs[0].stmts[0]
    assert stmt.if_part.condition.not_op == False
    assert stmt.if_part.condition.first.rvalue.path[0].var_name.lexeme == 'x'
    assert stmt.if_part.condition.op == None
    assert stmt.if_part.condition.rest == None
    w = stmt.if_part.stmts[0]
    assert w.condition.not_op == False
    assert w.condition.first.rvalue.value.lexeme == 'true'
    assert w.condition.op == None
    assert w.condition.rest == None
    f = w.stmts[0]
    assert f.var_decl.var_def.data_type.is_array == False
    assert f.var_decl.var_def.data_type.type_name.lexeme == 'int'
    assert f.var_decl.expr.not_op == False
    assert f.var_decl.expr.first.rvalue.value.lexeme == '0'
    assert f.var_decl.expr.op == None
    assert f.var_decl.expr.rest == None
    assert f.condition.not_op == False
    assert f.condition.first.rvalue.path[0].var_name.lexeme == 'i'
    assert f.condition.first.rvalue.path[0].array_expr == None
    assert f.condition.op.lexeme == '<'
    assert f.condition.rest.not_op == False
    assert f.condition.rest.first.rvalue.path[0].var_name.lexeme == 'x'
    assert f.condition.rest.first.rvalue.path[0].array_expr == None
    assert f.condition.rest.op == None
    assert f.condition.rest.rest == None
    assert f.assign_stmt.lvalue[0].var_name.lexeme == 'i'
    assert f.assign_stmt.lvalue[0].array_expr == None
    assert f.assign_stmt.expr.not_op == False
    assert f.assign_stmt.expr.first.rvalue.path[0].var_name.lexeme == 'i'
    assert f.assign_stmt.expr.first.rvalue.path[0].array_expr == None
    assert f.assign_stmt.expr.op.lexeme == '+'
    assert f.assign_stmt.expr.rest.not_op == False
    assert f.assign_stmt.expr.rest.first.rvalue.value.lexeme == '1'
    assert f.assign_stmt.expr.rest.op == None
    assert f.assign_stmt.expr.rest.rest == None
    x = f.stmts[0]
    assert x.lvalue[0].var_name.lexeme == 'x'
    assert x.lvalue[0].array_expr == None
    assert x.expr.not_op == False
    assert x.expr.first.rvalue.path[0].var_name.lexeme == 'x'
    assert x.expr.first.rvalue.path[0].array_expr == None
    assert x.expr.op.lexeme == '+'
    assert x.expr.rest.not_op == False
    assert x.expr.rest.first.rvalue.value.lexeme == '2'
    assert x.expr.rest.op.lexeme == '+'
    assert x.expr.rest.rest.not_op == False
    assert x.expr.rest.rest.first.expr.not_op == False
    assert x.expr.rest.rest.first.expr.first.rvalue.path[0].var_name.lexeme == 'x'
    assert x.expr.rest.rest.first.expr.first.rvalue.path[0].array_expr == None
    assert x.expr.rest.rest.first.expr.op.lexeme == '+'
    assert x.expr.rest.rest.first.expr.rest.not_op == False
    assert x.expr.rest.rest.first.expr.rest.first.rvalue.path[0].var_name.lexeme == 'z'
    assert x.expr.rest.rest.first.expr.rest.first.rvalue.path[0].array_expr == None
    assert x.expr.rest.rest.first.expr.rest.op == None
    assert x.expr.rest.rest.first.expr.rest.rest == None

# TEST 10
def test_assign_with_if():
    in_stream = FileWrapper(io.StringIO(
        'int main() {'
        '   int x;'
        '   double y = 3.14;'
        '   string z = "hi\n";'
        '   if (y) {'
        '       print(z);'
        '   }'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 4
    one = p.fun_defs[0].stmts[0]
    assert one.var_def.data_type.is_array == False
    assert one.var_def.data_type.type_name.lexeme == 'int'
    assert one.var_def.var_name.lexeme == 'x'
    assert one.expr == None
    two = p.fun_defs[0].stmts[1]
    assert two.var_def.data_type.is_array == False
    assert two.var_def.data_type.type_name.lexeme == 'double'
    assert two.var_def.var_name.lexeme == 'y'
    assert two.expr.not_op == False
    assert two.expr.first.rvalue.value.lexeme == '3.14'
    assert two.expr.op == None
    assert two.expr.rest == None
    three = p.fun_defs[0].stmts[2]
    assert three.var_def.data_type.is_array == False
    assert three.var_def.data_type.type_name.lexeme == 'string'
    assert three.var_def.var_name.lexeme == 'z'
    assert three.expr.not_op == False
    assert three.expr.first.rvalue.value.lexeme == 'hi'
    assert three.expr.op == None
    assert three.expr.rest == None
    four = p.fun_defs[0].stmts[3]
    assert four.if_part.condition.not_op == False
    assert four.if_part.condition.first.rvalue.path[0].var_name.lexeme == 'y'
    assert four.if_part.condition.first.rvalue.path[0].array_expr == None
    assert four.if_part.condition.op == None
    assert four.if_part.condition.rest == None
    assert four.if_part.stmts[0].fun_name.lexeme == 'print'
    assert four.if_part.stmts[0].args[0].not_op == False
    assert four.if_part.stmts[0].args[0].first.rvalue.path[0].var_name.lexeme == 'z'
    assert four.if_part.stmts[0].args[0].first.rvalue.path[0].array_expr == None
    assert four.if_part.stmts[0].args[0].op == None
    assert four.if_part.stmts[0].args[0].rest == None
    assert four.else_ifs == []
    assert four.else_stmts == []

# TEST 11

def test_mix_of_statetements(): 
    in_stream = FileWrapper(io.StringIO(
        'bool my_fun(int z) {'
        '  int x = 1;'
        '  x = 2;'
        '  if (x) {return true;}'
        '  while (true) {x = x + 1;}'
        '  for (int i = 0; i < x; i = i + 1) {'
        '    x = x + 2;'
        '  }'
        '}'
    ))
    p = ASTParser(Lexer(in_stream)).parse()
    assert len(p.fun_defs[0].stmts) == 5
    s1 = p.fun_defs[0].stmts[0]
    assert s1.var_def.data_type.is_array == False
    assert s1.var_def.data_type.type_name.lexeme == 'int'
    assert s1.var_def.var_name.lexeme == 'x'
    assert s1.expr.not_op == False
    assert s1.expr.first.rvalue.value.lexeme == '1'
    assert s1.expr.op == None
    assert s1.expr.rest == None
    s2 = p.fun_defs[0].stmts[1]
    assert s2.lvalue[0].var_name.lexeme == 'x'
    assert s2.lvalue[0].array_expr == None
    assert s2.expr.not_op == False
    assert s2.expr.first.rvalue.value.lexeme == '2'
    assert s2.expr.op == None
    assert s2.expr.rest == None
    s3 = p.fun_defs[0].stmts[2]
    assert s3.if_part.condition.not_op == False
    assert s3.if_part.condition.first.rvalue.path[0].var_name.lexeme == 'x'
    assert s3.if_part.condition.first.rvalue.path[0].array_expr == None
    assert s3.if_part.condition.op == None
    assert s3.if_part.condition.rest == None
    assert s3.if_part.stmts[0].expr.not_op == False
    assert s3.if_part.stmts[0].expr.first.rvalue.value.lexeme == 'true'
    assert s3.if_part.stmts[0].expr.op == None
    assert s3.if_part.stmts[0].expr.rest == None
    assert s3.else_ifs == []
    assert s3.else_stmts == []
    s4 = p.fun_defs[0].stmts[3]
    assert s4.condition.not_op == False
    assert s4.condition.first.rvalue.value.lexeme == 'true'
    assert s4.condition.op == None
    assert s4.condition.rest == None
    assert s4.stmts[0].lvalue[0].var_name.lexeme == 'x'
    assert s4.stmts[0].lvalue[0].array_expr == None
    assert s4.stmts[0].expr.not_op == False
    assert s4.stmts[0].expr.first.rvalue.path[0].var_name.lexeme == 'x'
    assert s4.stmts[0].expr.first.rvalue.path[0].array_expr == None
    assert s4.stmts[0].expr.op.lexeme == '+'
    assert s4.stmts[0].expr.rest.not_op == False