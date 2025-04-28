"""Implementation of the MyPL Virtual Machine (VM).

NAME: Alicia Domingo
DATE: Spring 2024
CLASS: CPSC 326

"""

from src.mypl_error import *
from src.mypl_opcode import *
from src.mypl_frame import *

class VM:

    def __init__(self):
        """Creates a VM."""
        self.struct_heap = {}        # id -> dict
        self.array_heap = {}         # id -> list
        self.next_obj_id = 2024      # next available object id (int)
        self.frame_templates = {}    # function name -> VMFrameTemplate
        self.call_stack = []         # function call stack

    def __repr__(self):
        """Returns a string representation of frame templates."""
        s = ''
        for name, template in self.frame_templates.items():
            s += f'\nFrame {name}\n'
            for i in range(len(template.instructions)):
                s += f'  {i}: {template.instructions[i]}\n'
        return s

    def add_frame_template(self, template):
        """Add the new frame info to the VM. 

        Args: 
            frame -- The frame info to add.

        """
        self.frame_templates[template.function_name] = template

    def error(self, msg, frame=None):
        """Report a VM error."""
        if not frame:
            raise VMError(msg)
        pc = frame.pc - 1
        instr = frame.template.instructions[pc]
        name = frame.template.function_name
        msg += f' (in {name} at {pc}: {instr})'
        raise VMError(msg)
    
    def is_int_or_float(self, s):
        # Check if string is empty
        if not s:
            return False
        
        # Check if string contains only digits or a single decimal point
        if all(char.isdigit() or char == '.' for char in s):
            # Check if there's at most one decimal point
            if s.count('.') <= 1:
                return True
        return False
    
    #----------------------------------------------------------------------
    # RUN FUNCTION
    #----------------------------------------------------------------------
    
    def run(self, debug=False):
        """Run the virtual machine."""
        # grab the "main" function frame and instantiate it
        if not 'main' in self.frame_templates:
            self.error('No "main" function')
        frame = VMFrame(self.frame_templates['main'])
        self.call_stack.append(frame)

        # run loop (continue until run out of call frames or instructions)
        while self.call_stack and frame.pc < len(frame.template.instructions):
            # get the next instruction
            instr = frame.template.instructions[frame.pc]
            # increment the program count (pc)
            frame.pc += 1
            # for debugging:
            if debug:
                print('\n')
                print('\t FRAME.........:', frame.template.function_name)
                print('\t PC............:', frame.pc)
                print('\t INSTRUCTION...:', instr)
                val = None if not frame.operand_stack else frame.operand_stack[-1]
                print('\t NEXT OPERAND..:', val)
                cs = self.call_stack
                fun = cs[-1].template.function_name if cs else None
                print('\t NEXT FUNCTION..:', fun)

            #------------------------------------------------------------
            # Literals and Variables
            #------------------------------------------------------------

            if instr.opcode == OpCode.PUSH:
                frame.operand_stack.append(instr.operand)

            elif instr.opcode == OpCode.POP:
                frame.operand_stack.pop()
                
            elif instr.opcode == OpCode.STORE:
                x = frame.operand_stack.pop()
                frame.variables.insert(instr.operand, x)
                
            elif instr.opcode == OpCode.LOAD:
                x = frame.variables[instr.operand]
                frame.operand_stack.append(x)
            

            #------------------------------------------------------------
            # Operations
            #------------------------------------------------------------
            
            # ARITHMETIC OPERATORS
        
            elif instr.opcode == OpCode.ADD:
                if len(frame.operand_stack) >= 2:
                    x = frame.operand_stack.pop()
                    y = frame.operand_stack.pop()
                    
                    if x == None or y == None:
                        raise MyPLError('VM Error: Stack must contain two valid ints or doubles')
                    
                    result = y + x
                    frame.operand_stack.append(result)
        
            elif instr.opcode == OpCode.SUB:
                if len(frame.operand_stack) >= 2:
                    x = frame.operand_stack.pop()
                    y = frame.operand_stack.pop()
                    
                    if x == None:
                        raise MyPLError('VM Error: Stack must contain two valid ints or doubles')
                    if y == None:
                        raise MyPLError('VM Error: Stack must contain two valid ints or doubles')
                    
                    result = y - x
                    frame.operand_stack.append(result)
            
            elif instr.opcode == OpCode.MUL:
                if len(frame.operand_stack) >= 2:
                    x = frame.operand_stack.pop()
                    y = frame.operand_stack.pop()
                    
                    if x == None or y == None:
                        raise MyPLError('VM Error: Stack must contain two valid ints or doubles')
                    
                    result = y * x
                    frame.operand_stack.append(result)
            
            elif instr.opcode == OpCode.DIV:
                if len(frame.operand_stack) >= 2:
                    x = frame.operand_stack.pop()
                    y = frame.operand_stack.pop()
                    
                    
                    if x == None or y == None:
                        raise MyPLError('VM Error: Stack must contain two valid ints or doubles')
                    elif x == 0:
                        raise MyPLError('VM Error: Division by 0 error')
                    
                    if type(x) == int and type(y) == int:
                        result = int(y / x)
                    else:
                        result = y / x
                    frame.operand_stack.append(result)
             
            # LOGICAL OPERATORS       
            elif instr.opcode == OpCode.AND:
                x = frame.operand_stack.pop()
                y = frame.operand_stack.pop()
                
                if x == None or y == None:
                    raise MyPLError('VM Error: Cannot contain None type')
                
                result = y and x
                frame.operand_stack.append(result)
            
            elif instr.opcode == OpCode.OR:
                x = frame.operand_stack.pop()
                y = frame.operand_stack.pop()
                
                if x == None or y == None:
                    raise MyPLError('VM Error: Cannot contain None type')
                
                result = y or x
                frame.operand_stack.append(result)
            
            elif instr.opcode == OpCode.NOT:
                x = frame.operand_stack.pop()
                
                if x == None:
                    raise MyPLError('VM Error: Cannot contain None type')
                
                result = not x
                frame.operand_stack.append(result)
                
            # RELATIONAL OPERATORS
            elif instr.opcode == OpCode.CMPLT:
                x = frame.operand_stack.pop()
                y = frame.operand_stack.pop()
                
                if x == None or y == None:
                    raise MyPLError('VM Error: Cannot contain None type')
                
                result = y < x
                frame.operand_stack.append(result)
            
            elif instr.opcode == OpCode.CMPLE:
                if len(frame.operand_stack) >= 2:
                    x = frame.operand_stack.pop()
                    y = frame.operand_stack.pop()
                    
                    if x == None:
                        raise MyPLError('VM Error: Cannot contain None type')
                    if y == None:
                        raise MyPLError('VM Error: Cannot contain None type')
                    
                    result = y <= x
                    frame.operand_stack.append(str(result).lower())
            
            elif instr.opcode == OpCode.CMPEQ:
                x = frame.operand_stack.pop()
                y = frame.operand_stack.pop()
                
                result = y == x
                frame.operand_stack.append(result)
            
            elif instr.opcode == OpCode.CMPNE:
                x = frame.operand_stack.pop()
                y = frame.operand_stack.pop()
                
                result = y != x
                frame.operand_stack.append(result)

            #------------------------------------------------------------
            # Branching
            #------------------------------------------------------------

            elif instr.opcode == OpCode.JMP:
                frame.pc = instr.operand
                
            elif instr.opcode == OpCode.JMPF:
                x = frame.operand_stack.pop()
                if not x or x == 'false':
                    frame.pc = instr.operand 
                 
            #------------------------------------------------------------
            # Functions
            #------------------------------------------------------------

            elif instr.opcode == OpCode.RET:
                return_val = frame.operand_stack.pop()
                self.call_stack.pop()
                if not len(self.call_stack) == 0:
                    frame = self.call_stack[-1]
                frame.operand_stack.append(return_val)
            
            elif instr.opcode == OpCode.CALL:
                fun_name = instr.operand
                new_frame_template = self.frame_templates[fun_name]
                new_frame = VMFrame(new_frame_template)
                self.call_stack.append(new_frame)
                for _ in range(0, new_frame_template.arg_count):
                    arg = frame.operand_stack.pop()
                    new_frame.operand_stack.append(arg)
                frame = new_frame
                
            #------------------------------------------------------------
            # Built-In Functions
            #------------------------------------------------------------

            elif instr.opcode == OpCode.WRITE:
                if not frame.operand_stack == []:
                    x = frame.operand_stack.pop()
                    
                    if x == None:
                        print('null', end='')
                    else:
                        if isinstance(x, bool):
                            print(str(x).lower(), end='')
                        else:
                            print(x, end='')
                            
            elif instr.opcode == OpCode.READ:
                result = input()
                frame.operand_stack.append(result)
                                 
            elif instr.opcode == OpCode.LEN:
                x = frame.operand_stack.pop()
                if not x == None and type(x) == str:
                    frame.operand_stack.append(len(x))
                elif x == None:
                    raise MyPLError('VM Error: Cannot get length of None type')
                else:
                    obj = self.array_heap
                    frame.operand_stack.append(len(obj[x]))
                
            elif instr.opcode == OpCode.GETC:
                x = frame.operand_stack.pop() 
                if x == None:
                    raise MyPLError('VM Error: Cannot be None type')
                
                y = frame.operand_stack.pop() 
                if y == None:
                    raise MyPLError('VM Error: Cannot be None type')
                
                if y > len(x) - 1 or y < 0:
                    raise MyPLError('VM Error: Index too large for string')
                result = x[y]
                frame.operand_stack.append(result)
                                
            elif instr.opcode == OpCode.TOINT:
                x = frame.operand_stack.pop()
                if x == None:
                    raise MyPLError('VM Error: Cannot be a None type')
                
                if type(x) == float:
                    frame.operand_stack.append(int(x))
                elif type(x) == str and x.isdigit():
                    frame.operand_stack.append(int(x))
                else:
                    raise MyPLError('VM Error: TOINT opcode requires a string, int, or double')   
                
            elif instr.opcode == OpCode.TODBL:
                x = frame.operand_stack.pop()
                if x == None:
                    raise MyPLError('VM Error: Cannot be a None type')
                
                if type(x) == str and not self.is_int_or_float(x):
                    raise MyPLError('VM Error: String must just contain a int or double')
                elif type(x) == int or type(x) == float:
                    frame.operand_stack.append(float(x))
                else:
                    frame.operand_stack.append(float(x))
                 
            elif instr.opcode == OpCode.TOSTR:
                x = frame.operand_stack.pop()
                if x == None:
                    raise MyPLError('VM Error: Cannot be a None type')
                
                frame.operand_stack.append(str(x))
            
            #------------------------------------------------------------
            # Heap
            #------------------------------------------------------------
            elif instr.opcode == OpCode.ALLOCS:
                oid = self.next_obj_id
                self.next_obj_id += 1
                self.struct_heap[oid] = {}
                frame.operand_stack.append(oid)
            
            elif instr.opcode == OpCode.SETF:
                a = instr.operand
                value = frame.operand_stack.pop()
                if value == None:
                    raise MyPLError('VM Error: value is None. You cannot have any None types')
                oid = frame.operand_stack.pop()
                if oid == None:
                    raise MyPLError('VM Error: oid is None. You cannot have any None types')
                
                obj = self.struct_heap
                obj[oid][a] = value
                self.struct_heap = obj
                 
            elif instr.opcode == OpCode.GETF:
                oid = frame.operand_stack.pop()
                if oid == None:
                    raise MyPLError('VM Error: oid cannot be None type')
                a = instr.operand
                obj = self.struct_heap
                frame.operand_stack.append(obj[oid][a])
                
            elif instr.opcode == OpCode.ALLOCA:
                oid = self.next_obj_id
                self.next_obj_id += 1
                array_length = frame.operand_stack.pop()
                if array_length == None or array_length < 0:
                    raise MyPLError('VM Error: Array length cannot be None type or less than 0')
                
                self.array_heap[oid] = ['null' for _ in range(array_length)]
                frame.operand_stack.append(oid)
            
            elif instr.opcode == OpCode.SETI:
                value = frame.operand_stack.pop()
                index = frame.operand_stack.pop()
                oid = frame.operand_stack.pop()
                
                if index == None or oid == None:
                    raise MyPLError('VM Error: Index cannot be None Type')
                
                obj = self.array_heap
                if len(obj[oid]) <= index or index < 0:
                    raise MyPLError('VM Error: Index is too large for allocated array')
                
                obj[oid][index] = value
                self.array_heap = obj
            
            elif instr.opcode == OpCode.GETI:
                index = frame.operand_stack.pop()
                oid = frame.operand_stack.pop()
                if index == None or oid == None:
                    raise MyPLError('VM Error: Index or oid cannot be None')

                obj = self.array_heap
                if len(obj[oid]) <= index or index < 0:
                    raise MyPLError('VM Error: Index too large for allocated array')
                frame.operand_stack.append(obj[oid][index])

            #------------------------------------------------------------
            # Special 
            #------------------------------------------------------------

            elif instr.opcode == OpCode.DUP:
                x = frame.operand_stack.pop()
                frame.operand_stack.append(x)
                frame.operand_stack.append(x)

            elif instr.opcode == OpCode.NOP:
                # do nothing
                pass

            else:
                self.error(f'unsupported operation {instr}')