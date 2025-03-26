import sys
import asyncio
from flex_compiler.compiler import *
from utils import get_version

def main():
    # Handle special command line arguments
    if len(sys.argv) == 1:
        # No arguments provided, show usage
        print("Usage: flex <source_file .lx,.flex> or flex --version")
        sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--version":
            print(get_version())
            sys.exit(0)
        
        # Process normal source file
        source_file = sys.argv[1]
        if not source_file:  # Empty string check
            print("Error: No source file provided")
            print("Usage: flex <source_file .lx,.flex> or flex --version")
            sys.exit(1)
            
        AI = False
        WEB = False
        try:
            compile_and_run(source_file, AI, WEB)
        except SyntaxError as e:
            # Catch the SyntaxError and print only the error message without the full traceback
            print(e)
        except ZeroDivisionError as z:
            print(z)
        except FileNotFoundError as f:
            print(f"Error: {f}")
            sys.exit(1)
    else:
        print("Usage: flex <source_file .lx,.flex> or flex --version")
        sys.exit(1)

# Usage example
if __name__ == "__main__":
    main()