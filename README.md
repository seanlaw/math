# Math

This project provides a simple interactive interface for doing math. Currently, there is only support for subtraction (take aways). 

# Requirements

bokeh

# Example

To try the subtraction app:

'''
bokeh serve --show subtraction.py
'''

This should fire up the app in your browser. The circles can be taken away by clicking on them and choosing the right answer will automatically load up a new problem. 

#To Do

* Track correct and incorrect answers via logging and intelligently reinforce questions
* Add tabs for addition, multiplication, fractions
* Allow parents to add their own questions
