import numpy as np
import random 
import Types


def generate_maze(
        width: int, 
        height: int, 
        s: float = 0.0, 
        c: float = 0.0, 
        seed: int = random.randint(0, 10000)
        ) -> Types.ProtoMaze:
    '''
    Parameters: 
    - width and height: width and height of the maze
    - s: chance the maze will overwrite to go straight (normal 0.0)
    - c: chance a visited cell will be connected anyways (normal 0.0)
    '''
    
    # Set seed to allow deterministic maze creation
    random.seed(seed)

    # Create an array of all positions in the maze, and weather anh cardinal direction connects to another position
    maze = [
        [{"visited": False, "N": False, "E": False, "S": False, "W": False} for _ in range(width)] 
        for _ in range(height)
    ]

    w_pos = h_pos = 0 
    maze_carver(w_pos, h_pos, s, "N", c, maze, width, height)
    return maze

def maze_carver(
        w_pos: int, 
        h_pos: int, 
        s: float, 
        prev_dir: str, 
        c: float,
        maze: Types.ProtoMaze, 
        width: int, 
        height: int
        ):
    '''
    Docstring for maze_carver
    '''
    
    maze[h_pos][w_pos]["visited"] = True

    # Create array of directions and shuffle
    directions = ["N", "S", "E", "W"]

    # Add paramater to make paths straighter 
    random.shuffle(directions)
    if (random.random() <= s):
        directions.remove(prev_dir)
        directions.insert(0, prev_dir)
    
    for d in directions:
        nw, nh = w_pos, h_pos

        if d == "N": nh -= 1
        if d == "S": nh += 1
        if d == "W": nw -= 1
        if d == "E": nw += 1

        # Avoid index out of bounds error
        if 0 <= nw < width and 0 <= nh < height:
            # Visit if cell is not yet visited, or with a random chance c to create cycles
            if not maze[nh][nw]["visited"] or random.random() <= c:
                # Knock down the walls between cells
                if d == "N":
                    maze[h_pos][w_pos]["N"] = True
                    maze[nh][nw]["S"] = True
                if d == "S":
                    maze[h_pos][w_pos]["S"] = True
                    maze[nh][nw]["N"] = True
                if d == "W":
                    maze[h_pos][w_pos]["W"] = True
                    maze[nh][nw]["E"] = True
                if d == "E":
                    maze[h_pos][w_pos]["E"] = True
                    maze[nh][nw]["W"] = True

            # Only continue to carve if cell was unvisited
            if not maze[nh][nw]["visited"]: 
                maze_carver(nw, nh, s, d, c, maze, width, height)

def maze_to_array(maze: Types.ProtoMaze) -> Types.Maze:
    '''
    Turns a maze of type Maze into a numpy array of floats, where -1 is a wall, and 0 is a hallway.
    '''
    height = len(maze)
    width = len(maze[0])

    arr_width = 2 * width + 1
    arr_height = 2 * height + 1  

    maze_array = np.full([arr_height, arr_width], -1)

    for hi in range(height):
        for wi in range(width): 
            twi = 2 * wi + 1 # Translated Width Index
            thi = 2 * hi + 1 # Translated Height Index

            # Clear current space
            maze_array[thi][twi] = 0

            if 0 <= twi < arr_width and 0 <= thi < arr_height:
                # Check East
                if maze[hi][wi]["E"] == True:
                    maze_array[thi][twi + 1] = 0
                # Check South
                if maze[hi][wi]["S"] == True:
                    maze_array[thi + 1][twi] = 0

    return maze_array.astype(np.float32)