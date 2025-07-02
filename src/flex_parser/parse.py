import flex_parser.glopal_vars as gv
from flex_parser.parse_statement import *

def parse(tokens, AI, model_name=None):
    statements = []
    
    #global pos

    while gv.pos < len(tokens):
        statement = parse_statement(tokens, AI, model_name)
        if statement:  # Only add valid statements
            statements.append(statement)
            
    x=statements
  
    gv.pos =0
    return x


#### bug: if we decleraed an empty id in the last line of code we get : An error occurred: list index out of range  #####