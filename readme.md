# How to run a script
```bash
python3 lex_core.py <file>
```
example:
```bash
python3 lex_core.py test.txt
```

# Example of Code
```
# WHILE STATEMENT
var test = 1
while test < 4 then test = test + 1
"Var test after while loop:"
test

\n # Salto de linea
# FOR STATEMENT
var example = 0
for i to 4 then example = example + i
"Var example after for loop:"
example

\n # Salto de linea
# A FUNCTION
function sum(a,b) a+b
"Result of sum function:"
sum(example, test)
```

# AST
Operator AND -> Operator OR -> Logical Comparisons -> Addition and Subtraction -> Multiplication and Division -> Power 

# Variables
FLOAT | INT -> var num = `value`
BOOLEAN -> bool true_or_false = `value`
STRING -> string hi = `"Hello World"`

# IF Syntax
If `condition` then `expresion` elif `condition` then `expresion` else `expresion`

# While Syntax
While `condition` then `expresion`

# For Syntax
variable init on 0 -> For `variable` to `condition` then `expresion` 
variable don't init on 0 -> For `variable` = `value` to `condition` then `expresion`

# Define a functions - Three methods
function sum(a,b) does a+b
function sub(a,b) -> a-b
function mul(a,b) a*b