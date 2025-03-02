import turtle as t
import random

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
    x = col * cell_size - (ncols * cell_size) // 2
    y = (nrows - row - 1) * cell_size - (nrows * cell_size) // 2
    return x, y

# draw initial grid and create matrix
def draw_grid(nrows, ncols, screen):
    screen.tracer(0)
    t.pencolor("black")
    t.speed(0)

    # initialize grid and mark every vertex as not visited
    grid = [[0 for _ in range(ncols)] for _ in range(nrows)]

    # draw nrows x ncols grid
    for row in range(nrows):
        for col in range(ncols):
            # go to (x, y)
            x, y = get_coord(row, col, nrows, ncols, cell_size)
            t.penup()
            t.goto(x, y)
            t.pendown()

            # draw square
            for _ in range(4):
                t.forward(cell_size)
                t.right(90)

    screen.update()
    screen.tracer(1)
    return grid

# draw path between two points
def draw_path(start, end, color="red"):
    x1, y1 = get_coord(start[0], start[1], nrows, ncols, cell_size)
    x2, y2 = get_coord(end[0], end[1], nrows, ncols, cell_size)

    t.pencolor(color)
    t.penup()
    screen.tracer(0)
    t.goto(x1, y1)
    screen.update()
    screen.tracer(1)
    t.pendown()
    t.goto(x2, y2)
    t.penup()

# generate uniform spanning tree with wilson's algorithm
def wilsons_algorithm(grid):
    t.pencolor("red")
    t.speed(1)
    t.pensize(2)

    nrows = len(grid) - 1
    ncols = len(grid[0]) - 1

    # initialize root of tree; default (0, 0)
    root = (0, 0)
    visited = {root}

    # everything else goes in not_visited
    not_visited = {(row, col) for row in range(nrows + 1) for col in range(ncols + 1)}
    not_visited.remove(root)

    # wilson's algorithm
    while not_visited:
        # pick a random vertex to start at
        start = random.choice(list(not_visited))
        path = [start]

        # wilson's algorithm
        while path[-1] not in visited:
            row, col = path[-1]

            # random walk
            dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            new_row, new_col = row + dir[0], col + dir[1]

            # check that we are in bounds
            if 0 <= new_row <= nrows and 0 <= new_col <= ncols:
                if (new_row, new_col) in path: # loop detected so remove path
                    loop_start = path.index((new_row, new_col))
                    path = path[:loop_start + 1]
                else: # no loop so append next vertex
                    path.append((new_row, new_col))

        for i in range(len(path) - 1):
            visited.add(path[i])
            not_visited.discard(path[i])

            # draw next edge
            x1, y1 = get_coord(path[i][0], path[i][1], nrows, ncols, cell_size)
            x2, y2 = get_coord(path[i + 1][0], path[i + 1][1], nrows, ncols, cell_size)
            t.penup()
            t.goto(x1, y1)
            t.pendown()
            t.goto(x2, y2)
            t.dot(5, "red")

if __name__ == "__main__":

    nrows = int(input("number of rows: "))
    ncols = int(input("number of columns: "))

    screen = turtle_setup()
    grid = draw_grid(nrows, ncols, screen)
    wilsons_algorithm(grid)

    # closes turtle
    t.hideturtle()
    t.done()