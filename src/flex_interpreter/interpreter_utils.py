import ast
from flex_AI.useModel import *
import re
import flex_interpreter.glopal_vars as gv
import flex_interpreter.execute.execute_function as exeFunc
from flex_interpreter.evaluating_values import eval_value, handle_function_call


def checkType(value,type,line_number,line_content,AI):
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

def eval_condition(condition, line_number, line_content,isFunc,AI):
    try:
        if 'EMPTY_COND' in condition:
            return True
        # Replace 'true' and 'false' with Python's 'True' and 'False'
        condition = condition.replace('true', 'True').replace('false', 'False')
        # Replace '=>' with '>=' and '=<' with '<=' to match Python's syntax
        condition = condition.replace('=>', '>=').replace('=<', '<=')
        if 'FUNC_CALL' in condition:
            pattern = r"\('FUNC_CALL'.*?\*'\)"
            func_call_stmt = re.search(pattern, condition).group()
            func_call_stmt=ast.literal_eval(func_call_stmt)
            value=eval_value(func_call_stmt, line_number, line_content, AI, None, isFunc)
            condition = re.sub(pattern, str(value), condition)
        # return eval(condition, {}, variables)  # Use the variables dictionary to resolve variable names
        if isFunc==False:
            return eval(condition, {}, {k: v[0] for k, v in gv.variables.items()})  # Use variable values for evaluation
        else:
            return eval(condition, {}, {k: v[0] for k, v in gv.variablesFunc.items()})
    except NameError as e:
        error_message = f"Variable not defined in condition: {str(e)}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error evaluating condition: {str(e)}\n{line_number}: '{line_content.strip()}'"
        handle_error(error_message, AI)



def format_string(string, line_number, line_content, AI, func=False):
    # Find all {var} in the string and replace with variable values if they exist
    matches = re.findall(r'\{(.*?)\}', string)
    for match in matches:
        if re.match(r'^-\s*[a-zA-Z_]\w*', match.strip()):  # Checks for negative variables
            error_message = f"Negative variables are not allowed in formatted strings: '{match}'.\n{line_number}, line content is: '{line_content.strip()}'"
            handle_error(error_message, AI)

        # Check if the match is a function call
        func_call_match = re.match(r'^([a-zA-Z_]\w*)\((.*)\)$', match.strip())
        if func_call_match:
            # It's a function call
            func_name = func_call_match.group(1)
            args = func_call_match.group(2)

            # Parse the arguments into a list
            arg_list = [arg.strip() for arg in args.split(',') if arg.strip()]
            statement = ['FUNC_CALL', func_name, arg_list,line_number, line_content]

            # Call execute_function_call with the statement array
            try:
                value = handle_function_call(statement,line_number, line_content, AI, func)
                string = string.replace(f'{{{match}}}', str(value))
            except Exception as e:
                handle_error(f"Error while executing function '{func_name}': {e}", AI)
        else:
            # Evaluate regular variables or expressions
            try:
                if not func:
                    value = eval(match, {}, {k: v[0] for k, v in gv.variables.items()})
                else:
                    value = eval(match, {}, {k: v[0] for k, v in gv.variablesFunc.items()})
                string = string.replace(f'{{{match}}}', str(value))
            except Exception:
                # If the variable is not found, leave it unchanged
                string = string.replace(f'{{{match}}}', f'{{{match}}}')

    return string


def eval_list_index(var_name, index, line_number, line_content,AI, insideFunc=False):
    """Evaluate list index access (e.g., x[2])."""
    try:
        # Retrieve the list from the appropriate scope
        if insideFunc and var_name in gv.variablesFunc:
            lst = gv.variablesFunc[var_name][0]
        elif var_name in gv.variables:
            lst = gv.variables[var_name][0]
        else:
            error_message = f"List '{var_name}' not defined.\n{line_number}: '{line_content.strip()}'"
            handle_error(error_message, AI)
        # Ensure the index is an integer
        index = int(index)
        # Return the value at the specified index
        return lst[index]
    except IndexError:
        error_message = f"Index out of range for list '{var_name}' at {line_number}.\nLine content: {line_content.strip()}"
        handle_error(error_message, AI)
    except ValueError:
        error_message = f"Invalid index type for list '{var_name}' at {line_number}.\nLine content: {line_content.strip()}"
        handle_error(error_message, AI)
