from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *

def execute_list_decl(statement, AI, insideFunc, variables, variablesFunc):
    var_name = statement[1]
    if 'FUNC_CALL' in statement[2]:  # If the value is a function call
        elements = eval_value(statement[2], statement[3], statement[4], AI, None, insideFunc)    
    else:
        elements = [eval_value(elem, statement[3], statement[4], AI,None,insideFunc) for elem in statement[2]]
    
    if insideFunc:
        variablesFunc[var_name] = [elements, 'list', True]  # Modify the function-scoped variable
        checkType(variablesFunc[var_name][0], variablesFunc[var_name][1], statement[3], statement[4], AI)
    else:
        variables[var_name] = [elements, 'list', True]  # Modify the global variable
        checkType(variables[var_name][0], variables[var_name][1], statement[3], statement[4], AI)

    return variables, variablesFunc  # Return the updated variables

# def execute_list_assign(statement, AI, insideFunc, variables, variablesFunc):
#     var_name, index_expr, value_expr, line_number, line_content = statement[1:]
    
#     index = eval_value(index_expr, line_number, line_content, AI)
#     new_value = eval_value(value_expr, line_number, line_content, AI)
#     if insideFunc and var_name in variablesFunc:
#         variablesFunc[var_name][0][index] = new_value
#     elif var_name in variables:
#         variables[var_name][0][index] = new_value
#     else:
#         error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
#         handle_error(error_message, AI)

#     return variables, variablesFunc  # Return the updated variables

def execute_list_assign(statement, AI, insideFunc, variables, variablesFunc):
    if statement[0] == 'LIST_ASSIGN':
        var_name, index_expr, value_expr, line_number, line_content = statement[1:]
    else:
        var_name, index_expr, line_number, line_content = statement[1:]   

    # Evaluate the index expression (can be int or list of ints)
    index_list = eval_value(index_expr, line_number, line_content, AI,None,insideFunc)
    if not isinstance(index_list, list):
        index_list = [index_list]

    # Evaluate the value to assign
    if statement[0] == 'LIST_ASSIGN':
        new_value = eval_value(value_expr, line_number, line_content, AI,None,insideFunc)

    # Choose the correct variable scope
    if insideFunc and var_name in variablesFunc:
        target = variablesFunc[var_name][0]
    elif var_name in variables:
        target = variables[var_name][0]
    else:
        error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

    # Traverse to the correct nested position
    try:
        for idx in index_list[:-1]:
            target = target[idx]
        if statement[0] == 'LIST_ASSIGN':
            target[index_list[-1]] = new_value
        elif statement[0] == 'LIST_INCREMENT':
            target[index_list[-1]] += 1
        elif statement[0] == 'LIST_DECREMENT':
            target[index_list[-1]] -= 1
    except (IndexError, TypeError) as e:
        error_message = (
            f"Invalid list assignment for '{var_name}' at index {index_list}.\n"
            f"{line_number}: '{line_content.strip()}'\nError: {e}"
        )
        handle_error(error_message, AI)

    return variables, variablesFunc


def execute_list_add(statement, AI, insideFunc, variables, variablesFunc):
    value, var_name, line_number, line_content = statement[1:]
    new_value = eval_value(value, line_number, line_content, AI,None,insideFunc)
    
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
        index = eval_value(index, line_number, line_content, AI,None,insideFunc)
    
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
    new_value = eval_value(value, line_number, line_content, AI,None,insideFunc)
    
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
    index = eval_value(statement[1][2], statement[3], statement[4], AI, None, insideFunc)
    new_value = eval_value(statement[2], statement[3], statement[4], AI, None, insideFunc)

    # Modify the list in the appropriate scope
    if insideFunc and var_name in variablesFunc:
        variablesFunc[var_name][0][index] = new_value
    elif var_name in variables:
        variables[var_name][0][index] = new_value
    else:
        error_message = f"List '{var_name}' not defined.\n{statement[3]}: '{statement[4].strip()}'"
        handle_error(error_message, AI)

    return variables,variablesFunc
