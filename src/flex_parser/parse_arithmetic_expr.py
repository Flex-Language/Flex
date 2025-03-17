from flex_AI.useModel import *
from flex_parser.parser_utils import *

def parse_arithmetic_expr(tokens, AI):
    left = parse_term(tokens, AI)  # Get the initial term
    while current_token(tokens)[0] in ('PLUS', 'MINUS'):  # While we see + or -
        operator = next_token(tokens)[1]  # Consume the operator
        right = parse_term(tokens, AI)  # Get the next term
        left = f"{left} {operator} {right}"  # Combine them into a single expression
    return left  # Return the complete expression

def parse_term(tokens, AI):
    """Parses terms, which may involve multiplication and division."""
    left = parse_primary(tokens, AI)  # Get the initial value
    while current_token(tokens)[0] in ('MULT', 'DIV'):  # While we see * or /
        operator = next_token(tokens)[1]  # Consume the operator
        right = parse_primary(tokens, AI)  # Get the next primary expression
        left = f"{left} {operator} {right}"  # Combine them into a single expression
    return left  # Return the complete term

def parse_primary(tokens, AI):
    """Parses primary expressions (numbers, IDs, or expressions in parentheses)."""
    if current_token(tokens)[0] == 'LPAREN':
        next_token(tokens)  # Consume '('
        expr = parse_arithmetic_expr(tokens, AI)  # Recursively parse the expression inside parentheses
        expect(tokens, 'RPAREN', AI)  # Expect and consume the closing ')'
        return f"({expr})"
    elif current_token(tokens)[0] == 'MINUS':
        return handle_minus(tokens, AI)  # Handle negative numbers
    elif current_token(tokens)[0] == 'ID':
        return parse_identifier_or_array(tokens, AI)
    elif current_token(tokens)[0] in ('NUMBER', 'ID', 'TRUE', 'FALSE', 'STRING'):
        return next_token(tokens)[1]  # Return the token value
    else:
        tok = current_token(tokens)
        error_message = f"Expected NUMBER, ID, or '(' at {tok[2]}, but got {tok[0]}\nLine content: '{tok[3]}'" # there is an bug here that it dont print the line content###################
        handle_error(error_message, AI)

def handle_minus(tokens, AI):
    """Handles multiple consecutive minus signs and ensures the next token is a NUMBER."""
    sign = 1  # Start with positive
    while current_token(tokens)[0] == 'MINUS':
        next_token(tokens)  # Consume the minus sign
        sign *= -1  # Flip the sign each time we encounter a minus
    if current_token(tokens)[0] != 'NUMBER':
        tok = current_token(tokens)
        error_message = f"Expected NUMBER after '-' at line {tok[2]}, but got {tok[0]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)
    return str(sign * int(next_token(tokens)[1]))  # Return the signed number

def parse_identifier_or_array(tokens, AI):
    """Parses identifiers and array indexing."""
    identifier = next_token(tokens)[1]  # Get the identifier
    if current_token(tokens)[0] == 'LBRACKET':  # Check for array indexing
        next_token(tokens)  # Consume '['
        index = parse_arithmetic_expr(tokens, AI)  # Parse the index expression
        expect(tokens, 'RBRACKET', AI)  # Expect and consume ']'
        return f"{identifier}[{index}]"
    return identifier
