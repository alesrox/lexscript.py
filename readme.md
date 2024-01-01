# Lexscript
Strongly and static typed language based on python, is under development.
At the moment it's made with python, perhabs in the future the code will be migrated at javascript.

# Example of Code
Code:
```python
# Variables
string hi = "Hello World"
println(hi)

bool boolean = 1 > 2
println("Boolean variable value: ", boolean)

var num = if boolean then 2 * 2 else -1 ^ 2
println("Num variable value:", num)

# WHILE STATEMENT
var test = 1
while test < 4 then test = test + 1
println("Var test after while loop:", test)

# FOR STATEMENT
var example = 0
for i to 4 then example = example + i 
# example = 10, at the end of for loop

println("Drawing a 3x3 square: ")
for i to 2 then
    for j to 2 then
        print("* ")
    end
    println(" ")
end

# FUNCTIONS
function sum(a: var, b: var) a + b
println("Result of sum function: ", sum(example, test))

function mul(a: var, b: var) does
    var result = a * b
    return result
end

println("Result of mul function: ", mul(example, test))
```
Output:
```
Hello World
Boolean variable value: False
Num variable value: 1
Var test after while loop: 4
Var example after for loop: 10
Drawing a square: 
* * *
* * *
* * *
Result of sum function: 14
Result of mul function: 40
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

# Bult-in Functions
- print()         -> Print all the arguments in a line
- println()       -> Print all the arguments in diferents lines
- input()         -> return the user input
- input_num()     -> return the user input as a number
- clear()         -> clean the terminal
- exit()          -> close the program
- is_a_number()   -> return true if the argument is a number
- is_a_string()   -> return true if the argument is a string
- is_a_function() -> return true if the argument is a function
- sqrt()          -> return the square root of the argument