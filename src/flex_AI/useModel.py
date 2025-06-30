import requests
import json
import os
import sys
import shutil  # For terminal size detection
import textwrap  # For text wrapping
import re  # For ANSI code handling

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

# Load optimized Flex system prompt
def load_flex_system_prompt(debug_mode=False):
    """
    Load the optimized flex_language_spec.json system prompt.
    Falls back to legacy text examples if JSON not found.
    
    Args:
        debug_mode (bool): Whether to print debug information
        
    Returns:
        str: The system prompt content
    """
    base_dir = get_base_dir()
    
    # Try to load the optimized JSON system prompt first
    json_locations = [
        # PyInstaller bundled path
        os.path.join(base_dir, "flex_AI", "flex_language_spec.json"),
        # Development path
        os.path.join(base_dir, "flex_language_spec.json"),
        # Alternative paths
        os.path.join(os.path.dirname(base_dir), "flex_AI", "flex_language_spec.json")
    ]
    
    for json_path in json_locations:
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                spec_data = json.load(file)
                
                if debug_mode:
                    print(f"\033[92mLoaded optimized Flex system prompt from: {json_path}\033[0m")
                
                # Build the enhanced system prompt
                return build_enhanced_system_prompt(spec_data)
                
        except FileNotFoundError:
            if debug_mode:
                print(f"\033[93mOptimized prompt not found at: {json_path}\033[0m")
            continue
        except json.JSONDecodeError as e:
            if debug_mode:
                print(f"\033[91mError parsing JSON at {json_path}: {e}\033[0m")
            continue
    
    # Fallback to legacy examples if JSON not found
    if debug_mode:
        print("\033[93mFalling back to legacy text examples...\033[0m")
    
    return "You are an assistant for the Flex programming language. " + load_flex_examples_legacy(debug_mode)

def build_enhanced_system_prompt(spec_data):
    """
    Build an enhanced system prompt from the loaded JSON specification.
    
    Args:
        spec_data (dict): The loaded flex_language_spec.json data
        
    Returns:
        str: Enhanced system prompt
    """
    prompt_parts = []
    
    # Add AI instructions if available
    if "ai_system_prompt" in spec_data:
        ai_prompt = spec_data["ai_system_prompt"]
        
        prompt_parts.append(f"ROLE: {ai_prompt.get('role', 'Flex Programming Assistant')}")
        prompt_parts.append(f"DESCRIPTION: {ai_prompt.get('description', '')}")
        
        # Add critical instructions
        if "CRITICAL_INSTRUCTIONS" in ai_prompt:
            prompt_parts.append("\n=== CRITICAL INSTRUCTIONS ===")
            for key, instruction in ai_prompt["CRITICAL_INSTRUCTIONS"].items():
                prompt_parts.append(f"• {key}: {instruction}")
        
        # Add instant reference
        if "INSTANT_REFERENCE" in ai_prompt:
            prompt_parts.append("\n=== INSTANT REFERENCE ===")
            for key, syntax in ai_prompt["INSTANT_REFERENCE"].items():
                prompt_parts.append(f"• {key}: {syntax}")
    
    # Add essential knowledge
    if "ESSENTIAL_FLEX_KNOWLEDGE" in spec_data:
        essential = spec_data["ESSENTIAL_FLEX_KNOWLEDGE"]
        prompt_parts.append(f"\n=== ESSENTIAL KNOWLEDGE ===")
        prompt_parts.append(f"Language: {essential.get('language_identity', 'Flex')}")
        prompt_parts.append(f"Philosophy: {essential.get('core_philosophy', '')}")
        
        if "unique_features" in essential:
            prompt_parts.append("Key Features: " + ", ".join(essential["unique_features"]))
    
    # Add critical syntax patterns
    if "CRITICAL_SYNTAX_PATTERNS" in spec_data:
        patterns = spec_data["CRITICAL_SYNTAX_PATTERNS"]
        prompt_parts.append("\n=== SYNTAX PATTERNS ===")
        
        if "mixed_declaration_styles" in patterns:
            styles = patterns["mixed_declaration_styles"]
            prompt_parts.append(f"Franco: {styles.get('franco', '')}")
            prompt_parts.append(f"English: {styles.get('english', '')}")
    
    # Add common error solutions
    if "COMMON_ERROR_SOLUTIONS" in spec_data:
        prompt_parts.append("\n=== COMMON ERROR SOLUTIONS ===")
        for error, solution in spec_data["COMMON_ERROR_SOLUTIONS"].items():
            prompt_parts.append(f"• {error}: {solution}")
    
    return "\n".join(prompt_parts)

