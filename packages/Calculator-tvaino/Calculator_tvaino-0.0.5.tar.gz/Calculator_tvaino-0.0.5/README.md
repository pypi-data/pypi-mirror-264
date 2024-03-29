# Calculator package

This package is a calculator class that performs basic arithmetical operations: addition, substraction, multiplication, devision and taking root.

## Installation

You can install the package through pip:

pip install Calculator_tvaino

## Usage

1. Importing calculator to your Python project:

*from Calculator import Calc*

2. Create an instance of the Calculator class:

*Calc = Calculator()*

3. Perform arithmetic operations by calling the appropriate methods and store the to the memory:

- Addition: add(number)
- Subtraction: subtract(number)
- Multiplication: multiply(number)
- Division: divide(number)
- Square root: root(number)

Example:

*calc.add(4)* #adds 4 to the memory
*calc.divide(2)* #devides the number of memory by 2

4. Access the current result by calling the memory attribute "mem":

*print(calc.mem)* #prints the result of arithmetical operations stored in memory

5. Clear the memory:

*calc.reset* #restets the memory to zero. **Clear the memory before starting a new sequence of arithmetic operations!**

6. Example:

<font color="green">\# Import Calculator</font> 

from Calculator import Calculator

<font color="green">\# Create a Calculator instance.</font>  
calc = Calculator()

<font color = "green">\# Perform arithmetic operations.</font>  
calc.add(5)  
calc.multiply(3)  
calc.divide(2)  

<font color = "green">\# Access the result.</font>  
print("Result:", calc.mem)  <font color = "green"># Output: 7.5</font>  

<font color = "green">\# Reset the memory.</font>  
calc.reset()  

<font color = "green">\# Perform another operation.</font>  
calc.root(16)

<font color = "green">\# Access the result.</font>  
print(calc.mem) <font color = "green">  # Output: 4.0</font>

#Tests performed








