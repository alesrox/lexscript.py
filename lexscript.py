import os
import sys
from string import ascii_letters

# CONSTANTS
DIGITS = "0123456789"
LETTERS = ascii_letters
LETERS_NUMBER = LETTERS + DIGITS

# TOKENS
# DATATYPE TOKENS
INT		         = 'INT'
FLOAT            = 'FLOAT'
BOOLEAN          = 'BOOLEAN'
# SPECIAL TOKENS
STATEMENT        = 'STATEMENT'
IDENTIFIER       = 'IDENTIFIER'
KEYWORD          = 'KEYWORD'
EQ               = 'EQ'
LEFTPAREN        = '(' #'LEFT_PARENTHESIS'
RIGHTPAREN       = ')' #'RIGHT_PARENRHESIS'
EOF		         = 'EOF'
COMMENT          = '#'
COMMA            = 'COMMA'
END_LINE         = 'END_LINE'
NEW_LINE         = 'NEW_LINE'
# OPERATION TOKENS
ADD              = 'ADD'
SUB              = 'SUB'
MUL              = 'MUL'
DIV              = 'DIV'
POW              = 'POWER'
# LOGIC TOKENS
NOT              = 'NOT'
AND              = 'AND'
OR               = 'OR'
COMPARISON       = 'COMPARISION'
NOT_EQUAL        = 'NOT_EQUAL'
LOWER_THAN       = 'LOWER_THAN'
LOWER_OR_EQUAL   = 'LOWER_OR_EQUAL_THAN'
GREATER_THAN     = 'GREATER_THAN'
GREATER_OR_EQUAL = 'GREATER_OR_EQUAL_THAN'
# STATEMENTS    
IF               = 'IF'
THEN             = 'THEN'
ELIF             = 'ELIF'
ELSE             = 'ELSE'
WHILE            = 'WHILE'
FOR              = 'FOR'
TO               = 'TO'
END              = 'END'
# KEYWORDS    
FUNCTION         = 'FUNCTION'
DOES             = 'DOES'
ALT_DOES         = '->'
RETURN           = 'RETURN'
GLOBAL           = 'GLOBAL'
NUMBER           = 'VAR'
STRING           = 'STRING'
BOOL             = 'BOOL'
TRUE             = 'True'
FALSE            = 'False'      

# Special Groups
LOGIC = (AND, OR, COMPARISON, NOT_EQUAL, LOWER_THAN, GREATER_THAN, LOWER_OR_EQUAL, GREATER_OR_EQUAL)
LOGIC_COMPARISONS = (COMPARISON, NOT_EQUAL, LOWER_THAN, GREATER_THAN, LOWER_OR_EQUAL, GREATER_OR_EQUAL)

global_variables = {}
local_variables = {}
bult_in_function = ['print', 'println', 'input', 'input_num', 'clear', 'exit', 'is_a_number', 'is_a_string', 'is_a_function']
num_line = 0

def new_num_line():
    global num_line
    num_line += 1

def get_num_line():
    global num_line
    return num_line

class Token:
    def __init__(self, struct, value = None):
        self.struct = struct
        self.value = value
    
    def __repr__(self) -> str:
        if self.value or self.value == 0: return f"{self.struct}: {self.value}"
        return f"{self.struct}"

# Creating the number token, it can have more than one digit
def make_number(current_char: str, code: str, position: int) -> (Token, int):
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

    token_number = Token(FLOAT, float(num)) if dot else Token(INT, int(num))
    return token_number, position - 1

# Creating a string
def make_string(current_char: str, code: str, position: int) -> (Token, int):
    string = '"'
    position += 1
    current_char = code[position]

    while current_char != COMMENT:
        string += current_char
        if current_char == '"': break

        position += 1
        current_char = code[position]

    if string[0] == '"' and string[-1] == '"':
        return Token(STRING, string[1:-1]), position
    else:
        raise SyntaxError('Expected a \'"\'')


