from flex_parser.parse_arithmetic_expr import *
from flex_parser.parser_utils import *
import  flex_parser.glopal_vars as gv
# from flex_parser.statement.parse_list import parse_list_assignment_statement

def parse_function_call_statement(tokens, AI, line_number, line_content):
    func_name = current_token(tokens)[1]
    next_token(tokens)  # Consume the function name
    expect(tokens, 'LPAREN', AI)  # Expect '('

    args = []
    while current_token(tokens)[0] != 'RPAREN':
        if current_token(tokens)[0] in ('NUMBER', 'ID', 'STRING','MINUS'):
                args.append(parse_arithmetic_expr(tokens, AI,line_number,line_content))  
        else:
            error_message = f"Unexpected token {current_token(tokens)[0]} while parsing function arguments at {line_number}\nLine content: '{line_content}'"
            handle_error(error_message, AI)

        if current_token(tokens)[0] == 'COMMA':
            next_token(tokens)  # Consume the comma
        elif current_token(tokens)[0] != 'RPAREN':
            error_message = f"Expected RPAREN, got {current_token(tokens)[0]} at {current_token(tokens)[2]}"
            handle_error(error_message, AI)

    expect(tokens, 'RPAREN', AI)  # Expect closing ')'
    # return func_name
    return ('FUNC_CALL', func_name, args, line_number, line_content,'*')

def parse_not_expression(tokens, AI, line_number, line_content):
    """Processes a 'not' expression from the tokens."""
    expect(tokens, 'NOT', AI)  # Consume 'not'
    if current_token(tokens)[0] == 'LPAREN':
        expect(tokens, 'LPAREN', AI)  # Consume '('
        inner_expr = parse_expr(tokens, AI,line_number,line_content)  # Recursively parse the inner expression
        expect(tokens, 'RPAREN', AI)  # Consume ')'
        return f"(not {inner_expr})"
    else:
        inner_expr = parse_expr(tokens, AI,line_number,line_content)  # Parse the inner expression
        return f"(not {inner_expr})"

def parse_list_access(tokens, AI, line_number, line_content):
    # """Processes a list access expression like x[3]."""
    # var_name = expect(tokens, 'ID', AI)  # Expect the list variable name
    # expect(tokens, 'LBRACKET', AI)  # Consume '['
    # index = parse_expr(tokens, AI,line_number,line_content)  # Parse the index expression
    # expect(tokens, 'RBRACKET', AI)  # Consume ']'
    # return f"{var_name}[{index}]"
    
    # """Processes a list access expression like x[3] or x[0][2]."""
    var_name = expect(tokens, 'ID', AI)  # Get the base variable name
    access_expr = var_name

    # Keep parsing nested list accesses like x[0][1][2]
    while gv.pos < len(tokens) and tokens[gv.pos][0] == 'LBRACKET':
        expect(tokens, 'LBRACKET', AI)
        index = parse_expr(tokens, AI, line_number, line_content)
        expect(tokens, 'RBRACKET', AI)
        access_expr = f"{access_expr}[{index}]"

    return access_expr

def parse_negative_number(tokens, AI, line_number, line_content):
    """Processes a negative number expression."""
    next_token(tokens)  # Consume '-'
    if current_token(tokens)[0] == 'NUMBER':
        return '-' + expect(tokens, 'NUMBER', AI)  # Prepend '-' to the number
    else:
        tok = current_token(tokens)
        error_message = f"Expected NUMBER after '-' at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)
        

def parse_right_side(tokens, AI, line_number, line_content):
    """Processes the right side of an operator expression."""
    if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
        return parse_list_access(tokens, AI,line_number, line_content)
    # else:
    #     return parse_arithmetic_expr(tokens, AI,line_number,line_content)
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
        return parse_function_call_statement(tokens, AI, line_number, line_content)
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] in ('PLUS', 'MINUS', 'DIV', 'MULT'):
        return parse_arithmetic_expr(tokens, AI,line_number,line_content) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
    elif current_token(tokens)[0] == 'ID':
        return expect(tokens, 'ID', AI)
    elif current_token(tokens)[0] == 'NUMBER' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] in ('PLUS', 'MINUS', 'DIV', 'MULT'):
        return parse_arithmetic_expr(tokens, AI,line_number,line_content) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
    elif current_token(tokens)[0] == 'MINUS':
        return parse_arithmetic_expr(tokens, AI,line_number,line_content) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
    elif current_token(tokens)[0] == 'NUMBER':
        return expect(tokens, 'NUMBER', AI)
    elif current_token(tokens)[0] == 'STRING':
        return expect(tokens, 'STRING', AI)
    elif current_token(tokens)[0] == 'TRUE':
        return expect(tokens, 'TRUE', AI)
    elif current_token(tokens)[0] == 'FALSE':
        return expect(tokens, 'FALSE', AI)
    elif current_token(tokens)[0] == 'MINUS':
        return parse_negative_number(tokens, AI,line_number,line_content)
    else:
        tok = current_token(tokens)
        error_message = f"Expected ID, NUMBER, BOOLEAN, or STRING at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)

