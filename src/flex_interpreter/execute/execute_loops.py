from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *
from flex_interpreter import execution
from flex_interpreter import glopal_vars as gv

def execute_while(statement, AI, insideFunc):
    condition = statement[1]
    block = statement[2]
    line_number, line_content = statement[3], statement[4]

    while eval_condition(condition, line_number, line_content, insideFunc, AI) or condition in ('true', '1'):
        try:
            execution.run(block, AI,gv.web, insideFunc, True)
        except StopIteration:  # Catch the break statement
            break

def execute_for(statement, AI, insideFunc):
    init_statement = statement[1]
    condition = statement[2]
    increment_statement = statement[3]
    block = statement[4]
    line_number, line_content = statement[5], statement[6]

    # Execute the initialization part
    execution.run([init_statement], AI,gv.web, insideFunc, True)

    # Execute the for loop
    while eval_condition(condition, line_number, line_content, insideFunc, AI):
        try:
            execution.run(block, AI, gv.web,insideFunc, True)
        except StopIteration:  # Catch the break statement
            break
        # Execute the increment
        execution.run([increment_statement], AI,gv.web, insideFunc, True)

#################################################################################3


def set_default_variable_in_karr(variables, variablesFunc,statement,AI, insideFunc, line_number, line_content):
    """
    Sets the default variable in the correct scope.
    """ 
    if variablesFunc:
        if statement==None:
            gv.variablesFunc['default'] = [0, 'INT', True]
        elif statement[0] == 'STANDALONE_VAR':
            var_name=statement[1]
            if var_name not in gv.variablesFunc:
                gv.variablesFunc[var_name] = [0, None, True]
            elif gv.variablesFunc[var_name][0]== None and gv.variablesFunc[var_name][1] in ('INT','FLOAT'):
                gv.variablesFunc[var_name][0] = 0
        elif statement[0] == 'NUMBER' or statement[0] == '-VE_NUMBER':
            number = statement[1]
            gv.variablesFunc['default'] = [int(number), 'INT', True]
        elif statement[0]=='ASSIGN':
            var_name=statement[1]
            val=eval_value(statement[2],line_number, line_content, AI, None, insideFunc)
            gv.variablesFunc[var_name] = [int(val), None, True]
        else:
            gv.variablesFunc['default'] = [0, 'INT', True]
    else:
        if statement==None:
            gv.variables['default'] = [0, 'INT', True]
        elif statement[0] == 'STANDALONE_VAR':
            var_name=statement[1]
            if var_name not in gv.variables:
                gv.variables[var_name] = [0, None, True]
            elif gv.variables[var_name][0]== None and gv.variables[var_name][1] in ('INT','FLOAT'):
                gv.variables[var_name][0] = 0
        elif statement[0] == 'NUMBER' or statement[0] == '-VE_NUMBER':
            number = statement[1]
            gv.variables['default'] = [int(number), 'INT', True]
        elif statement[0]=='ASSIGN':
            var_name=statement[1]
            val=eval_value(statement[2],line_number, line_content, AI, None, insideFunc)
            gv.variables[var_name] = [int(val), None, True]
        else:
            gv.variables['default'] = [0, 'INT', True]

def determine_loop_parameters_in_karr(number, init_statement, line_number, line_content, AI,insideFunc):
    """
    Determines the loop parameters (increment/decrement) based on the given number.
    """
    flag=0
    try:
        if insideFunc:
            if init_statement==None:
                var_name = 'default'
            elif init_statement[0]=="NUMBER" or init_statement[0]=="-VE_NUMBER":
                var_name = 'default'
            else:
                var_name = init_statement[1]
            
            if int(number) < gv.variablesFunc[var_name][0]:
                plusminus = 'DECREMENT'
                bigless = '>'
            else:
                plusminus = 'INCREMENT'
                bigless = '<'
        else:
            number=eval_value(number, line_number, line_content, AI,None,insideFunc)   
            if init_statement==None:
                var_name = 'default'
                init_number=gv.variables[var_name][0]
            elif init_statement[0]=="NUMBER" or init_statement[0]=="-VE_NUMBER":
                var_name = 'default'
                init_number=gv.variables[var_name][0]
            # If it's a LIST_ACCESS, apply the indices
            elif init_statement[0] in ("LIST_ACCESS",'LIST_ASSIGN'):   
                var_name = init_statement[1]
                init_number=gv.variables[var_name][0]
                indices = init_statement[2]  # ['5', '0'] in your example
                var_name = var_name + ''.join(f'[{i}]' for i in indices)
                for idx in indices:
                    init_number = init_number[int(idx)]
            else:
                var_name = init_statement[1]
                init_number=gv.variables[var_name][0]
            if int(number) < int(init_number):
                flag=0
                plusminus = 'DECREMENT'
                bigless = '>'
            else:
                flag=1
                plusminus = 'INCREMENT'
                bigless = '<'
    except ValueError as v:
        error_message = f"{v}\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    
    condition = f'{var_name} {bigless} {number}'
    increment_statement = (
        (plusminus, var_name, line_number, line_content)
    )
    if '[' in var_name and flag==0:
        plusminus = 'LIST_DECREMENT'
        increment_statement = (
            plusminus,init_statement[1], init_statement[2], line_number, line_content
        )

    elif '[' in var_name and flag==1:
        plusminus = 'LIST_INCREMENT'
        increment_statement = (
            plusminus,init_statement[1], init_statement[2], line_number, line_content
        )
    return condition, increment_statement

def execute_loop_in_karr(init_statement, condition, increment_statement, block, AI, insideFunc, line_number, line_content):
    """
    Executes the loop with the provided condition and increment statement.
    """
    # Execute the initialization part
    if init_statement is not None:
        execution.run([init_statement], AI,gv.web, insideFunc, True)

    # Execute the loop
    while eval_condition(condition, line_number, line_content, insideFunc, AI):
        try:
            execution.run(block, AI,gv.web, insideFunc, True)
        except StopIteration:  # Catch the break statement
            break
        execution.run([increment_statement], AI,gv.web, insideFunc, True)  # Execute the increment

def execute_karr(statement, AI, insideFunc, variables, variablesFunc):
    """
    Main function to execute the KARR loop based on the given statement.
    """
    line_number, line_content = statement[4], statement[5]
    init_statement = statement[1]
    set_default_variable_in_karr(variables, variablesFunc,init_statement,AI, insideFunc,line_number, line_content)
    
    number = statement[2]
    block = statement[3]
    
    condition, increment_statement = determine_loop_parameters_in_karr(number, init_statement, line_number, line_content, AI,insideFunc)
   
    execute_loop_in_karr(init_statement, condition, increment_statement, block, AI, insideFunc, line_number, line_content)
    if variables and 'default' in gv.variables:
        del gv.variables['default']
    elif variablesFunc and 'default' in gv.variablesFunc:  
        del gv.variablesFunc['default']
