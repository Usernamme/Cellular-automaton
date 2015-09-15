import Tkinter as tk

class life:

    def __init__(self, board, side, multiplier, live_list, born_list, input_cells):

        self.board = board
        self.side = side
        self.multiplier = multiplier

        self.paused = True

        self.live_list = live_list #number of neighbors required for a cell to survive
        self.born_list = born_list #number of neigbors required for a dead cell to become live
        self.input_cells = input_cells #manually created cell groups

        self.iterations = set() #used for checking if the board has stabilized
        self.age = 0
        self.stable = False

    #gets coords for all possible neighbors of a cell
    def get_neighbors(self, x, y):

        #the two if statements create the numbers to which the coords of the
        #original cell will be added to create the neighboring cell coords
        #if the cell is on the edge the neigbors wrap around to the other side
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
        neighbors = []
        for loc in locs:
            neighbors.append((x + loc[0], y + loc[1]))

        return neighbors

    #counts living neigbors of a cell
    def count_neigbors(self, x, y):

        count = 0
        self.neighbors = self.get_neighbors(x, y)
        for cell in self.neighbors:
            if cell in self.board:
                count += 1
        return count

    #advances the board to the next generation
    #board could also be called live_previously
    def step(self):

        live = set()
        dead_previously = set()
        for cell in self.board:
            #checks which living cells will survive
            if self.count_neigbors(cell[0], cell[1]) in self.live_list:
                live.add(cell)
            #the only dead cells that have the possibility of becoming living
            #are the neighbors of previously living cells
            dead_previously.update(self.get_neighbors(cell[0], cell[1]))

        #chceck which dead cells with the possibiity of becoming live become live
        for cell in dead_previously:
            if self.count_neigbors(cell[0], cell[1]) in self.born_list:
                live.add(cell)

        self.board = set(live)
        self.age += 1

    def stability_check(self): #TODO doesnt do what i want it to do

        if not self.stable:
            self.iterations.add(frozenset(self.board))

            if self.age % 4 == 0:
                if len(self.iterations) <= 2:
                    self.stable = True
                else:
                    self.iterations = set()

    #button command
    def pause(self):

        self.paused = not self.paused

    #switches the state of a cell where the user clicks
    def add_cell(self, event):

        cell = (event.x/self.multiplier, event.y/self.multiplier)
        if cell in self.board:
            self.board.remove(cell)
        else:
            self.board.add(cell)
        self.draw_board()

    #button command
    def cell_input(self): #button command

        self.board.update(self.input_cells)

    #also binds the left mouse button to add_cell inside the game window
    def tkinter_init(self):

        self.master = tk.Tk()

        self.window = tk.Canvas(self.master, width=self.side*10, height=self.side*10)
        self.window.bind("<Button-1>", self.add_cell)
        self.window.pack()

        self.pause_button = tk.Button(self.master, text="Pause/Unpause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT)

        self.speed_entry = tk.Entry(self.master, width=8)
        self.speed_entry.pack(side=tk.RIGHT)
        self.speed_entry.insert(0, "500")

        self.speed_label = tk.Label(self.master, text="Generation duration in ms:")
        self.speed_label.pack(side=tk.RIGHT)

        self.input_button = tk.Button(self.master, text="Input", command=self.cell_input)
        self.input_button.pack(side=tk.LEFT)

    #creates a black square as the game board's background and draws
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
