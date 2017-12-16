(Udacity's Artificial Intelligence NanoDegree - Term 1 - Project 1)
# sudoku
This program solves any sudoku puzzle!
just write a sudoku puzzle as a flattened string (with the unknown values as a '.'):
# puzzle = '12321342233...2.3.3..433.2..etc'
create a sudoku object, initialised with that puzzle
# s = Sudoku(puzzle)
the puzzle can now be seen as a grid using the following command:
# s.display()
and solved using an array of heuristics / methods using the command:
# s.solve()
if you wish to solve a variant of the sudoku puzzle wherein the diagonals must be considered, then initialise the sudoku object like so:
# s = Sudoku(puzzle,diagonal = True)
similarly, if you wish to see the methods and process the program uses to solve the puzzle, use this command when initialising:
# s = Sudoku(puzzle, debug = True)
Enjoy
