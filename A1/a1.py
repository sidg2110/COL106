class Stack:
    """
    Implementation of stack data structure as a linked list
    
    Args:
        value (int) (optional) : If not None, creates a stack with a single node with this value. Else, creates a empty stack
    """

    class _Node:
        """
        Represents an individual node in the stack

        Args:
            element (int) : Value stored in the node
            next (_Node) : Pointer to the node in the stack pushed just before
        """
        def __init__(self, value, next):            
            self._value = value
            self._next =  next
            self._multiplier = 1     # Multiplier for the value computed in the inner level
            self._distance = 0       # Distance travelled in this level

    def __init__(self, value=None):
        self._head = None       # Pointer to the top of the stack
        self._size = 0          # Length of stack
        if value is not None:
            self.push(value)

    def push(self , value):
        """
        Pushes a new node on top of the stack.

        Args:
            value (int) : value stored in the new node
        """
        self._head = self._Node(value, self._head)
        self._size += 1

    def pop(self) :
        """
        Deletes the topmost node of the stack and returns its value

        Returns:
            tuple (int): value, multiplier and distance attributes of the top node of the stack
        """
        if self._size == 0:             # Cannot pop if the stack is empty.
            raise Exception('Stack is Empty')
        
        value = self._head._value
        distance = self._head._distance
        multiplier = self._head._multiplier
        self._head = self._head._next       # Change the head pointer to the second to top node
        self._size -= 1
        return (value, multiplier, distance)

    def top(self):
        """
        Access the multiplier stored in the top node of the stack.

        Returns:
            tuple(int): value, multiplier and distance attributes of the top node of the stack
        """
        return (self._head._value, self._head._multiplier, self._head._distance)
    
    def modify_top(self, value=0, multiplier=1, distance=0):
        """
        Modifies the top element of the stack

        Args:
            value (int) : integer to be added to self._head._value
            multiplier (int) : integer to be set as self._head._multiplier
            distance (int) : integer to be added to self._head._distance
        """
        if self._size == 0:
            raise Exception('Stack is empty')

        self._head._value += value
        self._head._multiplier = multiplier
        self._head._distance += distance

def findPositionandDistance(program):
    """
    Given a series of instructions to move the agent, computes the final co-ordinates of the agent

    Args:
        program (str) : series of instructions (format specified in ./Assignment_1.pdf) to move the agent

    Returns:
        tuple (int):
            - The final x co-ordinate of the agent
            - The final y co-ordinate of the agent
            - The final z co-ordinate of the agent
            - Distance travelled by the agent
    """

    # We store the instructions along each dimension in a separate stack
    # Initialize each stack with 0 to represent the initial coordinates as (0, 0, 0)
    x_stack, y_stack, z_stack = Stack(value=0), Stack(value=0), Stack(value=0)

    stacks = {'X': x_stack,
              'Y': y_stack,
              'Z': z_stack
            }
    operations = {'-': -1, '+': 1}
    
    curr_operator = None        # Stores the latest operator encountered in the program
    curr_multiplier = 0         # Stores the value of the multiplier for the next level
    
    program_idx = 0
    while program_idx < len(program):
        char = program[program_idx]
        
        if char == '-' or char == '+':
            curr_operator = operations[char]
            program_idx += 1
        
        elif char == 'X' or char == 'Y' or char =='Z':
            # We add/subtract from the corresponding stack. Distance is increased by 1 in the corresponding stack
            stacks[char].modify_top(value=curr_operator, distance=1)
            program_idx += 1
        
        elif char.isdigit():
            # We iterate till we have captured all the digits
            while program[program_idx].isdigit():
                curr_multiplier = curr_multiplier * 10 + int(program[program_idx])
                program_idx += 1
        
        elif char == '(':
            # Initialises a new level
            for stack in stacks.values():
                stack.modify_top(multiplier=curr_multiplier)
                stack.push(value=0)
            curr_multiplier = 0
            program_idx += 1
        
        else:
            # char is ')'
            # Closes the current level. Modify the coordinates and distances in the previous level
            for stack in stacks.values():
                inner_value, _, inner_distance = stack.pop()
                _, outer_multiplier, _ = stack.top()
                stack.modify_top(value=(inner_value*outer_multiplier), multiplier=1, distance=(inner_distance*outer_multiplier))
            curr_multiplier=0
            program_idx += 1

    # The first level in the program remains in the stack
    x_coordinate, _, x_distance = x_stack.pop()
    y_coordinate, _, y_distance = y_stack.pop()
    z_coordinate, _, z_distance = z_stack.pop()
    total_distance = x_distance + y_distance + z_distance

    return [x_coordinate, y_coordinate, z_coordinate, total_distance]

if __name__ == '__main__':
    answers = []
    with open('input.txt', 'r') as file:
        for line in file:
            program = line.strip()
            answers.append(findPositionandDistance(program))
    with open('output.txt', 'w') as file:
        for answer in answers:
            file.write(f"{answer}\n")