import os
import sys
import time
from math import sqrt, sin, cos
from string import ascii_letters

#  SETTINGS
sys.setrecursionlimit(3000)

# CONSTANTS
DIGITS = "0123456789"
LETTERS = ascii_letters
LETERS_NUMBER = LETTERS + DIGITS

# TOKENS
# DATATYPE TOKENS
INT		          = 'INT'
FLOAT             = 'FLOAT'
BOOLEAN           = 'BOOLEAN'
# SPECIAL TOKENS
STATEMENT         = 'STATEMENT'
IDENTIFIER        = 'IDENTIFIER'
KEYWORD           = 'KEYWORD'
EQ                = 'EQ'
EQ_ADD            = 'EQ_ADD'
EQ_SUB            = 'EQ_SUB'
EQ_MUL            = 'EQ_MUL'
EQ_DIV            = 'EQ_DIV'
EQ_MOD            = 'EQ_MOD'
EQ_POW            = 'EQ_POW'
LEFTPAREN         = '(' #'LEFT_PARENTHESIS'
RIGHTPAREN        = ')' #'RIGHT_PARENRHESIS'
EOF		          = 'EOF'
COMMENT           = '#'
COMMA             = 'COMMA'
END_LINE          = 'END_LINE'
NEW_LINE          = 'NEW_LINE'
ARG_TYPE          = 'ARG_TYPE'
# OPERATION TOKENS
ADD               = 'ADD'
SUB               = 'SUB'
MUL               = 'MUL'
DIV               = 'DIV'
MOD               = 'MOD'
POW               = 'POWER'
# LOGIC TOKENS 
NOT               = 'NOT'
AND               = 'AND'
OR                = 'OR'
COMPARISON        = 'COMPARISION'
NOT_EQUAL         = 'NOT_EQUAL'
LOWER_THAN        = 'LOWER_THAN'
LOWER_OR_EQUAL    = 'LOWER_OR_EQUAL_THAN'
GREATER_THAN      = 'GREATER_THAN'
GREATER_OR_EQUAL  = 'GREATER_OR_EQUAL_THAN'
# STATEMENTS    
IF                = 'IF'
THEN              = 'THEN'
ELIF              = 'ELIF'
ELSE              = 'ELSE'
WHILE             = 'WHILE'
FOR               = 'FOR'
TO                = 'TO'
END               = 'END'
# KEYWORDS    
FUNCTION          = 'FUNCTION'
FUNCTION_RETURNED = "FUNCTION-RETURNED"
DOES              = 'DOES'
ALT_DOES          = '->'
RETURN            = 'RETURN'
GLOBAL            = 'GLOBAL'
NUMBER            = 'VAR'
STRING            = 'STRING'
BREAK             = 'BREAK'
CONTINUE          = 'CONTINUE'
BOOL              = 'BOOL'
TRUE              = 'True'
FALSE             = 'False'      

# MATH VARIABLES
MATH_E   = 2.718281828459045
MATH_PI  = 3.141592653589793
MATH_TAU = 2 * MATH_PI
inf = float("inf")
nan = float("nan")

global_variables = {
    "MATH_E":   ("VAR", MATH_E),
    "MATH_PI":  ("VAR", MATH_PI), 
    "MATH_TAU": ("VAR", MATH_TAU),
    "inf":      ("VAR", inf),
    "nan":      ("VAR", nan)
}

bult_in_function = [
    'print', 'println', 
    'input', 'input_num', 
    'clear', 'exit', 
    'is_a_number', 
    'is_a_string', 
    'is_a_function', 
    'sqrt'
]

num_line_code = 0
def get_num_line(): global num_line_code; return num_line_code + 1
def set_line(num_line: int): global num_line_code; num_line_code = num_line

class Token:
    def __init__(self, struct: str, value: str, line: int):
        self.struct = struct
        self.value = value
        self.line = line
    
    def __repr__(self) -> str:
        if self.value or self.value == 0: return f"{self.struct}: {self.value}"
        return f"{self.struct}"

# Creating the number token, it can have more than one digit
def make_number(current_char: str, code: str, position: int, num_line: int) -> (Token, int):
    num = ""
    dot = False

    if current_char == " ": position += 1; current_char = code[position];
    while current_char != COMMENT and current_char in DIGITS + '.':
        if current_char == '.':
            if dot: break;
            num += '.'
            dot = True
        else:
            num += current_char

        position += 1
        current_char = code[position]

    token_number = Token(FLOAT, float(num), num_line) if dot else Token(INT, int(num), num_line)
    return token_number, position - 1

