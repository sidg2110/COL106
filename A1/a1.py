# REFERENCES : 
# Class Slides for implementation of Stack class using Linked List data structure
# W3C School for reference to string methods; particularly isdigit() method

class Stack :           # Implementation of Stack data structure using Linked List data structure

    class _Node :       # Define private class Node to create a new node in the linked list
        
        def __init__(self , element , next) :
            # Initialises the instance of Node class
            # elements => Data stored
            # next => Pointer to the address of next element in the list
            
            self._element = element     # Private property 'element' is defined
            self._next =  next          # Private property 'next' is defined

    def __init__(self) :
        # Initialises the instance of Stack class

        self._head = None       # Private property 'head' stores the data and pointer of the next element. Initially empty stack is created with no data
        self._size = 0          # Private property 'size' is defined. Equal to length of stack (linked list)

    def push(self , e) :
        # Adds a element 'e' to the top of the stack

        self._head = self._Node(e , self._head)
        self._size += 1

    def pop(self) :
        # Deletes the topmost element of the stack and returns that element

        if self._size == 0:             # Cannot pop if the stack is empty. Therefore, raises an exception.
            raise Exception('Stack is Empty')
        
        answer = self._head._element

        self._head = self._head._next       # The topmost element is now the second to topmost element in the original stack
        self._size -= 1

        return answer

def findPositionandDistance(input_string):

    # input_string => str : series of instruction along which the drone moves
    # Output => list : list of length 4 containing the x, y, z co-ordinates and the distance travelled by the drone

    # Algorithm :
    # Treats each parenthesis as a level of instruction. Upon encountering '(' , creates a new level. Upon encountering ')', deletes the topmost level.
    
    number_stack = Stack()      # Initialises a stack to store the multiplier (number of times the instructions are repeated) of each level.
    
    x_stack = Stack()           # Initialises a stack to store the x co-ordinate of the drone.
    x_stack.push(0)             # Creates the bottom-most level. The final value in this level is the final x co-ordinate
    
    y_stack = Stack()           # Initialises a stack to store the y co-ordinate of the drone.
    y_stack.push(0)             # Creates the bottom-most level. The final value in this level is the final y co-ordinate
    
    z_stack = Stack()           # Initialises a stack to store the z co-ordinate of the drone.
    z_stack.push(0)             # Creates the bottom-most level. The final value in this level is the final z co-ordinate
    
    distance_stack = Stack()    # Initialises a stack to store the distance travelled by the drone
    distance_stack.push(0)      # Creates the bottom-most level. The final value in this level is the total distance travelled

    input_length = len(input_string)

    i = 0     # Iterator to traverse the length of input string

    while i < input_length :

        character = input_string[i]

        if character.isdigit() :        # isdigit() method checks whether the given string is composed entirely of digits from 0-9 or not
            j = i+1
            while input_string[j].isdigit() :       # Checks each character and combines the digits to form the multiplier number.
                character = character + input_string[j]
                j += 1
            number_stack.push(int(character))

            i = j
            continue

        elif character == '(' :          # Creates a new level in x, y, z and distance stack
        
            x_stack.push(0)
            y_stack.push(0)
            z_stack.push(0)
            distance_stack.push(0)
       
            i += 1
            continue

        elif character == '+' :         # Signifies that one instruction is being given to the drone

            if input_string[i+1] == 'X' :
                temp = x_stack.pop()
                temp += 1
                x_stack.push(temp)
            elif input_string[i+1] == 'Y' :
                temp = y_stack.pop()
                temp += 1
                y_stack.push(temp)
            elif input_string[i+1] == 'Z' :
                temp = z_stack.pop()
                temp += 1
                z_stack.push(temp)
            
            temp_distance = distance_stack.pop()    # Irrespective of the direction of movement, the distance increments by 1 unit
            temp_distance += 1
            distance_stack.push(temp_distance)

            i += 2
            continue
        
        elif character == '-' :         # Signifies that one instruction is being given to the drone

            if input_string[i+1] == 'X' :
                temp = x_stack.pop()
                temp -= 1
                x_stack.push(temp)
            elif input_string[i+1] == 'Y' :
                temp = y_stack.pop()
                temp -= 1
                y_stack.push(temp)
            elif input_string[i+1] == 'Z' :
                temp = z_stack.pop()
                temp -= 1
                z_stack.push(temp)
            
            temp_distance = distance_stack.pop()    # Irrespective of the direction of movement, the distance increments by 1 unit
            temp_distance += 1
            distance_stack.push(temp_distance)

            i += 2
            continue

        elif character == ')' :        # Signifies the end of the current level. Deletes the topmost level and store the result in the next level

            multiplier = number_stack.pop()

            # Top elements of each stack
            x_stack_top = x_stack.pop()
            y_stack_top = y_stack.pop()
            z_stack_top = z_stack.pop()
            distance_stack_top = distance_stack.pop()

            # Final value of the current level
            x_adder = multiplier * x_stack_top
            y_adder = multiplier * y_stack_top
            z_adder = multiplier * z_stack_top
            distance_added = multiplier * distance_stack_top

            # Value of the next to topmost level
            x_stack_top = x_stack.pop()
            y_stack_top = y_stack.pop()
            z_stack_top = z_stack.pop()
            distance_stack_top = distance_stack.pop()

            # Value of the topmost level is added to the next level. Finishes the evaluation of the instruction of the topmost level
            x_stack.push(x_stack_top + x_adder)
            y_stack.push(y_stack_top + y_adder)
            z_stack.push(z_stack_top + z_adder)
            distance_stack.push(distance_stack_top + distance_added)

            i += 1
            continue

    # Final value of the bottom-most level of stacks
    x_coordinate = x_stack.pop()
    y_coordinate = y_stack.pop()
    z_coordinate = z_stack.pop()
    distance = distance_stack.pop()

    return [x_coordinate , y_coordinate , z_coordinate , distance]