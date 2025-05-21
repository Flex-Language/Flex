# Flex Programming Language - Complete Guide

## Introduction

Welcome to **Flex**, a flexible and beginner-friendly programming language that allows you to write code in multiple syntax styles, including **Franko Arabic, English, and C-style syntax**. **Flex** is designed for all levels of programmers, from children to professionals, providing an easy-to-learn syntax with powerful programming capabilities.
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Flex-Language/Flex)

### Why Flex?
Flex is unique because it:
- Supports **multiple programming styles**, allowing developers to write code in a way they are most comfortable with.
- Bridges the gap between **high-level scripting languages (like Python)** and **low-level languages (like C)**.
- Uses **regular expressions (regex)** for tokenization, making parsing and error handling efficient.
- Has **intuitive and readable syntax**, making it an excellent choice for beginners while still being powerful for advanced users.
- Is designed to be **cross-platform**, ensuring compatibility across different operating systems.

This guide will take you from the basics to advanced concepts, with **clear explanations and code examples with outputs**.

---

# 1. Getting Started with Flex

### 1.1 Features of Flex
- Supports multiple syntaxes (**Franko Arabic, English, C-style, etc.**)
- Uses **regular expressions (regex)** for efficient tokenization
- Provides **control flow structures** (*if-else, loops, functions*)
- Allows **variable declarations** with intuitive keywords
- Implements **built-in functions** for input and output
- **No need for semicolons** (`;`) at the end of statements
- **Blocks** are enclosed within `{}`
- **Seamless integration** with Python and C-style and Flex syntax
- **Automatic type detection** when variables are assigned values

### 1.2 Writing Your First Flex Program
```flex
etb3("Hello, Flex!")
```
**Output:**
```
Hello, Flex!
```

---

# 2. Syntax and Basic Constructs

## 2.1 Variables and Data Types

### Integer
```flex
rakm x = 10
int y = 5
rakm z=2, m=1, n=0
etb3("{x} and {y}")
etb3("count down {z} {m} {n}")
```
**Output:**
```
10 and 5
count down 2 1 0
```

### Float
```flex
kasr pi = 3.14
float radius = 3
etb3("Value of pi is {pi} and the radius value is {radius}")
```
**Output:**
```
Value of pi is 3.14 and the radius value is 3.0
```

### Boolean
```flex
isActive = true
bool isComplete = false
etb3("Active: {isActive}, Complete: {isComplete}")
```
**Output:**
```
Active: True, Complete: False
```

### String
```flex
klma message = "Welcome to Flex!"
string letter = "Welcome to the world!"
etb3(message)
etb3(letter)
```
**Output:**
```
Welcome to Flex!
Welcome to the world!
```

### Lists (Arrays)
```flex
dorg myList = [1, 2.3, "hello", true]
list alist = [15,3,26,1000]
etb3(myList)
etb3(alist)
```
**Output:**
```
[1, 2.3, 'hello', True]
[15, 3, 26, 1000]

```

### Auto Declaration 
```flex
x=5
y=2.43
z="hello"
l="m"
etb3(x)
etb3(y)
etb3(z)
etb3(l)
```
**Output:**
```
5
2.43
hello
m

```

### print
```flex
x= "hello world to print in many ways"
etb3(x)
out("this is {x}")
print(x)
cout("this way for {x}")
output("{x}")
printf("to print {x}")
```

**Output:**
```
hello world to print in many ways
this is hello world to print in many ways
hello world to print in many ways
this way for hello world to print in many ways
hello world to print in many ways
to print hello world to print in many ways
```

---

# 3. Input and Output

## 3.1 Getting User Input
```flex
etb3("Enter your name:")
klma name = da5l()
etb3("Hello, {name}!")
etb3("Enter your age:")
age = scan()
etb3("your age is {age}")
etb3("Enter your birthday:")
klma dateofbirth = read()
etb3("you were born on {dateofbirth}.")
etb3("Enter your phone number:")
number = input()
etb3("your phone number is {number}.")
etb3("Enter your favorite color:")
klma color = da5al()
etb3("your color is {color}!")
etb3("Enter your pet type:")
pet = d5l()
etb3("your pet is, {pet}!")
```

**Output:**
```
Enter your name:
```
*Input:* 
`lina`
```
Hello, lina!
```
```
Enter your age:
```
*Input:* 
`23`
```
your age is 23
```
```
Enter your birthday:
```
*Input:* 
`10-2-1999`
```
you were born on 10-2-1999.
```
```
Enter your phone number:
```
*Input:* `01002325428`
```
your phone number is 1002325428.
```
```
Enter your favorite color:
```
*Input:* `red`
```

your color is red!
```
```
Enter your pet type:
```
*Input:* `cat`
```
your pet is, cat!
```

---

# 4. Conditional Statements