# Legacy function for backward compatibility
def load_flex_examples_legacy(debug_mode=False):
    """
    Legacy function to load example files (for backward compatibility).
    
    Args:
        debug_mode (bool): Whether to print debug information
        
    Returns:
        str: Example content or empty string
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
        return "Here are examples of Flex code:\n\n" + "\n\n".join(examples)
    else:
        if debug_mode:
            print("\033[93mWarning: No example files were found. AI responses may have limited Flex language knowledge.\033[0m")
        return "Here are the core Flex language features you should know about."

# Load the optimized flex system prompt when module is imported
flex_system_prompt = load_flex_system_prompt(debug_mode=False)

# Legacy compatibility - keep this for existing code that might reference it
def load_flex_examples(debug_mode=False):
    """Legacy function - redirects to new system"""
    return load_flex_examples_legacy(debug_mode)

flex_data = load_flex_examples_legacy(debug_mode=False)  # For backward compatibility

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
        model_name = "openai/gpt-4o-mini"  # Default model
    
    # API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://flex-language.org",  # Replace with your actual site
        "X-Title": "Flex Language"  # Replace with your application name
    }
    
    # Request payload with optimized Flex system prompt
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": flex_system_prompt},
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

def get_terminal_width():
    """Get the current terminal width with fallback for different environments."""
    try:
        # Try to get terminal size
        size = shutil.get_terminal_size()
        width = size.columns
        
        # Ensure minimum and maximum reasonable widths
        if width < 60:  # Minimum for readability
            return 60
        elif width > 120:  # Maximum for readability
            return 120
        else:
            return width
    except:
        # Fallback to 80 if terminal size detection fails
        return 80

def get_visible_length(text):
    """Get the visible length of text, excluding ANSI color codes."""
    if not text:
        return 0
    # Remove ANSI escape sequences to get actual visible length
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    return len(clean_text)

def pad_line_to_width(line, target_width, fill_char=' '):
    """Pad a line to exact target width, accounting for ANSI color codes."""
    visible_length = get_visible_length(line)
    if visible_length >= target_width:
        return line
    padding_needed = target_width - visible_length
    return line + (fill_char * padding_needed)

def wrap_text(text, width, indent=0):
    """Wrap text to specified width with optional indentation."""
    if not text:
        return [""]
    
    indent_str = " " * indent
    wrapper = textwrap.TextWrapper(
        width=width - indent,
        initial_indent=indent_str,
        subsequent_indent=indent_str,
        break_long_words=False,
        break_on_hyphens=False
    )
    
    # Handle multiple lines
    lines = text.split('\n')
    wrapped_lines = []
    
    for line in lines:
        if line.strip():
            wrapped_lines.extend(wrapper.wrap(line))
        else:
            wrapped_lines.append("")
    
    return wrapped_lines

def convert_bold_formatting(text):
    """
    Convert **bold text** markdown formatting to ANSI bold codes for terminal display.
    Also enhances special AI section headers for better visual impact.
    
    Args:
        text (str): Text that may contain **bold** formatting
        
    Returns:
        str: Text with **bold** converted to ANSI bold codes and enhanced section headers
    """
    import re
    
    # Replace **text** with ANSI bold formatting
    # Pattern matches **any text** including text with spaces, punctuation, etc.
    bold_pattern = r'\*\*(.*?)\*\*'
    
    def replace_bold(match):
        bold_text = match.group(1)
        
        # Special handling for AI section headers
        special_sections = {
            'COMPREHENSIVE ERROR ANALYSIS': '\033[96m\033[1m🔍 COMPREHENSIVE ERROR ANALYSIS\033[0m',
            'PROGRAM IMPACT': '\033[93m\033[1m⚠️ PROGRAM IMPACT\033[0m', 
            'COMPLETE SOLUTION': '\033[92m\033[1m🛠️ COMPLETE SOLUTION\033[0m',
            'SOLUTION VERIFICATION': '\033[92m\033[1m✅ SOLUTION VERIFICATION\033[0m',
            'PREVENTION STRATEGY': '\033[94m\033[1m🛡️ PREVENTION STRATEGY\033[0m',
            'BEFORE/AFTER CODE': '\033[95m\033[1m📝 BEFORE/AFTER CODE\033[0m'
        }
        
        # Check if this is a special section header
        if bold_text in special_sections:
            return special_sections[bold_text]
        
        # Regular bold formatting for other text
        return f'\033[1m{bold_text}\033[0m'  # ANSI bold start + text + reset
    
    # Apply bold formatting conversion
    formatted_text = re.sub(bold_pattern, replace_bold, text)
    
    return formatted_text

def format_ai_response(response, model_name=None):
    """
    Format the AI response with enhanced terminal UI including colors, sections, and better visual hierarchy.
    Now fully responsive and adaptive to terminal size.
    
    Args:
        response (str): The raw AI response
        model_name (str): The model name used (for display)
        
    Returns:
        str: Beautifully formatted response
    """
    if not response or len(response.strip()) == 0:
        return "\033[91m⚠ Empty response received\033[0m"
    
    # Convert **bold text** to ANSI bold formatting
    response = convert_bold_formatting(response)
    
    # Get dynamic terminal width
    terminal_width = get_terminal_width()
    content_width = terminal_width - 2  # Account for borders
    
    # Color codes
    HEADER = '\033[96m'      # Cyan
    SUCCESS = '\033[92m'     # Green
    WARNING = '\033[93m'     # Yellow
    ERROR = '\033[91m'       # Red
    INFO = '\033[94m'        # Blue
    BOLD = '\033[1m'         # Bold
    UNDERLINE = '\033[4m'    # Underline
    RESET = '\033[0m'        # Reset
    PURPLE = '\033[95m'      # Purple
    GRAY = '\033[90m'        # Gray
    
    # Icons
    AI_ICON = "🤖"
    SUCCESS_ICON = "✅"
    ERROR_ICON = "❌"
    INFO_ICON = "💡"
    CODE_ICON = "📝"
    WARNING_ICON = "⚠️"
    FLEX_ICON = "🚀"
    
    formatted_lines = []
    
    # Responsive Header
    formatted_lines.append("")
    formatted_lines.append(f"{HEADER}{'═' * terminal_width}{RESET}")
    
    # Center the header text or truncate if too long
    header_text = f"{AI_ICON} FLEX AI ASSISTANT • {model_name or 'gpt-4o-mini'}"
    if len(header_text) <= terminal_width - 4:
        padding = (terminal_width - len(header_text)) // 2
        formatted_lines.append(f"{HEADER}{' ' * padding}{BOLD}{header_text}{RESET}{HEADER}{' ' * (terminal_width - len(header_text) - padding)}{RESET}")
    else:
        # Truncate if too long
        truncated = header_text[:terminal_width - 4] + "..."
        formatted_lines.append(f"{HEADER}{BOLD}{truncated}{RESET}")
    
    formatted_lines.append(f"{HEADER}{'═' * terminal_width}{RESET}")
    
    # Split response into sections
    lines = response.split('\n')
    current_section = []
    in_code_block = False
    code_language = ""
    
    for line in lines:
        # Detect code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block - responsive
                inner_width = content_width
                formatted_lines.append(f"{INFO}┌{'─' * inner_width}┐{RESET}")
                
                # Code block header with language
                header_text = f" {CODE_ICON} Code Example ({code_language})"
                remaining_space = max(1, inner_width - len(header_text) - 1)
                formatted_lines.append(f"{INFO}│{BOLD}{header_text}{RESET}{INFO}{'─' * remaining_space}│{RESET}")
                formatted_lines.append(f"{INFO}├{'─' * inner_width}┤{RESET}")
                
                for code_line in current_section:
                    # Convert tabs to spaces (4 spaces per tab) for consistent formatting
                    code_line_formatted = code_line.expandtabs(4)
                    
                    # Syntax highlighting for Flex keywords (preserve original spacing)
                    highlighted_line = highlight_flex_syntax(code_line_formatted)
                    
                    # Handle long lines by wrapping or truncating
                    if len(code_line_formatted) > inner_width - 2:
                        # For long lines, split carefully while preserving indentation
                        leading_spaces = len(code_line_formatted) - len(code_line_formatted.lstrip())
                        content = code_line_formatted[leading_spaces:]
                        
                        # First line keeps original indentation
                        available_width = inner_width - 2 - leading_spaces
                        if available_width > 10:  # Ensure minimum space for content
                            first_part = content[:available_width]
                            remaining = content[available_width:]
                            
                            # Display first part with original indentation
                            first_line = code_line_formatted[:leading_spaces] + first_part
                            highlighted_first = highlight_flex_syntax(first_line)
                            padded_line = pad_line_to_width(highlighted_first, inner_width-2)
                            formatted_lines.append(f"{INFO}│{RESET} {padded_line} {INFO}│{RESET}")
                            
                            # Display remaining content with continued indentation (extra 2 spaces)
                            if remaining.strip():
                                continued_line = " " * (leading_spaces + 2) + remaining.strip()
                                highlighted_continued = highlight_flex_syntax(continued_line)
                                padded_continued = pad_line_to_width(highlighted_continued, inner_width-2)
                                formatted_lines.append(f"{INFO}│{RESET} {padded_continued} {INFO}│{RESET}")
                        else:
                            # If not enough space, just truncate with ellipsis
                            truncated = code_line_formatted[:inner_width-5] + "..."
                            highlighted_truncated = highlight_flex_syntax(truncated)
                            padded_line = pad_line_to_width(highlighted_truncated, inner_width-2)
                            formatted_lines.append(f"{INFO}│{RESET} {padded_line} {INFO}│{RESET}")
                    else:
                        # Line fits, just pad to box width while preserving spacing
                        padded_line = pad_line_to_width(highlighted_line, inner_width-2)
                        formatted_lines.append(f"{INFO}│{RESET} {padded_line} {INFO}│{RESET}")
                
                formatted_lines.append(f"{INFO}└{'─' * inner_width}┘{RESET}")
                formatted_lines.append("")
                current_section = []
                in_code_block = False
                code_language = ""
            else:
                # Start of code block
                if current_section:
                    # Process previous section
                    formatted_lines.extend(format_text_section(current_section, terminal_width))
                    current_section = []
                
                code_language = line.strip()[3:] or "flex"
                in_code_block = True
            continue
        
        if in_code_block:
            current_section.append(line)
        else:
            current_section.append(line)
    
    # Process remaining section
    if current_section:
        if in_code_block:
            # Handle unclosed code block - responsive
            inner_width = content_width
            formatted_lines.append(f"{INFO}┌{'─' * inner_width}┐{RESET}")
            
            # Header for unclosed code block
            header_text = f" {CODE_ICON} Code Example"
            remaining_space = max(1, inner_width - len(header_text) - 1)
            formatted_lines.append(f"{INFO}│{BOLD}{header_text}{RESET}{INFO}{'─' * remaining_space}│{RESET}")
            formatted_lines.append(f"{INFO}├{'─' * inner_width}┤{RESET}")
            
            for code_line in current_section:
                # Convert tabs to spaces (4 spaces per tab) for consistent formatting
                code_line_formatted = code_line.expandtabs(4)
                
                # Syntax highlighting for Flex keywords (preserve original spacing)
                highlighted_line = highlight_flex_syntax(code_line_formatted)
                
                # Handle long lines
                if len(code_line_formatted) > inner_width - 2:
                    # For long lines, split carefully while preserving indentation
                    leading_spaces = len(code_line_formatted) - len(code_line_formatted.lstrip())
                    content = code_line_formatted[leading_spaces:]
                    
                    # First line keeps original indentation
                    available_width = inner_width - 2 - leading_spaces
                    if available_width > 10:  # Ensure minimum space for content
                        first_part = content[:available_width]
                        remaining = content[available_width:]
                        
                        # Display first part with original indentation
                        first_line = code_line_formatted[:leading_spaces] + first_part
                        highlighted_first = highlight_flex_syntax(first_line)
                        padded_line = pad_line_to_width(highlighted_first, inner_width-2)
                        formatted_lines.append(f"{INFO}│{RESET} {padded_line} {INFO}│{RESET}")
                        
                        # Display remaining content with continued indentation (extra 2 spaces)
                        if remaining.strip():
                            continued_line = " " * (leading_spaces + 2) + remaining.strip()
                            highlighted_continued = highlight_flex_syntax(continued_line)
                            padded_continued = pad_line_to_width(highlighted_continued, inner_width-2)
                            formatted_lines.append(f"{INFO}│{RESET} {padded_continued} {INFO}│{RESET}")
                    else:
                        # If not enough space, just truncate with ellipsis
                        truncated = code_line_formatted[:inner_width-5] + "..."
                        highlighted_truncated = highlight_flex_syntax(truncated)
                        padded_line = pad_line_to_width(highlighted_truncated, inner_width-2)
                        formatted_lines.append(f"{INFO}│{RESET} {padded_line} {INFO}│{RESET}")
                else:
                    # Line fits, just pad to box width while preserving spacing
                    padded_line = pad_line_to_width(highlighted_line, inner_width-2)
                    formatted_lines.append(f"{INFO}│{RESET} {padded_line} {INFO}│{RESET}")
            
            formatted_lines.append(f"{INFO}└{'─' * inner_width}┘{RESET}")
        else:
            formatted_lines.extend(format_text_section(current_section, terminal_width))
    
    # Responsive Footer
    formatted_lines.append("")
    formatted_lines.append(f"{SUCCESS}{'─' * terminal_width}{RESET}")
    
    # Center footer text or truncate if too long
    footer_text = f"{FLEX_ICON} Flex AI • Ready for your next question!"
    if len(footer_text) <= terminal_width - 4:
        padding = (terminal_width - len(footer_text)) // 2
        formatted_lines.append(f"{SUCCESS}{' ' * padding}{BOLD}{footer_text}{RESET}{SUCCESS}{' ' * (terminal_width - len(footer_text) - padding)}{RESET}")
    else:
        # Truncate if too long
        truncated = footer_text[:terminal_width - 4] + "..."
        formatted_lines.append(f"{SUCCESS}{BOLD}{truncated}{RESET}")
    
    formatted_lines.append(f"{SUCCESS}{'─' * terminal_width}{RESET}")
    formatted_lines.append("")
    
    return '\n'.join(formatted_lines)

def format_text_section(lines, terminal_width):
    """Format a text section with proper styling and responsive text wrapping."""
    HEADER = '\033[96m'      # Cyan
    SUCCESS = '\033[92m'     # Green
    WARNING = '\033[93m'     # Yellow
    ERROR = '\033[91m'       # Red
    INFO = '\033[94m'        # Blue
    BOLD = '\033[1m'         # Bold
    RESET = '\033[0m'        # Reset
    GRAY = '\033[90m'        # Gray
    
    # Icons
    SUCCESS_ICON = "✅"
    ERROR_ICON = "❌"
    INFO_ICON = "💡"
    WARNING_ICON = "⚠️"
    BULLET = "•"
    ARROW = "→"
    
    formatted = []
    content_width = terminal_width - 4  # Account for prefix and spacing
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            formatted.append("")
            continue
        
        # Headers (### or **)
        if stripped.startswith('###'):
            text = stripped[3:].strip()
            prefix = ""
            color = HEADER
            
            if 'Immediate fix' in text or 'Solution' in text:
                prefix = f"{SUCCESS}┃ {SUCCESS_ICON} "
                color = SUCCESS
            elif 'Explanation' in text:
                prefix = f"{INFO}┃ {INFO_ICON} "
                color = INFO
            elif 'Prevention' in text:
                prefix = f"{WARNING}┃ {WARNING_ICON} "
                color = WARNING
            else:
                prefix = f"{HEADER}┃ "
                color = HEADER
            
            # Wrap long headers
            if len(text) > content_width:
                wrapped_lines = wrap_text(text, content_width)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{prefix}{BOLD}{wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{color}┃   {BOLD}{wrapped_line}{RESET}")
            else:
                formatted.append(f"{prefix}{BOLD}{text}{RESET}")
            
        elif stripped.startswith('**') and stripped.endswith('**'):
            text = stripped[2:-2]
            prefix = ""
            color = HEADER
            
            if 'Problem' in text or 'Error' in text:
                prefix = f"{ERROR}┃ {ERROR_ICON} "
                color = ERROR
            elif 'Solution' in text or 'Fix' in text:
                prefix = f"{SUCCESS}┃ {SUCCESS_ICON} "
                color = SUCCESS
            elif 'Prevention' in text:
                prefix = f"{WARNING}┃ {WARNING_ICON} "
                color = WARNING
            else:
                prefix = f"{HEADER}┃ "
                color = HEADER
            
            # Wrap long bold headers
            if len(text) > content_width:
                wrapped_lines = wrap_text(text, content_width)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{prefix}{BOLD}{wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{color}┃   {BOLD}{wrapped_line}{RESET}")
            else:
                formatted.append(f"{prefix}{BOLD}{text}{RESET}")
        
        # Bullet points
        elif stripped.startswith('- ') or stripped.startswith('• '):
            text = stripped[2:]
            if len(text) > content_width - 4:
                wrapped_lines = wrap_text(text, content_width - 4)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{INFO}  {BULLET} {wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{INFO}    {wrapped_line}{RESET}")
            else:
                formatted.append(f"{INFO}  {BULLET} {text}{RESET}")
        
        # Numbered lists
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == '.':
            text = stripped[2:].strip()
            prefix = f"{INFO}  {stripped[0]}. "
            if len(text) > content_width - 6:
                wrapped_lines = wrap_text(text, content_width - 6)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{prefix}{wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{INFO}      {wrapped_line}{RESET}")
            else:
                formatted.append(f"{prefix}{text}{RESET}")
        
        # Special keywords
        elif any(keyword in stripped.lower() for keyword in ['error', 'problem', 'issue', 'wrong']):
            if len(stripped) > content_width:
                wrapped_lines = wrap_text(stripped, content_width)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{ERROR}┃ {wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{ERROR}┃ {wrapped_line}{RESET}")
            else:
                formatted.append(f"{ERROR}┃ {stripped}{RESET}")
                
        elif any(keyword in stripped.lower() for keyword in ['fix', 'solution', 'correct']):
            if len(stripped) > content_width:
                wrapped_lines = wrap_text(stripped, content_width)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{SUCCESS}┃ {wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{SUCCESS}┃ {wrapped_line}{RESET}")
            else:
                formatted.append(f"{SUCCESS}┃ {stripped}{RESET}")
                
        elif any(keyword in stripped.lower() for keyword in ['note', 'tip', 'remember']):
            if len(stripped) > content_width:
                wrapped_lines = wrap_text(stripped, content_width)
                for i, wrapped_line in enumerate(wrapped_lines):
                    if i == 0:
                        formatted.append(f"{WARNING}┃ {INFO_ICON} {wrapped_line}{RESET}")
                    else:
                        formatted.append(f"{WARNING}┃   {wrapped_line}{RESET}")
            else:
                formatted.append(f"{WARNING}┃ {INFO_ICON} {stripped}{RESET}")
        
        # Regular text
        else:
            if len(stripped) > content_width - 2:
                wrapped_lines = wrap_text(stripped, content_width - 2)
                for wrapped_line in wrapped_lines:
                    formatted.append(f"  {wrapped_line}")
            else:
                formatted.append(f"  {stripped}")
    
    return formatted

def highlight_flex_syntax(code_line):
    """Apply syntax highlighting to Flex code while preserving indentation and spacing."""
    KEYWORD = '\033[95m'     # Purple - keywords
    STRING = '\033[93m'      # Yellow - strings  
    COMMENT = '\033[90m'     # Gray - comments
    NUMBER = '\033[96m'      # Cyan - numbers
    OPERATOR = '\033[91m'    # Red - operators
    RESET = '\033[0m'        # Reset
    
    if not code_line:
        return code_line
    
    # Preserve leading whitespace
    leading_whitespace = code_line[:len(code_line) - len(code_line.lstrip())]
    content = code_line[len(leading_whitespace):]
    
    if not content.strip():  # If line is only whitespace
        return code_line
    
    line = content
    
    # Comments (handle carefully to preserve spacing)
    if '#' in line:
        parts = line.split('#', 1)
        if len(parts) == 2:
            line = parts[0] + f"{COMMENT}#{parts[1]}{RESET}"
    
    # Franco Arabic keywords (improved pattern matching)
    franco_keywords = ['rakm', 'kasr', 'so2al', 'klma', 'dorg', 'sndo2', 'etb3', 'da5l', 'lw', 'aw', 'gher', 'karr', 'l7d', 'talama', 'rg3', 'w2f']
    english_keywords = ['int', 'float', 'bool', 'string', 'list', 'fun', 'print', 'scan', 'if', 'elif', 'else', 'for', 'while', 'return', 'break']
    
    import re
    
    # Use word boundaries for better keyword matching
    for keyword in franco_keywords + english_keywords:
        # Match keywords as whole words
        pattern = r'\b' + re.escape(keyword) + r'\b'
        line = re.sub(pattern, f'{KEYWORD}{keyword}{RESET}', line)
    
    # Strings (handle both single and double quotes)
    line = re.sub(r'"([^"]*)"', f'{STRING}"\\1"{RESET}', line)
    line = re.sub(r"'([^']*)'", f'{STRING}\'\\1\'{RESET}', line)
    
    # Numbers (improved pattern for floats and integers)
    line = re.sub(r'\b(\d+\.?\d*)\b', f'{NUMBER}\\1{RESET}', line)
    
    # Operators (improved spacing handling)
    operators = ['==', '!=', '<=', '>=', '=', '+', '-', '*', '/', '%', '<', '>']  # Order matters - longer first
    for op in operators:
        escaped_op = re.escape(op)
        # Match operators with optional spaces around them
        pattern = r'(\s*)(' + escaped_op + r')(\s*)'
        replacement = r'\1' + f'{OPERATOR}\\2{RESET}' + r'\3'
        line = re.sub(pattern, replacement, line)
    
    # Restore leading whitespace
    return leading_whitespace + line

# Function to interact with the assistant (enhanced version)
def ask_assistant(prompt, model_name=None):
    """
    Process the prompt using OpenRouter and display with enhanced formatting.
    
    Args:
        prompt (str): The prompt to send to the model
        model_name (str, optional): If provided, uses OpenRouter with this model
        
    Returns:
        None: Prints the beautifully formatted response to console
    """
    try:
        # Get the response
        response = use_openrouter(prompt, model_name)
        
        # Format and display the response
        formatted_response = format_ai_response(response, model_name)
        print(formatted_response)
        
    except Exception as e:
        error_msg = f"Error getting AI response: {str(e)}"
        print(f"\033[91m❌ {error_msg}\033[0m")

def handle_error(error_message, AI, model_name=None):
    """Enhanced error handler with user retry prompt and full file context option."""
    if AI:
        # Get terminal width for responsive display
        terminal_width = get_terminal_width()
        
        # Enhanced responsive error display
        print(f"\033[91m{'═' * terminal_width}\033[0m")
        
        # Center or truncate error header
        error_header = "❌ FLEX COMPILATION ERROR"
        if len(error_header) <= terminal_width - 4:
            padding = (terminal_width - len(error_header)) // 2
            print(f"\033[91m{' ' * padding}{error_header}{' ' * (terminal_width - len(error_header) - padding)}\033[0m")
        else:
            truncated = error_header[:terminal_width - 4] + "..."
            print(f"\033[91m{truncated}\033[0m")
        
        print(f"\033[91m{'═' * terminal_width}\033[0m")
        
        # Wrap error message if too long
        if len(error_message) > terminal_width - 4:
            wrapped_lines = wrap_text(error_message, terminal_width - 4)
            for line in wrapped_lines:
                print(f"\033[93m⚠️  {line}\033[0m")
        else:
            print(f"\033[93m⚠️  {error_message}\033[0m")
        
        print(f"\033[94m{'─' * terminal_width}\033[0m")
        
        # Center AI assistance message
        ai_message = "🤖 Getting AI assistance..."
        if len(ai_message) <= terminal_width - 4:
            padding = (terminal_width - len(ai_message)) // 2
            print(f"\033[96m{' ' * padding}{ai_message}{' ' * (terminal_width - len(ai_message) - padding)}\033[0m")
        else:
            print(f"\033[96m{ai_message}\033[0m")
        
        print(f"\033[94m{'─' * terminal_width}\033[0m")
        
        # Import here to avoid circular imports
        import flex_interpreter.glopal_vars as gv
        
        # Use model_name parameter if provided, otherwise use global model_name
        active_model = model_name or gv.model_name or "openai/gpt-4o-mini"
        
        # First AI response with just error context
        ask_assistant(error_message, active_model)
        
        # Enhanced user interaction for retry with full context
        while True:
            print(f"\033[96m{'─' * terminal_width}\033[0m")
            print(f"\033[96m🔄 RETRY OPTIONS\033[0m")
            print(f"\033[93m1. Try again with FULL FILE CONTEXT (better analysis)\033[0m")
            print(f"\033[94m2. Try again with ERROR ONLY (quick response)\033[0m")  
            print(f"\033[91m3. Exit and fix manually\033[0m")
            print(f"\033[96m{'─' * terminal_width}\033[0m")
            
            try:
                choice = input(f"\033[96mChoose an option (1-3): \033[0m").strip()
                
                if choice == '1':
                    # Get full file context with enhanced debugging
                    if gv.source_file_path and os.path.exists(gv.source_file_path):
                        try:
                            with open(gv.source_file_path, 'r', encoding='utf-8') as file:
                                full_file_content = file.read()
                            
                            # Debug information
                            file_size = len(full_file_content)
                            line_count = full_file_content.count('\n') + 1
                            
                            print(f"\033[96m🔍 Analyzing with full file context...\033[0m")
                            print(f"\033[94m📊 File stats: {file_size} characters, {line_count} lines\033[0m")
                            print(f"\033[94m📁 File path: {gv.source_file_path}\033[0m")
                            
                            # Verify file content is not empty
                            if not full_file_content.strip():
                                print(f"\033[91m❌ Warning: File appears to be empty!\033[0m")
                                continue
                            
                            # Enhanced prompt with full context - GUARANTEED to include entire file
                            enhanced_prompt = f"""COMPREHENSIVE FLEX FILE ANALYSIS

