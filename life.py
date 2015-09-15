import Tkinter as tk

class life:
    """Class made to simulate a 2d cellular automaton using Tkinter for graphics.
       Currently only allows 2 possible cell states.
       Cells are tuples of the 2 """
    def __init__(self, board, side, multiplier, live_list, born_list, input_cells):
        self.board = board
        self.side = side
        self.multiplier = multiplier

        self.paused = True

        self.live_list = live_list #Number of neighbors required for a cell to survive
        self.born_list = born_list #Number of neigbors required for a dead cell to become live
        self.input_cells = input_cells #Manually created cell groups

        self.iterations = set() #used for checking if the board has stabilized
        self.age = 0
        self.stable = False

    #Gets coords for all possible neighbors of a cell
    def get_neighbors(self, cell):
        #The two if statements create the values to which the coords of the
        #original cell will be added to create the neighboring cell coords
        #if the cell is on the edge the neigbors wrap around to the other side
        x = cell[0]
        y = cell[1]

        if x == 0:
            xlocs = [self.side-1,0,1]
        elif x == self.side-1:
            xlocs = [-1,0,-self.side+1]
        else:
            xlocs = range(-1,2)

        if y == 0:
            ylocs = [self.side-1,0,1]
        elif y == self.side-1:
            ylocs = [-1,0,-self.side+1]
        else:
            ylocs = range(-1,2)

        locs = [(a,b) for a in xlocs for b in ylocs]
        locs.remove((0,0))
        neighbors = set()
        for loc in locs:
            neighbors.add((x + loc[0], y + loc[1]))

        return neighbors

    #Advances the board to the next generation
    #board could also be called live_previously
    def step(self):
        live = set()
        potentially_born = set()
        #The conjunction of the list of all neighbors of a cell
        #and the board gives us the living neighbors of the cell
        #which is what is used to determine the number of neighbors of a cell
        for cell in self.board:
            #Checks which living cells will survive
            if len(self.get_neighbors(cell) & self.board) in self.live_list:
                live.add(cell)
            #The only dead cells that have the possibility of becoming living
            #are the neighbors of previously living cells
            potentially_born.update(self.get_neighbors(cell))

        #Check which dead cells with the possibiity of becoming live become live
        for cell in potentially_born:
            if len(self.get_neighbors(cell) & self.board) in self.born_list:
                live.add(cell)

        self.board = set(live)
        self.age += 1

    def stability_check(self): #XXX doesn't work, was an attempt at detecting loops
        if not self.stable:
            self.iterations.add(frozenset(self.board))

            if self.age % 4 == 0:
                if len(self.iterations) <= 2:
                    self.stable = True
                else:
                    self.iterations = set()

    #Tkinter button command switching the boolean self.paused
    def pause(self):
        self.paused = not self.paused

    #Switches the state of a cell where the user clicks
    def add_cell(self, event):
        cell = (event.x/self.multiplier, event.y/self.multiplier)
        if cell in self.board:
            self.board.remove(cell)
        else:
            self.board.add(cell)
        self.draw_board()

    #Tkinter button command adding the set input_cells into the board
    def cell_input(self):
        self.board.update(self.input_cells)

    #Contains all the Tkinter code and should be run right after creating
    #a class. Isn't in __init__ because of methods used by button widgets
    def tkinter_init(self):
        self.master = tk.Tk()

        self.window = tk.Canvas(self.master, width=self.side*10, height=self.side*10)
        self.window.bind("<Button-1>", self.add_cell)
        self.window.pack()

        self.speed_entry = tk.Entry(self.master, width=8)
        self.speed_entry.pack(side=tk.RIGHT)
        self.speed_entry.insert(0, "250")

        self.speed_label = tk.Label(self.master, text="Generation duration in ms:")
        self.speed_label.pack(side=tk.RIGHT)

        self.input_button = tk.Button(self.master, text="Input", command=self.cell_input)
        self.input_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.master, text="Pause/Unpause", command=self.pause)
        self.pause_button.pack()

    #Creates a black square as the game board's background and draws
    #a white square for each live cell with a width of multiplier pixels
    def draw_board(self):
        self.window.delete("all")
        self.window.create_rectangle(0, 0,
                                     (self.side + 1)*self.multiplier,
                                     (self.side + 1)*self.multiplier,
                                     fill="black")
        for cell in self.board:
            self.window.create_rectangle(cell[0]*self.multiplier,
                                         cell[1]*self.multiplier,
                                         (cell[0] + 1)*self.multiplier,
                                         (cell[1] + 1)*self.multiplier,
                                         fill="#FFFFFF",outline="black")
