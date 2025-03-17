from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter.evaluating_values import *



def check_variable_redeclaration(var_name, variables_scope, line_number, line_content, AI):
    """
    Checks if a variable is already defined in the given scope and raises an error if so.
    """
    if var_name in variables_scope and variables_scope[var_name][2]:
        error_message = f"Variable '{var_name}' already defined.\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)

def declare_variable(var_type, var_name, value, variables_scope, is_inside_func, line_number, line_content, AI):
    """
    Declares a variable and initializes it with a value or sets it to None if no value is provided.
    """
    isDeclared = True
    var_value=eval_value(value, line_number, line_content, AI, var_type, is_inside_func)
    variables_scope[var_name] = [
        var_value,
        var_type,
        isDeclared
    ]

def handle_uninitialized_variable(var_name, variables_scope):
    """
    Sets the variable value to None if it was declared without initialization.
    """
    variables_scope[var_name][0] = None

def check_and_cast_variable(var_name, variables_scope, line_number, line_content, AI):
    """
    Checks and casts the variable's value to its declared type.
    """
    variables_scope[var_name][0] = checkType(
        variables_scope[var_name][0],
        variables_scope[var_name][1],
        line_number,
        line_content,
        AI
    )

def execute_var_decl(statement, AI, insideFunc, variables, variablesFunc):
    """
    Executes the VAR_DECL (variable declaration) statement.
    """
    non_if = True  # Update the non_if flag

    scope = variablesFunc if insideFunc else variables

    if len(statement) == 5:
        var_type, vars, line_number, line_content = statement[1], statement[2], statement[3], statement[4]
        for var in vars:
            check_variable_redeclaration(var[0], scope, line_number, line_content, AI)
            declare_variable(var_type, var[0], var[1], scope, insideFunc, line_number, line_content, AI)
    # elif len(statement) == 5:
    #     var_type, var_name, value = statement[1], statement[2], None
    #     line_number, line_content = statement[3], statement[4]
    #     declare_variable(var_type, var_name, value, scope, insideFunc, line_number, line_content, AI)
        
            if var[1] is None:
                handle_uninitialized_variable(var[0], scope)
            else:
                check_and_cast_variable(var[0], scope, line_number, line_content, AI)

    return non_if, variables, variablesFunc
