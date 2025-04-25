import  flex_parser.glopal_vars as gv
from flex_parser import parse_statement
from flex_parser.parser_utils import *
from flex_parser.parse_block import *
from flex_parser.parse_expr import *
from flex_parser.parse_arithmetic_expr import *

def parse_while_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'while'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete while statement at end of input
    expect(tokens, 'LPAREN', AI)  # Expect '(' after 'while'
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle missing ')'
    expect(tokens, 'RPAREN', AI)  # Expect closing ')'
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('WHILE', condition, block, line_number, line_content)

def parse_talama_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'while'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete while statement at end of input
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('WHILE', condition, block, line_number, line_content)

def parse_for_statement(tokens, AI, line_number, line_content):
   
    gv.forLoopFlag = True
    next_token(tokens)  # Consume 'for'
    expect(tokens, 'LPAREN', AI)  # Expect '(' after 'for'

    # Parse initialization (e.g., i = 0)
    init_statement = parse_statement.parse_statement(tokens, AI)
    
    if (init_statement != None and init_statement[0] == 'STANDALONE_VAR'):
        pass
    else:
        expect(tokens, 'SEMICOLON', AI)  # Expect ';' after initialization

    # Parse condition (e.g., i < 10)
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    
    expect(tokens, 'SEMICOLON', AI)  # Expect ';' after condition

    # Parse increment (e.g., i++)
    increment_statement = parse_statement.parse_statement(tokens, AI)
   
    expect(tokens, 'RPAREN', AI)  # Expect ')' after increment

    # Parse block of code inside the for loop
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements

    gv.forLoopFlag = False
    return ('FOR', init_statement, condition, increment_statement, block, line_number, line_content)

def parse_repeat_statement(tokens, AI, line_number, line_content):
    
    gv.forLoopFlag = True
    gv.karrFlag=True
    next_token(tokens)  # Consume 'karr'
    # Parse initialization (e.g., i = 0)
    if (current_token(tokens)[0] != 'UNTILL'):
        init_statement = parse_statement.parse_statement(tokens, AI)
        if (init_statement != None and init_statement[0] == 'STANDALONE_VAR'):
            pass
        else:
            expect(tokens, 'UNTILL', AI)  # Expect ';' after condition
        # Parse increment (e.g., i++)
    else:
        init_statement = None
        expect(tokens, 'UNTILL', AI)
    number = parse_karr_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses

    # Parse block of code inside the for loop
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    gv.forLoopFlag = False
    return ('KARR', init_statement, number, block, line_number, line_content)

def parse_break_statement(tokens, line_number, line_content):
    next_token(tokens)  # Consume 'break'
    return ('BREAK', line_number, line_content)

def parse_return_statement(tokens, AI, line_number, line_content):
    """Parses a return statement."""
    expect(tokens, 'RETURN', AI)  # Consume 'return'
    if gv.pos < len(tokens) and current_token(tokens)[0] not in ('NEWLINE', 'RBRACE'):
        return_value = parse_arithmetic_expr(tokens, AI,line_number,line_content)  # Parse the return value
    else:
        return_value = None  # No expression to return
    return ('RETURN', return_value, line_number, line_content)