# Creating a string
def make_string(current_char: str, code: str, position: int, num_line: int) -> (Token, int):
    string = '"'
    position += 1
    current_char = code[position]

    while current_char != COMMENT:
        string += current_char
        if current_char == '"': break

        position += 1
        current_char = code[position]

    if string[0] == '"' and string[-1] == '"':
        return Token(STRING, string[1:-1], num_line), position
    else:
        set_line(num_line)
        raise SyntaxError('Expected a \'"\'')


# Creating tokens for the language's reserved words, usually to create variables or functions.
def make_identifier(current_char: str, code: str, position: int, num_line: int) -> (Token, int):
    id_str = ""

    while current_char != COMMENT and current_char in LETTERS + DIGITS + '_':
        id_str += current_char
        position += 1
        current_char = code[position]

    position -= 1
    id_str_upper = id_str.upper()

    # VARIABLES
    if id_str_upper == NUMBER:
        return Token(KEYWORD, NUMBER, num_line), position
    elif id_str_upper == STRING:
        return Token(KEYWORD, STRING, num_line), position
    elif id_str_upper == BOOL:
        return Token(KEYWORD, BOOL, num_line), position
    elif id_str == TRUE or id_str == FALSE:
        return Token(BOOLEAN, id_str, num_line == TRUE), position
    elif id_str_upper == FUNCTION:
        return Token(KEYWORD, FUNCTION, num_line), position
    elif id_str_upper == DOES:
        return Token(KEYWORD, DOES, num_line), position
    elif id_str_upper == RETURN:
        return Token(KEYWORD, RETURN, num_line), position
    elif id_str_upper == END:
        return Token(KEYWORD, END, num_line), position
    elif id_str_upper == GLOBAL:
        return Token(KEYWORD, GLOBAL, num_line), position
    elif id_str_upper == BREAK:
        return Token(KEYWORD, BREAK, num_line), position
    elif id_str_upper == CONTINUE:
        return Token(KEYWORD, CONTINUE, num_line), position

    
    # LOGIC OPERATORS
    if id_str_upper == AND:
        return Token(AND, None, num_line), position
    elif id_str_upper == OR:
        return Token(OR, None, num_line), position
    elif id_str_upper == NOT:
        return Token(NOT, None, num_line), position
    
    # STATEMENT
    if id_str_upper == IF:
        return Token(STATEMENT, IF, num_line), position
    elif id_str_upper == THEN:
        return Token(STATEMENT, THEN, num_line), position
    elif id_str_upper == ELSE:
        return Token(STATEMENT, ELSE, num_line), position
    elif id_str_upper == ELIF:
        return Token(STATEMENT, ELIF, num_line), position

    # WHILE
    if id_str_upper == WHILE:
        return Token(STATEMENT, WHILE, num_line), position
    
    # FOR
    if id_str_upper == FOR:
        return Token(STATEMENT, FOR, num_line), position
    elif id_str_upper == TO:
        return Token(STATEMENT, TO, num_line), position
    

    # DEAFULT
    return Token(IDENTIFIER, id_str, num_line), position

def next_char(code: str, position: int): return code[position+1], position+1

