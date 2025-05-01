import flex_parser.glopal_vars as gv
from flex_parser.parser_utils import *
from flex_parser.parse_arithmetic_expr import *
from flex_parser.parse_expr import parse_expr

def parse_variable_operations_statement(tokens, AI, var_name, line_number, line_content):
    
    next_token(tokens)  # Consume the identifier
    current_tok_type = current_token(tokens)[0]

    if current_tok_type == 'INCREMENT':
        next_token(tokens)
        return ('INCREMENT', var_name, line_number, line_content)
    elif current_tok_type == 'SEMICOLON' and gv.forLoopFlag:
        next_token(tokens)
        return ('STANDALONE_VAR', var_name, line_number, line_content)
    elif current_tok_type == 'UNTILL' and gv.forLoopFlag:
        next_token(tokens)
        return ('STANDALONE_VAR', var_name, line_number, line_content)
    elif current_tok_type == 'DECREMENT':
        next_token(tokens)
        return ('DECREMENT', var_name, line_number, line_content)
    elif current_tok_type == 'ADD':
        return parse_list_add_in_variable_operations(tokens, AI, var_name, line_number, line_content)
    elif current_tok_type == 'POP':
        return parse_list_pop_in_variable_operations(tokens, AI, var_name, line_number, line_content)
    elif current_tok_type == 'REMOVE':
        return parse_list_remove_in_variable_operations(tokens, AI, var_name, line_number, line_content)
    elif current_tok_type == 'ASSIGN':
        return parse_assignment_in_variable_operations(tokens, AI, var_name, line_number, line_content)
    else:
        error_message = f"The Variable '{var_name}' is alone! at {line_number}\nLine content: '{line_content.strip()}'"
        handle_error(error_message, AI)
    # return None

def parse_list_add_in_variable_operations(tokens, AI, var_name, line_number, line_content):
    expect(tokens, 'ADD', AI)
    expect(tokens, 'LPAREN', AI)
    value = parse_arithmetic_expr(tokens, AI, line_number, line_content)
    expect(tokens, 'RPAREN', AI)
    return ('LIST_ADD', value, var_name, line_number, line_content)

def parse_list_pop_in_variable_operations(tokens, AI, var_name, line_number, line_content):
    expect(tokens, 'POP', AI)
    expect(tokens, 'LPAREN', AI)
    if current_token(tokens)[0] == 'RPAREN':
        index = None
    else:
        index = parse_arithmetic_expr(tokens, AI, line_number, line_content)
    expect(tokens, 'RPAREN', AI)
    return ('LIST_POP', index, var_name, line_number, line_content)

def parse_list_remove_in_variable_operations(tokens, AI, var_name, line_number, line_content):
    expect(tokens, 'REMOVE', AI)
    expect(tokens, 'LPAREN', AI)
    value = parse_arithmetic_expr(tokens, AI, line_number, line_content)
    expect(tokens, 'RPAREN', AI)
    return ('LIST_REMOVE', value, var_name, line_number, line_content)

def parse_assignment_in_variable_operations(tokens, AI, var_name, line_number, line_content):
    expect(tokens, 'ASSIGN', AI)
    if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
        value = parse_arithmetic_expr(tokens, AI, line_number, line_content)
    elif current_token(tokens)[0] == 'LBRACKET' and gv.pos + 1 < len(tokens):
        value = parse_list_statement(tokens, AI, line_number, line_content)
    elif current_token(tokens)[0] == 'SCAN':
        expect(tokens, 'SCAN', AI)
        expect(tokens, 'LPAREN', AI)
        expect(tokens, 'RPAREN', AI)
        value = "scan_now"
    elif current_token(tokens)[0] == 'STRING':
        value = expect(tokens, 'STRING', AI)
    # elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
    #     value = parse_function_call_in_variable_operations(tokens, AI,line_number, line_content)
    else:
        value = parse_arithmetic_expr(tokens, AI, line_number, line_content)

    return ('ASSIGN', var_name, value, line_number, line_content)

def parse_function_call_in_variable_operations(tokens, AI, line_number, line_content):
    func_name = expect(tokens, 'ID', AI)
    expect(tokens, 'LPAREN', AI)

    args = []
    while current_token(tokens)[0] != 'RPAREN':
        if current_token(tokens)[0] in ('NUMBER', 'ID', 'STRING','MINUS'):
            if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
                list_var = expect(tokens, 'ID', AI)
                expect(tokens, 'LBRACKET', AI)
                index = parse_arithmetic_expr(tokens, AI, line_number, line_content)
                expect(tokens, 'RBRACKET', AI)
                args.append(('LIST_ELEMENT', list_var, index))
            else:
                args.append(parse_arithmetic_expr(tokens, AI, line_number, line_content))
        else:
            error_message = f"Unexpected token {current_token(tokens)[0]} while parsing function arguments at {line_number}\nLine content: '{line_content}'"
            handle_error(error_message, AI)

        if current_token(tokens)[0] == 'COMMA':
            next_token(tokens)
        elif current_token(tokens)[0] != 'RPAREN':
            error_message = f"Expected RPAREN, got {current_token(tokens)[0]}"
            handle_error(error_message, AI)

    expect(tokens, 'RPAREN', AI)
    return ('FUNC_CALL', func_name, args)

def parse_standalone_increment_decrement_statement(tokens, AI, operator, line_number, line_content):
    next_token(tokens)  # Consume '++' or '--'
    if current_token(tokens)[0] == 'ID':
        var_name = expect(tokens, 'ID', AI)  # Expect an identifier (e.g., ++x)
        return (operator, var_name, line_number, line_content)
    else:
        # Error handling for missing variable after increment/decrement
        error_message = f"Expected a variable name after '{operator}' at {line_number}\nLine content: '{line_content.strip()}'"
        handle_error(error_message, AI)

# def parse_list_statement(tokens, AI, line_number, line_content):
#     if current_token(tokens)[0] == 'LBRACKET':  # Handle initialized list
#         expect(tokens, 'LBRACKET', AI)  # Expect '['
#         elements = []
#         while current_token(tokens)[0] != 'RBRACKET':  # Parse elements until ']'
#             element = parse_expr(tokens, AI,line_number,line_content)
#             elements.append(element)
#             if current_token(tokens)[0] == 'COMMA':  # Handle comma-separated elements
#                 next_token(tokens)  # Consume ','

#         expect(tokens, 'RBRACKET', AI)  # Expect ']'
#         return elements

#     else:
#         error_message = f"Expected '[' or '=' after list name at {line_number}\nLine content: '{line_content}'"
#         handle_error(error_message, AI)

def parse_list_statement(tokens, AI, line_number, line_content):
    def parse_list_elements():
        elements = []
        while current_token(tokens)[0] != 'RBRACKET':
            if current_token(tokens)[0] == 'LBRACKET':
                next_token(tokens)  # Consume '['
                nested_elements = parse_list_elements()  # Recursive call
                expect(tokens, 'RBRACKET', AI)
                elements.append(nested_elements)
            else:
                element = parse_expr(tokens, AI, line_number, line_content)
                elements.append(element)
            
            if current_token(tokens)[0] == 'COMMA':
                next_token(tokens)  # Consume ','
        
        return elements

    if current_token(tokens)[0] == 'LBRACKET':
        expect(tokens, 'LBRACKET', AI)

        elements = parse_list_elements()  # Use recursive list parser
        expect(tokens, 'RBRACKET', AI)
        return elements
    
    else:
        error_message = f"Expected '[' or '=' after list name at {line_number}\nLine content: '{line_content}'"
        handle_error(error_message, AI)
