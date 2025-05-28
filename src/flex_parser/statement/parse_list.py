import  flex_parser.glopal_vars as gv
from flex_parser.parser_utils import *
from flex_parser.parse_expr import *
from flex_parser.parse_arithmetic_expr import *
from flex_parser.statement.parse_variable_declaration import parse_func_call_in_variable_declaration

# def parse_list_declaration_statement(tokens, AI, line_number, line_content):
#     next_token(tokens)  # Consume 'list'
#     var_name = expect(tokens, 'ID', AI)  # Expect list name

#     if current_token(tokens)[0] == 'ASSIGN':  # Handle initialized list
#         expect(tokens, 'ASSIGN', AI)
#         expect(tokens, 'LBRACKET', AI)  # Expect '['

#         elements = []
#         while current_token(tokens)[0] != 'RBRACKET':  # Parse elements until ']'
#             element = parse_expr(tokens, AI,line_number,line_content)
#             elements.append(element)
#             if current_token(tokens)[0] == 'COMMA':  # Handle comma-separated elements
#                 next_token(tokens)  # Consume ','

#         expect(tokens, 'RBRACKET', AI)  # Expect ']'
#         return ('LIST_DECL', var_name, elements, line_number, line_content)

#     elif current_token(tokens)[0] == 'LBRACKET':  # Handle empty list declaration
#         expect(tokens, 'LBRACKET', AI)
#         expect(tokens, 'RBRACKET', AI)  # Consume ']'
#         return ('LIST_DECL', var_name, [], line_number, line_content)
#     else:
#         error_message = f"Expected '[' or '=' after list name at {line_number}\nLine content: '{line_content}'"
#         handle_error(error_message, AI)

def parse_list_declaration_statement(tokens, AI, line_number, line_content):
    def parse_list_elements():
        elements = []
        while current_token(tokens)[0] != 'RBRACKET':
            if current_token(tokens)[0] == 'LBRACKET':
                next_token(tokens)  # Consume '['
                nested_elements = parse_list_elements()  # Recursive call
                expect(tokens, 'RBRACKET', AI)
                elements.append(nested_elements)
            else:
                element = parse_expr(tokens, AI, line_number, line_content)
                elements.append(element)
            
            if current_token(tokens)[0] == 'COMMA':
                next_token(tokens)  # Consume ','
        
        return elements

    next_token(tokens)  # Consume 'list'
    var_name = expect(tokens, 'ID', AI)  # Expect list name

    if current_token(tokens)[0] == 'ASSIGN':
        expect(tokens, 'ASSIGN', AI)
        if current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':
            elements = parse_func_call_in_variable_declaration(tokens, AI, line_number, line_content)  # Parse function call
        elif current_token(tokens)[0] == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LBRACKET':
            elements = parse_list_assignment_statement(tokens, AI, line_number, line_content)  # Parse function call
        else:
            expect(tokens, 'LBRACKET', AI)
            elements = parse_list_elements()  # Use recursive list parser
            expect(tokens, 'RBRACKET', AI)
        return ('LIST_DECL', var_name, elements, line_number, line_content)

    elif current_token(tokens)[0] == 'LBRACKET':
        expect(tokens, 'LBRACKET', AI)
        expect(tokens, 'RBRACKET', AI)
        return ('LIST_DECL', var_name, [], line_number, line_content)
    
    else:
        error_message = f"Expected '[' or '=' after list name at {line_number}\nLine content: '{line_content}'"
        handle_error(error_message, AI)


# def parse_list_assignment_statement(tokens, AI, line_number, line_content):
#     # Handle list index access for assignment or reading
#     var_name = expect(tokens, 'ID', AI)  # Expect list name
#     expect(tokens, 'LBRACKET', AI)  # Consume '['
#     index = parse_expr(tokens, AI,line_number,line_content)  # Parse the index expression
#     expect(tokens, 'RBRACKET', AI)  # Consume ']'

#     if current_token(tokens)[0] == 'ASSIGN':
#         expect(tokens, 'ASSIGN', AI)  # Consume '='
#         if current_token(tokens)[0] == 'SCAN':
#             expect(tokens, 'SCAN', AI)
#             expect(tokens, 'LPAREN', AI)
#             expect(tokens, 'RPAREN', AI)
#             value = "scan_now"
#         else:
#             value = parse_arithmetic_expr(tokens, AI,line_number,line_content)  # Parse the value being assigned
#         return ('LIST_ASSIGN', var_name, index, value, tokens[gv.pos - 1][2], tokens[gv.pos - 1][3])
#     else:
#         # If no assignment, treat it as a read access
#         return ('LIST_ACCESS', var_name, index, tokens[gv.pos - 1][2], tokens[gv.pos - 1][3])

def parse_list_assignment_statement(tokens, AI, line_number, line_content):
    var_name = expect(tokens, 'ID', AI)  # Expect list name

    indices = []
    while current_token(tokens)[0] == 'LBRACKET':
        expect(tokens, 'LBRACKET', AI)
        index = parse_expr(tokens, AI, line_number, line_content)
        expect(tokens, 'RBRACKET', AI)
        indices.append(index)

    if len(indices) <= 1:
        indices=indices[0]
    if current_token(tokens)[0] == 'ASSIGN':
        expect(tokens, 'ASSIGN', AI)
        if current_token(tokens)[0] == 'SCAN':
            expect(tokens, 'SCAN', AI)
            expect(tokens, 'LPAREN', AI)
            expect(tokens, 'RPAREN', AI)
            value = "scan_now"
        else:
            value = parse_arithmetic_expr(tokens, AI, line_number, line_content)
        return ('LIST_ASSIGN', var_name, indices, value, tokens[gv.pos - 1][2], tokens[gv.pos - 1][3])
    elif current_token(tokens)[0] == 'INCREMENT':
        expect(tokens, 'INCREMENT', AI)
        return ('LIST_INCREMENT', var_name, indices, tokens[gv.pos - 1][2], tokens[gv.pos - 1][3])
    elif current_token(tokens)[0] == 'DECREMENT':
        expect(tokens, 'DECREMENT', AI)
        return ('LIST_DECREMENT', var_name, indices, tokens[gv.pos - 1][2], tokens[gv.pos - 1][3])
    else:
        return ('LIST_ACCESS', var_name, indices, tokens[gv.pos - 1][2], tokens[gv.pos - 1][3])
