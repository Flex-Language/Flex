from flex_AI.useModel import *
from flex_parser.parser_utils import *

def parse_arithmetic_expr(tokens, AI, line_number, line_content):
    left = parse_term(tokens, AI,line_number,line_content)  # Get the initial term
    while current_token(tokens)[0] in ('PLUS', 'MINUS'):  # While we see + or -
        operator = next_token(tokens)[1]  # Consume the operator
        right = parse_term(tokens, AI,line_number,line_content)  # Get the next term
        left = f"{left} {operator} {right}"  # Combine them into a single expression
    return left  # Return the complete expression

def parse_term(tokens, AI, line_number, line_content):
    """Parses terms, which may involve multiplication and division."""
    left = parse_primary(tokens, AI,line_number,line_content)  # Get the initial value
    while current_token(tokens)[0] in ('MULT', 'DIV'):  # While we see * or /
        operator = next_token(tokens)[1]  # Consume the operator
        right = parse_primary(tokens, AI,line_number,line_content)  # Get the next primary expression
        left = f"{left} {operator} {right}"  # Combine them into a single expression
    return left  # Return the complete term

def parse_primary(tokens, AI, line_number, line_content):
    """Parses primary expressions (numbers, IDs, or expressions in parentheses)."""
    if current_token(tokens)[0] == 'LPAREN':
        next_token(tokens)  # Consume '('
        expr = parse_arithmetic_expr(tokens, AI,line_number,line_content)  # Recursively parse the expression inside parentheses
        expect(tokens, 'RPAREN', AI)  # Expect and consume the closing ')'
        return f"({expr})"
    elif current_token(tokens)[0] == 'MINUS':
        return handle_minus(tokens, AI,line_number,line_content)  # Handle negative numbers
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
        return parse_function_call_in_variable_operations(tokens, AI,line_number, line_content)
    elif current_token(tokens)[0] == 'ID':
        return parse_identifier_or_array(tokens, AI,line_number,line_content)  # Handle identifiers and array indexing
    elif current_token(tokens)[0] in ('NUMBER', 'ID', 'TRUE', 'FALSE', 'STRING'):
        return next_token(tokens)[1]  # Return the token value
    else:
        tok = current_token(tokens)
        error_message = f"Expected NUMBER, ID, or '(' at {tok[2]}, but got {tok[0]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)

def handle_minus(tokens, AI, line_number, line_content):
    """Handles multiple consecutive minus signs and ensures the next token is a NUMBER."""
    sign = 1  # Start with positive
    while current_token(tokens)[0] == 'MINUS':
        next_token(tokens)  # Consume the minus sign
        sign *= -1  # Flip the sign each time we encounter a minus
    if current_token(tokens)[0] != 'NUMBER':
        tok = current_token(tokens)
        error_message = f"Expected NUMBER after '-' at line {line_number}, but got {tok[0]}\nLine content: '{line_content}'"
        handle_error(error_message, AI)
    return str(sign * int(next_token(tokens)[1]))  # Return the signed number

def parse_identifier_or_array(tokens, AI, line_number, line_content):
    """Parses identifiers and array indexing."""
    identifier = next_token(tokens)[1]  # Get the identifier
    if current_token(tokens)[0] == 'LBRACKET':  # Check for array indexing
        indices = []
        while current_token(tokens)[0] == 'LBRACKET':
            expect(tokens, 'LBRACKET', AI)
            index = parse_arithmetic_expr(tokens, AI, line_number, line_content)
            expect(tokens, 'RBRACKET', AI)
            indices.append(index)
        id_str=f"{identifier}"
        for i in indices:
            id_str+=f"[{i}]"
        return id_str
    
    return identifier

def parse_function_call_in_variable_operations(tokens, AI, line_number, line_content):
    func_name = expect(tokens, 'ID', AI)
    expect(tokens, 'LPAREN', AI)

    args = []
    while current_token(tokens)[0] != 'RPAREN':
        if current_token(tokens)[0] in ('NUMBER', 'ID', 'STRING','MINUS'):
            if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
                list_var = expect(tokens, 'ID', AI)
                expect(tokens, 'LBRACKET', AI)
                index = parse_arithmetic_expr(tokens, AI,line_number,line_content)
                expect(tokens, 'RBRACKET', AI)
                args.append(('LIST_ELEMENT', list_var, index))
            else:
                args.append(parse_arithmetic_expr(tokens, AI,line_number,line_content))
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
    # return f"{func_name}({', '.join(map(str, args))})"  # Return the function call as a string
