from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *

def execute_list_decl(statement, AI, insideFunc, variables, variablesFunc):
    var_name = statement[1]
    elements = [eval_value(elem, statement[3], statement[4], AI) for elem in statement[2]]
    
    if insideFunc:
        variablesFunc[var_name] = [elements, 'list', True]  # Modify the function-scoped variable
    else:
        variables[var_name] = [elements, 'list', True]  # Modify the global variable

    return variables, variablesFunc  # Return the updated variables

def execute_list_assign(statement, AI, insideFunc, variables, variablesFunc):
    var_name, index_expr, value_expr, line_number, line_content = statement[1:]
    index = eval_value(index_expr, line_number, line_content, AI)
    new_value = eval_value(value_expr, line_number, line_content, AI)
    
    if insideFunc and var_name in variablesFunc:
        variablesFunc[var_name][0][index] = new_value
    elif var_name in variables:
        variables[var_name][0][index] = new_value
    else:
        error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

    return variables, variablesFunc  # Return the updated variables

def execute_list_add(statement, AI, insideFunc, variables, variablesFunc):
    value, var_name, line_number, line_content = statement[1:]
    new_value = eval_value(value, line_number, line_content, AI)
    
    if insideFunc and var_name in variablesFunc:
        variablesFunc[var_name][0].append(new_value)
    elif var_name in variables:
        variables[var_name][0].append(new_value)
    else:
        error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

    return variables, variablesFunc  # Return the updated variables

def execute_list_pop(statement, AI, insideFunc, variables, variablesFunc):
    index, var_name, line_number, line_content = statement[1:]
    
    if index is not None:
        index = eval_value(index, line_number, line_content, AI)
    
    try:
        if insideFunc and var_name in variablesFunc:
            variablesFunc[var_name][0].pop(index)
        elif var_name in variables:
            if index is None:
                variables[var_name][0].pop()
            else:
                variables[var_name][0].pop(index)
        else:
            error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
    except TypeError:
        error_message = f"List index '{index}' not a number.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except IndexError:
        error_message = f"List index '{index}' out of range.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

    return variables, variablesFunc  # Return the updated variables

def execute_list_remove(statement, AI, insideFunc, variables, variablesFunc):
    value, var_name, line_number, line_content = statement[1:]
    new_value = eval_value(value, line_number, line_content, AI)
    
    try:
        if insideFunc and var_name in variablesFunc:
            variablesFunc[var_name][0].remove(new_value)
        elif var_name in variables:
            variables[var_name][0].remove(new_value)
        else:
            error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
    except ValueError:
        error_message = f"The item '{new_value}' is not in list.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except IndexError:
        error_message = f"List indexx out of range.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

    return variables, variablesFunc  # Return the updated variables

def execute_assign_list_access(statement, AI, insideFunc, variables, variablesFunc):
    """
    Executes the ASSIGN statement for list access (e.g., x[2] = value).
    """
    var_name = statement[1][1]
    index = eval_value(statement[1][2], statement[3], statement[4], AI)
    new_value = eval_value(statement[2], statement[3], statement[4], AI)

    # Modify the list in the appropriate scope
    if insideFunc and var_name in variablesFunc:
        variablesFunc[var_name][0][index] = new_value
    elif var_name in variables:
        variables[var_name][0][index] = new_value
    else:
        error_message = f"List '{var_name}' not defined.\n{statement[3]}: '{statement[4].strip()}'"
        handle_error(error_message, AI)

    return variables,variablesFunc
