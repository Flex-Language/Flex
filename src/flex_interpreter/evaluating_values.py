from flex_AI.useModel import *
import flex_interpreter.glopal_vars as gv
from flex_interpreter.interpreter_utils import *
from flex_interpreter import execution 
from flex_interpreter.return_ex import  *
import re
import sys

def checkType2(value,type,line_number,line_content,AI):
    if (type != None):
        type=type.lower()
    if type=='int' and isinstance(value,float):
        return int(value)
    elif (type=='str' or type=='string') and not isinstance(value,str):
        error_message = f"non String in a string variable! at {line_number}\nLine content: {line_content}"
        handle_error(error_message, AI)
    elif type=='float' and isinstance(value,int):
        return float(value)
    elif type=='bool' and (value!=True and value!=False):
        error_message = f"non bool in a Bool variable! at {line_number}\nLine content: {line_content}"
        handle_error(error_message, AI)  
    elif type in ('int','float','list') and isinstance(value,bool):
        error_message = f"Bool in a number variable! at {line_number}\nLine content: {line_content}"
        handle_error(error_message, AI)
    elif type in ('int','float','bool','list') and isinstance(value,str):
        error_message = f"String in a non string variable! at {line_number}\nLine content: {line_content.strip()}"
        handle_error(error_message, AI)
    elif type in ('int','float','bool',) and isinstance(value,list):
        error_message = f"list in a non list variable! at {line_number}\nLine content: {line_content.strip()}"
        handle_error(error_message, AI)
    elif type == 'list' and not isinstance(value, list):
        error_message = f"non list in a list! at {line_number}\nLine content: {line_content.strip()}"
        handle_error(error_message, AI)
    else:
        return value

def eval_value(value, line_number, line_content, AI, var_type=None, func=False):
    
    if value is None and var_type is None:
        handle_uninitialized_variable_error(line_number, line_content, AI)
    elif value is None:
        return None
    elif value[0] == "FUNC_CALL":
        return handle_function_call(value, line_number, line_content, AI,func)
    elif isinstance(value, list):
        return [eval_value(v, line_number, line_content, AI, var_type, func) for v in value]
    elif isinstance(value, tuple) and value[0] == 'LIST_ELEMENT':
        return handle_list_element(value, line_number, line_content, AI, func)
    elif isinstance(value, tuple) and value[0] == 'LIST_ACCESS':
        return handle_list_access(value, line_number, line_content, AI, func)
    elif value.isdigit() or '.' in value:
        return handle_numeric_value(value,line_number,line_content,AI,func)
    elif value == "scan_now":
        return handle_scan_now(var_type, line_number, line_content, AI)
    elif value in  ('true','True','TRUE','sa7','s7','sah','saa7'):
        return True
    elif value in ('false','False','FALSE','ghalt','ghlt','ghalat'):
        return False
    elif not func:
        return handle_global_scope(value, line_number, line_content, AI,func)
    else:
        return handle_function_scope(value, line_number, line_content, AI,func)

def handle_uninitialized_variable_error(line_number, line_content, AI):
    error_message = f"Attempting to use an uninitialized variable.\n{line_number}: '{line_content.strip()}'"
    handle_error(error_message, AI)

def handle_function_call(value, line_number, line_content, AI,func):
    func_name = value[1]
    func_args = value[2] if len(value) > 2 else []
    arg_len = len(func_args)

    if func_name == "length":
        if len(func_args) != 1:
            error_message = f"Function 'length' expects 1 argument but got {len(func_args)}.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
        arg = eval_value(func_args[0], line_number, line_content, AI, 'string',func)
        if isinstance(arg, str):
                arg = checkType2(arg, 'string', line_number, line_content, AI)
        elif isinstance(arg, list):
                arg = checkType2(arg, 'list', line_number, line_content, AI)
        else:
            error_message = f"Function 'length' expects a string or a list argument.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
        return len(arg)   
    if func_name not in gv.functions:
        error_message = f"Function '{func_name}' is not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    try:
        func_params, func_block = gv.functions[func_name][arg_len]
    except KeyError:
        param_vals = list(gv.functions[func_name].keys())
        final_str = f"{param_vals[0]} "
        for i in range(1, len(param_vals)):
            final_str += 'or '
            final_str += f"{param_vals[i]} "
        error_message = f"Function '{func_name}' expects {final_str}argument(s) but got {len(func_args)}.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)


    if len(func_params) != len(func_args):
        error_message = f"Function '{func_name}' expects {len(func_params)} arguments but got {len(func_args)}.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

    local_scope = {}
    for i, (param_type, param_name) in enumerate(func_params):
        arg_value = eval_value(func_args[i], line_number, line_content, AI, param_type,func)
        arg_value = checkType2(arg_value, param_type, line_number, line_content, AI)
        local_scope[param_name] = [arg_value, param_type, True]

    # print(local_scope)
    return handle_function(func_block, local_scope, line_number, line_content, AI)

