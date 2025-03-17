from flex_parser.parser_utils import *

def parse_import_statement(tokens, AI, line_number, line_content):
    """
    Parse an import statement, e.g., 'geeb filename.txt'.
    """
    next_token(tokens)  # Consume 'geeb'
    if current_token(tokens)[0] != 'STRING':
        error_message = f"Expected a string (filename) after 'geeb' at {line_number}\nLine content: '{line_content.strip()}'"
        handle_error(error_message, AI)

    filename = current_token(tokens)[1].strip('"')  # Extract filename
    next_token(tokens)  # Consume the filename token
    return ('IMPORT', filename, line_number, line_content)