# LEXER <-> SYNTACTIC ANALYSIS
# Walk through the code to translate it into tokens.
# Remove spaces and tabs and add a ";" to know when it ends
def lexer(code: str) -> list:
    ENDFILE = "¿"
    code += ENDFILE
    tokens = []
    position = 0
    num_line = 0
    current_char = code[position]

    while current_char != ENDFILE:
        if current_char == COMMENT:
            while current_char != ENDFILE:
                current_char, position = next_char(code, position)
                if current_char == "\n": num_line += 1; break
            if current_char == ENDFILE: break
        elif current_char in ' \t':
            current_char, position = next_char(code, position)
            continue
        elif current_char == '\n':
            num_line += 1
            tokens.append(Token(NEW_LINE, None, num_line))
        elif current_char in DIGITS:
            token_number, position = make_number(current_char, code, position, num_line)
            tokens.append(token_number)
        elif current_char in LETTERS:
            token, position = make_identifier(current_char, code, position, num_line)
            tokens.append(token)
        elif current_char == '"':
            token_string, position = make_string(current_char, code, position, num_line)
            tokens.append(token_string)
        elif current_char == '=':
            if code[position+1] == '=':
                current_char, position = next_char(code, position)
                tokens.append(Token(COMPARISON, None, num_line))
            else:
                tokens.append(Token(EQ, None, num_line))
        elif current_char == '+':
            if code[position+1] == '=':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(EQ_ADD, None, num_line))
                continue
            tokens.append(Token(ADD, None, num_line))
        elif current_char == '-':
            if code[position+1] == '>':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(KEYWORD, ALT_DOES, num_line))
                continue
            if code[position+1] == '=':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(EQ_SUB, None, num_line))
                continue
            if position > 0:
                if tokens[-1].struct in (FLOAT, INT, IDENTIFIER):
                    current_char, position = next_char(code, position)
                    tokens.append(Token(SUB, None, num_line))
                    continue
            current_char, position = next_char(code, position)
            token_number, position = make_number(current_char, code, position, num_line)
            token_number.value = -1 * token_number.value
            tokens.append(token_number)
        elif current_char == '*':
            if code[position+1] == '=':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(EQ_MUL, None, num_line))
                continue
            tokens.append(Token(MUL, None, num_line))
        elif current_char == '/':
            if code[position+1] == '=':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(EQ_DIV, None, num_line))
                continue
            tokens.append(Token(DIV, None, num_line))
        elif current_char == '%':
            if code[position+1] == '=':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(EQ_MOD, None, num_line))
                continue
            tokens.append(Token(MOD, None, num_line))
        elif current_char == '^':
            if code[position+1] == '=':
                current_char, position = next_char(code, position + 1)
                tokens.append(Token(EQ_POW, None, num_line))
                continue
            tokens.append(Token(POW, None, num_line))
        elif current_char == '!' and code[position+1] == '=':
            current_char, position = next_char(code, position)
            tokens.append(Token(NOT_EQUAL, None, num_line))
        elif current_char == '<':
            if code[position+1] == '=':
                current_char, position = next_char(code, position)
                tokens.append(Token(LOWER_OR_EQUAL, None, num_line))
            else:
                tokens.append(Token(LOWER_THAN, None, num_line))
        elif current_char == '>':
            if code[position+1] == '=':
                current_char, position = next_char(code, position)
                tokens.append(Token(GREATER_OR_EQUAL, None, num_line))
            else:
                tokens.append(Token(GREATER_THAN, None, num_line))
        elif current_char == "(":
            tokens.append(Token(LEFTPAREN, None, num_line))
        elif current_char == ")":
            tokens.append(Token(RIGHTPAREN, None, num_line))
        elif current_char == ',':
            tokens.append(Token(KEYWORD, COMMA, num_line))
        elif current_char == ':':
            tokens.append(Token(KEYWORD, ARG_TYPE, num_line))
        else:
            set_line(num_line)
            raise SyntaxError(f"Unexpected caracter: \'{current_char}\'")
        
        current_char, position = next_char(code, position)
    
    return tokens


