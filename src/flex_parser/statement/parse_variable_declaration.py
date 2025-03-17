import  flex_parser.glopal_vars as gv
from flex_parser.parser_utils import *
from flex_parser.parse_arithmetic_expr import *

def parse_variable_type_in_variable_declaration(tokens, AI, line_number, line_content):
    # Consume type (e.g., int, float, bool)
    var_type = next_token(tokens)[0]
    if current_token(tokens)[0] == 'EOF':
        error_message = f"Missing variable name after type '{var_type}' at {line_number}\nLine content: '{line_content}'"
        handle_error(error_message, AI)
    return var_type

def parse_variable_name_in_variable_declaration(tokens, AI, line_number, line_content):
    # Expect and consume variable name
    if current_token(tokens)[0] != 'ID':
        error_message = f"Expected variable name after type at {line_number}\nLine content: '{line_content}'"
        handle_error(error_message, AI)
    return expect(tokens, 'ID', AI)

def parse_assignment_in_variable_declaration(tokens, AI):
    # Handle assignment logic (e.g., '=', list, scan, string, function call, or expression)
    if current_token(tokens)[0] == 'ASSIGN':
        expect(tokens, 'ASSIGN', AI)  # Consume '='
        if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
            value = parse_arithmetic_expr(tokens, AI)  # Parse list element
        elif current_token(tokens)[0] == 'SCAN':
            value = parse_scan_in_variable_declaration(tokens, AI)
        elif current_token(tokens)[0] == 'STRING':
            value = expect(tokens, 'STRING', AI)
        elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
            value = parse_func_call_in_variable_declaration(tokens, AI)
        else:
            value = parse_arithmetic_expr(tokens, AI) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
        return value
    return None

def parse_scan_in_variable_declaration(tokens, AI):
    # Handle scan statement
    expect(tokens, 'SCAN', AI)
    expect(tokens, 'LPAREN', AI)
    expect(tokens, 'RPAREN', AI)
    return "scan_now"

def parse_func_call_in_variable_declaration(tokens, AI):
    # Handle function call with arguments
    func_name = expect(tokens, 'ID', AI)  # Get the function name
    expect(tokens, 'LPAREN', AI)  # Consume '('

    args = []
    while current_token(tokens)[0] != 'RPAREN':  # Continue until closing parenthesis
        if current_token(tokens)[0] in ('NUMBER', 'ID', 'STRING'):
            if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
                args.append(parse_arithmetic_expr(tokens, AI))
            else:
                args.append(parse_arithmetic_expr(tokens, AI))  # Parse a simple argument
        else:
            error_message = f"Unexpected token {current_token(tokens)[0]} while parsing function arguments"
            handle_error(error_message, AI)
        
        if current_token(tokens)[0] == 'COMMA':
            next_token(tokens)  # Consume the comma and continue to next argument
        elif current_token(tokens)[0] != 'RPAREN':
            error_message = f"Expected RPAREN, got {current_token(tokens)[0]}"
            handle_error(error_message, AI)
    
    expect(tokens, 'RPAREN', AI)  # Consume the closing ')'
    return ('FUNC_CALL', func_name, args)

def parse_variable_declaration_statement(tokens, AI, line_number, line_content):
    # Step 1: Parse the variable type
    var_type = parse_variable_type_in_variable_declaration(tokens, AI, line_number, line_content)
    
    # Step 2: Parse variable names and optional assignments
    variables = []
    while True:
        var_name = parse_variable_name_in_variable_declaration(tokens, AI, line_number, line_content)
        
        # Check if there's an assignment
        value = None
        if current_token(tokens)[0] == 'ASSIGN':  # '=' token
            # expect(tokens, 'ASSIGN', AI)  # Consume '='
            value = parse_assignment_in_variable_declaration(tokens, AI)
        
        # Store the parsed variable
        variables.append((var_name, value))
        
        # Check if there are more variables separated by commas
        if current_token(tokens)[0] == 'COMMA':  # ',' token
            expect(tokens, 'COMMA', AI)  # Consume ','
        else:
            break  # Exit loop if no more variables
    
    # Step 3: Ensure the statement ends properly
    if current_token(tokens)[0] not in {'NEWLINE', 'EOF'}:
        error_message = f"Unexpected token in variable declaration at {line_number}\nLine content: '{line_content.strip()}'"
        handle_error(error_message, AI)
    
    # Step 4: Return parsed variable declaration
    return ('VAR_DECL', var_type, variables, line_number, line_content)


