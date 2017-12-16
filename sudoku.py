class Sudoku:
    x, y = 'ABCDEFGHI', '123456789'

    def __init__(self, puzzle_str, diagonal = True, debug = False):
        if len(puzzle_str) == 9*9:
            self.boxes = self.cross(self.x, self.y)
            self.grid = self.grid(puzzle_str)
            rows = [self.cross(r,self.y) for r in self.x]
            cols = [self.cross(self.x,c) for c in self.y]
            squares = [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
            self.combo = rows + cols + squares 
            if diagonal:
                diagonals = [[a+b for a,b in zip(self.x,self.y)],[a+b for a,b in zip(self.x,self.y[::-1])]]
                self.combo += diagonals
            self.units = dict((s, [u for u in self.combo if s in u]) for s in self.boxes)
            self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.boxes)
            self.debug = debug
            if debug: print('sudoku created')
        else:
            print('''invalid format detected. 
            Please ensure the puzzle is a flattened string 
            consisting of 81 values 
            (corresponding to the 9x9 values in a sudoku grid)
            Each value should be a single integer 
            ranging between 1-9
            or alternatively a '.' 
            to indicate an unknown value 
            (e.g. "12345..92.4...etc")
            ''')

    def grid(self, puzzle):
        grid = {}
        for box, p in zip(self.boxes, puzzle):
            if p == '.':
                p = self.y
            grid[box] = p    
        return grid

    def cross(self, x,y):
        return [a+b for a in x for b in y]

    def display(self):
        width = 1 + max(len(self.grid[s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.x:
            print(''.join(self.grid[r+c].center(width)+('|' if c in '36' else '') for c in self.y))
            if r in 'CF': 
                print(line)

    def eliminate(self):
        #solved_values = [value for value in self.grid.keys() if len(self.grid[value]) == 1]
        for box in self.boxes:
            if len(self.grid[box]) == 1: #solved value
                for peer in self.peers[box]:
                    if self.grid[box] in self.grid[peer]:
                        if self.debug: print('\n elimination: remove',box,"'s",self.grid[box],'from',peer,"'s",self.grid[peer])
                        self.grid[peer] = self.grid[peer].replace(self.grid[box], '')
                        if self.debug: print('   ...to',self.grid[peer])

    def only_choice(self):
        for unit in self.combo:
            for n in self.y:
                dplaces = [box for box in unit if n in self.grid[box]]
                if len(dplaces) == 1 and self.grid[dplaces[0]] != n:
                    if self.debug: print('\n only choice: \n  modifying',dplaces[0],'from',self.grid[dplaces[0]],'to',n)
                    self.grid[dplaces[0]] = n
    
    def naked_twins(self):
        for combination in self.combo:
            candidates = {t : self.grid[t] for t in combination if len(self.grid[t]) > 1}
            twins = {}
            for c in candidates.items():
                if c[1] in twins:
                    twins[c[1]].append(c[0])
                else:
                    twins[c[1]] = [c[0]]
            for twin in twins.items():
                if len(twin[1]) > 1 and len(twin[0]) == 2: #make sure its a twin, not a triplet, etc
                    for other_candidate in candidates:
                        if other_candidate != twin[1][0] and other_candidate != twin[1][1]:
                            if self.debug: print('\n naked twin:',twin)
                            if twin[0] in self.grid[other_candidate]:
                                if self.debug: print('  modifying',other_candidate,'from',self.grid[other_candidate])
                                self.grid[other_candidate] = self.grid[other_candidate].strip(twin[0])
                                if self.debug: print('  ...to',self.grid[other_candidate])

    def clone(self):
        copy = Sudoku('0'*81)
        copy.boxes = self.boxes
        copy.grid = self.grid
        copy.combo = self.combo
        copy.units = self.units
        copy.peers = self.peers
        if self.debug: print('\n sudoku cloned')
        return copy

    def reduce_puzzle(self):
        solutions = []
        while True:
            self.eliminate()
            self.only_choice()
            self.naked_twins()
            prev_solutions = solutions
            solutions = [value for value in self.grid.keys() if len(self.grid[value]) == 1]
            if len(solutions) == 9*9: 
                if self.debug: print('\n solved')
                return True
            elif len(prev_solutions) == len(solutions): 
                if self.debug: print('\n stalled')
                return False    

    def trial_and_error(self):     
        min_val, min_box = min((len(self.grid[min_box]), min_box) for min_box in self.boxes if len(self.grid[min_box]) > 1)
        for val in self.grid[min_box]:
            if self.debug: print('\n trial and error:  \n',min_box,min_val)
            clone = self.clone()
            clone.grid[min_box] = val
            clone.solve()

    def solve(self):
        solved = self.reduce_puzzle()
        if solved is False: 
            solutions = [value for value in self.grid.keys() if len(self.grid[value]) == 1]
            if len([box for box in self.grid.keys() if len(self.grid[box]) == 0]): #failed if any squares are empty
                if self.debug: print("\n incomplete solution")
                return False
            #elif [self.grid[box] == self.grid[peer] for box in self.boxes for peer in self.peers]: #failed if any squares are duplicates of peers
            #    print("\n invalid solution")
            #    return False
            self.trial_and_error()
        else:
            self.display()
            return True
 
if __name__ == '__main__':    
    example_puzzle = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    example_puzzle3 = '..3...6..9..3.5..1..18.64....8..2...7.......8..67.82....26..5..8..2....9..5.1.3..'
    example_puzzle2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    a = Sudoku(diag_sudoku_grid)
    a.solve()
    print('\n')
    b = Sudoku(example_puzzle3, diagonal = False)
    b.solve()
    print('\n')
    c = Sudoku(example_puzzle, diagonal = False)
    c.solve()

