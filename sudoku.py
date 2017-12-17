class Sudoku:
    x, y = 'ABCDEFGHI', '123456789'

    def __init__(self, puzzle_str, diagonal = False, debug = False):
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
                        if other_candidate not in twin[1]:
                            if self.debug: print('\n naked twin:',twin)
                            if len(set(twin[0]).intersection(self.grid[other_candidate])) > 0:
                                if self.debug: print('  modifying',other_candidate,'from',self.grid[other_candidate])
                                self.grid[other_candidate] = self.grid[other_candidate].strip(twin[0])
                                if self.debug: print('  ...to',self.grid[other_candidate])

    def solve(self):
        solutions = []
        while True:
            self.only_choice()
            self.naked_twins()
            self.eliminate()
            if len([box for box in self.grid.keys() if len(self.grid[box]) == 0]): #BASE CONDITION - if any squares are empty then its invalid solution
                if self.debug: print("\n invalid solution")
                return False
            prev_solutions = solutions
            solutions = [value for value in self.grid.keys() if len(self.grid[value]) == 1]
            if len(solutions) == 9*9: 
                if self.debug: print('\n solved')
                self.display()
                return True
            elif all(len(self.grid[s]) == 1 for s in self.boxes):
                self.display()
                return True
            elif len(prev_solutions) == len(solutions): 
                if self.debug: print('\n stalled')
                self.trial_and_error()
                return False

    def trial_and_error(self):     
        min_val, min_box = min((len(self.grid[min_box]), min_box) for min_box in self.boxes if len(self.grid[min_box]) > 1)
        if self.debug: print('\n trial and error:  \n',min_val,min_box,self.grid[min_box])
        for v in self.grid[min_box]:
            old_grid = self.grid.copy()
            self.grid[min_box] = v
            self.solve()
            self.grid = old_grid
            
if __name__ == '__main__':            
    diag = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    easy = '.21.37..4...24..9..63..5...2...16.38.39...15.81.35...9...4..91..4..79...3..12.46.'
    med = '..37.896.........39...3..4...8..5.7.2.9...8.6.7.6..5...3..9...86.........152.76..'
    hard = '....41..8..87.2.153....8.....3....6...5.3.2...4....7.....4....253.2.79..7..95....'
    evil = '.....549..491........9..7...2.6.7.3.6.......7.3.4.8.1...2..1........362..578.....'
    udacity = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    d,e,m,h,v,u = Sudoku(diag,diagonal = True),Sudoku(easy),Sudoku(med),Sudoku(hard),Sudoku(evil),Sudoku(udacity)
    print('\n diagonal:')
    d.solve()
    print('\n easy:')
    e.solve()
    print('\n medium:')
    m.solve()
    print('\n hard:')
    h.solve()
    print('\n evil:')
    v.solve()
    print('\n udacity:')
    u.solve()
