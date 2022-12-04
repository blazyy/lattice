# Lattice - A pathfinding visualizer

This is a pathfinding visualizer built using PyGame. To know more about how I built this, please read my [blog post](https://faaez.co.in/blog/pathfinding-visualizer).

Currently, it has the capability to visualize the following algorithms:

* Depth First Search
* Breadth First Search
* Dijkstra's Shortest Path Algorithm
* A* Search
* Iterative Randomized Depth First Search for Maze Generation

Since the game has no UI based controls (except for drawing walls and origin/goal nodes), you will have to use the keyboard to achieve certain behaviours. Following is the event key mapping which will show you how to do everything you need to do:

## Event mapping:

* Drag mouse - Draw walls 
* C - Clear Lattice
* M - Generate maze (using randomized DFS)
* E - Erases wall nodes (Have to hold down key while dragging/clicking mouse)
* O - Sets origin node (Have to hold down key while dragging/clicking mouse, can only set 1 origin)
* G - Sets goal node (Have to hold down key while dragging/clicking mouse, can only set 1 goal)
* R - Generate random walls
* L - Begin Game of Life simulation
* D - Begin DFS visualization (only starts if Origin and Goal are both set)
* B - Begin BFS visualization (only starts if Origin and Goal are both set)
* K - Begin Dijkstra's Pathfinding visualization
* A - Begin A* Search Visualization
* Q - Quit

**Note** During a visualization, keystrokes will still be recorded but won't be acted upon in real-time, so please don't press keys before a visualization has stopped. Else, the events will stack and you will have no control over the visualization until it has finished processing all your past inputs. 