🎯 ANALYSIS TARGET:
- File: {gv.source_file_path}
- Size: {file_size} characters, {line_count} lines
- Error: {error_message}

📋 COMPLETE FILE CONTENT (ANALYZE THE ENTIRE FILE):
```flex
{full_file_content}
```

🔍 ENHANCED AI ANALYSIS PROTOCOL:

⚠️ CRITICAL DIRECTIVES:
• NEVER provide solutions based only on the error message - ALWAYS consider the complete file content provided
• ENSURE proposed changes maintain the program's overall structure and functionality  
• MENTALLY execute the entire program with your proposed fix to ensure no new issues
• MAINTAIN the existing code style, variable naming patterns, and syntax preferences shown in the file
• ALWAYS check for Franco l7d loop safety issues when analyzing complete files - this is the #1 source of runtime errors

🧠 MANDATORY ANALYSIS STEPS:

STEP 1 - WHOLE FILE COMPREHENSION:
• Read and understand EVERY line of the provided file
• Map all variable declarations and their scope
• Identify all function definitions and their relationships  
• Understand the program's overall purpose and flow
• Note any imports or external dependencies

STEP 2 - ERROR CONTEXTUALIZATION:
• Find the exact line and character position of the error
• Understand how this error affects the entire program execution
• Identify all variables, functions, and imports that relate to this error
• Determine if this is an isolated error or symptom of larger architectural issue
• Check for similar patterns elsewhere in the file that might have same issue

