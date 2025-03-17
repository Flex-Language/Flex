
from flex_parser.parser_utils import *
from flex_parser import parse_statement 
import  flex_parser.glopal_vars as gv

def validate_opening_brace(tokens, AI):
    """Validates the presence of an opening brace '{'."""
    if current_token(tokens)[0] != 'LBRACE':
        tok = current_token(tokens)
        error_message = f"Expected opening brace '{{' at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)
    expect(tokens, 'LBRACE', AI)  # Consume the opening '{'

def validate_closing_brace(tokens, AI):
    """Validates the presence of a closing brace '}'."""
    if gv.pos >= len(tokens) or current_token(tokens)[0] != 'RBRACE':
        tok = current_token(tokens)
        error_message = f"Missing closing brace '}}' at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)
    expect(tokens, 'RBRACE', AI)  # Consume the closing '}'

def parse_statements_in_block(tokens, AI):
    """Parses all statements inside a block."""
    statements = []
    while gv.pos < len(tokens):
        current_tok_type = current_token(tokens)[0]

        # Exit block if a matching closing brace '}' is found
        if current_tok_type == 'RBRACE':
            break

        # Parse individual statements and add to the list
        statement = parse_statement.parse_statement(tokens, AI)
        if statement:
            statements.append(statement)

    return statements
  
def parse_block(tokens,AI):
    """Parses a block of code enclosed in { }."""
    statements = []

    validate_opening_brace(tokens, AI)

    # Parse statements inside the block
    statements = parse_statements_in_block(tokens, AI)

    validate_closing_brace(tokens, AI)

    return statements
    