# Creating tokens for the language's reserved words, usually to create variables or functions.
def make_identifier(current_char: str, code: str, position: int) -> (Token, int):
    id_str = ""

    while current_char != COMMENT and current_char in LETTERS + '_':
        id_str += current_char
        position += 1
        current_char = code[position]

    position -= 1
    id_str_upper = id_str.upper()

    # VARIABLES
    if id_str_upper == NUMBER:
        return Token(KEYWORD, NUMBER), position
    elif id_str_upper == STRING:
        return Token(KEYWORD, STRING), position
    elif id_str_upper == BOOL:
        return Token(KEYWORD, BOOL), position
    elif id_str == TRUE or id_str == FALSE:
        return Token(BOOLEAN, id_str == TRUE), position
    elif id_str_upper == FUNCTION:
        return Token(KEYWORD, FUNCTION), position
    elif id_str_upper == DOES:
        return Token(KEYWORD, DOES), position
    elif id_str_upper == RETURN:
        return Token(KEYWORD, RETURN), position
    elif id_str_upper == END:
        return Token(KEYWORD, END), position
    elif id_str_upper == GLOBAL:
        return Token(KEYWORD, GLOBAL), position

    
    # LOGIC OPERATORS
    if id_str_upper == AND:
        return Token(AND), position
    elif id_str_upper == OR:
        return Token(OR), position
    elif id_str_upper == NOT:
        return Token(NOT), position
    
    # STATEMENT
    if id_str_upper == IF:
        return Token(STATEMENT, IF), position
    elif id_str_upper == THEN:
        return Token(STATEMENT, THEN), position
    elif id_str_upper == ELSE:
        return Token(STATEMENT, ELSE), position
    elif id_str_upper == ELIF:
        return Token(STATEMENT, ELIF), position

    # WHILE
    if id_str_upper == WHILE:
        return Token(STATEMENT, WHILE), position
    
    # FOR
    if id_str_upper == FOR:
        return Token(STATEMENT, FOR), position
    elif id_str_upper == TO:
        return Token(STATEMENT, TO), position
    

    # DEAFULT
    return Token(IDENTIFIER, id_str), position

def next_char(code: str, position: int): return code[position+1], position+1

# LEXER <-> SYNTACTIC ANALYSIS
# Walk through the code to translate it into tokens.
# Remove spaces and tabs and add a ";" to know when it ends
def lexer(code: str) -> list:
    ENDFILE = "¿"
    code += ENDFILE
    tokens = []
    position = 0
    current_char = code[position]

    while current_char != ENDFILE:
        if current_char == COMMENT:
            while current_char != ENDFILE:
                current_char, position = next_char(code, position)
                if current_char == "\n": break
            
            if current_char == ENDFILE: break
        elif current_char in ' \t':
            position += 1
            current_char = code[position]
            continue
        elif current_char == '\n':
            tokens.append(Token(NEW_LINE))
        elif current_char in DIGITS:
            token_number, position = make_number(current_char, code, position)
            tokens.append(token_number)
        elif current_char in LETTERS:
            token, position = make_identifier(current_char, code, position)
            tokens.append(token)
        elif current_char == '"':
            token_string, position = make_string(current_char, code, position)
            tokens.append(token_string)
        elif current_char == '=':
            if code[position+1] == '=':
                current_char, position = next_char(code, position)
                tokens.append(Token(COMPARISON))
            else:
                tokens.append(Token(EQ))
        elif current_char == '+':
            tokens.append(Token(ADD))
        elif current_char == '-':
            if code[position+1] == '>':
                current_char, position = next_char(code, position)
                tokens.append(Token(KEYWORD, ALT_DOES))
                continue

            if position > 0:
                if tokens[-1].struct in (FLOAT, INT, IDENTIFIER):
                    current_char, position = next_char(code, position)
                    tokens.append(Token(SUB))
                    continue

            current_char, position = next_char(code, position)
            token_number, position = make_number(current_char, code, position)
            token_number.value = -1 * token_number.value
            tokens.append(token_number)
        elif current_char == '*':
            tokens.append(Token(MUL))
        elif current_char == '/':
            tokens.append(Token(DIV))
        elif current_char == '^':
            tokens.append(Token(POW))
        elif current_char == '!' and code[position+1] == '=':
            current_char, position = next_char(code, position)
            tokens.append(Token(NOT_EQUAL))
        elif current_char == '<':
            if code[position+1] == '=':
                current_char, position = next_char(code, position)
                tokens.append(Token(LOWER_OR_EQUAL))
            else:
                tokens.append(Token(LOWER_THAN))
        elif current_char == '>':
            if code[position+1] == '=':
                current_char, position = next_char(code, position)
                tokens.append(Token(GREATER_OR_EQUAL))
            else:
                tokens.append(Token(GREATER_THAN))
        elif current_char == "(":
            tokens.append(Token(LEFTPAREN))
        elif current_char == ")":
            tokens.append(Token(RIGHTPAREN))
        elif current_char == ',':
            tokens.append(Token(KEYWORD, COMMA))
        else:
            raise SyntaxError(f"Unexpected caracter: \'{current_char}\'")
        
        current_char, position = next_char(code, position)
    
    return tokens

