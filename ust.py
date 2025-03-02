# generate uniform spanning tree via wilson's algorithm; vertex based

import turtle as t
import random
import time

# universal cell size
cell_size = 40

# setup turtle
def turtle_setup():
    screen = t.Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)
    return screen
    
# get coordinate given row and column number
def get_coord(row, col, nrows, ncols, cell_size):
    x = col * cell_size - (ncols - 1) * cell_size / 2
    y = (nrows - 1 - row) * cell_size - (nrows - 1) * cell_size / 2
    return x, y

# draw path between two points
def draw_path(start, end, color, node=False):
    x1, y1 = get_coord(*start, nrows, ncols, cell_size)
    x2, y2 = get_coord(*end, nrows, ncols, cell_size)

    t.pencolor(color)
    t.penup()
    if node:
        screen.tracer(0)
    t.goto(x1, y1)
    if node:
        screen.update()
        screen.tracer(1)
        t.dot(5, color)
    t.pendown()
    t.goto(x2, y2)
    if node:
        t.dot(5, color)

# draw grid using draw_path
def draw_grid(nrows, ncols, screen):
    screen.tracer(0)
    t.speed(0)

    # draw vertical edges
    for col in range(ncols + 1):
        for row in range(nrows):
            draw_path((row, col), (row + 1, col), "black")

    # draw horizontal edges
    for row in range(nrows + 1):
        for col in range(ncols):
            draw_path((row, col), (row, col + 1), "black")

    screen.update()
    screen.tracer(1)

# generate uniform spanning tree with wilson's algorithm
def wilsons_algorithm(nrows, ncols):
    t.speed(1)
    t.pensize(2)

    # initialize root of tree; default (0, 0)
    root = (0, 0)
    visited = {root}
    not_visited = {(row, col) for row in range(nrows + 1) for col in range(ncols + 1)} - visited

    # wilson's algorithm
    while not_visited:
        # pick a random vertex to start at
        start = random.choice(list(not_visited))
        path = [start]

        # conduct random walk
        while path[-1] not in visited:
            row, col = path[-1]

            # random walk
            dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            new_row, new_col = row + dir[0], col + dir[1]

            # check that we are in bounds
            if 0 <= new_row <= nrows and 0 <= new_col <= ncols:
                if (new_row, new_col) in path: # loop detected so remove path
                    loop_start_index = path.index((new_row, new_col))
                    path = path[:loop_start_index + 1]
                else: # no loop so append next vertex
                    path.append((new_row, new_col))

        for i in range(len(path) - 1):
            visited.add(path[i])
            not_visited.discard(path[i])
            draw_path(path[i], path[i + 1], "red", True)

        time.sleep(0.2)

if __name__ == "__main__":

    print("generating m x n grid of VERTICES...")
    nrows = int(input("number of rows: "))
    ncols = int(input("number of columns: "))

    screen = turtle_setup()
    draw_grid(nrows, ncols, screen)
    wilsons_algorithm(nrows, ncols)

    # closes turtle
    t.hideturtle()
    t.done()