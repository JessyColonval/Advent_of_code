from typing import Dict, List


class Disk():
    """
    Object modeling part 2 of the problem posed on day 9 of Advent of Code
    2024. It represents a disk and compacts it by moving its files into
    sufficiently large free spaces closer to the beginning of the disk.

    Attributes
    ----------
    __disk: List[int]
        Disk representation with its files (File ID) and its free spaces (-1).
    __files: Dict[int, List[int]]
        Files on the disk. Each file ID is associated with a list of two
        elements: its position on the disk and its size.
    __size: int
        The size of the disk.
    __last_iid: int
        The last file ID present on the disk.
    """

    __disk: List[int]
    __files: Dict[int, List[int]]
    __size: int
    __last_iid: int

    def __init__(self, disk_map: List[int]):
        iid = 0
        self.__size = 0
        self.__disk = []
        self.__files = {}
        for i, n in enumerate(disk_map):
            if i % 2 == 0:
                self.__files[iid] = [self.__size, n]
                for _ in range(0, n):
                    self.__disk.append(iid)
                iid += 1
            else:
                for _ in range(0, n):
                    self.__disk.append(-1)
            self.__size += n
        self.__last_iid = iid - 1

    def __str__(self):
        result = ['.' for _ in range(0, self.__size)]
        for fid, finfos in self.__files.items():
            fpos = finfos[0]
            fsize = finfos[1]
            strfid = str(fid)
            for i in range(fpos, fpos+fsize):
                result[i] = strfid
        return "".join(result)

    @staticmethod
    def build_from_string(disk_map: str):
        """
        Build an object Disk with a disk map represented as a string instead of
        an array of integers.

        Parameters
        ----------
        str
            the disk map.
        """
        if not disk_map.isdigit():
            raise ValueError("Your disk map must contain only numbers!")
        return Disk([int(char) for char in disk_map])

    @property
    def size(self) -> int:
        """
        The size of the disk.

        Return
        ------
        int
            the size.
        """
        return self.__size

    def __move(self, iid: int, fspos: int) -> None:
        """
        Moves a file on the disk.

        Parameters
        ----------
        iid: int
            The file ID.
        fspos: int
            The starting index of the disk where the file will be stored.
        """
        if iid not in self.__files:
            raise ValueError("Unexpected file's id!")
        if fspos < 0 or fspos >= self.__size:
            raise ValueError("Unexpected position of free space in the disk!")
        if self.__disk[fspos] != -1:
            raise ValueError("No free space at this position!")

        # Gets the file and the free space in the disk.
        fpos = self.__files[iid][0]
        fsize = self.__files[iid][1]

        # Updates the file's information with its new position in the disk.
        self.__files[iid][0] = fspos
        for i in range(fspos, fspos+fsize):
            self.__disk[i] = iid

        # Removes the free space taken by the file.
        for i in range(fpos, fpos+fsize):
            self.__disk[i] = -1

    def __find_free_space(self, iid: int, start: int, end: int) -> int:
        """
        Finds the first free space on disk capable of storing the file given.

        Parameters
        ----------
        iid: int
            The file ID.
        start: int
            The starting index of the disk where the search is to begin.
        end: int
            The starting index of the disc where the search is to end.

        Return
        ------
        int
            the starting index of the disk where the file can be stored,
            if none is found, the return value is -1.
        """
        fsize = self.__files[iid][1]
        for i in range(start, end):
            if self.__disk[i] == -1 and all(self.__disk[j] == -1
                                            for j in range(i, i+fsize)):
                return i
        return -1

    def fragmentation(self) -> None:
        """
        Compact the disk by moving files in descending ID order into the first
        sufficiently large free space encountered.
        """
        for iid in range(self.__last_iid, -1, -1):
            fpos = self.__files[iid][0]
            fsid = self.__find_free_space(iid, 0, fpos)
            if fsid != -1:
                self.__move(iid, fsid)

    def score(self) -> int:
        """
        Computes the filesystem checksum of the disk in its current state.

        Return
        ------
        int
            the filesystem checksum.
        """
        result = 0
        for fid, finfos in self.__files.items():
            fpos = finfos[0]
            fsize = finfos[1]
            for i in range(fpos, fpos+fsize):
                result += i * fid
        return result