# Parser <-> Analizador sintáctico
# Make the Abstract Syntax Tree
# Order AST: AND Operator -> OR Operator -> Logic comparisons ->
#       -> Addition and Subtraction -> Multiplication and Division -> Power 
def parser(tokens: list, in_function: bool = False, local_variables: dict = None) -> tuple:
    global global_variables

    ast_variables = local_variables if in_function and local_variables else global_variables

    if not tokens:
        return None
    
    operators = (
        (AND, OR),
        (COMPARISON, NOT_EQUAL, LOWER_THAN, GREATER_THAN, LOWER_OR_EQUAL, GREATER_OR_EQUAL),
        (ADD, SUB),
        (MUL, DIV, MOD),
        (POW),
    )

    def create_ast(operator_group: int = 0) -> tuple:
        nonlocal tokens
        
        if operator_group == 5:
            return non_operators()

        left = create_ast(operator_group + 1)

        while tokens and tokens[0].struct in operators[operator_group]:
            operator = tokens.pop(0)
            right = create_ast(operator_group + 1)
            left = (operator.struct, left, right)
        return left

    # Non operators like functions, variables, strings, numbers, booleans, etc...
    def non_operators() -> str:
        nonlocal tokens
        token = tokens.pop(0)
        set_line(token.line)
        
        # If it's a number, boolean or string return itself
        if token.struct in (INT, FLOAT, BOOLEAN, STRING):
            return token.value
        # If it's a identifier (variable) check if it's calling its value or assigning itself
        elif token.struct == IDENTIFIER:
            if tokens:
                if token.value in bult_in_function: # Check if it's a bult in function
                    return execute_builtin_funcs(token.value)
                elif token.value in ast_variables: # check if it's calling itself
                    if ast_variables[token.value][0] in (FUNCTION, FUNCTION_RETURNED): # if it's a functions, execute itself
                        if tokens[0].struct == LEFTPAREN:
                            return execute_function(token.value)

                    return ast_variables[token.value][1]
                elif token.value in global_variables:
                    if global_variables[token.value][0] in (FUNCTION, FUNCTION_RETURNED): # if it's a functions, execute itself
                        if tokens[0].struct == LEFTPAREN:
                            return execute_function(token.value)
                    
                    raise ValueError(f"Non defined variable: \'{token.value}\'")
                else:
                    set_line(token.line)
                    raise ValueError(f"Non defined variable: \'{token.value}\'")
            elif token.value in ast_variables:
                return ast_variables[token.value][1]
            else:
                set_line(token.line)
                raise ValueError(f"Non defined variable: \'{token.value}\'")
        elif token.value == GLOBAL:
            sub_token = tokens.pop(0)
            if sub_token.value in (NUMBER, BOOLEAN, STRING) and tokens[0].struct == IDENTIFIER:
                variable = tokens.pop(0)
                if tokens.pop(0).struct == EQ:
                    global_variables[variable.value] = (variable.value, create_ast())
                    if tokens:
                        if tokens[0].struct == END_LINE: tokens.pop(0)
                        return parser(tokens, in_function, local_variables)
                else:
                    set_line(token.line)
                    raise SyntaxError("Equal sign (=) was expected")
            elif sub_token.struct == IDENTIFIER and sub_token.value in global_variables:
                if tokens:
                    if tokens[0].struct == EQ:
                        tokens.insert(0, sub_token)
                        assignment(global_variables[sub_token.value][0], True)
                        if tokens:
                            if tokens[0].struct == END_LINE: tokens.pop(0)
                            parser(tokens, in_function, local_variables)
                        # return global_variables[sub_token.value][1]
                    else:
                        return global_variables[sub_token.value][1]
                else:
                    return global_variables[sub_token.value][1]
            else:
                set_line(token.line)
                raise SyntaxError("Global variable definition id not defined correctly")
        elif token.struct == LEFTPAREN:
            result = create_ast()
            tt = tokens.pop(0)

            if tt.value == ',':
                result += create_ast()
            elif tt.struct != ')':
                set_line(tt.line)
                raise SyntaxError("A closing parenthesis was expected")
            
            return result
        elif token.struct == NOT:
            return (NOT, None, create_ast())
        elif token.struct == NEW_LINE:
            parser(tokens, in_function, local_variables)
        elif token.struct == END_LINE:
            if in_function:
                return parser(tokens, in_function, local_variables)

            parser(tokens, in_function, local_variables)
        elif token.value == END:
            if tokens:
                if tokens[0].struct == END_LINE: tokens.pop(0)
                parser(tokens, in_function, local_variables)
        elif token.value == RETURN:
            return create_ast()
        elif token.value == BREAK:
            return BREAK
        elif token.value == CONTINUE:
            return CONTINUE
        else:
            set_line(token.line)
            raise SyntaxError(f"Unexpected symbol: {token.value if token.value else token.struct}")

    # IF Statement
    def if_statement() -> any:
        nonlocal tokens
        line = tokens[0].line
        condition = create_ast()  # Condición para evaluar el IF-THEN
    
        if condition == None:
            return None
        
        if not tokens:
            set_line(line)
            raise SyntaxError("THEN STATEMENT was expected")
        
        multi_line = False
        if not tokens: set_line(line); raise SyntaxError("THEN STATEMENT was expected")
        if tokens.pop(0).value == THEN:
            if tokens[0].struct == NEW_LINE: 
                multi_line = True
                tokens.pop(0)
            inside_if_tokens = []
            
            while tokens:
                token = tokens.pop(0)
                if token.value == END: break
                if token.struct == END_LINE and not inside_if_tokens: continue

                if token.value in (IF, FOR, WHILE): 
                    new_tokens = check_substatements(tokens, token)
                    inside_if_tokens += new_tokens
                    continue

                if token.value in (ELSE, ELIF): 
                    tokens.insert(0, token)
                    break 

                if token.struct in (NEW_LINE, END_LINE): 
                    if not multi_line: break
                    if tokens[0].value in (ELSE, ELIF) or tokens[0].value == END: break
                    inside_if_tokens.append(Token(END_LINE, None, token.line))
                    continue

                inside_if_tokens.append(token)

            if evaluate(condition):
                if tokens:
                    if tokens[0].value in (ELSE, ELIF):
                        while tokens:
                            if tokens[0].value == END: tokens.pop(0); break
                            if tokens[0].struct == NEW_LINE: 
                                if not multi_line: break
                            tokens.pop(0)
                
                return parser(inside_if_tokens, in_function, local_variables)
            else:
                if not tokens: return None
                token = tokens.pop(0)
                if token.value == ELSE:
                    inside_else_tokens = []
                    while tokens:
                        token = tokens.pop(0)
                        if token.struct == END_LINE and not inside_else_tokens: continue
                        if token.value in (IF, FOR, WHILE): 
                            new_tokens = check_substatements(tokens, token)
                            inside_else_tokens += new_tokens
                            continue
                        if token.value == END: break
                        if token.struct == NEW_LINE: 
                            if not multi_line: break
                            if tokens[0].value == END: tokens.pop(0); break
                            inside_if_tokens.append(Token(END_LINE, None, token.line))
                            continue
                        
                        inside_else_tokens.append(token)

                    return parser(inside_else_tokens, in_function, local_variables)
                
                if token.value == ELIF:
                    return if_statement()
                
                tokens.insert(0, token)
                return parser(tokens, in_function, local_variables)
        else:
            set_line(line)
            raise SyntaxError("THEN STATEMENT was expected")
    
    # While loop statement
    def while_statement() -> any:
        nonlocal tokens
        line = tokens[0].line
        aux_tokens = tokens.copy()
        condition = create_ast()
        aux_expresion = []

        if not tokens: set_line(line); raise SyntaxError("THEN STATEMENT was expected")
        if tokens.pop(0).value == THEN:
            multi_line = False
            if tokens[0].struct == NEW_LINE:
                tokens.pop(0)
                multi_line = True
            
            while tokens:
                token = tokens.pop(0)
                # Checking if are a substatement
                if token.value in (IF, FOR, WHILE): 
                    new_tokens = check_substatements(tokens, token)
                    aux_expresion += new_tokens
                    continue
                if token.struct == NEW_LINE: 
                    if not multi_line: break
                    if tokens[0].value == END: tokens.pop(0); break
                    aux_expresion.append(Token(END_LINE, None, token.line))
                    continue
                if token.value == END: break
                aux_expresion.append(token)
            final_tokens = tokens.copy()

            res = None
            while True:
                tokens = aux_tokens.copy()
                condition = create_ast()
                if not evaluate(condition): break
                expresion = aux_expresion.copy()
                res = parser(expresion, in_function, local_variables)
                if res == CONTINUE: continue
                if res and in_function: tokens = []; return res
                if res == BREAK: break
        else:
            set_line(line)
            raise SyntaxError("THEN STATEMENT was expected")
        
        tokens = final_tokens.copy()

    # For loop statement
    def for_statement() -> any:
        nonlocal tokens
        
        for_variable = tokens.pop(0)

        if for_variable.struct == IDENTIFIER:
            token = tokens.pop(0)
            if token.struct == EQ:
                value = create_ast() 
                if type(evaluate(value)) not in (float, int): 
                    set_line(token.line)
                    raise ValueError(f"{for_statement.value} expected to be a number")
                ast_variables[for_variable.value] = (NUMBER, value) 
                if tokens.pop(0).value != TO: 
                    set_line(token.line)
                    raise SyntaxError("TO STATEMENT was expected")
            elif token.struct == STATEMENT and token.value == TO:
                value = 0
                ast_variables[for_variable.value] = (NUMBER, 0)
            else:
                set_line(token.line)
                raise SyntaxError("Invalid for statement syntax")

        to_variable_tokens = []
        while tokens:
            token = tokens.pop(0)
            if token.struct == NEW_LINE: set_line(token.line); raise SyntaxError("Expected value on TO statement")
            if token.value == THEN: 
                tokens.insert(0, token)
                break
            to_variable_tokens.append(token)

        aux_tokens = tokens.copy()
        tokens = to_variable_tokens
        line = tokens[0].line
        to_variable = create_ast()
        tokens = aux_tokens
        
        multi_line = False
        if not tokens: set_line(line); raise SyntaxError("THEN STATEMENT was expected")
        if tokens.pop(0).value == THEN:
            if tokens[0].struct == NEW_LINE:
                tokens.pop(0)
                multi_line = True
            aux_for_body = []

            while tokens:
                token = tokens.pop(0)
                # Checking if are a substatement
                if token.value in (IF, FOR, WHILE): 
                    new_tokens = check_substatements(tokens, token)
                    aux_for_body += new_tokens
                    continue
                
                if token.struct == NEW_LINE: 
                    if not multi_line: break
                    if tokens[0].value == END: tokens.pop(0); break
                    aux_for_body.append(Token(END_LINE, None, token.line))
                    continue

                if token.value == END: break
                aux_for_body.append(token)

            for_from = int(evaluate(value))
            for_to = int(evaluate(to_variable)) + 1

            #if tokens[0].value == END: tokens.pop(0)
            for i in range(for_from, for_to):
                if i == for_to: break
                for_body = aux_for_body.copy()
                ast_variables[for_variable.value] = (NUMBER, i)
                res = parser(for_body, in_function, local_variables)
                if res:
                    tokens = []
                    return res
        else:
            set_line(line)
            raise SyntaxError("THEN STATEMENT was expected")

    def check_substatements(tokens: list, first_token: Token, check_function: bool = False):
            aux_tokens = [first_token]
            find_end = False
            return_token = False
            while tokens:
                aux_token = tokens.pop(0)
                if aux_token.value in (IF, FOR, WHILE):
                    new_tokens = check_substatements(tokens, aux_token)
                    aux_tokens += new_tokens
                    continue
                if aux_token.value == THEN:
                    if tokens[0].struct == NEW_LINE:
                        find_end = True
                if aux_token.struct == NEW_LINE and not find_end: 
                    aux_tokens.append(aux_token)
                    break
                if check_function and token.value == RETURN: return_token = True
                if aux_token.value == END: aux_tokens.append(aux_token); break
                aux_tokens.append(aux_token)
            
            if check_function: return aux_tokens, return_token
            return aux_tokens

    # Declaration and reassignment of variables
    def assignment(struct: str, global_var: bool = False) -> str:
        nonlocal tokens
        
        identifier_token = tokens.pop(0)

        if identifier_token.struct == IDENTIFIER:
            if tokens.pop(0).struct == EQ:
                expression_tokens = []
                while tokens:
                    token = tokens.pop(0)
                    if token.struct == NEW_LINE: break
                    elif token.struct == END_LINE: break
                    expression_tokens.append(token)
                aux_tokens = tokens.copy()
                tokens = expression_tokens
                line = tokens[0].line
                if tokens[0].struct == STATEMENT and tokens[0].value == IF:
                    tokens.pop(0)
                    expression = if_statement()
                elif tokens[0].struct == IDENTIFIER and tokens[0].value in bult_in_function:
                    expression = execute_builtin_funcs(tokens.pop(0).value)
                elif tokens[0].struct == IDENTIFIER: 
                    if tokens[0].value not in ast_variables: 
                        set_line(tokens[0].line)
                        raise ValueError(f"Non defined variable: \'{tokens[0].value}\'")
                    try:
                        if tokens[1].struct == LEFTPAREN:
                            expression = execute_function(tokens.pop(0).value)
                        else:
                            expression = create_ast()
                    except IndexError:
                        expression = create_ast()
                else:
                    expression = create_ast()
                
                tokens = aux_tokens
                result = evaluate(expression)
                if struct == STRING and type(result) != str:
                    type_error = "boolean" if type(result) == bool else "number"
                    set_line(line)
                    raise ValueError(f"Cannot assign a {type_error} to a string")
                else:
                    if struct != STRING and type(result) == str:
                        type_error = "boolean" if struct == BOOL else "number"
                        set_line(line)
                        raise ValueError(f"Cannot assign a string to a {type_error}")
                
                if struct == BOOL and type(result) in (int, float, str):
                    set_line(line)
                    raise ValueError("Can't assign a number to a boolean")
                else:
                    if struct != BOOL and type(result) == bool:
                        set_line(line)
                        raise ValueError("Can't assign a boolean to a number")
                if not global_var:
                    ast_variables[identifier_token.value] = (struct, expression)
                else:
                    global_variables[identifier_token.value] = (struct, expression)
            else:
                set_line(identifier_token.line)
                raise SyntaxError("An equal sign '=' was expected for assignment")
        else:
            set_line(identifier_token.line)
            raise SyntaxError("Identifier expected for assignment")
    # Define a function
    def define_function() -> any:
        nonlocal tokens
        function_token = tokens.pop(0)
        function_name = function_token.value
        function_body = []
        function_arguments = []

        if function_name not in global_variables:
            token = tokens.pop(0)
            if token.struct == LEFTPAREN:
                while tokens:
                    arg = tokens.pop(0)
                    if arg.struct == IDENTIFIER:
                        if tokens.pop(0).value == ARG_TYPE:
                            function_arguments.append((tokens.pop(0).value, arg.value))
                        else:
                            set_line(arg.line)
                            raise SyntaxError(f"Function argument '{arg.value}' don't typed")
                    elif arg.struct == KEYWORD and arg.value == COMMA:
                        continue
                    elif arg.struct == RIGHTPAREN:
                        break
                    else:
                        set_line(arg.line)
                        raise SyntaxError(f"Invalid argument in function definition: {arg.value}")
                
                try:
                    if tokens[0].value in (DOES, ALT_DOES): tokens.pop(0)
                except IndexError:
                    set_line(arg.line)
                    raise SyntaxError("Empty function")
                
                multi_line = False
                single_line = False
                function_type = FUNCTION
                if tokens[0].struct == NEW_LINE: 
                    tokens.pop(0)
                else:
                    single_line = True
                    tokens.insert(0, Token(KEYWORD, RETURN, tokens[0].line))
                
                while tokens:
                    token = tokens.pop(0)
                    if token.value in (IF, FOR, WHILE): 
                        new_tokens, return_token = check_substatements(tokens, token), True
                        if return_token: function_type = FUNCTION_RETURNED
                        function_body += new_tokens
                        continue

                    if token.value == END: break
                    if token.struct == NEW_LINE:
                        multi_line = True
                        if single_line:
                            if tokens[0].value == END: token = tokens.pop(0)
                            break
                        continue

                    if multi_line: 
                        multi_line = False
                        function_body.append(Token(END_LINE, None, token.line))
                    
                    if token.struct == KEYWORD and token.value == RETURN: function_type = FUNCTION_RETURNED
                    function_body.append(token)

                ast_variables[function_name] = (function_type, function_arguments, function_body)
            elif token.struct == EQ:
                token = tokens.pop(0)
                if token.struct == IDENTIFIER and token.value in global_variables:
                    if global_variables[token.value][0] in (FUNCTION, FUNCTION_RETURNED):
                        global_variables[function_name] = global_variables[token.value]
                else:
                    set_line(token.line)
                    raise SyntaxError(f"Invalid function definition, unexpected '{token.value}' function")
            else:
                set_line(token.line)
                raise SyntaxError("Invalid function definition, expected a '('")
        else:
            set_line(function_token.line)
            raise SyntaxError("Invalid function name or already defined")
    
    # Executing a function
    def execute_function(name_function):
        def get_type(type_var) -> str:
            if type_var in (int, float): return NUMBER
            if type_var == str: return STRING
            return BOOL

        def get_name_type(type_var) -> str:
            if type_var == NUMBER: return "number"
            if type_var == BOOL: return BOOLEAN.lower()
            return STRING.lower()

        nonlocal tokens
        line = tokens.pop(0).line
        called_arguments = []
        while tokens:
            if tokens[0].struct == RIGHTPAREN: 
                line = tokens[0].line
                break

            arg = create_ast()
            called_arguments.append((get_type(type(evaluate(arg))), arg))
            token = tokens.pop(0)
            if token.value != COMMA:
                line = token.line
                break
        
        local_arguments = {}
        function_arguments = global_variables[name_function][1]
        if len(called_arguments) == len(function_arguments):
            for i in range(len(called_arguments)):
                if function_arguments[i][0] != called_arguments[i][0]:
                    set_line(line)
                    raise SyntaxError(f"Expected a {get_name_type(function_arguments[i][0])} not a {get_name_type(called_arguments[i][0])} on function calling")
                local_arguments[function_arguments[i][1]] = (function_arguments[i][0], called_arguments[i][1])
            
            if FUNCTION_RETURNED == global_variables[name_function][0]:
                return parser(global_variables[name_function][2].copy(), in_function=True, local_variables=local_arguments)
            else:
                parser(global_variables[name_function][2].copy(), in_function=True, local_variables=local_arguments)
        else:
            set_line(line)
            raise TypeError("Invalid numbers of arguments on function")
        
    # Executing a bult in function
    def execute_builtin_funcs(name_function: str):
        nonlocal tokens
        line = tokens.pop(0).line
        args = []
        token = tokens.pop(0)
        while tokens:
            if token.struct == RIGHTPAREN: 
                line = token.line
                break
            if token.value == COMMA: token = tokens.pop(0); continue
            if token.struct == IDENTIFIER:
                if token.value in global_variables:
                    if global_variables[token.value][0] in (FUNCTION, FUNCTION_RETURNED):
                        if not tokens: 
                            args.append(None)
                        elif tokens[0].struct == LEFTPAREN:
                            args.append(evaluate(execute_function(token.value)))
                        else:
                            args.append(None)
                        token = tokens.pop(0)
                        continue
            
            tokens.insert(0, token)
            arg = evaluate(create_ast())
            token = tokens.pop(0)
            args.append(arg)
        
        match name_function:
            case 'print':
                for arg in args:
                    print(f"{arg}", end=" ")
                
            case 'println':
                for arg in args:
                    print(f"{arg}", end=" ")
                
                print("\n", end="")
            case 'input':
                return input(args[0]) if args else input()
            case 'input_num':
                try:
                    ans = input(args[0]) if args else input()
                    return float(ans)
                except ValueError:
                    set_line(line)
                    raise ValueError(f"Impossible convert '{ans}' to a number")
            case 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            case 'exit':
                exit()
            case 'is_a_number':
                if len(args) == 1:
                    return True if type(args[0]) == int else False
                else:
                    set_line(line)
                    raise TypeError("Invalid numbers of arguments on function")
            case 'is_a_string':
                if len(args) == 1:
                    return True if type(args[0]) == str else False
                else:
                    set_line(line)
                    raise TypeError("Invalid numbers of arguments on function")
            case 'is_a_function':
                # If args[0] == None then the argument is a Function
                if len(args) == 1:
                    return True if not args[0] else False
                else:
                    set_line(line)
                    raise TypeError("Invalid numbers of arguments on function")
            case 'sqrt':
                set_line(line)
                if len(args) == 1:
                    return sqrt(args[0])
                else:
                    set_line(line)
                    raise TypeError("Invalid numbers of arguments on function")

    # Main parser logic
    while tokens:
        token = tokens.pop(0)
        # Declarate variables
        if token.struct == KEYWORD and token.value == FUNCTION:
            define_function()
        elif token.struct == KEYWORD and token.value in (NUMBER, BOOL, STRING):
            if tokens[0].value in ast_variables:
                set_line(tokens[0].line)
                raise SyntaxError(f"Variable '{tokens[0].value}' already exists")
            assignment(token.value)
        # Variable redeclaration and type checking (It is a strongly typed language)
        elif token.struct == IDENTIFIER and token.value in ast_variables and tokens:
            if ast_variables[token.value][0] in (FUNCTION, FUNCTION_RETURNED):
                if tokens[0].struct != LEFTPAREN:
                    return ast_variables[token.value]
                
                execute_function(token.value)
            elif tokens[0].struct == EQ:
                tokens.insert(0, token)
                assignment(ast_variables[token.value][0])
            elif "EQ_" in tokens[0].struct:
                    operation = tokens[0].struct
                    tokens[0] = Token(EQ, None, tokens[0].line)
                    tokens.insert(1, token)
                    tokens.insert(2, Token(operation[3::], None, tokens[0].line))
                    tokens.insert(0, token)
                    assignment(ast_variables[token.value][0])
            else:
                tokens.insert(0, token)
                return create_ast()
        elif token.struct == IDENTIFIER and token.value in bult_in_function and tokens:
            if tokens[0].struct == LEFTPAREN:
                execute_builtin_funcs(token.value)
            else:
                set_line(tokens[0].line)
                raise TypeError("Opening parenthesis was expected")
        elif token.struct == STATEMENT and token.value == IF:
            res = if_statement()
            if res: return res
                # parser(tokens, in_function, local_variables)
        elif token.struct == STATEMENT and token.value == WHILE:
            res = while_statement()
            if res: return res
        elif token.struct == STATEMENT and token.value == FOR:
            res = for_statement()
            if res: return res
        elif token.struct == END_LINE:
            continue
        else:
            tokens.insert(0, token)
            return create_ast()