# Parser <-> Analizador sintáctico
# Make the Abstract Syntax Tree
# Order: AND Operator -> OR Operator -> Logic comparisons ->
#       -> Addition and Subtraction -> Multiplication and Division -> Power 
def parser(tokens: list) -> tuple:
    def AST(tokens: list, in_function: bool = False) -> tuple:
        global global_variables
        global local_variables

        if in_function:
            ast_variables = local_variables
        else:
            ast_variables = global_variables

        if not tokens:
            return None

        # AND, OR Operators
        def logic_operations() -> tuple:
            nonlocal tokens
            left = logic_comparisons()

            while tokens and tokens[0].struct in (AND, OR):
                operator = tokens.pop(0)
                right = logic_comparisons()
                left = (operator.struct, left, right)
            return left
        
        # Logic Comparisons
        def logic_comparisons() -> tuple:
            nonlocal tokens
            left = add_subtract()

            while tokens and tokens[0].struct in LOGIC_COMPARISONS:
                operator = tokens.pop(0)
                right = add_subtract()
                left = (operator.struct, left, right)
            return left
        
        # Addition and Subtraction
        def add_subtract() -> tuple:
            nonlocal tokens
            left = multiply_divide()

            while tokens and tokens[0].struct in (ADD, SUB):
                operator = tokens.pop(0)
                right = multiply_divide()
                left = (operator.struct, left, right)
            return left
        
        # Multiplication and Division
        def multiply_divide() -> tuple:
            nonlocal tokens
            left = power()

            while tokens and tokens[0].struct in (MUL, DIV):
                operator = tokens.pop(0)
                right = power()
                left = (operator.struct, left, right)
            return left
        
        # Power
        def power() -> tuple:
            nonlocal tokens
            left = non_operators()
            
            while tokens and tokens[0].struct == POW:
                operator = tokens.pop(0)
                right = non_operators()
                left = (operator.struct, left, right)
            return left
        
        # Non operators like functions, variables, strings, numbers, booleans, etc...
        def non_operators() -> str:
            nonlocal tokens
            
            token = tokens.pop(0)
            
            # If it's a number, boolean or string return itself
            if token.struct in (INT, FLOAT, BOOLEAN, STRING):
                return token.value
            # If it's a identifier (variable) check if it's calling its value or assigning itself
            elif token.struct == IDENTIFIER:
                if tokens != []:
                    if tokens[0].struct == EQ: # check if it have to assigning itself
                        tokens.insert(0, token)
                        assignment(ast_variables[token.value][0])
                        return ast_variables[token.value][1]
                    elif token.value in ast_variables: # check if it's calling itself
                        if ast_variables[token.value][0] == FUNCTION: # if it's a functions, execute itself
                            if tokens[0].struct == LEFTPAREN:
                                return execute_function(token.value)
                        
                        return ast_variables[token.value][1]
                    # Check if it's a bult in function
                    elif token.value in bult_in_function:
                        return execute_builtin_funcs(token.value)
                    else:
                        raise ValueError(f"Non defined variable: \'{token.value}\'")
                elif token.value in ast_variables:
                    return ast_variables[token.value][1]
                else:
                    raise ValueError(f"Non defined variable: \'{token.value}\'")
            elif token.value in (NUMBER, BOOLEAN, STRING, FUNCTION):
                var_name = assignment(token.value)
                return ast_variables[var_name][1]
            elif token.value == GLOBAL:
                if tokens.pop(0).value in (NUMBER, BOOLEAN, STRING) and tokens[0].struct == IDENTIFIER:
                    variable = tokens.pop(0)
                    if tokens.pop(0).struct == EQ:
                        global_variables[variable.value] = (variable.value, logic_operations())
                        if tokens and in_function:
                            if tokens[0].struct == END_LINE: tokens.pop(0)
                            return AST(tokens)
                    else:
                        raise SyntaxError("Equal sign (=) was expected")
                else:
                    raise SyntaxError("Global variable definition id not defined correctly")
            elif token.struct == LEFTPAREN:
                result = logic_operations()
                tt = tokens.pop(0)

                if tt.value == ',':
                    result += logic_operations()
                elif tt.struct != ')':
                    raise SyntaxError("A closing parenthesis was expected")
                
                return result
            elif token.value in (IF, ELIF):
                if_statement()
            elif token.struct == NOT:
                return (NOT, None, logic_operations())
            elif token.struct == NEW_LINE:
                new_num_line()
                parser(tokens)
            elif token.struct == RIGHTPAREN:
                pass
            elif token.struct == END_LINE:
                parser(tokens)
                pass
            elif token.value == END:
                if tokens != []:
                    if tokens[0].struct == END_LINE:
                        tokens.pop(0)
                        parser(tokens)
                    else:
                        raise SyntaxError()
            elif token.value == RETURN:
                return logic_operations()
            else:
                raise SyntaxError(f"Unexpected symbol: {token.value if token.value else token.struct}")

        # IF Statement
        def if_statement() -> any:
            nonlocal tokens
            condition = logic_operations()  # Condición para evaluar el IF-THEN
        
            if condition == None:
                return None
            
            if tokens == []:
                SyntaxError("Se esperaba THEN-STATEMENT")
            
            multi_line = False
            if tokens == []: raise SyntaxError("THEN STATEMENT was expected")
            if tokens.pop(0).value == THEN:
                if tokens[0].struct == NEW_LINE: 
                    multi_line = True
                    tokens.pop(0)
                inside_if_tokens = []
                
                while tokens:
                    token = tokens.pop(0)
                    if token.value == END: new_num_line(); break

                    if token.value in (IF, FOR, WHILE): 
                        new_tokens = check_substatements(tokens, token)
                        inside_if_tokens += new_tokens
                        continue

                    if token.value in (ELSE, ELIF): 
                        tokens.insert(0, token)
                        break 

                    if token.struct == NEW_LINE: 
                        if not multi_line: break;
                        new_num_line()
                        if tokens[0].value in (ELSE, ELIF) or tokens[0].value == END: break
                        inside_if_tokens.append(Token(END_LINE))
                        continue

                    inside_if_tokens.append(token)

                if evaluate(condition):
                    if tokens:
                        if tokens[0].value in (ELSE, ELIF):
                            while tokens:
                                if tokens[0].value == END: tokens.pop(0); break
                                if not multi_line and tokens[0].value == NEW_LINE: break
                                tokens.pop(0)

                    return AST(inside_if_tokens)
                else:
                    if tokens == []: return None

                    token = tokens.pop(0)
                    if token.value == ELSE:
                        inside_else_tokens = []
                        while tokens:
                            token = tokens.pop(0)
                            if token.value in (IF, FOR): 
                                new_tokens = check_substatements(tokens, token)
                                inside_else_tokens += new_tokens
                                continue
                            if token.value == END: break
                            if token.struct == NEW_LINE: 
                                if not multi_line: break;
                                new_num_line()
                                if tokens[0].value == END: tokens.pop(0); break
                                inside_if_tokens.append(Token(END_LINE))
                                continue
                            
                            inside_else_tokens.append(token)

                        return AST(inside_else_tokens)
                    
                    if token.value == ELIF:
                        return if_statement()
                    
                    tokens.insert(0, token)
                    return None
            else:
                raise SyntaxError("THEN STATEMENT was expected")
        
        # While loop statement
        def while_statement() -> any:
            nonlocal tokens
            
            aux_tokens = tokens.copy()
            condition = logic_operations()
            aux_expresion = []

            if tokens == []: raise SyntaxError("THEN STATEMENT was expected")
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
                        new_num_line()
                        if tokens[0].value == END: tokens.pop(0); break
                        aux_expresion.append(Token(END_LINE))
                        continue
                    if token.value == END: break
                    aux_expresion.append(token)
                final_tokens = tokens.copy()

                while True:
                    tokens = aux_tokens.copy()
                    condition = logic_operations()
                    if not evaluate(condition): break
                    expresion = aux_expresion.copy()
                    AST(expresion)
            else:
                raise SyntaxError("THEN STATEMENT was expected")
            
            tokens = final_tokens.copy()

        # For loop statement
        def for_statement() -> any:
            nonlocal tokens
            
            for_variable = tokens.pop(0)

            if for_variable.struct == IDENTIFIER:
                token = tokens.pop(0)
                if token.struct == EQ:
                    value = logic_operations() 
                    if type(evaluate(value)) not in (float, int): raise ValueError(f"{for_statement.value} expected to be a number")
                    ast_variables[for_variable.value] = (NUMBER, value) 
                    if tokens.pop(0).value != TO: raise SyntaxError("TO STATEMENT was expected")
                elif token.struct == STATEMENT and token.value == TO:
                    value = 0
                    ast_variables[for_variable.value] = (NUMBER, 0)
                else:
                    raise SyntaxError("Invalid for statement syntax")

            to_variable_tokens = []
            while tokens:
                token = tokens.pop(0)
                if token.value == THEN: 
                    tokens.insert(0, token)
                    break
                to_variable_tokens.append(token)

            aux_tokens = tokens.copy()
            tokens = to_variable_tokens
            to_variable = logic_operations()
            tokens = aux_tokens
            
            multi_line = False
            if tokens == []: raise SyntaxError("THEN STATEMENT was expected")
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
                        new_num_line()
                        if tokens[0].value == END: tokens.pop(0); break
                        aux_for_body.append(Token(END_LINE))
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
                    AST(for_body)
            else:
                raise SyntaxError("THEN STATEMENT was expected")

        def check_substatements(tokens: list, first_token: Token):
                aux_tokens = [first_token]
                find_end = False
                while tokens:
                    aux_token = tokens.pop(0)
                    if aux_token.value in (IF, FOR, WHILE):
                        new_tokens = check_substatements(tokens, aux_token)
                        aux_tokens += new_tokens
                        continue
                    if aux_token.value == THEN:
                        if tokens[0].struct == NEW_LINE:
                            find_end = True
                    #if aux_token.struct == NEW_LINE: aux_tokens.append(Token(END_LINE)); continue
                    if aux_token.struct == NEW_LINE and not find_end: break
                    if aux_token.value == END: aux_tokens.append(aux_token); break
                    aux_tokens.append(aux_token)
                
                return aux_tokens

        # Declaration and reassignment of variables
        def assignment(struct) -> str:
            nonlocal tokens
            
            identifier_token = tokens.pop(0)

            if identifier_token.struct == IDENTIFIER:
                if tokens.pop(0).struct == EQ:
                    expression_tokens = []
                    while tokens:
                        token = tokens.pop(0)
                        if token.struct in (NEW_LINE, END_LINE): 
                            new_num_line()
                            break
                        expression_tokens.append(token)
                    aux_tokens = tokens.copy()
                    tokens = expression_tokens

                    if tokens[0].struct == STATEMENT and tokens[0].value == IF:
                        tokens.pop(0)
                        expression = if_statement()
                    elif tokens[0].struct == IDENTIFIER and tokens[0].value in bult_in_function:
                        expression = execute_builtin_funcs(tokens.pop(0).value)
                    elif tokens[0].struct == IDENTIFIER: 
                        if tokens[0].value not in ast_variables: 
                            raise ValueError(f"Non defined variable: \'{token.value}\'")
                        try:
                            if tokens[1].struct == LEFTPAREN:
                                expression = execute_function(tokens.pop(0).value)
                            else:
                                expression = logic_operations()
                        except IndexError:
                            expression = logic_operations()
                    else:
                        expression = logic_operations()
                    
                    tokens = aux_tokens
                    result = evaluate(expression)
                    if struct == STRING and type(result) != str:
                        type_error = "número" if type(result) == int else "booleano"
                        raise ValueError(f"Cannot assign a {type_error} to a string")
                    else:
                        if struct != STRING and type(result) == str:
                            type_error = "booleano" if struct == BOOL else "número"
                            raise ValueError(f"Cannot assign a string to a {type_error}")
                    
                    if struct == BOOL and type(result) in (int, float, str):
                        raise ValueError("Can't assign a number to a boolean")
                    else:
                        if struct != BOOL and type(result) == bool:
                            raise ValueError("Can't assign a boolean to a number")
                        
                    ast_variables[identifier_token.value] = (struct, expression)
                else:
                    raise SyntaxError("An equal sign '=' was expected for assignment")
            else:
                raise SyntaxError("Identifier expected for assignment")
        
        # Define a function
        def define_function() -> any:
            
            nonlocal tokens
            function_name = tokens.pop(0).value
            function_body = []
            function_arguments = []

            if function_name not in global_variables:
                token = tokens.pop(0)
                if token.struct == LEFTPAREN:
                    while tokens:
                        arg = tokens.pop(0)
                        if arg.struct == IDENTIFIER:
                            function_arguments.append((NUMBER, arg.value))
                        elif arg.struct == KEYWORD and arg.value == COMMA:
                            continue
                        elif arg.struct == RIGHTPAREN:
                            break
                        else:
                            raise SyntaxError(f"Invalid argument in function definition: {arg.value}")
                    
                    try:
                        if tokens[0].value in (DOES, ALT_DOES): tokens.pop(0)
                    except IndexError:
                        raise SyntaxError("Empty function")
                    
                    multi_line = False
                    single_line = False
                    function_type = FUNCTION
                    if tokens[0].struct == NEW_LINE: 
                        tokens.pop(0)
                    else:
                        single_line = True
                        tokens.insert(0, Token(KEYWORD, RETURN))
                    
                    while tokens:
                        token = tokens.pop(0)
                        if token.value == END: break
                        if token.struct == NEW_LINE:
                            new_num_line()
                            multi_line = True
                            if single_line:
                                if tokens[0].value == END: tokens.pop(0)
                                break
                            
                            continue

                        if multi_line: 
                            multi_line = False
                            function_body.append(Token(END_LINE))
                        
                        if token.struct == KEYWORD and token.value == RETURN: function_type += '-RETURNED'
                        function_body.append(token)

                    ast_variables[function_name] = (function_type, function_arguments, function_body)
                elif token.struct == EQ:
                    token = tokens.pop(0)
                    if token.struct == IDENTIFIER and token.value in global_variables:
                        if global_variables[token.value][0] in (FUNCTION, FUNCTION+'-RETURNED'):
                            global_variables[function_name] = global_variables[token.value]
                    else:
                        raise SyntaxError(f"Invalid function definition, unexpected '{token.value}' function")
                else:
                    raise SyntaxError("Invalid function definition, expected a '('")
            else:
                raise SyntaxError("Invalid function name or already defined")
        
        # Executing a function
        def execute_function(name_function):
            nonlocal tokens
            tokens.pop(0)
            function_arguments = []
            while tokens:
                if tokens[0].struct == RIGHTPAREN: break

                arg = logic_operations()
                function_arguments.append(arg)
                if tokens.pop(0).value != COMMA:
                    break
            
            arguments = global_variables[name_function][1]
            if len(function_arguments) == len(arguments):
                for i in range(len(function_arguments)):
                    local_variables[arguments[i][1]] = (arguments[i][0], function_arguments[i])
                
                if FUNCTION+'-RETURNED' == global_variables[name_function][0]:
                    return AST(global_variables[name_function][2].copy(), in_function=True)
                else:
                    AST(global_variables[name_function][2].copy(), in_function=True)
            else:
                raise TypeError("Invalid numbers of arguments on function")
            
        # Executing a bult in function
        def execute_builtin_funcs(name_function: str):
            nonlocal tokens

            tokens.pop(0)
            args = []

            token = tokens.pop(0)
            while tokens:
                if token.struct == RIGHTPAREN: break
                if token.value == COMMA: token = tokens.pop(0); continue
                if token.struct == IDENTIFIER:
                    if token.value in global_variables:
                        if global_variables[token.value][0] in (FUNCTION, FUNCTION+'-RETURNED'):
                            args.append(evaluate(execute_function(token.value)))
                            token = tokens.pop(0)
                            continue
                
                tokens.insert(0, token)
                arg = evaluate(logic_operations())
                token = tokens.pop(0)
                args.append(arg)
            
            match name_function:
                case 'print':
                    for arg in args:
                        print(f"{arg}", end="")
                    
                case 'println':
                    for arg in args:
                        print(f"{arg}", end="")
                    
                    print("\n", end="")
                case 'input':
                    return input(args[0]) if args else input()
                case 'input_num':
                    try:
                        ans = input(args[0]) if args else input()
                        return float(ans)
                    except ValueError:
                        print(args)
                        raise ValueError(f"Impossible convert '{ans}' to a number")
                case 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                case 'exit':
                    exit()
                case 'is_a_number':
                    if len(args) == 1:
                        return True if type(args[0]) == int else False
                    else:
                        raise TypeError("Invalid numbers of arguments on function")
                case 'is_a_string':
                    if len(args) == 1:
                        return True if type(args[0]) == str else False
                    else:
                        raise TypeError("Invalid numbers of arguments on function")
                case 'is_a_function':
                    # If args[0] == None then the argument is a Function
                    if len(args) == 1:
                        return True if not args[0] else False
                    else:
                        raise TypeError("Invalid numbers of arguments on function")
    
        # Main parser logic
        while tokens:
            token = tokens.pop(0)
            # Declarate variables
            if token.struct == KEYWORD and token.value == FUNCTION:
                define_function()
            elif token.struct == KEYWORD and token.value in (NUMBER, BOOL, STRING):
                if tokens[0].value in ast_variables:
                    raise SyntaxError(f"Variable '{tokens[0].value}' already exists")
                assignment(token.value)
            # Variable redeclaration and type checking (It is a strongly typed language)
            elif token.struct == IDENTIFIER and token.value in ast_variables and tokens != []:
                if ast_variables[token.value][0] in (FUNCTION, FUNCTION+'-RETURNED'):
                    if tokens[0].struct != LEFTPAREN:
                        return ast_variables[token.value]
                    
                    if FUNCTION+'-RETURNED' == global_variables[token.value][0]:
                        print(1)
                        exit()
                    
                    execute_function(token.value)
                elif tokens[0].struct == EQ:
                    tokens.insert(0, token)
                    assignment(ast_variables[token.value][0])
                else:
                    tokens.insert(0, token)
                    return logic_operations()
            elif token.struct == IDENTIFIER and token.value in bult_in_function and tokens:
                if tokens[0].struct == LEFTPAREN:
                    execute_builtin_funcs(token.value)
                else:
                    raise TypeError("Opening parenthesis was expected")
            elif token.struct == STATEMENT and token.value == IF:
                if_statement()
            elif token.struct == STATEMENT and token.value == WHILE:
                while_statement()
            elif token.struct == STATEMENT and token.value == FOR:
                for_statement()
            elif token.struct == NOT:
                return (NOT, None, logic_operations())
            elif token.struct == NEW_LINE:
                new_num_line()
                parser(tokens)
                break
            else:
                tokens.insert(0, token)
                return logic_operations()

    AST(tokens)

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
            return left / right
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
    tokens = lexer(code)
    try:
        parser(tokens)
    except Exception as error:
        print(f"\n{type(error).__name__} on line {get_num_line()}: {error}")

def debug(code: str) -> any:
    print("------ CODE -------")
    print(code)
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
        file = open('test.lexscript')

    code = file.read()
    if '--debug' in sys.argv:
        debug(code)
    else:
        execute(code)