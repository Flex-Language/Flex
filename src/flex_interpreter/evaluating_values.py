from flex_AI.useModel import *
import flex_interpreter.glopal_vars as gv
from flex_interpreter.interpreter_utils import *
from flex_interpreter import execution 
from flex_interpreter.return_ex import  *
import re

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
    else:
        return value

def eval_value(value, line_number, line_content, AI, var_type=None, func=False):
    
    if value is None and var_type is None:
        handle_uninitialized_variable_error(line_number, line_content, AI)
    elif value is None:
        return None
    elif value[0] == "FUNC_CALL":
        return handle_function_call(value, line_number, line_content, AI,func)
    elif isinstance(value, tuple) and value[0] == 'LIST_ELEMENT':
        return handle_list_element(value, line_number, line_content, AI, func)
    elif value.isdigit() or '.' in value:
        return handle_numeric_value(value)
    elif value == "scan_now":
        return handle_scan_now(var_type, line_number, line_content, AI)
    elif value == 'true':
        return True
    elif value == 'false':
        return False
    elif isinstance(value, tuple) and value[0] == 'LIST_ACCESS':
        return handle_list_access(value, line_number, line_content, AI, func)
    elif not func:
        return handle_global_scope(value, line_number, line_content, AI)
    else:
        return handle_function_scope(value, line_number, line_content, AI)

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
    func_params, func_block = gv.functions[func_name][arg_len]


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

def handle_numeric_value(value):
    return int(value) if '.' not in value else float(value)

def handle_scan_now(var_type, line_number, line_content, AI):
    if gv.web:
      print("Enter value:")
    
    value = input()
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
            # return eval(value, {}, {k: v[0] for k, v in gv.variables.items()})
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

def handle_global_scope(value, line_number, line_content, AI):
    try:
        if value in gv.variables:
            if gv.variables[value][0] is None:
                error_message = f"Variable '{value}' is uninitialized.\n{line_number}: '{line_content.strip()}'"
                handle_error(error_message, AI)

            return gv.variables[value][0]

        return eval(value, {}, {k: v[0] for k, v in gv.variables.items()})
    except NameError:
        error_message = f"Variable '{value}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except ZeroDivisionError:
        error_message = f"Division by Zero!\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error evaluating expression: {e}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)

def handle_function_scope(value, line_number, line_content, AI):
    try:
        if value in gv.variablesFunc:
            if gv.variablesFunc[value][0] is None:
                error_message = f"Variable '{value}' is uninitialized.\n{line_number}: '{line_content.strip()}'"
                handle_error(error_message, AI)

            return gv.variablesFunc[value][0]

        return eval(value, {}, {k: v[0] for k, v in gv.variablesFunc.items()})
    except NameError:
        error_message = f"Variable '{value}' not defined.\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except ZeroDivisionError:
        error_message = f"Division by Zero!\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error evaluating expression: {e}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
