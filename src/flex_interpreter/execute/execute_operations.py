from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *
from flex_interpreter.glopal_vars import *


def execute_increment(statement, AI, insideFunc, variables, variablesFunc):
    var_name = statement[1]
    line_number, line_content = statement[2], statement[3]

    if not insideFunc:
        if var_name not in variables:
            error_message = f"Variable '{var_name}' not defined.\n{line_number}: {line_content.strip()}"
            handle_error(error_message, AI)
        variables[var_name][0] += 1
    else:
        if var_name not in variablesFunc:
            error_message = f"Variable '{var_name}' not defined.\n{line_number}: {line_content.strip()}"
            handle_error(error_message, AI)
        variablesFunc[var_name][0] += 1
   
    return variables,variablesFunc

def execute_decrement(statement, AI, insideFunc, variables, variablesFunc):
    var_name = statement[1]
    line_number, line_content = statement[2], statement[3]

    if not insideFunc:
        if var_name not in variables:
            error_message = f"Variable '{var_name}' not defined.\n{line_number}: {line_content.strip()}"
            handle_error(error_message, AI)
        variables[var_name][0] -= 1
    else:
        if var_name not in variablesFunc:
            error_message = f"Variable '{var_name}' not defined.\n{line_number}: {line_content.strip()}"
            handle_error(error_message, AI)
        variablesFunc[var_name][0] -= 1

    return variables,variablesFunc

def execute_break(statement, AI, insideLoop, non_if, skip_next):
    line_number, line_content = statement[1], statement[2]

    non_if = True  # Update the non_if flag
    if not insideLoop:
        error_message = f"Break not inside a loop!\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)

    if not skip_next:  # If not skipping, raise StopIteration to break the loop
        raise StopIteration()

    return non_if  # Return the updated non_if flag

def execute_assign(statement, AI, insideFunc, variables, variablesFunc):
    """
    Executes the ASSIGN statement for variable assignment.
    """
    non_if = True  # Update the non_if flag
    if insideFunc:
        
        if len(statement) == 5:  # When all elements are present
            var_name, value, line_number, line_content = statement[1], statement[2], statement[3], statement[4]
            if var_name in variablesFunc:
                variablesFunc[var_name][0] = eval_value(value, line_number, line_content, AI, variablesFunc[var_name][1], insideFunc)
            else:
                variablesFunc[var_name] = [eval_value(value, line_number, line_content, AI, None, insideFunc), None, True]
        else:
            error_message = f"Unexpected statement format for 'ASSIGN': {statement}"
            handle_error(error_message, AI)

        variablesFunc[var_name][0] = checkType(
            variablesFunc[var_name][0], variablesFunc[var_name][1], line_number, line_content, AI
        )
        
    else:
        if len(statement) == 5:  # When all elements are present
            var_name, value, line_number, line_content = statement[1], statement[2], statement[3], statement[4]
            if var_name in variables: 
                variables[var_name][0] = eval_value(value, line_number, line_content, AI, variables[var_name][1])
            else:
                variables[var_name] = [eval_value(value, line_number, line_content, AI), None, True]
        else:
            error_message = f"Unexpected statement format for 'ASSIGN': {statement}"
            handle_error(error_message, AI)

        variables[var_name][0] = checkType(
            variables[var_name][0], variables[var_name][1], line_number, line_content, AI
        )
        
    return non_if,variables,variablesFunc  # Return updated non_if flag
