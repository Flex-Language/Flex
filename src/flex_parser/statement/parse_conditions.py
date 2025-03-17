from flex_parser.parser_utils import *
from flex_parser.parse_block import *
from flex_parser.parse_expr import *

def parse_if_statement(tokens, AI, line_number, line_content):
    """Parses an if statement."""
    next_token(tokens)  # Consume 'if'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete if statement at end of input

    expect(tokens, 'LPAREN', AI)  # Expect '(' after 'if'
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle missing ')'

    expect(tokens, 'RPAREN', AI)  # Expect closing ')'
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)

    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('IF_BLOCK', condition, block, line_number, line_content)

def parse_lw_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'if'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete if statement at end of input
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('IF_BLOCK', condition, block, line_number, line_content)

def parse_elif_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'elif'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete if statement at end of input
    expect(tokens, 'LPAREN', AI)  # Expect '(' after 'if'
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle missing ')'
    expect(tokens, 'RPAREN', AI)  # Expect closing ')'
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('ELIF_BLOCK', condition, block, line_number, line_content)

def parse_aw_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'elif'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete if statement at end of input
    condition = parse_expr(tokens, AI,line_number,line_content)  # Parse the condition inside the parentheses
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('ELIF_BLOCK', condition, block, line_number, line_content)

def parse_else_statement(tokens, AI, line_number, line_content):
    next_token(tokens)  # Consume 'else'
    if current_token(tokens)[0] == 'EOF':
        return None  # Gracefully handle incomplete if statement at end of input
    if current_token(tokens)[0] == 'NEWLINE':
        next_token(tokens)
    block = parse_block(tokens, AI)  # Parse the block of statements
    return ('ELSE_BLOCK', None, block, line_number, line_content)
