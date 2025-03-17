import sys
from flex_compiler.compiler import *

# Usage example
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    AI = False
    try:
        compile_and_run(source_file,AI)
    except SyntaxError as e:
        # Catch the SyntaxError and print only the error message without the full traceback
        print(e)
    except ZeroDivisionError as z:
        print(z)