import turtle as t
import random

# universal cell size
cell_size = 40

def turtle_setup():
    screen = t.Screen()
    screen.setup(width=600, height=600)

    return screen
    
def get_coord(row, col, nrows, ncols, cell_size):
    x = col * cell_size - (ncols * cell_size) // 2
    y = (nrows - row - 1) * cell_size - (nrows * cell_size) // 2
    return x, y

def draw_grid(nrows, ncols, screen):
    screen.tracer(0)
    t.pencolor("black")
    t.speed(0)

    grid = []

    # mark every vertex as not visited
    for row in range(nrows + 1):
        grid.append([False] * (ncols + 1))

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
            
            t.penup()

    screen.update()
    screen.tracer(1)
    return grid

def complete_random_walk(grid):
    # visited = {boundary points of grid}
    # not_visited = {interior points}

    # while (not_visited is not empty):
    #   choose random point from not_visited
    #   conduct a random walk:
    #   while (current location is not in visited):
    #       choose a random direction
    #       advance to next point, draw using turtle
    #       move point to visited

    t.pencolor("red")
    t.speed(1)
    t.pensize(2)

    nrows = len(grid) - 1
    ncols = len(grid[0]) - 1

    # list of visited and not visited vertices
    visited = set()
    not_visited = set()

    # populate visited with boundary points
    for row in range(nrows + 1):
        visited.add((row, 0))
        visited.add((row, ncols))
    
    for col in range(ncols + 1):
        visited.add((0, col))
        visited.add((nrows, col))

    # everything else goes in not_visited
    for row in range(nrows + 1):
        for col in range(ncols + 1):
            if (row, col) not in visited:
                not_visited.add((row, col))
    

    print("VISITED")
    print(visited)

    print("NOT VISITED")
    print(not_visited)

    # generate uniform spanning tree via wilson's algorithm
    while not_visited:
        start = random.choice(list(not_visited))
        current = start
        # mark current as visited
        visited.add(current)
        not_visited.discard(current)

        x, y = get_coord(current[0], current[1], nrows, ncols, cell_size)
        t.penup()
        t.goto(x, y)
        t.dot(5, "red")

        print("STARTING AT", current)

        # random walk until we hit a visited point
        while True:
            row, col = current
            dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  # right, up, left, down
            new_row, new_col = row + dir[0], col + dir[1]

            # check that we are in bounds
            if 0 > new_row or new_row > nrows or 0 > new_col or new_col > ncols:
                break

            # move to new point
            current = (new_row, new_col)

            print("NOW AT", current)
                
            # draw path to (new_x, new_y)
            new_x, new_y = get_coord(new_row, new_col, nrows, ncols, cell_size)
            t.pendown()
            t.goto(new_x, new_y)
            t.dot(5, "red")

            # check that we are not at boundary
            if current in visited:
                break

            # mark new location as visited
            visited.add(current)
            not_visited.discard(current)
        
        t.penup()
        
        print("\nUPDATES")
        
        print("VISITED")
        print(visited)

        print("NOT VISITED")
        print(not_visited)

if __name__ == "__main__":

    nrows = int(input("number of rows: "))
    ncols = int(input("number of columns: "))

    screen = turtle_setup()
    grid = draw_grid(nrows, ncols, screen)
    complete_random_walk(grid)

    t.hideturtle()
    t.done()