def handle_function(func_block, local_scope, line_number, line_content, AI):
   
    previous_variablesFunc = gv.variablesFunc.copy()
    gv.variablesFunc = local_scope
    # print(gv.variablesFunc)

    try:
        execution.run(func_block, AI,gv.web, True)
       # error_message = f"No return value for this function.\n{line_number}: '{line_content.strip()}'"
       # handle_error(error_message, AI)
    except ReturnException as return_exception:
        return return_exception.value
    finally:
            # Restore previous function variables (clear local scope)
            gv.variablesFunc.clear()
            gv.variablesFunc = previous_variablesFunc

def handle_list_element(value, line_number, line_content, AI, func):
    var_name, index = value[1], eval_value(value[2], line_number, line_content, AI)
    return eval_list_index(var_name, index, line_number, line_content, AI, func)

def handle_numeric_value(value,line_number,line_content,AI,func):
    # value= evaluate_expression(value, line_number, line_content, AI,func)
    # return int(value) if '.' not in value else float(value)
    return handle_global_scope(value, line_number, line_content, AI,func) if not func else handle_function_scope(value, line_number, line_content, AI,func)


def handle_scan_now(var_type, line_number, line_content, AI):
    if gv.web:
        # Signal that we're requesting input with the special marker
        print("__FLEX_INPUT_REQUEST__", flush=True)
        # Force flush to ensure immediate output without buffering
        sys.stdout.flush()
    
    value = input()
    
    if gv.web:
        # Signal that input has been received
        print("__FLEX_INPUT_RECEIVED__", flush=True)
        sys.stdout.flush()
        
    try:
        # if var_type == "string" or var_type is None:
        #     return value
        if value.isdigit():
            return int(value)
        elif value == '':
            error_message = "Pressed the Enter key in an input! don't do that."
            handle_error(error_message, AI)
        elif value[0] == '-' and value[1:].isdigit():
            return int(value)
        elif re.fullmatch(r'[-+]?\d*\.\d+', value):  # Check if the value is a float
            return float(value)
        else:
            return value
    except Exception as e:
        error_message = f"{e}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

def handle_list_access(value, line_number, line_content, AI, func):
    var_name, index = value[1], eval_value(value[2], line_number, line_content, AI)
    return eval_list_index(var_name, index, line_number, line_content, AI, func)
    

def handle_global_scope(value, line_number, line_content, AI,func):
    try:
        if isinstance(value, str) and value in gv.variables:
            if gv.variables[value][0] is None:
                error_message = f"Variable '{value}' is uninitialized.\n{line_number}: '{line_content.strip()}'"
                handle_error(error_message, AI)
            return gv.variables[value][0]

        
        # Replace any FUNC_CALL tuples in a complex expression
        evaluated_value = evaluate_expression(value, line_number, line_content, AI,func)
        # Use eval if it's a string expression
        if isinstance(evaluated_value, str):
            return eval(evaluated_value, {}, {k: v[0] for k, v in gv.variables.items()})
        else:
            return evaluated_value

    except NameError:
        error_message = f"Variable '{value}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except ZeroDivisionError:
        error_message = f"Division by Zero or Modulo by Zero!\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error evaluating expression: {e}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