## 4.1 If-Else Condition
```flex
rakm x = 5
lw x > 3 {
    etb3("x is greater than 3")
}
gher {
    etb3("x is not greater than 3")
}
```
**Output:**
```
x is greater than 3
```

## 4.2 If-Else with Multiple Conditions
```flex
rakm x = -2
lw x > 10 { etb3("x is greater than 10") }
aw x == 5 { etb3("x is equal to 5") }
aw x <= 0 { etb3("x is less than or equal 0") }
gher { etb3("x is less than 10") }
```
**Output:**
```
x is less than or equal 0
```

## 4.3 If in Another Way
```flex
rakm x = 5
if (x > 3) { etb3("x is greater than 3") }
else { etb3("x is not greater than 3") }
```
**Output:**
```
x is greater than 3
```
## 4.4 If in Another Way
```flex
rakm x = 5
lw x > 3 and x < 9 {
    etb3("x is between 3 and 9")
}
gher {
    etb3("x is not in the middle of 3 and 9")
}
```
**Output:**
```
x is between 3 and 9
```
## 4.5 If in Another Way
```flex
kasr x = 5.45
cond (x > 10) {
    etb3("{x} is bigger than 10")
}
gher {
    etb3("{x} is less than 10")
}
```
**Output:**
```
5.45 is less than 10
```
## 4.6 Else in Another Way
```flex
rakm x = 2
lw x > 3 {
    etb3("x is greater than 3")
}
otherwise {
    etb3("x is not greater than 3")
}
```
**Output:**
```
x is not greater than 3
```
## 4.7 Else in Another Way
```flex
kasr x = 5.23
lw x > 3 {
    etb3("x is greater than 3")
}
else {
    etb3("x is not greater than 3")
}
```
**Output:**
```
x is greater than 3
```

---

# 5. Loops

## 5.1 While Loop
```flex
rakm i = 0
talama i < 5 {
    etb3(i)
    i++
}
```
**Output:**
```
0
1
2
3
4
```

## 5.2 While Loop in Another Way
```flex
i = 1.0
tlma i < 5.0 {
    etb3(i)
    i++
}
```
**Output:**
```
1.0
2.0
3.0
4.0
```

## 5.3 While Loop in Another Way
```flex
i = 30
talma i >= 25 {
    etb3(i)
    i--
}
```
**Output:**
```
29
28
27
26
25
```

## 5.4 While Loop in Another Way
```flex
i = 4
while (i == 4) {
    etb3(i)
    i++
}
```
**Output:**
```
4
```
## 5.5 While Loop in Another Way
```flex
i = 0
loop (i < 6) {
    etb3(i)
    i++
}
```
**Output:**
```
0
1
2
3
4
5
```

## 5.6 For Loop
```flex
karr x=4 l7d 10 {etb3(x)}
```
**Output:**
```
4
5
6
7
8
9
```
## 5.7 For Loop in Another Way
```flex
karr x l7d 10 {etb3("hello world 10 times")} //x will automatically be initiated by 0
```
**Output:**
```
4
5
6
7
8
9
```
## 5.8 For Loop in Another Way
```flex
karr l7d 10 {etb3("hello 10 times")} //automatically be initiated by 0
```
**Output:**
```
hello 10 times
hello 10 times
hello 10 times
hello 10 times
hello 10 times
hello 10 times
hello 10 times
hello 10 times
hello 10 times
hello 10 times
```
## 5.9 For Loop in Another Way
```flex
n=15
for (int i=5; i <= n; i++) {etb3("hello {i}")}
```
**Output:**
```

```
---

# 6. Functions

## 6.1 Defining and Calling Functions
```flex
sndo2 add(rakm a, rakm b) {
    rg3 a + b
}

rakm result = add(3, 7)
etb3("Result: {result}")
```
**Output:**
```
Result: 10
```

## 6.2 Functions in Antoher Way
```flex
fun add(rakm a, rakm b) {
    rg3 a + b
}

rakm result = add(3, 7)
etb3("Result: {result}")
```
**Output:**
```
Result: 10
```

## 6.3 Functions and Return in Antoher Way
```flex
sando2 add(rakm a, rakm b) {
    rg3 a + b
}

rakm result = add(3, 7)
etb3("Result: {result}")
```
**Output:**
```
Result: 10
```

## 6.4 Functions and Return in Antoher Way
```flex
fn add(rakm a, rakm b) {
    return a + b
}

rakm result = add(3, 7)
etb3("Result: {result}")
```
**Output:**
```
Result: 10
```
## 6.5 Functions and Return in Antoher Way
```flex
function add(rakm a, rakm b) {
    rg3 (-1) * a + b
}

rakm result = add(3, 7)
etb3("Result: {result}")
```
**Output:**
```
Result: 4
```

---

# 7. List Operations

