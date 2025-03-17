from flex_AI.useModel import *

def check_brace_matching(tokens,AI): 
    brace_stack = []
    
    for i, token in enumerate(tokens):
        token_type, token_value, line_number, line_content = token  # Unpack all four values
        
        if token_type == 'LBRACE':
            # Push opening brace onto the stack
            brace_stack.append(token)
        
        elif token_type == 'RBRACE':
            # Pop from the stack when a closing brace is found
            if not brace_stack:
                # If there's no matching opening brace
                error_message = f"Unmatched closing brace '}}' at {line_number}\nLine content: {line_content}"
                handle_error(error_message, AI)
            brace_stack.pop()
    
    # After the loop, if there are unmatched opening braces
    if brace_stack:
        unmatched_token = brace_stack[-1]
        error_message = f"Unmatched opening brace '{{' found at {unmatched_token[2]}\nLine content: {unmatched_token[3]}"
        handle_error(error_message, AI)
        