def parse_operator_expression(tokens, AI, left, line_number, line_content):
    """Processes an operator expression with potential chaining."""
    if gv.pos < len(tokens) and current_token(tokens)[0] in ('GT', 'LT', 'EQ', 'NEQ', 'GE', 'LE'):
        op = next_token(tokens)[1]
        right = parse_right_side(tokens, AI, line_number, line_content)
        left = f"{left} {op} {right}"
        

        while gv.pos < len(tokens) and current_token(tokens)[0] in ('AND', 'OR'):
            op = next_token(tokens)[1]  # Consume 'and' or 'or'
            right = parse_expr(tokens, AI,line_number,line_content)  # Recursively parse the right side
            left = f"({left} {op} {right})"  # Combine the expressions

    if gv.pos < len(tokens) and current_token(tokens)[0] == 'NOT':
        next_token(tokens)  # Consume 'not'
        left = f"not {parse_expr(tokens, AI,line_number,line_content)}"  # Apply 'not' to the next expression

    return left

def parse_expr(tokens, AI, line_number, line_content):
    if current_token(tokens)[0] == 'NOT':
        return parse_not_expression(tokens, AI, line_number, line_content)
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
        left = parse_list_access(tokens, AI,line_number, line_content)
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
        left = parse_function_call_statement(tokens, AI, line_number, line_content)
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] in ('PLUS', 'MINUS', 'DIV', 'MULT'):
        left = parse_arithmetic_expr(tokens, AI,line_number,line_content) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
    elif current_token(tokens)[0] == 'ID':
        left = expect(tokens, 'ID', AI)
    elif current_token(tokens)[0] == 'STRING':
        left = expect(tokens, 'STRING', AI)
    elif current_token(tokens)[0] == 'NUMBER' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] in ('PLUS', 'MINUS', 'DIV', 'MULT'):
        return parse_arithmetic_expr(tokens, AI,line_number,line_content) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
    elif current_token(tokens)[0] == 'MINUS':
        return parse_arithmetic_expr(tokens, AI,line_number,line_content) if gv.pos < len(tokens) else None  # Parse the arithmetic expression
    elif current_token(tokens)[0] == 'NUMBER':
        left = expect(tokens, 'NUMBER', AI)
    elif current_token(tokens)[0] == 'TRUE':
        left = expect(tokens, 'TRUE', AI)
    elif current_token(tokens)[0] == 'FALSE':
        left = expect(tokens, 'FALSE', AI)
    elif current_token(tokens)[0] == 'MINUS':
        left = parse_negative_number(tokens, AI, line_number, line_content)
    else:
        if gv.forLoopFlag:
            return ('EMPTY_COND', line_number, line_content)
        tok = current_token(tokens)
        error_message = f"Expected ID, NUMBER, or BOOLEAN at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)
        
    return parse_operator_expression(tokens, AI, left, line_number, line_content)


def parse_karr_expr(tokens, AI, line_number, line_content):
    if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
        return parse_list_access(tokens, AI,line_number, line_content)
    elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
        return parse_function_call_statement(tokens, AI, line_number, line_content)
    elif current_token(tokens)[0] == 'ID':
        return expect(tokens, 'ID', AI)
    elif current_token(tokens)[0] == 'NUMBER':
        return expect(tokens, 'NUMBER', AI)
    elif current_token(tokens)[0] == 'MINUS':
        return parse_negative_number(tokens, AI, line_number, line_content)
    else:
        tok = current_token(tokens)
        error_message = f"Expected ID, NUMBER, or BOOLEAN at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)