## 7.1 List Operations
```flex
dorg myList = [1, 2, 3]
myList.push(4)
etb3(myList)
myList.pop()
etb3(myList)
```
**Output:**
```
[1, 2, 3, 4]
[1, 2, 3]
```

## 7.2 List in Another Way
```flex
list myList = [1, 2, 3]
myList.push(4)
etb3(myList)
myList.pop()
etb3(myList)
```
**Output:**
```
[1, 2, 3, 4]
[1, 2, 3]
```

---

# 8. import Operations

## 8.1 geeb Operations
```flex
sando2 absolute(rakm a){
    lw a < 0 {
        x = a * (-1)
        rg3 x
    }
    gher{ rg3 a}
}
```

```
geeb "path to the .lx file "
x= -400
postive = absolute(x)
etb3("{x} after absolute is {postive}")
```
**Output:**
```
-400 after absolute is 400
```

## 8.2 geep Operations
```flex
sando2 absolute(rakm a){
    lw a < 0 {
        x = a * (-1)
        rg3 x
    }
    gher{ rg3 a}
}
```

```
geep "path to the .lx file "
x= -400
postive = absolute(x)
etb3("{x} after absolute is {postive}")
```
**Output:**
```
-400 after absolute is 400
```

## 8.3 import Operations
```flex
sando2 absolute(rakm a){
    lw a < 0 {
        x = a * (-1)
        rg3 x
    }
    gher{ rg3 a}
}
```

```
import "path to the .lx file "
x= -400
postive = absolute(x)
etb3("{x} after absolute is {postive}")
```
**Output:**
```
-400 after absolute is 400
```

---


# 9. List Operations

## 9.1 Dorg Operation
```flex
# Define a list
dorg arrr = [-1, 2, -3, 4, 99]  

# Access elements by index and perform operations
rakm num = 4
etb3(arrr[num] + arrr[num])  # 99 + 99 = 198

# Finding the length of a list
rakm y = length(arrr)  
lw length(arrr) < 3 {
    etb3("List is too short!")
}
etb3(y)

# Creating and modifying lists
dorg xx = [6, 2, 3, 4]
etb3(xx)  # Print the initial list

# Adding elements
xx.push(23)  # Equivalent to push
xx.push("worddd")
etb3(xx)  # Print list after additions

# Removing elements
xx.pop()  # Removes the last element (pop)
etb3(xx)  

xx.remove(3)  # Removes the value 3 from the list
etb3(xx)
```

**Output:**
```
198
5
[6, 2, 3, 4]
[6, 2, 3, 4, 23, 'worddd']
[6, 2, 3, 4, 23]
[6, 2, 4, 23]
```

## 9.2 List Operation
```flex

# Creating and modifying lists
dorg xx = [6, 2, 3, 4]
etb3(xx)  # Print the initial list

# Merging lists & performing calculations
dorg qq = [12, 22, 34]
etb3("x0+q1={xx[0] + qq[1]}")  # Print formatted string with calculation
etb3(xx[0] + qq[1])  # Sum of first element of xx and second of qq

# Arithmetic operations with list elements
rakm no = xx[0] * xx[1]
rakm ew = xx[0] * xx[1]
etb3(no - ew)  # Should print 0
etb3("no is {no}")

# Conditional check with list values
lw xx[0] < xx[1] {
    etb3("xo is smaller")
}

```


**Output:**
```
[6, 2, 3, 4]
x0+q1=28
28
0
no is 12
```

---

# 10. break Operation

## 10.1 w2f Operation
```flex
rakm i = 0
talama i < 10 {
    etb3(i)
    lw i == 4 {
        w2f
    }
    i++
}

```
**Output:**
```
0
1
2
3
4
```

## 10.2 break in Another Way
```flex
rakm i = 0
talama i < 10 {
    etb3(i)
    lw i == 4 {
        break
    }
    i++
}
```
**Output:**
```
0
1
2
3
4
```
## 10.3 stop in Another Way
```flex
rakm i = 0
talama i < 10 {
    etb3(i)
    lw i == 4 {
        stop
    }
    i++
}
```
**Output:**
```
0
1
2
3
4
```

---

# 11. More Advanced Examples
```flex
sndo2 multiply(rakm a, rakm b) {
    rg3 a * b
}

rakm x = 5
rakm y = 6
print("{x} x {y} = {multiply(x, y)}")
```
**Output:**
```
5 x 6 = 30
```

---

# Conclusion

Congratulations! You have now learned the basics of **Flex** mixed with **Python and C**! 🚀 This guide covered:
- **Variables and Data Types**
- **Input and Output**
- **Conditional Statements**
- **Loops and Iterations**
- **Functions and Error Handling**
- **Advanced Features (Lists, Nested Loops, Mixed Syntax, etc.)**

Feel free to experiment with **Flex** and create your own programs!

---

### 🚀 Start Coding in Flex Now!
To explore more about **Flex**, join the community and contribute to the development. Happy coding! 🎉