def evaluate(ast: tuple) -> any:
    if not ast and ast != 0:
        return None

    if type(ast) in (str, int, float, bool):
        return ast

    if type(ast[1]) == tuple: 
        left = evaluate(ast[1])
    elif ast[1] in (TRUE, FALSE):
        left = True if ast[1] else False
    else:
        left = ast[1]
    
    if type(ast[2]) == tuple:
        right = evaluate(ast[2])
    elif ast[2] in (TRUE, FALSE):
        right = True if ast[2] == TRUE else False
    else:
        right = ast[2]

    match (ast[0]):
        case 'ADD':
            return left + right
        case 'SUB':
            return left - right
        case 'MUL':
            return left * right
        case 'DIV':
            try:
                return left / right
            except ZeroDivisionError:
                return nan if left == 0 else inf
        case 'MOD':
            try:
                return left % right
            except ZeroDivisionError:
                return nan
        case 'POWER':
            return left ** right
        case 'COMPARISION':
            return left == right
        case 'NOT_EQUAL':
            return left != right
        case 'LOWER_THAN':
            return left < right
        case 'GREATER_THAN':
            return left > right
        case 'LOWER_OR_EQUAL_THAN':
            return left <= right
        case 'GREATER_OR_EQUAL_THAN':
            return left >= right
        case 'NOT':
            return not right
        case 'AND':
            return left and right
        case 'OR':
            return left or right

def execute(code: str) -> any:
    try:
        lines = code.split("\n")
        tokens = lexer(code)
        parser(tokens)
    except Exception as error:
        print(f"\n{type(error).__name__} on line {get_num_line()}: {error}")
        print(f"{lines[get_num_line()-1]}")

def debug(code: str) -> any:
    print("----- TOKENS ------")
    tokens = lexer(code)
    print(tokens)
    print("----- RESULTS -----")
    parser(tokens)

# Only for testing
if __name__ == '__main__':
    sys.argv.pop(0)

    try:
        file = open(sys.argv[-1])
    except:
        file = open('test.lx')

    try:
        startTime = time.time()
        code = file.read()
        debug(code) if '--debug' in sys.argv else execute(code)
        if '--time' in sys.argv: print(f"\n\nExecuting time: {(time.time() - startTime)*1000:.2f} miliseconds or {(time.time() - startTime):.5f} seconds")
    except KeyboardInterrupt:
        print(f"\n\nKeyboard Interrupt - Executing time: {(time.time() - startTime)*1000:.2f} miliseconds or {(time.time() - startTime):.5f} seconds")
