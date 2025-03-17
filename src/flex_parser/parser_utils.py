from flex_AI.useModel import *
import flex_parser.glopal_vars as gv

def next_token(tokens):
    
    if gv.pos < len(tokens):
        gv.pos += 1
        return tokens[gv.pos - 1]
    else:
        return ('EOF', '', '', '')  # Return an EOF-like token if we run out of tokens

def current_token(tokens):
    
    if gv.pos < len(tokens):
        return tokens[gv.pos]
    else:
        return ('EOF', '', '', '')  # Return an EOF-like token if we are out of bounds

def expect(tokens, tok_type,AI):
    
    if gv.pos >= len(tokens):
        # End of input reached without the expected token; handle gracefully
        return None
    tok = next_token(tokens)
    if tok[0] != tok_type:
        error_message = f"Expected {tok_type}, got {tok[0]} at {tok[2]}\nLine content: '{tok[3]}'"
        handle_error(error_message, AI)
    return tok[1]



def skip_newlines(tokens):
    """Skips over newline tokens to reach meaningful tokens."""
    
    while gv.pos < len(tokens):
        if current_token(tokens)[0] == 'NEWLINE':
            next_token(tokens)
        else:
            break
