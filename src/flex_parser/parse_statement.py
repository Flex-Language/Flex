import flex_parser.glopal_vars as gv
from flex_parser.parse_expr import parse_negative_number
from flex_parser.parser_utils import *
from flex_parser.statement.parse_loops import parse_return_statement,parse_while_statement,parse_for_statement,parse_break_statement,parse_talama_statement,parse_repeat_statement
from flex_parser.statement.parse_conditions import parse_if_statement, parse_elif_statement,parse_lw_statement,parse_else_statement,parse_aw_statement
from flex_parser.statement.parse_print import parse_print_statement
from flex_parser.statement.parse_variable_declaration import parse_variable_declaration_statement
from flex_parser.statement.parse_function import parse_function_declaration_statement,parse_function_call_statement
from flex_parser.statement.parse_list import parse_list_declaration_statement,parse_list_assignment_statement
from flex_parser.statement.parse_variable_operations import parse_variable_operations_statement,parse_standalone_increment_decrement_statement
from flex_parser.statement.parse_import import parse_import_statement


def parse_statement(tokens,AI):
   
    # Skip over newlines or empty tokens
    skip_newlines(tokens)
    # print(f'pos:{gv.pos}        tokLen:{len(tokens)}')
    if gv.pos >= len(tokens):
        return None

    tok_type, tok_value, line_number, line_content = current_token(tokens)

    if tok_type == 'RETURN':
        return parse_return_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'IF':    
        return parse_if_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'LW':
        return parse_lw_statement(tokens, AI, line_number, line_content)
    elif tok_type=='ELIF':
        return parse_elif_statement(tokens, AI, line_number, line_content)
    elif tok_type=='AW':
        return parse_aw_statement(tokens, AI, line_number, line_content)
    elif tok_type=='ELSE':
        return parse_else_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'WHILE':
        return parse_while_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'TALAMA':
         return parse_talama_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'FOR':
        return parse_for_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'REPEAT':
        return parse_repeat_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'BREAK':
       return parse_break_statement(tokens, line_number, line_content)
    elif tok_type == 'PRINT':
        return parse_print_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'LIST':                                                                    # Handle list declaration
        return parse_list_declaration_statement(tokens, AI, line_number, line_content)    
    elif current_token(tokens)[0] == 'ID' and tokens[gv.pos + 1][0] == 'LBRACKET':                 #list assignment
        return parse_list_assignment_statement(tokens, AI, line_number, line_content)
    elif tok_type in ('INT', 'FLOAT', 'BOOL','STR'):                                            # Variable declaration
        return parse_variable_declaration_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'NUMBER' and gv.karrFlag:
        number= expect(tokens, 'NUMBER', AI)
        return ('NUMBER', number, line_number, line_content)
    elif tok_type == 'MINUS' and gv.karrFlag:
        numberNeg= parse_negative_number(tokens, AI, line_number, line_content)
        return ('-VE_NUMBER', numberNeg, line_number, line_content)
    elif tok_type == 'FUN':                                                                     # fun declaration
        return parse_function_declaration_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'ID' and gv.pos + 1 < len(tokens) and tokens[gv.pos + 1][0] == 'LPAREN':          # fun call
        return parse_function_call_statement(tokens, AI, line_number, line_content)   
    elif tok_type == 'ID' and gv.pos + 1 <= len(tokens):                                             # Handle variable assignments and increments/decrements
        return parse_variable_operations_statement(tokens, AI, tok_value, line_number, line_content)
    elif tok_type in ('INCREMENT', 'DECREMENT'):                                                 # Handle increment (++x) and decrement (--x)
       return parse_standalone_increment_decrement_statement(tokens, AI, tok_type, line_number, line_content)
    elif tok_type == 'RBRACE':                                                                   # Handle closing brace
        return None
    elif tok_type == 'IMPORT':  # Handle 'geeb' keyword
        return parse_import_statement(tokens, AI, line_number, line_content)
    elif tok_type == 'EOF':
        next_token(tokens)  # finished parsing the file
    else:
        if gv.forLoopFlag:
            return ('EMPTY', line_number, line_content)
        else:
            error_message = f"Unexpected token: {tok_value} at {line_number}\nLine content: '{line_content.strip()}'"
            handle_error(error_message, AI)

    