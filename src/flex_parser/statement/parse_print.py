import  flex_parser.glopal_vars as gv
from flex_parser.parser_utils import *
from flex_parser.parse_arithmetic_expr import *
from flex_parser.statement.parse_function import parse_function_call_statement


def parse_print_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'print'
    if current_token(tokens)[0] == 'EOF':
        return (line_number, line_content)  # Gracefully handle missing '(' after print
    expect(tokens, 'LPAREN', AI)
    if current_token(tokens)[0] == 'ID' and tokens[gv.pos + 1][0] == 'LBRACKET':
        message = parse_arithmetic_expr(tokens, AI, line_number, line_content)  # Handle list access, e.g., print(x[2])
        # Handle list access, e.g., print(x[2])
    elif current_token(tokens)[0] == 'ID' and tokens[gv.pos + 1][0] == 'LPAREN':
        func_name = current_token(tokens)[1]
        next_token(tokens)  # Consume the function name
        expect(tokens, 'LPAREN', AI)  # Expect the '(' after the function name

        # Parse function arguments
        args = []
        while current_token(tokens)[0] != 'RPAREN':
            if current_token(tokens)[0] == 'COMMA':  # Skip commas
                next_token(tokens)
                continue
            if current_token(tokens)[0] in ('NUMBER', 'ID', 'STRING', 'MINUS'):
                args.append(parse_arithmetic_expr(tokens, AI, line_number, line_content))  # Parse the argument
            else:
                handle_error(f"Invalid argument in function call: {current_token(tokens)}", AI)
        expect(tokens, 'RPAREN', AI)  # Expect closing ')'
        message = ('FUNC_CALL', func_name, args)
    elif current_token(tokens)[0] in ('NUMBER', 'ID', 'MINUS'):
        message = parse_arithmetic_expr(tokens, AI,line_number,line_content)  # Parse the arithmetic expression
    else:
        message = expect(tokens, 'STRING', AI)  # Fallback to string if not an expression
    if current_token(tokens)[0] == 'EOF':
        return (line_number, line_content)  # Gracefully handle missing ')'
    expect(tokens, 'RPAREN', AI)

    return ('PRINT', message, line_number, line_content)
