from typing import List, Dict
import numpy as np

# While creating the maze
Cell = Dict[str, bool] 
ProtoMaze = List[List[Cell]]

# After making it into an ndarray maze, and running ACO
Maze = np.ndarray
Coord = tuple[int, int]
Path = list[Coord]