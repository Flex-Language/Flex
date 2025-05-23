import requests
import json
import os
import sys

# Get the appropriate base directory path for relative file access
def get_base_dir():
    """
    Returns the appropriate base directory path based on whether
    the application is running as a bundled executable or not
    """
    # Check if the application is running as a bundled executable
    if getattr(sys, 'frozen', False):
        # If bundled with PyInstaller, use sys._MEIPASS
        base_dir = sys._MEIPASS
    else:
        # If running as a normal Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return base_dir

# Load flex example files
def load_flex_examples(debug_mode=False):
    """
    Load all example files from the data directories.
    Returns a string containing all the content concatenated.
    
    Args:
        debug_mode (bool): Whether to print debug information
    """
    examples = []
    base_dir = get_base_dir()
    
    # Define paths to individual example files - first try bundled path, then development path
    data_locations = [
        # PyInstaller bundled paths
        {
            "compiler_data_dir": os.path.join(base_dir, "flex_AI", "data", "Compiler_AI"),
            "ammar_data_dir": os.path.join(base_dir, "flex_AI", "data", "ammar_data")
        },
        # Development paths
        {
            "compiler_data_dir": os.path.join(base_dir, "data", "Compiler_AI"),
            "ammar_data_dir": os.path.join(base_dir, "data", "ammar_data")
        }
    ]
    
    # Try all possible locations for data files
    for location in data_locations:
        compiler_data_dir = location["compiler_data_dir"]
        ammar_data_dir = location["ammar_data_dir"]
        
        example_files = [
            os.path.join(compiler_data_dir, "data.txt"),
            os.path.join(ammar_data_dir, "total.txt")
        ]
        
        if debug_mode:
            debug_info = f"Searching for data files in: {compiler_data_dir} and {ammar_data_dir}"
            print(f"\033[94m{debug_info}\033[0m")  # blue debug message
        
        # Check if any files exist in this location
        files_found = False
        
        # Read each file and add its content to examples
        for file_path in example_files:
            try:
                with open(file_path, 'r') as file:
                    examples.append(file.read())
                    files_found = True
                    if debug_mode:
                        print(f"\033[92mFound and loaded: {file_path}\033[0m")  # green success
            except FileNotFoundError:
                if debug_mode:
                    print(f"\033[93mWarning: Could not find example file {file_path}\033[0m")  # yellow warning
        
        # If we found files in this location, no need to check other locations
        if files_found:
            break
    
    # Return concatenated content, or empty string if no examples were found
    if examples:
        return "\n\n".join(examples)
    else:
        if debug_mode:
            print("\033[93mWarning: No example files were found. AI responses may have limited Flex language knowledge.\033[0m")
        return ""

# Load the flex examples when module is imported
flex_data = load_flex_examples(debug_mode=False)

# Function to use OpenRouter API
def use_openrouter(prompt, model_name=None, api_key=None):
    """
    Use OpenRouter API to get a response from the specified model.
    
    Args:
        prompt (str): The prompt to send to the model
        model_name (str): The name of the OpenRouter model to use
        api_key (str): The OpenRouter API key
        
    Returns:
        str: The model's response
    """
    # Check if API key is provided or try to get from environment
    if not api_key:
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            error_message = "OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable."
            print(f"\033[91m{error_message}\033[0m")  # red
            sys.exit(1)
    
    # Set default model if none provided
    if not model_name:
        model_name = "openai/gpt-4.1-mini"  # Default model
    
    # API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://flex-language.org",  # Replace with your actual site
        "X-Title": "Flex Language"  # Replace with your application name
    }
    
    # Request payload with system prompt containing Flex language examples
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are an assistant for the Flex programming language. Here are examples of Flex code to help you understand the language syntax and features:\n\n" + flex_data},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the response
        result = response.json()
        
        # Extract and return the model's response
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            return message
        else:
            error_message = f"Unexpected response format from OpenRouter: {result}"
            print(f"\033[91m{error_message}\033[0m")  # red
            return f"Error: {error_message}"
            
    except requests.exceptions.RequestException as e:
        error_message = f"Error connecting to OpenRouter API: {str(e)}"
        print(f"\033[91m{error_message}\033[0m")  # red
        return f"Error: {error_message}"
    except json.JSONDecodeError:
        error_message = "Error parsing response from OpenRouter API"
        print(f"\033[91m{error_message}\033[0m")  # red
        return f"Error: {error_message}"
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(f"\033[91m{error_message}\033[0m")  # red
        return f"Error: {error_message}"

# Function to interact with the assistant (legacy OpenAI version)
def ask_assistant(prompt, model_name=None):
    """
    Process the prompt using either OpenAI (legacy) or OpenRouter based on model_name.
    
    Args:
        prompt (str): The prompt to send to the model
        model_name (str, optional): If provided, uses OpenRouter with this model
        
    Returns:
        None: Prints the response to console
    """
    if model_name:
        # Use OpenRouter with the specified model
        response = use_openrouter(prompt, model_name)
        print(f"\033[92m{response}\033[0m")  # green
    else:
        # Legacy OpenAI implementation would go here
        # For now, we'll just use OpenRouter with a default model
        response = use_openrouter(prompt)
        print(f"\033[92m{response}\033[0m")  # green



def handle_error(error_message, AI, model_name=None):
    """Handles errors based on the AI flag."""
    if (AI == True):
        print("\033[91m"+ error_message +"\033[0m")  # red
        
        # Import here to avoid circular imports
        import flex_interpreter.glopal_vars as gv
        
        # Use model_name parameter if provided, otherwise use global model_name
        if model_name:
            ask_assistant(error_message, model_name)
        elif gv.model_name:
            ask_assistant(error_message, gv.model_name)
        else:
            # Use default model if no specific model is provided
            ask_assistant(error_message)
            
        raise SyntaxError("\033[92m"+ "Flex AI :)" +"\033[0m") # green
    else:
        raise SyntaxError("\033[91m"+ error_message +"\033[0m") # red

