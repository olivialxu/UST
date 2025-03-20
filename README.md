# Visualize Generation of Uniform Spanning Tree via Wilson's Algorithm
Alexandra Kim and Olivia Xu

This program visualizes the process of generating a uniform spanning tree (UST) on an m x n grid of vertices via Wilson's Algorithm, using Python turtle.

## Wilson's Algorithm:
1. **Initialization**: Denote the initial tree T_0 as the tree containing only the root vertex r (which is randomly chosen among all vertices in the graph)
2. **Loop Erasure Random Walk (LERW)**: If T_i is not yet a spanning tree, select a random vertex v not in T_i . Start a random walk from v (choose a cardinal direction at random (provided that the next vertex is in bounds) and advance forward). If the walk hits a vertex v in T_{i-1}, then erase the loop formed by the path from v to the vertex in T_{i-1}, return to v, and continue the random walk. When the random walk reaches a vertex in the tree T_{i-1}, then this new path is added to the existing tree to form T_i .
5. **Termination**: This algorithm terminates when the tree spans all vertices of the graph

## Our Program
1. Generate a grid of vertices (m x n) to represent the graph
2. Visually simulate the loop erasure random walk (LERW) via Wilson's Algorithm

## Sources
1. Josef Greilhuber our mentor!
2. [Random Explorations](https://bookstore.ams.org/view?ProductCode=STML/98) by Greg Lawson
2. [Uniform Spanning Trees and Determinantal Point Processes](https://n.ethz.ch/~ywigderson/math/static/UniformSpanningTrees.pdf) by Yuval Wigderson