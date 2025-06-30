import sys
import asyncio
import os
from flex_compiler.compiler import *
from utils import get_version
from flex_AI.useModel import ask_assistant

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
            print("Error: No model name or source file provided when using --ai flag")
            print("Usage: flex --ai <model_name> <source_file .lx,.flex> or flex --version")
            sys.exit(1)
        # Process normal source file
        source_file = sys.argv[1]
        if not source_file:  # Empty string check
            print("Error: No source file provided")
            print("Usage: flex <source_file .lx,.flex> [--web] or flex --version")
            sys.exit(1)
        AI = False
        WEB = False
        model_name = None
        try:
            compile_and_run(source_file, AI, WEB, model_name)
        except SyntaxError as e:
            # Catch the SyntaxError and print only the error message without the full traceback
            print(e)
        except ZeroDivisionError as z:
            print(z)
        except FileNotFoundError as f:
            print(f"Error: {f}")
            sys.exit(1)
    else:
        # Support: flex --ai <model_name> <file> or flex <file> --ai <model_name>
        AI = False
        WEB = False
        source_file = None
        model_name = None
        args = sys.argv[1:]
        
        if '--ai' in args:
            AI = True
            ai_index = args.index('--ai')
            
            # Check if a model name follows --ai
            if ai_index + 1 < len(args):
                if not args[ai_index + 1].startswith('--'):
                    # This could be either a model name or a source file
                    # Check if there's another argument after this one
                    if ai_index + 2 < len(args) and not args[ai_index + 2].startswith('--'):
                        # If there are two non-flag arguments after --ai, the first is model, second is file
                        model_name = args[ai_index + 1]
                        source_file = args[ai_index + 2]
                        # Remove --ai, model_name, and filename from args
                        del args[ai_index:ai_index+3]
                    else:
                        # Only one argument after --ai, assume it's the source file for backward compatibility
                        source_file = args[ai_index + 1]
                        # Remove --ai and filename from args
                        del args[ai_index:ai_index+2]
                else:
                    print("Error: No model name or source file provided when using --ai flag")
                    print("Usage: flex --ai <model_name> <source_file .lx,.flex> or flex --version")
                    sys.exit(1)
            else:
                print("Error: No model name or source file provided when using --ai flag")
                print("Usage: flex --ai <model_name> <source_file .lx,.flex> or flex --version")
                sys.exit(1)
                
            # Check if OpenRouter API key is set
            if not os.environ.get('OPENROUTER_API_KEY'):
                print("\033[91mError: OpenRouter API key not set. Please set the OPENROUTER_API_KEY environment variable.\033[0m")
                print("Example: export OPENROUTER_API_KEY=your_api_key_here")
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
            compile_and_run(source_file, AI, WEB, model_name)
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
