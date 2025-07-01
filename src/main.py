import sys
import asyncio
import os
from flex_compiler.compiler import *
from utils import get_version
from flex_AI.useModel import ask_assistant

def show_help():
    """Display comprehensive help information for Flex compiler."""
    help_text = """
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
\033[96m                               🚀 FLEX COMPILER HELP                                \033[0m
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m

\033[93m📋 DESCRIPTION:\033[0m
    Flex is a bilingual programming language supporting both Franco Arabic and English syntax.
    The Flex compiler can compile and execute .flex and .lx files with optional AI assistance.

\033[93m🎯 BASIC USAGE:\033[0m
    \033[92mflex <source_file>\033[0m                        Execute a Flex program
    \033[92mflex <source_file> [OPTIONS]\033[0m              Execute with additional options

\033[93m📁 SUPPORTED FILE EXTENSIONS:\033[0m
    \033[94m.flex\033[0m                                     Mixed Franco/English syntax files
    \033[94m.lx\033[0m                                       Franco Arabic focused files

\033[93m⚙️  AVAILABLE OPTIONS:\033[0m

    \033[95m--help\033[0m                                    Show this help message and exit
    \033[95m--version\033[0m                                 Display Flex version information
    \033[95m--web\033[0m                                     Enable web-based features (experimental)
    \033[95m--ai\033[0m <model> <file>                       Enable AI-powered debugging assistance

\033[93m🤖 AI ASSISTANCE:\033[0m
    The \033[95m--ai\033[0m flag provides intelligent error analysis and debugging help.
    
    \033[94mUsage Patterns:\033[0m
    \033[92mflex --ai <model_name> <file.lx>\033[0m         AI assistance with specific model
    \033[92mflex --ai <file.lx>\033[0m                      AI assistance with default model
    
    \033[94mSupported Models:\033[0m
    • openai/gpt-4o-mini                    (Default, fast responses)
    • openai/gpt-4o                         (Advanced reasoning)
    • meta-llama/llama-3.3-70b-instruct     (Open source, powerful)
    • anthropic/claude-3.5-sonnet           (Excellent for code analysis)
    • And many more from OpenRouter
    
    \033[94mAI Features:\033[0m
    • \033[92mError-only analysis\033[0m                    Quick debugging for simple issues
    • \033[92mFull file context\033[0m                      Comprehensive program analysis
    • \033[92mInteractive retry options\033[0m              Multiple analysis approaches
    • \033[92mStructured solutions\033[0m                   Step-by-step fixes with explanations

\033[93m📋 USAGE EXAMPLES:\033[0m

    \033[94m# Basic execution\033[0m
    \033[92mflex hello.lx\033[0m                            Run a Flex program
    \033[92mflex calculator.flex\033[0m                     Run mixed syntax program
    
    \033[94m# AI-powered debugging\033[0m
    \033[92mflex --ai openai/gpt-4o my_program.lx\033[0m    Get AI help with specific model
    \033[92mflex --ai my_program.flex\033[0m                Get AI help with default model
    
    \033[94m# Web features (experimental)\033[0m
    \033[92mflex my_program.lx --web\033[0m                 Enable web functionality
    
    \033[94m# Version\033[0m
    \033[92mflex --version\033[0m                           Show version information

\033[93m🔧 ENVIRONMENT SETUP:\033[0m
    For AI features, set your OpenRouter API key:
    \033[94mexport OPENROUTER_API_KEY=your_api_key_here\033[0m
    
    Get your free API key at: \033[96mhttps://openrouter.ai\033[0m

\033[93m📚 FLEX LANGUAGE FEATURES:\033[0m
    • \033[92mBilingual syntax\033[0m                       Franco Arabic + English keywords
    • \033[92mNo semicolons required\033[0m                 Clean, readable code
    • \033[92mAutomatic type detection\033[0m               Smart type inference
    • \033[92mString interpolation\033[0m                   {variable} syntax support
    • \033[92mBuilt-in AI debugging\033[0m                  Integrated error assistance
    • \033[92mMixed syntax support\033[0m                   Use both languages in one file

\033[93m⚠️  COMMON ISSUES:\033[0m
    • \033[91mFranco l7d loops\033[0m                       Always use 'length(array) - 1' for safety
    • \033[91mUndefined variables\033[0m                    Declare before use
    • \033[91mFile not found\033[0m                         Check file path and extension
    • \033[91mAPI key missing\033[0m                        Set OPENROUTER_API_KEY for AI features

\033[93m🌐 RESOURCES:\033[0m
    • Documentation: \033[96mhttps://deepwiki.com/Flex-Language/Flex\033[0m
    • Examples: \033[96mhttps://github.com/Flex-Language/Flex_docs_examples\033[0m

\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
\033[96m                         🎉 Happy coding with Flex! 🎉                             \033[0m
\033[96m═══════════════════════════════════════════════════════════════════════════════════\033[0m
"""
    print(help_text)

def main():
    # Handle special command line arguments
    if len(sys.argv) == 1:
        # No arguments provided, show usage
        print("Usage: flex <source_file .lx,.flex> or flex --version")
        print("Use 'flex --help' for detailed help information")
        sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--version":
            print(get_version())
            sys.exit(0)
        elif sys.argv[1] == "--help":
            show_help()
            sys.exit(0)
        elif sys.argv[1] == "--web":
            print("Error: No source file provided when using --web flag")
            print("Usage: flex <source_file .lx,.flex> [--web] or flex --version")
            print("Use 'flex --help' for detailed help information")
            sys.exit(1)
        elif sys.argv[1] == "--ai":
            print("Error: No model name or source file provided when using --ai flag")
            print("Usage: flex --ai <model_name> <source_file .lx,.flex> or flex --version")
            print("Use 'flex --help' for detailed help information")
            sys.exit(1)
        # Process normal source file
        source_file = sys.argv[1]
        if not source_file:  # Empty string check
            print("Error: No source file provided")
            print("Usage: flex <source_file .lx,.flex> [--web] or flex --version")
            print("Use 'flex --help' for detailed help information")
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
        
        # Check for help flag first
        if '--help' in args:
            show_help()
            sys.exit(0)
        
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
                    print("Use 'flex --help' for detailed help information")
                    sys.exit(1)
            else:
                print("Error: No model name or source file provided when using --ai flag")
                print("Usage: flex --ai <model_name> <source_file .lx,.flex> or flex --version")
                print("Use 'flex --help' for detailed help information")
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
            print("Use 'flex --help' for detailed help information")
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
