import re
from flex_AI.useModel import *
from flex_tokenizer.tokens import TOKENS


def match_token(code, tok_type, regex):
    """
    Attempt to match a token type to the given code string using the specified regex.
    """
    regex_match = re.match(regex, code)
    if regex_match:
        return regex_match.group(0)
    return None

def handle_long_comment(match, line_number):
    """
    Update the line number for multi-line comments based on the number of newlines in the match.
    """
    return line_number + match.count('\n')

def handle_newline(line_number,last_code_line_index):
    """
    Increment the line number for a newline token.
    """
    if line_number <= last_code_line_index:
        return line_number + 1
    return line_number


def add_token(tokens, tok_type, match, line_number, code_lines, tok_number):
    """
    Add a valid token to the tokens list along with its metadata.
    """
    tokens.append((tok_type, match, f'line {line_number}', code_lines[line_number - 1]))
    return tok_number + 1

def handle_unmatched_comment(line_number, code_lines, code, AI):
    """
    Handle unmatched comment markers and report an error.
    """
    error_message = f"Unmatched long comment at line {line_number}: {code_lines[line_number - 1]}"
    handle_error(error_message, AI)

def handle_unknown_token(tokens, tok_number, line_number, code_lines, AI):
    """
    Handle unknown tokens and report an error.
    """
    tokens.append(('Unknown Type', 'No match', f'line {line_number}', code_lines[line_number - 1]))
    error_message = f"Unknown token: {tokens[tok_number + 1]}"
    handle_error(error_message, AI)

def tokenize(code, AI, model_name=None):
    """
    Tokenize the given code and return a list of tokens with their metadata.
    """
    tokens = []
    line_number = 1
    tok_number = -1
    code_lines = code.splitlines()  # Split code into lines for error reporting
    last_code_line_index = len(code_lines) - 1
    while last_code_line_index >= 0 and code_lines[last_code_line_index].strip() == "":
        last_code_line_index -= 1

    while code:
        match = None
        for tok_type, regex in TOKENS:
            match = match_token(code, tok_type, regex)
            if match:
                if tok_type == 'LONG_COMMENT':  # Handle multi-line comments
                    line_number = handle_long_comment(match, line_number)
                if tok_type not in ('SKIP', 'COMMENT', 'LONG_COMMENT'):  # Skip spaces, comments, and long comments
                    tok_number = add_token(tokens, tok_type, match, line_number, code_lines, tok_number)
                code = code[len(match):]  # Move past this token
                if tok_type == 'NEWLINE':  # Track newlines for line numbers
                    line_number = handle_newline(line_number,last_code_line_index)
                break
        
        if not match:
            # Check if the issue is an unmatched comment marker
            if code.startswith("'''") or code.startswith("/*"):
                handle_unmatched_comment(line_number, code_lines, code, AI)
            else:
                handle_unknown_token(tokens, tok_number, line_number, code_lines, AI)
    
    tokens.append(('EOF', 'EOF', f'line {line_number}',code_lines[line_number-1]))
    
    return tokens