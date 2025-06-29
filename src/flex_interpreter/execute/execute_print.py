from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *
import flex_interpreter.glopal_vars as gv
import sys



# def handle_list_access_in_print(statement, line_number, line_content, AI, insideFunc):
#     """
#     Handles printing for list access, e.g., x[2].
#     """
#     var_name, index_expr = statement[1][1], statement[1][2]
#     index = eval_value(index_expr, line_number, line_content, AI)
#     result = eval_list_index(var_name, index, line_number, line_content, AI, insideFunc)
#     print(result)

def handle_expression_in_print(statement, line_number, line_content, AI, insideFunc):
    """
    Handles printing for arithmetic expressions or variables.
    """
    result = eval_value(statement[1], line_number, line_content, AI, None, insideFunc)
    
    print(result, flush=gv.web)
    if gv.web:
        sys.stdout.flush()

def handle_formatted_string_in_print(statement, line_number, line_content, AI, insideFunc):
    """
    Handles printing for formatted strings.
    """
    formatted_message = format_string(statement[1][1:-1], line_number, line_content, AI, insideFunc)
    print(formatted_message, flush=gv.web)
    if gv.web:
        sys.stdout.flush()

def handle_function_call_in_print(statement, line_number, line_content, AI, insideFunc):
    """
    Handles printing for function calls.
    """
    value = handle_function_call(statement, line_number, line_content, AI, insideFunc)
    
    print(value, flush=gv.web)
    if gv.web:
        sys.stdout.flush()

def execute_print(statement, AI, skip_next, insideFunc):
    """
    Executes the PRINT statement.
    """
   
    non_if = True  # Update the non_if flag
    line_number, line_content = statement[2], statement[3]
    if not skip_next:
        # if isinstance(statement[1], tuple) and statement[1][0] == 'LIST_ACCESS': 
        #     handle_list_access_in_print(statement, line_number, line_content, AI, insideFunc)
        if statement[1][0] == 'FUNC_CALL':
            handle_function_call_in_print(statement[1], line_number, line_content, AI, insideFunc)
        elif re.search(r'^[^"]*[\d+\-*/][^"]*$', statement[1]) or re.search(r'^[a-zA-Z_]\w*$', statement[1]) or re.search(r'^[a-zA-Z_]\w*(\[(\d+|[a-zA-Z_]\w*)\])*$',statement[1]):
            handle_expression_in_print(statement, line_number, line_content, AI, insideFunc)
        else:
            handle_formatted_string_in_print(statement, line_number, line_content, AI, insideFunc)

    skip_next = False  # Reset skip flag after each PRINT statement
    return non_if, skip_next  # Return updated flags
