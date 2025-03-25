import sys
from flex_compiler.compiler import *

# Usage example
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: flex <source_file .lx,.flex>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    AI = False
    WEB = False
    try:
        compile_and_run(source_file,AI,WEB)
    except SyntaxError as e:
        # Catch the SyntaxError and print only the error message without the full traceback
        print(e)
    except ZeroDivisionError as z:
        print(z)