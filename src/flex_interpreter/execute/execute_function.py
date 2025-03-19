from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *
from flex_interpreter.return_ex import  *

def execute_return(statement, insideFunc, AI, returned_value):
    """Handle the 'RETURN' statement and modify returned_value."""
    line_number, line_content = statement[2], statement[3]
    if insideFunc:
        # Evaluate the return value if present
        returned_value = eval_value(statement[1], line_number, line_content, AI, None, insideFunc) if len(statement) > 1 else None
        # Raise the custom exception with the return value
        raise ReturnException(returned_value)
    else:
        error_message = f"'return' statement outside of a function.\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    return returned_value

def execute_function(statement, functions):
    """Handle function definition and modify the functions dictionary."""
    func_name, params, block, line_number, line_content = statement[1], statement[2], statement[3], statement[4], statement[5]
    param_count = len(params)
    if func_name not in functions:
        functions[func_name] = {}  # Store function with params and block
    
    functions[func_name][param_count] = (params, block)
    return functions, params, block

def execute_function_call(statement, AI, functions):
    """Handle function call and modify variables or return value."""
    
    func_name, args, line_number, line_content = statement[1], statement[2], statement[3], statement[4]
    arg_count = len(args)
    if func_name not in functions and func_name != "length":
        error_message = f"Function '{func_name}' is not defined.\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    elif func_name == "length":
        return len(args)
    try:
        params, block = functions[func_name][arg_count]
    except KeyError:
        param_vals=list(functions[func_name].keys())
        final_str=f"{param_vals[0]} "
        for i in range (1,len(param_vals)):
            final_str+='or '
            final_str+=f"{param_vals[i]} "
        error_message = f"Function '{func_name}' expects {final_str}argument(s) but got {len(args)}.\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    # Check argument length
    if len(args) != len(params):
        error_message = f"Expected {len(params)} arguments but got {len(args)}.\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    
    # Evaluate the function call (or do other necessary actions)
    eval_value(statement, line_number, line_content, AI)
    return functions,params, block  # Return the updated functions dictionary
