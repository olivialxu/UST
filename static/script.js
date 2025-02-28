const socket = io();

const rows = 10, cols = 10;
const cellSize = 40;
const svgSize = Math.max(rows, cols) * cellSize + 50;

const svg = d3.select("svg")
    .attr("width", svgSize)
    .attr("height", svgSize)
    .style("background", "#f0f0f0");

// Draw the grid
for (let r = 0; r <= rows; r++) {
    for (let c = 0; c <= cols; c++) {
        svg.append("rect")
            .attr("x", c * cellSize)
            .attr("y", r * cellSize)
            .attr("width", cellSize)
            .attr("height", cellSize)
            .attr("stroke", "black")
            .attr("fill", "none");
    }
}

// Convert row/col to coordinates
function getCoord(row, col) {
    return [col * cellSize + cellSize / 2, row * cellSize + cellSize / 2];
}

// Listen for "draw_edge" event from Flask
socket.on("draw_edge", (data) => {
    const [x1, y1] = getCoord(data.from[0], data.from[1]);
    const [x2, y2] = getCoord(data.to[0], data.to[1]);

    svg.append("line")
        .attr("x1", x1)
        .attr("y1", y1)
        .attr("x2", x1)
        .attr("y2", y1)
        .attr("stroke", "red")
        .attr("stroke-width", 3)
        .transition()
        .duration(300)
        .attr("x2", x2)
        .attr("y2", y2);
});

// Listen for button press
document.getElementById("start").addEventListener("click", () => {
    svg.selectAll("line").remove(); 
    socket.emit("start_random_walk", { rows, cols });
});

socket.on("done", () => {
    alert("Tree generated.");
});
