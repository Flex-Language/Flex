
from flex_tokenizer.tokenizer import *
import sys
from flex_parser.parse import *
from flex_tokenizer.check_brace_matching import *
import flex_interpreter.glopal_vars as gv   
from flex_interpreter import execution   
from flex_AI.useModel import *

def execute_import(statement, AI, statements, import_list):
    """
    Execute an import statement to include code from a file and add functions to the global scope.
    Handles files with any extension and can take file names or locations.
    """
   
    
    if import_list not in gv.import_files and import_list != None:
        gv.import_files.append(import_list)
       
    filename = statement[1]
    line_number, line_content = statement[2], statement[3]

    # Check if the filename includes an extension
    if '.' not in filename:
        error_message = f"File '{filename}' does not have an extension. Please provide a valid file path or name with an extension."
        handle_error(error_message, AI)
        return

    try:
        with open(filename, 'r') as file:
            imported_code = file.read()
        
        # Tokenize and parse the imported code
        imported_tokens = tokenize(imported_code, AI)
        check_brace_matching(imported_tokens,AI)
        imported_statements = parse(imported_tokens, AI)
        

       
        filter_imported_statements = imported_statements
        filter_imported_statements = [
            item for item in filter_imported_statements
            if item[0] == 'FUN' or (item[0] == 'IMPORT' and item[1] not in gv.import_files)
        ]  # only get functions and unique imports
        
        all_statements = filter_imported_statements + statements
        
        for item in all_statements:
            if item[0] == 'IMPORT':
                if item[1] not in gv.import_files:
                    gv.import_files.append(item[1])
                     
        all_statements = [
            item for item in all_statements
            if not (item[0] == 'IMPORT' and item[1] == filename)
        ]  # remove import to avoid infinite loop
        
        # Execute the imported code with the original code
        execution.run(all_statements, AI, insideFunc=False)                               
        sys.exit()  # exit after done so you don't run again
        
    except FileNotFoundError:
        error_message = f"File '{filename}' not found at {line_number}\nLine content: '{line_content.strip()}'"
        handle_error(error_message, AI)
    except Exception as e:
        error_message = f"Error importing file '{filename}' at {line_number}: {str(e)}\nLine content: '{line_content.strip()}'"
        handle_error(error_message, AI)
