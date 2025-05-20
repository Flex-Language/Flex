from flex_parser.parser_utils import *
from flex_parser.parse_arithmetic_expr import *
from flex_parser.parse_block import *
from flex_AI.useModel import *

def parse_function_call_statement(tokens, AI, line_number, line_content):
    func_name = current_token(tokens)[1]
    next_token(tokens)  # Consume the function name
    expect(tokens, 'LPAREN', AI)  # Expect '('

    args = []
    while current_token(tokens)[0] != 'RPAREN':
        if current_token(tokens)[0] in ('NUMBER', 'ID', 'STRING','MINUS','TRUE','LIST','FALSE'):
                args.append(parse_arithmetic_expr(tokens, AI, line_number, line_content))  # Parse the argument
        else:
            error_message = f"Unexpected token {current_token(tokens)[0]} while parsing function arguments at {line_number}\nLine content: '{line_content}'"
            handle_error(error_message, AI)

        if current_token(tokens)[0] == 'COMMA':
            next_token(tokens)  # Consume the comma
        elif current_token(tokens)[0] != 'RPAREN':
            error_message = f"Expected RPAREN, got {current_token(tokens)[0]} at {current_token(tokens)[2]}"
            handle_error(error_message, AI)

    expect(tokens, 'RPAREN', AI)  # Expect closing ')'
    return ('FUNC_CALL', func_name, args, line_number, line_content)

def parse_function_declaration_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'fun'
    func_name = expect(tokens, 'ID', AI)  # Expect function name (like 'add')
    expect(tokens, 'LPAREN', AI)  # Expect '(' for function parameters

    params = parse_function_parameters_in_function_declaration(tokens, AI, line_number, line_content)  # Parse function parameters
    expect(tokens, 'RPAREN', AI)  # Expect closing ')'
    
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    
    block = parse_block(tokens, AI)  # Parse the function body
    return ('FUN', func_name, params, block, line_number, line_content)

# def parse_function_parameters_in_function_declaration(tokens, AI, line_number, line_content):
#     params = []
#     while current_token(tokens)[0] != 'RPAREN':
#         param_type_token = current_token(tokens)
#         if param_type_token[0] in ('INT', 'FLOAT', 'BOOL', 'STR', 'LIST'):
#             param_type = param_type_token[0]  # Store the type
#             next_token(tokens)  # Move to the next token (the variable name)
#         else:
#             error_message = f"Expected a type ('int', 'float', 'bool', 'string','list'), but got {param_type_token[0]} at {param_type_token[2]}\nLine content: '{param_type_token[3]}'"
#             handle_error(error_message, AI)

#         param_name = expect(tokens, 'ID', AI)  # Expect an identifier (variable name)
#         params.append((param_type, param_name))  # Add the (type, name) pair to params

#         if current_token(tokens)[0] == 'COMMA':  # Handle multiple parameters
#             next_token(tokens)  # Consume the ','

#     return params

def parse_function_parameters_in_function_declaration(tokens, AI, line_number, line_content):
    params = []
    while current_token(tokens)[0] != 'RPAREN':
        param_type = None
        param_type_token = current_token(tokens)
        
        # Check if the token is a type
        if param_type_token[0] in ('INT', 'FLOAT', 'BOOL', 'STR', 'LIST'):
            param_type = param_type_token[0]  # Store the type
            next_token(tokens)  # Move to the next token (the variable name)
        
        param_name = expect(tokens, 'ID', AI)  # Expect an identifier (variable name)
        params.append((param_type, param_name))  # Add the (type, name) pair to params
        
        # Handle multiple parameters
        if current_token(tokens)[0] == 'COMMA':
            next_token(tokens)  # Consume the ','
    
    return params
