# visualize generation of uniform spanning tree via wilson's algorithm
# source: https://n.ethz.ch/~ywigderson/math/static/UniformSpanningTrees.pdf

import turtle as t
import random
import time

# define cell size
cell_size = 40

# setup turtle
def turtle_setup():
    screen = t.Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)
    t.hideturtle()
    t.setundobuffer(1000000)
    return screen
    
# get coordinate given row and column number
def get_coord(row, col, nrows, ncols, cell_size):
    x = col * cell_size - (ncols - 1) * cell_size / 2
    y = (nrows - 1 - row) * cell_size - (nrows - 1) * cell_size / 2
    return x, y

def draw_dot(loc, color, nrows, ncols, size=5):
    x, y = get_coord(loc[0], loc[1], nrows, ncols, cell_size)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.dot(size, color)

# draw path between two points
def draw_path(start, end, color):
    x1, y1 = get_coord(*start, nrows, ncols, cell_size)
    x2, y2 = get_coord(*end, nrows, ncols, cell_size)

    t.pencolor(color)
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.goto(x2, y2)
    time.sleep(0.04)
    t.update()

# undraw
def undraw_path():
    for _ in range(4):
        t.undo()
    time.sleep(0.04)

# draw grid
def draw_grid(nrows, ncols):
    t.speed(0)
    for row in range(nrows):
        for col in range(ncols):
            draw_dot((row, col), "black", nrows, ncols)
    t.update()

# generate uniform spanning tree with wilson's algorithm
def wilsons_algorithm(nrows, ncols):
    t.speed(1)
    t.pensize(2)
    screen.tracer(1)

    # initialize root of tree; choose at random from list of all vertices
    not_visited = {(row, col) for row in range(nrows) for col in range(ncols)}
    root = random.choice(list(not_visited))

    # visually locate root 
    draw_dot(root, "red", nrows, ncols, 8)
    time.sleep(1)
    draw_dot(root, "white", nrows, ncols, 8)
    draw_dot(root, "blue", nrows, ncols)
    
    visited = {root}
    not_visited.remove(root)

    initial = True

    # wilson's algorithm
    while not_visited:
        start = random.choice(list(not_visited))
        draw_dot(start, "red", nrows, ncols)
        path = [start]

        # conduct random walk
        while True:
            old_pos = path[-1]

            # choose next node
            while True:
                dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                new_pos = (old_pos[0] + dir[0], old_pos[1] + dir[1])

                if 0 <= new_pos[0] < nrows and 0 <= new_pos[1] < ncols:
                    break

            # if existing tree hit
            if new_pos in visited:
                draw_path(old_pos, new_pos, "blue")
                for node in path:
                    visited.add(node)
                    not_visited.discard(node)
                break

            # loop detected
            if new_pos in path:
                loop_start_index = path.index(new_pos)
                draw_path(old_pos, new_pos, "red")
                time.sleep(0.6)

                # undraw path
                for _ in range(loop_start_index, len(path)):
                    undraw_path()

                path = path[:loop_start_index + 1]

            # no loop, so append next vertex
            else:
                path.append(new_pos)
                draw_path(old_pos, new_pos, "blue")

        if initial:
            draw_dot(root, "black", nrows, ncols)
            initial = False

        draw_dot(start, "black", nrows, ncols)

if __name__ == "__main__":
    print("generating m x n grid of vertices...")
    nrows = int(input("number of rows: "))
    ncols = int(input("number of columns: "))

    screen = turtle_setup()
    draw_grid(nrows, ncols)
    wilsons_algorithm(nrows, ncols)

    t.hideturtle()
    t.done()