STEP 3 - COMPREHENSIVE SOLUTION:
• Ensure fix doesn't break other parts of the program
• Maintain consistency with existing code style and patterns
• Consider performance implications for the entire program
• Provide alternative solutions if multiple approaches exist
• Include error prevention strategies for similar issues

STEP 4 - VERIFICATION PROTOCOL:
• Trace through program execution with the proposed fix
• Verify all function calls and variable access remain valid
• Check that data flow throughout the program remains logical
• Ensure no new errors are introduced elsewhere
• Confirm the fix aligns with the program's overall architecture

📋 REQUIRED RESPONSE FORMAT:

🔍 COMPREHENSIVE ERROR ANALYSIS:
[Detailed explanation of error within complete program context]

⚠️ PROGRAM IMPACT:
[How this error affects the entire application]

🛠️ COMPLETE SOLUTION:
[Step-by-step fix considering full codebase]

📝 BEFORE/AFTER CODE:
[Show exact changes with surrounding context]

✅ SOLUTION VERIFICATION:
[Explain why this fix works within the complete program]

🛡️ PREVENTION STRATEGY:
[How to avoid similar issues in this and other files]

🎯 MANDATORY DELIVERABLES:
• Exact line number and character position of error
• Complete explanation of root cause within program context
• Full solution with before/after code showing surrounding context
• Verification that solution works with the entire program
• At least 2 alternative approaches if applicable
• Prevention strategies specific to this program's architecture

