from life import *

side = 64 #side of the square board in cells
multiplier = 10 #width of a single cell in pixels
starting_cells = set([(32,30), (32,32)] + [(x,31) for x in range(29,36)])
live_list = [2,3] #number of neighbors required for a cell to survive
born_list = [3] #number of neigbors required for a dead cell to become live
input_cells = set([(32,30), (31,31), (32,31), (33,31), (32,32)]) #set of cells that will be put on the board by pressing a button

game = life(starting_cells, side, multiplier, live_list, born_list, input_cells)

game.tkinter_init()
game.draw_board()

def main():
    try:
        speed = int(game.speed_entry.get())
    except ValueError:
        speed = 250 #for some reason this is required instead of just pass

    if not game.paused:
        game.step()
        game.draw_board()

    game.master.after(speed, main)

main()
game.master.mainloop()
print game.board

#(32,30), (31,31), (32,31), (33,31), (32,32) - plusko
#(1,1), (1,2) (2,1), (2,2) - stvorec
#[(x,y) for x in range(1,3) for y in range(1,3)] - stvorec...
