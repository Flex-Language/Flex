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
        elif sys.argv[1] == "--web":
            print("Error: No source file provided when using --web flag")
            print("Usage: flex <source_file .lx,.flex> [--web] or flex --version")
            sys.exit(1)
        elif sys.argv[1] == "--ai":
            print("Error: No source file provided when using --ai flag")
            print("Usage: flex --ai <source_file .lx,.flex> or flex --version")
            sys.exit(1)
        # Process normal source file
        source_file = sys.argv[1]
        if not source_file:  # Empty string check
            print("Error: No source file provided")
            print("Usage: flex <source_file .lx,.flex> [--web] or flex --version")
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
        # Support: flex --ai <file> or flex <file> --ai
        AI = False
        WEB = False
        source_file = None
        args = sys.argv[1:]
        if '--ai' in args:
            AI = True
            ai_index = args.index('--ai')
            # Check if a filename follows --ai
            if ai_index + 1 < len(args) and not args[ai_index + 1].startswith('--'):
                source_file = args[ai_index + 1]
                # Remove --ai and filename from args
                del args[ai_index:ai_index+2]
            else:
                print("Error: No source file provided when using --ai flag")
                print("Usage: flex --ai <source_file .lx,.flex> or flex --version")
                sys.exit(1)
        # If not set by --ai, look for first non-flag as source_file
        if source_file is None:
            for arg in args:
                if not arg.startswith('--'):
                    source_file = arg
                    break
        # Process additional flags
        for arg in args:
            if arg == "--web":
                WEB = True
            # Add other flags as needed
        if not source_file:
            print("Error: No source file provided")
            print("Usage: flex <source_file .lx,.flex> [--web] or flex --version")
            sys.exit(1)
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

# Usage example
if __name__ == "__main__":
    main()