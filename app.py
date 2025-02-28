from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from flask_socketio import SocketIO
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*")

GRID_SIZE = 20 

@app.route('/')
def index():
    return render_template("index.html")

def get_neighbors(row, col, nrows, ncols):
    """Returns valid neighbors in a grid"""
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = [(row + dr, col + dc) for dr, dc in directions]
    return [(r, c) for r, c in neighbors if 0 <= r < nrows and 0 <= c < ncols]

@socketio.on('start_random_walk')
def complete_random_walk(data):
    """Runs Wilson’s Algorithm and sends real-time updates to the frontend"""
    nrows, ncols = data["rows"], data["cols"]
    
    visited = set()
    not_visited = set((r, c) for r in range(nrows) for c in range(ncols))

    # Choose a random start point
    start = random.choice(list(not_visited))
    visited.add(start)
    not_visited.remove(start)

    while not_visited:
        current = random.choice(list(not_visited))
        path = []

        while current not in visited:
            path.append(current)
            current = random.choice(get_neighbors(*current, nrows, ncols))

        # Add path to visited set
        for i in range(len(path) - 1):
            socketio.sleep(0.1)  # Slow down for visualization
            socketio.emit("draw_edge", {"from": path[i], "to": path[i + 1]})
            visited.add(path[i])
            not_visited.discard(path[i])

    socketio.emit("done")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, log_output=True)
