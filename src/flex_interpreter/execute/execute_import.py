
from flex_tokenizer.tokenizer import *
import sys
import os
from flex_parser.parse import *
from flex_tokenizer.check_brace_matching import *
import flex_interpreter.glopal_vars as gv   
from flex_interpreter import execution   
from flex_AI.useModel import *

def execute_import(statement, AI, statements, import_list):
    """
    Execute an import statement to include code from a file or all valid files from a folder and its subfolders.
    Handles .lx and .txt files when a folder is provided.
    """
    if import_list not in gv.import_files and import_list is not None:
        gv.import_files.append(import_list)

    filename = statement[1]
    line_number, line_content = statement[2], statement[3]

    imported_statements = []  # Store imported statements

    if os.path.isdir(filename):  # Check if filename is a folder
        file_list = get_files_from_folder(filename)

        if not file_list:
            error_message = f"No valid .lx or .txt files found in folder '{filename}' at line {line_number}\nLine content: '{line_content.strip()}'"
            handle_error(error_message, AI)
            return

        for file in file_list:
            imported_statements.extend(import_file(file, AI))  # Import each file
    else:
        # Check if the filename includes an extension
        if '.' not in filename:
            error_message = f"File or folder '{filename}' does not have an extension. Please provide a valid file path or name with an extension."
            handle_error(error_message, AI)
            return

        imported_statements.extend(import_file(filename, AI))  # Import single file

    # Merge imported statements with the original ones
    all_statements = imported_statements + statements

    # Ensure unique imports
    for item in all_statements:
        if item[0] == 'IMPORT' and item[1] not in gv.import_files:
            gv.import_files.append(item[1])

    # Remove self-imports to avoid infinite loops
    all_statements = [
        item for item in all_statements
        if not (item[0] == 'IMPORT' and item[1] == filename)
    ]

    # Execute all statements after importing
    execution.run(all_statements, AI, insideFunc=False)
    sys.exit()  # Exit to prevent re-execution


def get_files_from_folder(folder):
    """
    Recursively get all .lx and .txt files inside a folder and its subfolders.
    """
    file_list = []
    for root, _, files in os.walk(folder):  # Walk through all subdirectories
        for file in files:
            if file.endswith('.lx') or file.endswith('.txt') or file.endswith('.fx') or file.endswith('.flex'):
                file_list.append(os.path.join(root, file))
    return file_list


def import_file(filename, AI):
    """
    Import a single file, tokenize it, parse it, and return statements.
    """
    try:
        with open(filename, 'r') as file:
            imported_code = file.read()

        # Tokenize and parse the imported code
        imported_tokens = tokenize(imported_code, AI)
        check_brace_matching(imported_tokens, AI)
        imported_statements = parse(imported_tokens, AI)

        # Filter functions and unique imports
        return [
            item for item in imported_statements
            if item[0] == 'FUN' or (item[0] == 'IMPORT' and item[1] not in gv.import_files)
        ]
    except FileNotFoundError:
        error_message = f"File '{filename}' not found."
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error importing file '{filename}': {str(e)}"
        handle_error(error_message, AI)
    
    return []  # Return empty list if an error occurs
