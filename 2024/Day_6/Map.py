from copy import deepcopy
from enum import Enum
from Guard import Guard
from collections.abc import Sequence


class Status(Enum):
    """
    Enumeration of the various states of a patrol

    Members
    -------
    NONE: Status
        No patrols launched.
    QUIT: Status
        The guard has left the map.
    LOOP: Status
        The guard is in an endless loop.
    """
    NONE = 0
    QUIT = 1
    LOOP = 2


class Map():
    """
    A guard's patrol.

    Attributes
    ----------
        __obstacles: Sequence[Sequence[bool]]
            The presence of obstacles at every position.
        __visited: Sequence[Sequence[bool]]
            Cells visited by the guard during his last patrol.
        __n_row: int
            The number of rows.
        __n_col: int
            The number of columns.
        __guard: Guard
            The guard.
        __status: Status
            The status of the last patrol.
        __tmp_obs: Sequence[int]
            Coordinates of the temporary obstacle.
    """

    __obstacles: Sequence[Sequence[bool]]
    __visited: Sequence[Sequence[bool]]
    __n_row: int
    __n_col: int
    __guard: Guard
    __status: Status
    __tmp_obs: Sequence[int]

    def __init__(self, grid: Sequence[Sequence[bool]], guard: Guard):
        self.__obstacles = deepcopy(grid)
        self.__n_row = len(grid)
        self.__n_col = len(grid[0])
        self.__guard = guard
        self.__status = Status.NONE
        self.__tmp_obs = [-1, -1]
        self.__visited = [
            [False for _ in range(0, self.__n_col)]
            for _ in range(0, self.__n_row)
        ]

    @staticmethod
    def build(file_name: str):
        """
        Builds the Map object according to the information contained in a file.

        Parameters
        ----------
        file_name: str
            The path file

        Return
        ------
        Map
            the map with its guard and obstacles.
        """
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            guard = None
            grid = []
            for i in range(0, len(lines)):
                tab = list(lines[i].strip())
                row = []
                for j in range(0, len(tab)):
                    if tab[j] == '#':
                        row.append(True)
                    else:
                        row.append(False)
                        if tab[j] != '.':
                            guard = Guard(i, j, tab[j])
                grid.append(row)
            return Map(grid, guard)
        return None

    @property
    def status(self) -> Status:
        """
        The status of the last patrol.
        """
        return self.__status

    @property
    def visited(self) -> Sequence[Sequence[bool]]:
        """
        The already visited cells by the guard.
        """
        return self.__visited

    @property
    def guard(self) -> Guard:
        """
        The guard.
        """
        return self.__guard

    def add_temporary_obstacle(self, x: int, y: int) -> None:
        """
        Adds a temporary obstacle.

        Attributes
        ----------
        x: int
            the x coordinate of the temporary obstacle.
        y: int
            the y coordinate of the temporary obstacle.

        Raises
        ------
        ValueError
            when the coordinates are outside de map or in an already existed
            obstacle.
        """
        if (x < 0 or x >= self.__n_row or y < 0 or y >= self.__n_col):
            raise ValueError("Out of bound coordinates.")
        if self.__obstacles[x][y]:
            raise ValueError("An obstacle already exists.")
        xo, yo = self.__tmp_obs
        if xo != -1 and yo != -1:
            self.__obstacles[xo][yo] = False
        self.__tmp_obs = [x, y]
        self.__obstacles[x][y] = True

    def remove_temporary_obstacle(self) -> None:
        """
        Removes the temporary obstacle.
        """
        self.__obstacles[self.__tmp_obs[0]][self.__tmp_obs[1]] = False
        self.__tmp_obs = [-1, -1]

    def move(self):
        """
        Moves the guard if it can, or changes its direction if it faces an
        obstacle.
        """
        # The guard moves forward and gets its coordinates.
        self.__guard.forward()
        x, y = self.__guard.coords

        # Changes patrol status to QUIT if the guard leaves the map.
        if (x < 0 or y < 0 or x >= self.__n_row or y >= self.__n_col):
            self.__status = Status.QUIT

        # The guard steps back and changes direction if he has moved over an
        # obstacle.
        elif self.__obstacles[x][y]:
            self.__guard.backward()
            self.__guard.rotate()

    def patrol(self):
        """
        The guard performs its patrol.
        At the end, the status and visited cells are updated with this patrol.
        """
        # Reset the guard, the patrol's status and the visited cells.
        self.__status = Status.NONE
        self.__guard.reset()
        self.__visited = [
            [False for _ in range(0, self.__n_col)]
            for _ in range(0, self.__n_row)
        ]

        # The guard moves as long as he hasn't left the map, or as long as he
        # isn't walking in an endless loop.
        movements = set()
        while self.__status == Status.NONE:
            # Gets its coordinates.
            x, y = self.__guard.coords

            # Make its cells visited.
            self.__visited[x][y] = True

            # If the movement (i.e. same coordinates and direction) has already
            # been made, then the guard is in an endless loop.
            mov = hash(self.__guard)
            if mov in movements:
                self.__status = Status.LOOP
            else:
                movements.add(mov)

            # Move the guard.
            self.move()