⚠️ CRITICAL: Base your analysis on the COMPLETE file content provided above, not just the error message. You are analyzing a complete Flex program with {line_count} lines of code."""

                            # Show prompt preview for debugging (first 200 chars)
                            print(f"\033[90m📝 Prompt preview: {enhanced_prompt[:200]}...\033[0m")
                            
                            ask_assistant(enhanced_prompt, active_model)
                            
                        except Exception as e:
                            print(f"\033[91m❌ Error reading file: {e}\033[0m")
                            print(f"\033[91m📍 File path attempted: {gv.source_file_path}\033[0m")
                            continue
                    else:
                        print(f"\033[91m❌ Source file not available for context analysis\033[0m")
                        if gv.source_file_path:
                            print(f"\033[91m📍 Expected file path: {gv.source_file_path}\033[0m")
                            print(f"\033[91m📁 File exists: {os.path.exists(gv.source_file_path) if gv.source_file_path else 'No path set'}\033[0m")
                        else:
                            print(f"\033[91m📍 No source file path has been set in global variables\033[0m")
                        continue
                        
                elif choice == '2':
                    # Quick retry with error only
                    print(f"\033[96m⚡ Quick error analysis...\033[0m")
                    ask_assistant(error_message, active_model)
                    
                elif choice == '3':
                    # Exit
                    print(f"\033[92m👍 Exiting to manual fix. Good luck!\033[0m")
                    break
                    
                else:
                    print(f"\033[91m❌ Invalid choice. Please enter 1, 2, or 3.\033[0m")
                    continue
                    
                # Ask if user wants to try again after getting AI response
                print(f"\033[96m{'─' * terminal_width}\033[0m")
                retry = input(f"\033[96mTry again with another option? (y/n): \033[0m").strip().lower()
                if retry not in ['y', 'yes']:
                    break
                    
            except KeyboardInterrupt:
                print(f"\n\033[92m👍 Exiting AI assistance.\033[0m")
                break
            except EOFError:
                print(f"\n\033[92m👍 Exiting AI assistance.\033[0m") 
                break
        
        print(f"\033[94m{'─' * terminal_width}\033[0m")        
        raise SyntaxError("\033[92m🎉 Flex AI assistance completed! :)\033[0m")
    else:
        raise SyntaxError(f"\033[91m❌ {error_message}\033[0m")

# Test and validation functions
def test_system_prompt(debug_mode=True):
    """
    Test function to validate the system prompt is loading correctly.
    
    Args:
        debug_mode (bool): Whether to print detailed information
    """
    print("\033[94m=== Flex AI System Prompt Test ===\033[0m")
    
    # Test system prompt loading
    prompt = load_flex_system_prompt(debug_mode=True)
    
    if prompt and len(prompt) > 100:  # Basic validation
        print(f"\033[92m✓ System prompt loaded successfully ({len(prompt)} characters)\033[0m")
        
        # Check for key components
        key_components = [
            "ROLE:",
            "INSTANT REFERENCE",
            "ESSENTIAL KNOWLEDGE",
            "SYNTAX PATTERNS"
        ]
        
        found_components = []
        for component in key_components:
            if component in prompt:
                found_components.append(component)
        
        print(f"\033[92m✓ Found {len(found_components)}/{len(key_components)} key components\033[0m")
        
        if debug_mode:
            print(f"\033[94mPrompt preview (first 500 chars):\033[0m")
            print(f"\033[93m{prompt[:500]}...\033[0m")
        
        return True
    else:
        print(f"\033[91m✗ System prompt loading failed or too short\033[0m")
        return False

def get_system_prompt_info():
    """
    Get information about the current system prompt for debugging.
    
    Returns:
        dict: Information about the loaded system prompt
    """
    base_dir = get_base_dir()
    json_path = os.path.join(base_dir, "flex_language_spec.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            spec_data = json.load(file)
            
        ai_prompt = spec_data.get("ai_system_prompt", {})
        essential = spec_data.get("ESSENTIAL_FLEX_KNOWLEDGE", {})
        
        return {
            "status": "loaded_optimized",
            "version": ai_prompt.get("version", "unknown"),
            "role": ai_prompt.get("role", "unknown"),
            "language_identity": essential.get("language_identity", "unknown"),
            "json_path": json_path,
            "prompt_length": len(flex_system_prompt)
        }
    except:
        return {
            "status": "fallback_legacy",
            "version": "legacy",
            "role": "basic_assistant",
            "language_identity": "Flex",
            "json_path": "not_found",
            "prompt_length": len(flex_system_prompt)
        }

# Test and validation functions
def test_full_file_context(test_file_path=None, debug_mode=True):
    """
    Test function to verify that the full file context feature works correctly.
    
    Args:
        test_file_path (str, optional): Path to a test file. If None, creates a temporary test file.
        debug_mode (bool): Whether to print detailed information
    """
    import flex_interpreter.glopal_vars as gv
    
    print("\033[94m=== Full File Context Test ===\033[0m")
    
    # Create a test file if none provided
    if not test_file_path:
        test_content = """# Test Flex file for context analysis
