import numpy as np
import random
import Types

class ACO:
    def __init__(self, 
            maze: Types.Maze, start: Types.Coord, goal: Types.Coord, 
            ants: int, pheromones: float, evaporation: float, initialisation: float, alpha: float
        ) -> None:
        '''
        :param ants: number of ants for each iteration.
        :param evaporation: fraction by which all pheromones evaporate.
        :param alpha: chance of an ant trying a non-optimal next step.
        :initialisation: the level at which the pheromones will be set initialy
        :alpha: the chance (fraction) an ant takes a random path
        '''

        # Values
        self.ants = ants
        self.pheromones = pheromones
        self.evaporation = evaporation
        self.initialisation = initialisation
        self.alpha = alpha

        # Structural elements
        self.start = start
        self.goal = goal
        self.height, self.width = maze.shape
        
        # Initialise maze
        self.maze = self.initialise_maze(maze)

    def initialise_maze(self, maze: Types.Maze) -> Types.Maze:
        '''
        Initialises the maze with a pheromone level of 'initialisation' in every hallway .
        '''
        maze[maze == 0] = self.initialisation
        return maze

    def next_iteration(self):
        '''
        Runs one iteration of ants going through the maze and leaving pheromones
        '''

        paths = self.__find_paths()
        self.__update_pheromones(paths)
    
    ###################
    # Private functions
    ###################
        
    def __find_paths(self) -> list[Types.Path]:
        paths = []

        for ant in range(self.ants):
            # TODO: make path a heap, so you can easily pop elements (should be faster?)

            # keep the path and points on which we need to choose the next step
            last_pos = self.start
            pos = self.start
            path = [self.start]
            junctions = [self.start]
            
            
            while not pos == self.goal:
                # Get next step
                next_pos, was_junction = self.__find_next_step(last_pos, pos)

                # Go back when stuck in a corner or back on point where ant has already been
                if next_pos == pos or next_pos in junctions:
                    go_back_until = next_pos
                    next_pos = path.pop()
                    while next_pos != go_back_until:
                        next_pos = path.pop()

                # Update lists and positions
                path.append(next_pos)
                if was_junction: junctions.append(pos)
                last_pos = pos
                pos = next_pos
            
            paths.append(path)

        print(paths)
        return paths

    def __find_next_step(self, last_pos: Types.Coord, pos: Types.Coord) -> tuple[Types.Coord, bool]:
        """
        Returns the next step for the ant, or the current position if there is no valid next step.
        """
        x, y = pos
        neighbours: list[Types.Coord] = []

        moves = [(0, -1), (0, 1), (1, 0), (-1, 0)] # North, East, South, West

        # Loop over all possible next moves and save the valid ones
        for dx, dy in moves:
            nx, ny = int(x + dx), int(y + dy)

            # Check bounds
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                continue

            # Check if cell is not a wall or the last position (swap x and y when accessing the maze)
            if self.maze[ny, nx] == -1 or (nx, ny) == last_pos:
                continue
            
            # If we can go to the goal, always go there
            if (ny, nx) == self.goal:
                return (nx, ny), False
                
            neighbours.append((nx, ny))

        # Find the weights of each neighbour (swap x and y when accessing the maze)
        weights = []
        for x, y in neighbours:
            weights.append(self.maze[y, x])

        # Return current step if there is no valid neighbour
        if len(neighbours) == 0:
            return pos, False

        # Return a weighted choice of next steps and wheather current pos is a junction
        was_junction = len(neighbours) > 1
        next_step = random.choices(neighbours, weights=weights, k=1)[0]
        if random.uniform(0, 1) < self.alpha:
            next_step = random.choice(neighbours)
        return next_step, was_junction

    def __update_pheromones(self, paths: list[Types.Path]):
        # Evaporation 
        mask = self.maze != -1
        self.maze[mask] = (1 - self.evaporation) * self.maze[mask]

        # Deposition (swap x and y when accessing the maze)
        for path in paths: 
            pheromone_per_cell = self.pheromones / len(path)
            for x, y in path:
                self.maze[y, x] = self.maze[y, x] + pheromone_per_cell