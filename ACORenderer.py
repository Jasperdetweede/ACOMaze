from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np
import matplotlib.pyplot as plt
from ACO import ACO

class ACORenderer:
    """
    Handles rendering and interactive editing of a maze ndarray.

    Maze convention:
        -1 = wall
         0 = hallway
    """

    def __init__(self, optimiser: ACO):
        # Values
        self.optimiser = optimiser
        self.height, self.width = optimiser.maze.shape
        self.mode = "toggle"   # "draw", "erase", "toggle"
        self.mouse_down = False

        # Plotting
        self.fig, self.ax = plt.subplots()
        self.cmap = LinearSegmentedColormap.from_list(
            "pheromone",
            [(1, 1, 1), (0, 0.8, 0)]
        )
        self.norm = Normalize(vmin=0.0, vmax=1.0, clip=True)
        self.cmap.set_bad(color="black")

        data = np.ma.masked_where(self.optimiser.maze == -1, self.optimiser.maze)
        self.img = self.ax.imshow(
            data,
            cmap=self.cmap,
            norm=self.norm,
            interpolation="nearest"
        )

        # Functions
        self.ax.axis("off")
        self.ax.invert_yaxis()
        self.fig.tight_layout()

        self._connect_events()

    # -------------------------
    # Event wiring
    # -------------------------

    def _connect_events(self):
        canvas = self.fig.canvas
        canvas.mpl_connect("button_press_event", self._on_mouse_press)
        canvas.mpl_connect("button_release_event", self._on_mouse_release)
        canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
        canvas.mpl_connect("key_press_event", self._on_key_press)

    # -------------------------
    # Event handlers
    # -------------------------

    def _on_mouse_press(self, event):
        if event.button != 1:
            return
        self.mouse_down = True
        self._edit_from_event(event)

    def _on_mouse_release(self, event):
        self.mouse_down = False

    def _on_mouse_move(self, event):
        if not self.mouse_down:
            return
        self._edit_from_event(event)

    def _on_key_press(self, event):
        print("KEY EVENT:", repr(event.key))
        if event.key == "d":
            self.mode = "draw"
            print("Mode: draw")
        elif event.key == "e":
            self.mode = "erase"
            print("Mode: erase")
        elif event.key == "t":
            self.mode = "toggle"
            print("Mode: toggle")
        elif event.key == "i":
            print("Running next iteration")
            self.optimiser.next_iteration()
            self._redraw()
            

    # -------------------------
    # Editing logic
    # -------------------------

    def _edit_from_event(self, event):
        if event.xdata is None or event.ydata is None:
            return

        x = int(event.xdata + 0.5)
        y = int(event.ydata + 0.5)

        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        self._edit_cell(x, y)
        self._redraw()

    def _edit_cell(self, x: int, y: int):
        if self.mode == "draw":
            self.optimiser.maze[y, x] = -1
        elif self.mode == "erase":
            self.optimiser.maze[y, x] = 0.1
        elif self.mode == "toggle":
            self.optimiser.maze[y, x] = -self.optimiser.maze[y, x] - 1

    # -------------------------
    # Rendering
    # -------------------------

    def _redraw(self):
        data = np.ma.masked_where(self.optimiser.maze == -1, self.optimiser.maze)
        self.img.set_data(data)
        self.fig.canvas.draw_idle()

    # -------------------------
    # Public API
    # -------------------------

    def show(self):
        """
        Blocks execution and opens the interactive window.
        """
        plt.show()

    def get_maze(self) -> np.ndarray:
        """
        Returns the current maze state.
        """
        return self.optimiser.maze
