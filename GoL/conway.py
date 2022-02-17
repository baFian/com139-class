"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

from ast import parse
import sys, argparse
from turtle import left
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # TODO: Implement the rules of Conway's Game of Life
    for i in range(1,N-1):
        for j in range(1,N-1):
            cell = grid[i,j]
            NeibCont = 0
            #top left
            if grid[i-1,j-1] == 255:
                NeibCont += 1
            #up
            if grid[i-1,j] == 255:
                NeibCont += 1
            #top right
            if grid[i-1,j+1] == 255:
                NeibCont += 1
            #left
            if grid[i,j-1] == 255:
                NeibCont += 1
            #right
            if grid[i,j+1] == 255:
                NeibCont += 1
            #down left
            if grid[i+1,j-1] == 255:
                NeibCont += 1
            #down
            if grid[i+1,j] == 255:
                NeibCont += 1
            #down right
            if grid[i+1,j+1] == 255:
                NeibCont += 1
            

            if cell == 255:
                if NeibCont == 3 or NeibCont == 2:
                    cell = 255
                else:
                    newGrid[i,j] = 0
            else:
                if NeibCont == 3:
                    newGrid[i,j] = 255
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


def customGrid(grid, file, N):
    f = open(file,"r")
    grid = grid.reshape(-N,N)
    #print("The array dimension is ", len(grid.shape))
    for line in f:
        #print(line)
        x = line.split(",")
        
        grid[int(x[0]),int(x[1])] = 255

    return grid
# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    parser.add_argument("Size", type = int)
    parser.add_argument("file")
    args = parser.parse_args()
    print(args.Size)
    print(args.file)

    
    # set grid size
    #N = 100
    N = args.Size
    #Universe = N*N
        
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])

    grid = np.zeros((N*N),dtype=int)
    grid = customGrid(grid,args.file, N)

    # populate grid with random on/off - more off than on
    #grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    #grid = np.zeros(N*N).reshape(N, N)
    addGlider(1, 1, grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()

# call main
if __name__ == '__main__':
    main()