rakm x = 10
rakm y = 20
sndo2 add(rakm a, rakm b) {
    rg3 a + b
}

# This line has an intentional error
rakm result = add(x, y, z)  # z is not defined - this should cause an error
print("Result:", result)
"""
        test_file_path = "test_context.lx"
        try:
            with open(test_file_path, 'w') as f:
                f.write(test_content)
            if debug_mode:
                print(f"\033[92m✓ Created test file: {test_file_path}\033[0m")
        except Exception as e:
            print(f"\033[91m✗ Failed to create test file: {e}\033[0m")
            return False
    
    # Test file reading
    if not os.path.exists(test_file_path):
        print(f"\033[91m✗ Test file not found: {test_file_path}\033[0m")
        return False
    
    # Set the global variable
    gv.source_file_path = test_file_path
    
    # Test reading the file
    try:
        with open(test_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        file_size = len(content)
        line_count = content.count('\n') + 1
        
        print(f"\033[92m✓ Successfully read test file\033[0m")
        print(f"\033[94m📊 File stats: {file_size} characters, {line_count} lines\033[0m")
        
        if debug_mode:
            print(f"\033[94mFile content preview:\033[0m")
            print(f"\033[93m{content[:200]}{'...' if len(content) > 200 else ''}\033[0m")
        
        # Test the enhanced prompt creation
        error_message = "Test error: variable 'z' is not defined at line 8"
        enhanced_prompt = f"""COMPREHENSIVE FLEX FILE ANALYSIS

🎯 ANALYSIS TARGET:
- File: {test_file_path}
- Size: {file_size} characters, {line_count} lines
- Error: {error_message}

📋 COMPLETE FILE CONTENT (ANALYZE THE ENTIRE FILE):
```flex
{content}
```

🔍 ENHANCED AI ANALYSIS PROTOCOL:

⚠️ CRITICAL DIRECTIVES:
• NEVER provide solutions based only on the error message - ALWAYS consider the complete file content provided
• ENSURE proposed changes maintain the program's overall structure and functionality  
• MENTALLY execute the entire program with your proposed fix to ensure no new issues
• MAINTAIN the existing code style, variable naming patterns, and syntax preferences shown in the file
• ALWAYS check for Franco l7d loop safety issues when analyzing complete files - this is the #1 source of runtime errors

