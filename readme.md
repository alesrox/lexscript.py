# Lexscript
Strongly and static typed langague based on python, is under development.
At the moment it's made with python, perhabs in the future the code will be migratec at javascript.

# Example of Code
Code:
```javascript
# WHILE STATEMENT
var test = 1
while test < 4 then test = test + 1
println("Var test after while loop:", test)

# FOR STATEMENT
var example = 0
for i to 4 then example = example + i
println("Var example after for loop:", example)

# A FUNCTION
function sum(a,b) a+b
"Result of sum function:"
sum(example, test)
```
Output:
```
Var test after while loop: 4 
Var example after for loop: 10 
Result of sum function: 14
```

# How to run a script
```bash
python3 lexscript.py <file>
```
example:
```bash
python3 lexscript.py tryme.lexscript
```

# How to install language support on Visual Studio Code
1. Open command menu on Visual Studio: `Ctrl+Shift+P` on Linux and Windows or `Cmd+Shift+P` on MacOS
2. Write Extensions: Install from VSIX
3. Select lexscript-language-sopport.vsix

# Variables
- FLOAT | INT -> var num = `value`
- BOOLEAN -> bool true_or_false = `value`
- STRING -> string hi = `"Hello World"`

# IF Syntax
if `condition` then `expresion` elif `condition` then `expresion` else `expresion`

# While Syntax
while `condition` then `expresion`

# For Syntax
- variable init on 0 -> for `variable` to `condition` then `expresion` 
- variable don't init on 0 -> for `variable` = `value` to `condition` then `expresion`

# Define a functions - Three methods
```javascript
function sum(a,b) does a+b
function sub(a,b) -> a-b
function mul(a,b) a*b
```

# Bult-in Functions
- print()         -> Print all the arguments in a line
- println()       -> Print all the arguments in diferents lines
- input()         -> return the user input
- input_num()     -> return the user input as a number
- clear()         -> clean the terminal
- exit()          -> close the program
- is_a_number()   -> return true if the arguments is a number
- is_a_string()   -> return true if the arguments is a string
- is_a_function() -> return true if the arguments is a function