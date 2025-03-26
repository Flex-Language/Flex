import sys
import asyncio
from flex_compiler.compiler import *
from utils import checkFlexInstalled

async def main():
    # Check if Flex is installed
    flex_installed = await checkFlexInstalled()
    
    if not flex_installed:
        print("Warning: Flex interpreter not installed or not in PATH.")
        # Continue execution - this is just a warning
    
    if len(sys.argv) != 2:
        print("Usage: flex <source_file .lx,.flex>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    AI = False
    WEB = False
    try:
        compile_and_run(source_file, AI, WEB)
    except SyntaxError as e:
        # Catch the SyntaxError and print only the error message without the full traceback
        print(e)
    except ZeroDivisionError as z:
        print(z)

# Usage example
if __name__ == "__main__":
    asyncio.run(main())