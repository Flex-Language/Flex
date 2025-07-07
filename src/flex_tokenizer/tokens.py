# Token types
TOKENS = [
    ('FUN', r'\b(?:fun|sndo2|sando2|fn|function)\b'),  # Function keyword
    ('ADD', r'(.append|.push)'),  # List addition methods
    ('POP', r'(.pop)'),  # List pop method
    ('REMOVE', r'(.remove|.delete)'),  # List remove/delete methods
    ('SCAN', r'\b(scan|read|input|da5l|da5al|d5l)\b'),  # Input/scan keywords
    ('IF', r'\b(if|cond)\b'),  # If statement keywords
    ('LW', r'(\blw\b)'),  # If statement keyword in another language
    ('ELIF', r'(elif)'),  # Elif statement keyword
    ('AW', r'(\baw\b)'),  # Elif statement keyword in another language
    ('ELSE', r'(else|otherwise|gher)'),  # Else statement keywords
    ('PRINT', r'\b(etb3|out|output|print|printf|cout)\b'),  # Print statement keywords
    ('WHILE', r'(while|loop)'),  # While loop keywords
    ('TALAMA', r'(talama|talma|tlma)'),  # While loop keyword in another language
    ('FOR', r'for'),  # For loop keyword
    ('REPEAT', r'\b(krr|karr|karar)\b'),  # Repeat loop keyword
    ('UNTILL', r'(\bl7d\b)'),  # Until keyword
    ('SEMICOLON', r';'),  # Semicolon
    ('RETURN', r'\b(?:return|rg3|raga3)\b'),  # Return statement keywords
    ('BREAK', r'(break|stop|w2f|wa2af)'),  # Break statement keywords
    ('NUMBER', r'\d+(\.\d+)?'),  # Numbers and floats
    ('STRING', r'\".*?\"'),  # Strings
    ('LIST', r'\b(?:list|dorg|drg)\b'),  # List keyword
    ('LBRACKET', r'\['),  # Left square bracket
    ('RBRACKET', r'\]'),  # Right square bracket
    ('LPAREN', r'\('),  # Left parenthesis
    ('RPAREN', r'\)'),  # Right parenthesis
    ('LBRACE', r'\{'),  # Left curly brace
    ('RBRACE', r'\}'),  # Right curly brace
    ('GE', r'>=|=>'),  # Greater than or equal to
    ('LE', r'<=|=<'),  # Less than or equal to
    ('GT', r'>'),  # Greater than
    ('LT', r'<'),  # Less than
    ('AND', r'and'),  # And operator
    ('OR', r'or'),  # Or operator
    ('NOT', r'not'),  # Not operator
    ('EQ', r'=='),  # Equal operator
    ('NEQ', r'!='),  # Not equal operator
    ('ASSIGN', r'='),  # Assignment operator
    ('TRUE', r'\b(true|True|TRUE|sa7|s7|sah|saa7)\b'),  # Boolean true
    ('FALSE', r'(false|False|FALSE|ghalt|ghlt|ghalat)'),  # Boolean false
    ('INT', r'\b(?:int|rakm)\b'),  # Integer type
    ('FLOAT', r'\b(?:float|kasr|ksr)\b'),  # Float type
    ('BOOL', r'\b(?:bool|so2al|s2al|so2l)\b'),  # Boolean type
    ('STR', r'\b(?:string|klma|kalma)\b'),  # String type
    ('IMPORT', r'\b(geep|geeb|import)\b'),  # Import statement keywords
    ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),  # Identifiers (variable names)
    ('SKIP', r'[ \t]+'),  # Skip spaces and tabs
    ('NEWLINE', r'\n'),  # New lines
    ('INCREMENT', r'\+\+'),  # Increment operator
    ('DECREMENT', r'\-\-'),  # Decrement operator
    ('PLUS', r'\+'),  # Addition operator
    ('MINUS', r'-'),  # Subtraction operator
    ('MULT', r'\*'),  # Multiplication operator
    ('MOD', r'%'),  # Modulo operator
    ('LONG_COMMENT', r'\'\'\'[\s\S]*?\'\'\'|/\*[\s\S]*?\*/'),  # Long comments
    ('COMMENT', r'(#.*|//.*)'),  # Single-line comments
    ('DIV', r'\/'),  # Division operator
    ('COMMA', r','),  # Comma for separating parameters and arguments
]
