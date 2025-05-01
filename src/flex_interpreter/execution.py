import flex_interpreter.glopal_vars as gv
from flex_interpreter.execute.execute_conditions import execute_if, execute_if_block, execute_elif, execute_else
from flex_interpreter.execute.execute_list import execute_list_decl, execute_list_assign, execute_list_add, execute_list_pop, execute_list_remove, execute_assign_list_access
from flex_interpreter.execute.execute_loops import execute_while, execute_for, execute_karr
from flex_interpreter.execute.execute_operations import execute_break, execute_increment, execute_decrement, execute_assign
from flex_interpreter.execute.execute_function import execute_return, execute_function, execute_function_call
from flex_interpreter.execute.execute_variable_declaration import execute_var_decl
from flex_interpreter.execute.execute_print import execute_print
from flex_interpreter.execute.execute_import import execute_import

def run(statements,AI,WEB,insideFunc=False,insideLoop=False,forLoopLocal=False,import_list=None):
    
    skip_next = False  # To track if we need to skip the next statement
    if_first=False
    trueifFlag=False
    trueElifFlag=False
    non_if=True
    elif_finished=False
    if WEB:
        gv.web = True
    else:
        gv.web = False
    
    for statement in statements:
        
        # print(gv.variables)
        # print(gv.variablesFunc)
        if statement[0] == 'EMPTY':
            continue
        if statement[0] == 'IF':
            non_if = False
            elif_finished = False
            skip_next = execute_if(statement, AI, insideFunc, skip_next)
        elif statement[0] == 'IF_BLOCK':
            non_if = False
            elif_finished = False
            if_first = True
            trueifFlag = execute_if_block(statement, AI, insideFunc, insideLoop)
            skip_next = False  # Reset skip flag
        elif statement[0] == 'ELIF_BLOCK':
           trueElifFlag, elif_finished = execute_elif(statement, AI, insideFunc, insideLoop, if_first, non_if, trueifFlag, trueElifFlag, elif_finished)       
        elif statement[0] == 'ELSE_BLOCK':
             if_first = execute_else(statement, AI, insideFunc, insideLoop, if_first, non_if, trueifFlag, trueElifFlag, elif_finished)
        elif statement[0] == 'LIST_DECL':  # Handle list declaration
             gv.variables, gv.variablesFunc = execute_list_decl(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'LIST_ASSIGN':
             gv.variables, gv.variablesFunc = execute_list_assign(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0]=='LIST_ADD':
           gv.variables, gv.variablesFunc = execute_list_add(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0]=='LIST_POP':
           gv.variables, gv.variablesFunc = execute_list_pop(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0]=='LIST_REMOVE':
            gv.variables, gv.variablesFunc = execute_list_remove(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'RETURN':
            gv.returned_value =0
            gv.returned_value = execute_return(statement, insideFunc, AI, gv.returned_value)       
        elif statement[0] == 'FUN':  # Function definition
           gv.functions, params, block = execute_function(statement, gv.functions)  # Pass and return functions dictionary
        elif statement[0] == 'FUNC_CALL':  # Function call
            gv.functions,params, block = execute_function_call(statement, AI, gv.functions)    
        elif statement[0] == 'WHILE':
            non_if = True
            execute_while(statement, AI, insideFunc)
            skip_next = False  # Reset skip flag
        elif statement[0] == 'FOR':
             non_if = True
             execute_for(statement, AI, insideFunc)
        elif statement[0] == 'KARR':
            non_if=True
            execute_karr(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'BREAK':
             non_if = execute_break(statement, AI, insideLoop, non_if, skip_next)
        elif statement[0] == 'INCREMENT':
             non_if = True
             gv.variables,gv.variablesFunc = execute_increment(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'DECREMENT':
            non_if = True
            gv.variables,gv.variablesFunc = execute_decrement(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'PRINT':
            non_if, skip_next = execute_print(statement, AI, skip_next, insideFunc)
        elif statement[0] == 'VAR_DECL':  # Variable declaration
            non_if,gv.variables,gv.variablesFunc = execute_var_decl(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'ASSIGN' and isinstance(statement[1], tuple) and statement[1][0] == 'LIST_ACCESS':
           gv.variables,gv.variablesFunc = execute_assign_list_access(statement, AI, insideFunc, gv.variables, gv.variablesFunc)    
        elif statement[0] == 'ASSIGN':  # Variable assignment
            non_if,gv.variables,gv.variablesFunc = execute_assign(statement, AI, insideFunc, gv.variables, gv.variablesFunc)
        elif statement[0] == 'IMPORT':
           execute_import(statement, AI,statements,import_list)


