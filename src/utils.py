import subprocess
import asyncio
import sys
import os

def get_version():
    return "Flex Language 1.0.0"

async def execAsync(command, timeout=None):
    """
    Execute a command asynchronously.
    
    Args:
        command (str): The command to execute
        timeout (int, optional): Timeout in seconds
        
    Returns:
        dict: Command execution results
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        return {
            'stdout': stdout.decode().strip(),
            'stderr': stderr.decode().strip(),
            'code': process.returncode
        }
    except asyncio.TimeoutError:
        process.kill()
        raise TimeoutError(f"Command timed out after {timeout} seconds")

async def checkFlexInstalled():
    try:
        # Try to run 'flex --version' to check if it's installed
        result = await execAsync('flex --version', timeout=2)
        print('Flex interpreter found:', result['stdout'])
        return True
    except Exception as error:
        print('Flex interpreter not found:', str(error))
        return False 