def handle_function_scope(value, line_number, line_content, AI,func):
    try:
        if value in gv.variablesFunc:
            if gv.variablesFunc[value][0] is None:
                error_message = f"Variable '{value}' is uninitialized.\n{line_number}: '{line_content.strip()}'"
                handle_error(error_message, AI)

            return gv.variablesFunc[value][0]

        
        # Replace any FUNC_CALL tuples in a complex expression
        evaluated_value = evaluate_expression(value, line_number, line_content, AI,func)
        # Use eval if it's a string expression
        if isinstance(evaluated_value, str):
            return eval(evaluated_value, {}, {k: v[0] for k, v in gv.variablesFunc.items()})
        else:
            return evaluated_value
        # return eval(value, {}, {k: v[0] for k, v in gv.variablesFunc.items()})
    except NameError:
        error_message = f"Variable '{value}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except ZeroDivisionError:
        error_message = f"Division by Zero or Modulo by Zero!\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error evaluating expression: {e}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

def evaluate_expression(expr, line_number, line_content, AI, func):
    if 'FUNC_CALL' in expr:
        tuple_strings = re.findall(r"\('FUNC_CALL'.*?\)", expr)
        tuples = [ast.literal_eval(t) for t in tuple_strings]
        for t in tuples:
            expr = expr.replace(str(t), str(handle_function_call(t, line_number, line_content, AI,func)))
        # print("evaluate_expression after",expr)
        return expr
    elif isinstance(expr, list):
        return [evaluate_expression(e, line_number, line_content, AI,func) for e in expr]
    elif isinstance(expr, tuple):
        return tuple(evaluate_expression(e, line_number, line_content, AI,func) for e in expr)
    elif isinstance(expr, str) and expr in gv.variables and not func:
        if gv.variables[expr][0] is None:
            error_message = f"Variable '{expr}' is uninitialized.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
        return gv.variables[expr][0]
    elif isinstance(expr, str) and expr in gv.variablesFunc and func:
        if gv.variablesFunc[expr][0] is None:
            error_message = f"Variable '{expr}' is uninitialized.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
        return gv.variablesFunc[expr][0]
    elif isinstance(expr, (int, float, str)):
        return expr
    else:
        return expr
# def eval_list_index(var_name, index, line_number, line_content,AI, insideFunc=False):
#     """Evaluate list index access (e.g., x[2])."""
#     try:
#         # Retrieve the list from the appropriate scope
#         if insideFunc and var_name in gv.variablesFunc:
#             lst = gv.variablesFunc[var_name][0]
#         elif var_name in gv.variables:
#             lst = gv.variables[var_name][0]
#         else:
#             error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
#             handle_error(error_message, AI)
#         # Ensure the index is an integer
#         index = int(index)
#         # Return the value at the specified index
#         return lst[index]
#     except IndexError:
#         error_message = f"Index out of range for list '{var_name}' at {line_number}.\nLine content: {line_content.strip()}"
#         handle_error(error_message, AI)
#     except ValueError:
#         error_message = f"Invalid index type for list '{var_name}' at {line_number}.\nLine content: {line_content.strip()}"
#         handle_error(error_message, AI)
def eval_list_index(var_name, index, line_number, line_content, AI, insideFunc=False):
    """Evaluate nested list index access (e.g., x[2], x[1][0], x[1][2][3])."""
    try:
        # Retrieve the list from the appropriate scope
        if insideFunc and var_name in gv.variablesFunc:
            value = gv.variablesFunc[var_name][0]
        elif var_name in gv.variables:
            value = gv.variables[var_name][0]
        else:
            error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
            return handle_error(error_message, AI)

        # Ensure index is a list for uniform processing
        indices = [index] if isinstance(index, int) else index

        # Traverse nested indices
        for idx in indices:
            try:
                idx = int(idx)
                value = value[idx]
            except IndexError:
                error_message = f"Index {idx} out of range for list '{var_name}' at line {line_number}.\nLine content: {line_content.strip()}"
                return handle_error(error_message, AI)
            except (ValueError, TypeError):
                error_message = f"Invalid index '{idx}' for list '{var_name}' at line {line_number}.\nLine content: {line_content.strip()}"
                return handle_error(error_message, AI)
            except Exception as e:
                error_message = f"Error accessing list '{var_name}': {str(e)}\n{line_number}: '{line_content.strip()}'"
                return handle_error(error_message, AI)

        return value

    except Exception as e:
        error_message = f"Unexpected error in eval_list_index: {str(e)}\n{line_number}: '{line_content.strip()}'"
        return handle_error(error_message, AI)


import ast


