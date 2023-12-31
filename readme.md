# Lexscript
Strongly and static typed langague based on python, is under development.
At the moment it's made with python, perhabs in the future the code will be migratec at javascript.

# Example of Code
Code:
```python
# Strings
string hello = "Hello "
string world = "World"
println(hello + world)

# Booleans
bool boolean = 1 > 2
println("Boolean variable value: ", boolean)

# WHILE STATEMENT
var test = 1
while test < 4 then test = test + 1
println("Var test after while loop:", test)

# FOR STATEMENT
var example = 0
for i to 4 then example = example + i
println("Var example after for loop:", example)
println("Drawing a square: ")
for i to 4 then
    for j to 4 then
        print("* ")
    end
    println(" ")
end

# FUNCTIONS
function sum(a, b) does a + b
println("Result of sum function: ", sum(example, test))

function mul(a, b) does
    global var c = a * b
    return c
end

println("Result of mul function: ", mul(example, test))
print("Global variable from mul function: ", c)
```
Output:
```
Boolean variable value: False
Var test after while loop:4
Var example after for loop:10
Drawing a square: 
* * * * *  
* * * * *  
* * * * *  
* * * * *  
* * * * *  
Result of sum function: 14
Result of mul function: 40
Global variable from mul function: 40
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
**Multi-line:**
```
if <condition> then 
    <expresion> 
elif <condition> then 
    <expresion>
else 
    <expresion>
end
```
**Only in a line:**
if `condition` then `expression` elif `condition` then `expression` else `expression`

# While Syntax
**Only in a line:** while `condition` then `expresion`

**Multi-line:**
```
while <condition> then
    <while_body_code>
end
```

# For Syntax
**Only in a line:**
- variable init on 0 -> for `variable` to `condition` then `expresion` 
- variable don't init on 0 -> for `variable` = `value` to `condition` then `expresion`

**Multi-line:**
```
for <variable> to <condition> then
    <for_body_code>
end
```

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