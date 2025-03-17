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
            execution.run(block, AI, insideFunc, True)
        except StopIteration:  # Catch the break statement
            break

def execute_for(statement, AI, insideFunc):
    init_statement = statement[1]
    condition = statement[2]
    increment_statement = statement[3]
    block = statement[4]
    line_number, line_content = statement[5], statement[6]

    # Execute the initialization part
    execution.run([init_statement], AI, insideFunc, True)

    # Execute the for loop
    while eval_condition(condition, line_number, line_content, insideFunc, AI):
        try:
            execution.run(block, AI, insideFunc, True)
        except StopIteration:  # Catch the break statement
            break
        # Execute the increment
        execution.run([increment_statement], AI, insideFunc, True)

#################################################################################3


def set_default_variable_in_karr(variables, variablesFunc):
    """
    Sets the default variable in the correct scope.
    """
    if variablesFunc:
        gv.variablesFunc['default'] = [0, 'int', True]
    else:
        gv.variables['default'] = [0, 'int', True]

def determine_loop_parameters_in_karr(number, init_statement, line_number, line_content, AI):
    """
    Determines the loop parameters (increment/decrement) based on the given number.
    """
    try:
        number=eval_value(number, line_number, line_content, AI)
        if int(number) < 0:
            plusminus = 'DECREMENT'
            bigless = '>'
        else:
            plusminus = 'INCREMENT'
            bigless = '<'
    except ValueError as v:
        error_message = f"{v}\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    
    condition = f'{init_statement[1]} {bigless} {number}' if init_statement is not None else f'default {bigless} {number}'
    increment_statement = (
        (plusminus, init_statement[1], line_number, line_content)
        if init_statement is not None else
        (plusminus, 'default', line_number, line_content)
    )
    return condition, increment_statement

def execute_loop_in_karr(init_statement, condition, increment_statement, block, AI, insideFunc, line_number, line_content):
    """
    Executes the loop with the provided condition and increment statement.
    """
    # Execute the initialization part
    if init_statement is not None:
        execution.run([init_statement], AI, insideFunc, True)

    # Execute the loop
    while eval_condition(condition, line_number, line_content, insideFunc, AI):
        try:
            execution.run(block, AI, insideFunc, True)
        except StopIteration:  # Catch the break statement
            break
        execution.run([increment_statement], AI, insideFunc, True)  # Execute the increment

def execute_karr(statement, AI, insideFunc, variables, variablesFunc):
    """
    Main function to execute the KARR loop based on the given statement.
    """
    line_number, line_content = statement[4], statement[5]
    set_default_variable_in_karr(variables, variablesFunc)
    
    init_statement = statement[1]
    number = statement[2]
    block = statement[3]
    
    condition, increment_statement = determine_loop_parameters_in_karr(number, init_statement, line_number, line_content, AI)
    execute_loop_in_karr(init_statement, condition, increment_statement, block, AI, insideFunc, line_number, line_content)
