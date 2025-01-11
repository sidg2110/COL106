# Stacks
This programming assignment is based on Stack data structure.
We implement stack (built bottom-up) as a linked list of nodes. The methods in the class `Stack` allow modifications only to the topmost element.

## I/O Format
Here, a series of instructions is called a program.
Each line in `input.txt` corresponds to a separate program. There should be no spaces in any program.

The output for each program is written in a separate line in `output.txt`. The output is of the format `[x_coordinate, y_coordinate, z_coordinate, total_distance]`.

A sample input-output pair is available in the respective files.

## Constraints
1. Each character `X`, `Y` or `Z` must be preceded by `+` or `-`.
2. There should not be any operator [`+` or `-`] just before a digit.
3. An operator [`+` or `-`] must be followed by either `X`, `Y` or `Z`

Examples of forbidden inputs are - 
```
X+Y-Z
+X+2(Y+Z)
X++Y-Z
```

## Logic
Each `()` in the program corresponds to a new level. This means that we must first compute the net movements in the inner level before proceeding with the instructions in the outer level.

A stack is maintained for movements along each direction (x, y and z). Each node in the stack corresponds to one level of the program.

`(` represents the beginning of a new level. At the beginning of a new level, we store the multiplier for this level as an attribute of the previous level.

`)` represents the end of the current level. At the end of the level, the value stored in this level represents the net movement in the level. We multiply this value by the multiplier stored in the previous level and then add it to the value stored in the previous level.
