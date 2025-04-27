from collections.abc import Sequence, Mapping


class Guard():
    """
    Representation of a guard that can move in a 2-dimensional plane with 4
    possible directions.

    Attributes
    ----------
    __init_x: int
        Its original position in x.
    __init_y: int
        Its original position in y.
    __init_dir: int
        Its original direction represented with an int:
        0 is up; 1 is down; 2 is left; 3 is right.
    __coords: Sequence[int]
        Its current coordinates in x and y.
    __dir: int
        Its current direction.

    Class Attributes
    ----------------
    converts: Mapping[str, int]
        contains the mapping between the guard direction as a character and the
        corresponding integer.
    movements: Sequence[Sequence[int]]
        contains the movements the guard should make according to its current
        direction.
    rotations: Sequence[int]
        contains the rotation the guard should make according its current
        direction.
    """
    converts = {'^': 0, 'v': 1, '<': 2, '>': 3}
    movements = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    rotations = [3, 2, 0, 1]
    __init_x: int
    __init_y: int
    __coords: Sequence[int]
    __dir: int
    __init_dir: int

    def __init__(self, x: int, y: int, orientation: str):
        if orientation not in Guard.converts:
            raise ValueError("Unexpected guard's orientation!")
        self.__init_x = x
        self.__init_y = y
        self.__coords = [x, y]
        self.__dir = Guard.converts[orientation]
        self.__init_dir = self.__dir

    def __hash__(self):
        return hash((self.__dir, self.__coords[0], self.__coords[1]))

    @property
    def coords(self) -> Sequence[int]:
        """
        Gets the guard's coordinates.

        Return
        ------
        Sequence[int]
            its x and y position.
        """
        return self.__coords

    def reset(self) -> None:
        """
        Resets guard to its original position and direction.
        """
        self.__coords = [self.__init_x, self.__init_y]
        self.__dir = self.__init_dir

    def rotate(self) -> None:
        """
        The guard turn clockwise 90 degrees.
        """
        self.__dir = Guard.rotations[self.__dir]

    def forward(self) -> None:
        """
        The guard moves in the direction given to him.
        """
        self.__coords[0] += Guard.movements[self.__dir][0]
        self.__coords[1] += Guard.movements[self.__dir][1]

    def backward(self) -> None:
        """
        The guard moves in the opposite direction given to him.
        """
        self.__coords[0] -= Guard.movements[self.__dir][0]
        self.__coords[1] -= Guard.movements[self.__dir][1]