🧠 MANDATORY ANALYSIS STEPS:

STEP 1 - WHOLE FILE COMPREHENSION:
• Read and understand EVERY line of the provided file
• Map all variable declarations and their scope
• Identify all function definitions and their relationships  
• Understand the program's overall purpose and flow
• Note any imports or external dependencies

STEP 2 - ERROR CONTEXTUALIZATION:
• Find the exact line and character position of the error
• Understand how this error affects the entire program execution
• Identify all variables, functions, and imports that relate to this error
• Determine if this is an isolated error or symptom of larger architectural issue
• Check for similar patterns elsewhere in the file that might have same issue

STEP 3 - COMPREHENSIVE SOLUTION:
• Ensure fix doesn't break other parts of the program
• Maintain consistency with existing code style and patterns
• Consider performance implications for the entire program
• Provide alternative solutions if multiple approaches exist
• Include error prevention strategies for similar issues

STEP 4 - VERIFICATION PROTOCOL:
• Trace through program execution with the proposed fix
• Verify all function calls and variable access remain valid
• Check that data flow throughout the program remains logical
• Ensure no new errors are introduced elsewhere
• Confirm the fix aligns with the program's overall architecture

📋 REQUIRED RESPONSE FORMAT:

🔍 COMPREHENSIVE ERROR ANALYSIS:
[Detailed explanation of error within complete program context]

⚠️ PROGRAM IMPACT:
[How this error affects the entire application]

🛠️ COMPLETE SOLUTION:
[Step-by-step fix considering full codebase]

📝 BEFORE/AFTER CODE:
[Show exact changes with surrounding context]

✅ SOLUTION VERIFICATION:
[Explain why this fix works within the complete program]

🛡️ PREVENTION STRATEGY:
[How to avoid similar issues in this and other files]

🎯 MANDATORY DELIVERABLES:
• Exact line number and character position of error
• Complete explanation of root cause within program context
• Full solution with before/after code showing surrounding context
• Verification that solution works with the entire program
• At least 2 alternative approaches if applicable
• Prevention strategies specific to this program's architecture

⚠️ CRITICAL: Base your analysis on the COMPLETE file content provided above, not just the error message. You are analyzing a complete Flex program with {line_count} lines of code."""

        prompt_size = len(enhanced_prompt)
        print(f"\033[92m✓ Enhanced prompt created: {prompt_size} characters\033[0m")
        
        # Verify the full file content is in the prompt
        if content in enhanced_prompt:
            print(f"\033[92m✓ Full file content verified in prompt\033[0m")
        else:
            print(f"\033[91m✗ Full file content NOT found in prompt\033[0m")
            return False
        
        if debug_mode:
            print(f"\033[94mPrompt preview (first 300 chars):\033[0m")
            print(f"\033[93m{enhanced_prompt[:300]}...\033[0m")
        
        # Clean up test file if we created it
        if test_file_path == "test_context.lx":
            try:
                os.remove(test_file_path)
                if debug_mode:
                    print(f"\033[92m✓ Cleaned up test file\033[0m")
            except:
                if debug_mode:
                    print(f"\033[93m⚠ Could not clean up test file\033[0m")
        
        print(f"\033[92m🎉 Full file context test PASSED!\033[0m")
        return True
        
    except Exception as e:
        print(f"\033[91m✗ Test failed: {e}\033[0m")
        return False

def showcase_enhanced_context_mode(file_path):
    """
    Showcase the enhanced complete context mode with all AI instructions.
    This demonstrates the comprehensive AI capabilities when analyzing entire files.
    """
    print("\033[96m" + "="*100 + "\033[0m")
    print("\033[96m🚀 FLEX AI ENHANCED COMPLETE CONTEXT MODE SHOWCASE\033[0m")
    print("\033[96m" + "="*100 + "\033[0m")
    
    if not os.path.exists(file_path):
        print(f"\033[91m❌ File not found: {file_path}\033[0m")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        file_size = len(file_content)
        line_count = file_content.count('\n') + 1
        
        print(f"\033[94m📊 ANALYZING FILE: {file_path}\033[0m")
        print(f"\033[94m📈 File Statistics: {file_size} characters, {line_count} lines\033[0m")
        print()
        
        print("\033[93m🎯 ENHANCED AI CAPABILITIES ACTIVATED:\033[0m")
        print("\033[92m✅ HOLISTIC_ANALYSIS: Analyze ENTIRE file as complete program\033[0m")
        print("\033[92m✅ CONTEXTUAL_DEBUGGING: Understand error in relation to full program structure\033[0m") 
        print("\033[92m✅ ARCHITECTURAL_INSIGHT: Solutions consider complete codebase architecture\033[0m")
        print("\033[92m✅ COMPREHENSIVE_VALIDATION: Verify fixes work within entire file context\033[0m")
        print()
        
        print("\033[93m🧠 4-STEP ANALYSIS PROTOCOL:\033[0m")
        print("\033[94m📋 STEP 1: WHOLE FILE COMPREHENSION\033[0m")
        print("   • Read and understand EVERY line of the provided file")
        print("   • Map all variable declarations and their scope")
        print("   • Identify all function definitions and relationships")
        print("   • Understand program's overall purpose and flow")
        print()
        
        print("\033[94m🔍 STEP 2: ERROR CONTEXTUALIZATION\033[0m")
        print("   • Find exact line and character position of error")
        print("   • Understand how error affects entire program execution")
        print("   • Identify all variables/functions/imports related to error")
        print("   • Determine if isolated error or architectural issue")
        print()
        
        print("\033[94m🛠️ STEP 3: COMPREHENSIVE SOLUTION\033[0m")
        print("   • Ensure fix doesn't break other parts of program")
        print("   • Maintain consistency with existing code style")
        print("   • Consider performance implications for entire program")
        print("   • Provide alternative solutions if multiple approaches exist")
        print()
        
        print("\033[94m✅ STEP 4: VERIFICATION PROTOCOL\033[0m")
        print("   • Trace through program execution with proposed fix")
        print("   • Verify all function calls and variable access remain valid")
        print("   • Check data flow throughout program remains logical")
        print("   • Ensure no new errors introduced elsewhere")
        print()
        
        print("\033[93m🎯 MANDATORY DELIVERABLES:\033[0m")
        deliverables = [
            "Exact line number and character position of error",
            "Complete explanation of root cause within program context", 
            "Full solution with before/after code showing surrounding context",
            "Verification that solution works with the entire program",
            "At least 2 alternative approaches if applicable",
            "Prevention strategies specific to this program's architecture"
        ]
        for i, item in enumerate(deliverables, 1):
            print(f"\033[92m   {i}. {item}\033[0m")
        print()
        
        print("\033[93m⚠️ CRITICAL SAFETY CHECKS:\033[0m")
        safety_checks = [
            "NEVER provide solutions based only on error message",
            "ENSURE proposed changes maintain program integrity",
            "MENTALLY execute entire program with proposed fix",
            "MAINTAIN existing code style and syntax preferences",
            "ALWAYS check for Franco l7d loop safety issues"
        ]
        for check in safety_checks:
            print(f"\033[91m🔒 {check}\033[0m")
        print()
        
        # Show context comparison
        basic_error = "Sample error message"
        basic_size = len(basic_error)
        
        enhanced_context_size = 3000 + file_size  # Approximate enhanced prompt size
        
        print("\033[96m📊 CONTEXT POWER COMPARISON:\033[0m")
        print(f"\033[94m📝 Basic Error Mode: {basic_size} characters\033[0m")
        print(f"\033[92m🚀 Enhanced Context Mode: {enhanced_context_size}+ characters\033[0m")
        print(f"\033[93m⚡ Enhancement Factor: {enhanced_context_size // basic_size}x MORE CONTEXT!\033[0m")
        print()
        
        print("\033[96m🎉 RESULT: AI gets comprehensive understanding of your entire program!\033[0m")
        print("\033[96m" + "="*100 + "\033[0m")
        
    except Exception as e:
        print(f"\033[91m❌ Error reading file: {e}\033[0m")

def demonstrate_context_difference(file_path, error_message):
    """
    Demonstrate the difference between error-only and full-file context prompts.
    This shows exactly what the AI receives in each case.
    """
    print("\033[96m" + "="*80 + "\033[0m")
    print("\033[96m🔍 CONTEXT COMPARISON DEMONSTRATION\033[0m")
    print("\033[96m" + "="*80 + "\033[0m")
    
    # Error-only prompt (Option 2)
    print("\033[94m📝 OPTION 2 - ERROR ONLY PROMPT:\033[0m")
    print("\033[93m" + "-"*50 + "\033[0m")
    print(f"\033[91m{error_message}\033[0m")
    print("\033[93m" + "-"*50 + "\033[0m")
    print(f"\033[90mPrompt size: {len(error_message)} characters\033[0m")
    print()
    
    # Full file context prompt (Option 1)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                full_content = file.read()
            
            file_size = len(full_content)
            line_count = full_content.count('\n') + 1
            
            enhanced_prompt = f"""COMPREHENSIVE FLEX FILE ANALYSIS

