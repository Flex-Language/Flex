from flex_AI.useModel import *
from flex_interpreter.interpreter_utils import *
from flex_interpreter import execution
import flex_interpreter.glopal_vars as gv

def execute_if(statement, AI, insideFunc, skip_next):
    condition = statement[1]
    line_number, line_content = statement[2], statement[3]
    skip_next = not eval_condition(condition, line_number, line_content, insideFunc, AI)
    return skip_next

def execute_if_block(statement, AI, insideFunc, insideLoop):
    condition = statement[1]
    block = statement[2]
    line_number, line_content = statement[3], statement[4]
    if eval_condition(condition, line_number, line_content, insideFunc, AI):  # Only execute block if condition is true
        execution.run(block, AI,gv.web, insideFunc, insideLoop)  # Execute block recursively
        return True  # Indicating the block was executed
    return False  # Indicating the block was not executed

def execute_elif(statement, AI, insideFunc, insideLoop, if_first, non_if, trueifFlag, trueElifFlag, elif_finished):
    condition = statement[1]
    block = statement[2]
    line_number, line_content = statement[3], statement[4]
    if not if_first or non_if == True:
        error_message = f"Can't use elif before if\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    if eval_condition(condition, line_number, line_content, insideFunc, AI) and trueifFlag == False and trueElifFlag == False and elif_finished == False:  # Only execute block if condition is true
        trueElifFlag = True
        elif_finished = True
        execution.run(block, AI,gv.web, insideFunc, insideLoop)  # Execute block recursively
    else:
        trueElifFlag = False
    return trueElifFlag, elif_finished

def execute_else(statement, AI, insideFunc, insideLoop, if_first, non_if, trueifFlag, trueElifFlag, elif_finished):
    condition = statement[1]
    block = statement[2]
    line_number, line_content = statement[3], statement[4]
    if not if_first or non_if == True:
        error_message = f"Can't use else before if\n{line_number}: {line_content.strip()}"
        handle_error(error_message, AI)
    if trueifFlag == False and trueElifFlag == False and elif_finished == False:  # Only execute block if condition is true
        execution.run(block, AI,gv.web, insideFunc, insideLoop)  # Execute block recursively
    if_first = False
    return if_first

