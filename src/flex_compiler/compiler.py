
from flex_tokenizer.tokenizer import *
from flex_tokenizer.check_brace_matching import *
from flex_parser.parse import *
from flex_interpreter import execution

def compile_and_run(file_path,AI,WEB):
    import_list =[]
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        import_list.append(file_path)    
        # Tokenize the code
        tokens = tokenize(code,AI)
       
        # Parse the code
        check_brace_matching(tokens,AI)
        parsed_statements = parse(tokens,AI)
        # for i in parsed_statements:
        #     print(i)
       
       
        # Move the 'IMPORT' statement to the beginning
        import_stmt = [stmt for stmt in parsed_statements if stmt[0] == 'IMPORT']
        other_stmts = [stmt for stmt in parsed_statements if stmt[0] != 'IMPORT']

        # Combine the lists with 'IMPORT' first
        re_parsed_statements = import_stmt + other_stmts
        # Run the interpreter
        execution.run(re_parsed_statements,AI,WEB,import_list=import_list)
    
    except NameError as e:
        print(e)  # Only print the error message, no traceback
    except SyntaxError as s:
        # Catch the SyntaxError and print only the error message without the full traceback
        print(s)
    except ZeroDivisionError as z:
        print(z)
    except StopIteration as stop:
        print()
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle other exceptions gracefully without traceback