🎯 ANALYSIS TARGET:
- File: {file_path}
- Size: {file_size} characters, {line_count} lines
- Error: {error_message}

📋 COMPLETE FILE CONTENT (ANALYZE THE ENTIRE FILE):
```flex
{full_content}
```

🔍 ENHANCED AI ANALYSIS PROTOCOL:

⚠️ CRITICAL DIRECTIVES:
• NEVER provide solutions based only on the error message - ALWAYS consider the complete file content provided
• ENSURE proposed changes maintain the program's overall structure and functionality  
• MENTALLY execute the entire program with your proposed fix to ensure no new issues
• MAINTAIN the existing code style, variable naming patterns, and syntax preferences shown in the file
• ALWAYS check for Franco l7d loop safety issues when analyzing complete files - this is the #1 source of runtime errors

🧠 MANDATORY ANALYSIS STEPS:

STEP 1 - WHOLE FILE COMPREHENSION:
• Read and understand EVERY line of the provided file
• Map all variable declarations and their scope
• Identify all function definitions and their relationships  
• Understand the program's overall purpose and flow
• Note any imports or external dependencies

STEP 2 - ERROR CONTEXTUALIZATION:
• Find the exact line and character position of the error
• Understand how this error affects the entire program execution
• Identify all variables, functions, and imports that relate to this error
• Determine if this is an isolated error or symptom of larger architectural issue
• Check for similar patterns elsewhere in the file that might have same issue

STEP 3 - COMPREHENSIVE SOLUTION:
• Ensure fix doesn't break other parts of the program
• Maintain consistency with existing code style and patterns
• Consider performance implications for the entire program
• Provide alternative solutions if multiple approaches exist
• Include error prevention strategies for similar issues

STEP 4 - VERIFICATION PROTOCOL:
• Trace through program execution with the proposed fix
• Verify all function calls and variable access remain valid
• Check that data flow throughout the program remains logical
• Ensure no new errors are introduced elsewhere
• Confirm the fix aligns with the program's overall architecture

📋 REQUIRED RESPONSE FORMAT:

🔍 COMPREHENSIVE ERROR ANALYSIS:
[Detailed explanation of error within complete program context]

⚠️ PROGRAM IMPACT:
[How this error affects the entire application]

🛠️ COMPLETE SOLUTION:
[Step-by-step fix considering full codebase]

📝 BEFORE/AFTER CODE:
[Show exact changes with surrounding context]

✅ SOLUTION VERIFICATION:
[Explain why this fix works within the complete program]

🛡️ PREVENTION STRATEGY:
[How to avoid similar issues in this and other files]

🎯 MANDATORY DELIVERABLES:
• Exact line number and character position of error
• Complete explanation of root cause within program context
• Full solution with before/after code showing surrounding context
• Verification that solution works with the entire program
• At least 2 alternative approaches if applicable
• Prevention strategies specific to this program's architecture

⚠️ CRITICAL: Base your analysis on the COMPLETE file content provided above, not just the error message. You are analyzing a complete Flex program with {line_count} lines of code."""

            print("\033[94m📝 OPTION 1 - FULL FILE CONTEXT PROMPT:\033[0m")
            print("\033[93m" + "-"*50 + "\033[0m")
            print(f"\033[92m{enhanced_prompt[:500]}...\033[0m")
            print("\033[93m" + "-"*50 + "\033[0m")
            print(f"\033[90mPrompt size: {len(enhanced_prompt)} characters\033[0m")
            print(f"\033[90mFile content included: ✓ YES ({file_size} chars)\033[0m")
            print()
            
            # Show the advantage
            print("\033[96m🎯 THE ADVANTAGE:\033[0m")
            print(f"\033[92m• Error-only gives AI: {len(error_message)} characters of context\033[0m")
            print(f"\033[92m• Full-file gives AI: {len(enhanced_prompt)} characters of context\033[0m")
            print(f"\033[92m• That's {len(enhanced_prompt) // len(error_message)}x more information!\033[0m")
            print(f"\033[92m• AI can see ALL variables, functions, and relationships\033[0m")
            print(f"\033[92m• AI understands the complete program flow\033[0m")
            
        except Exception as e:
            print(f"\033[91m❌ Could not read file: {e}\033[0m")
    else:
        print(f"\033[91m❌ File not found: {file_path}\033[0m")
    
    print("\033[96m" + "="*80 + "\033[0m")

# Quick test when module is imported (only in debug mode)
if __name__ == "__main__":
    print("\033[96m🔧 Testing Flex AI components...\033[0m\n")
    
    # Test system prompt
    test_system_prompt(debug_mode=True)
    print()
    
    # Test full file context feature
    test_full_file_context(debug_mode=True)

