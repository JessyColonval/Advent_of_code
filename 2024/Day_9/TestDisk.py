from unittest import TestCase
from Disk import Disk


class TestDisk(TestCase):
    """
    Unit test class for Disk object.
    """

    def test_build_from_string_with_letter(self):
        """
        Checks if the Disk's build from a string raise an exception when a
        letter is present in the given disk map.
        """
        disk_map = "2333133121414131402a"
        self.assertRaises(ValueError, Disk.build_from_string, disk_map)

    def test_build_from_string_with_negative_number(self):
        """
        Checks if the Disk's build from a string raise an exception when a
        negative number (-) is present in the given disk map.
        """
        disk_map = "233313312141-4131402"
        self.assertRaises(ValueError, Disk.build_from_string, disk_map)

    def test_build_from_string_empty_map(self):
        """
        Checks if the Disk's build from a string raise an exception when a
        empty disk map is given.
        """
        self.assertRaises(ValueError, Disk.build_from_string, "")

    def test_build_from_string(self):
        """
        Checks if the Disk's build work correctly.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        self.assertEqual("00...111...2...333.44.5555.6666.777.888899",
                         str(disk))

    def test_get_size(self):
        """
        Checks if the size of the disk is correct.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        self.assertEqual(42, disk.size)

    def test_score_before_fragmentation(self):
        """
        Checks if the computed score of an unfragmented disk is working
        properly and if it is correct.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        self.assertEqual(4116, disk.score())

    def test_score_after_fragmentation(self):
        """
        Checks if the computed score of a fragmented disk is working properly
        and if it is correct.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        disk.fragmentation()
        self.assertEqual(2858, disk.score())

    def test_find_free_space(self):
        """
        Checks if free space search is working properly.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        self.assertEqual(2, disk._Disk__find_free_space(9, 0, 40))
        self.assertEqual(8, disk._Disk__find_free_space(9, 7, 40))
        self.assertEqual(12, disk._Disk__find_free_space(9, 11, 40))
        self.assertEqual(-1, disk._Disk__find_free_space(9, 15, 40))

    def test_move_unknow_file(self):
        """
        Checks if moving a file that doesn't exist produces an exception.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        self.assertRaises(ValueError, disk._Disk__move, 10, 2)
        self.assertRaises(ValueError, disk._Disk__move, -1, 2)

    def test_move_unknow_free_space(self):
        """
        Checks if moving a file into a space that is not free or does not exist
        produces an exception.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        self.assertRaises(ValueError, disk._Disk__move, 9, 5)
        self.assertRaises(ValueError, disk._Disk__move, 9, -1)
        self.assertRaises(ValueError, disk._Disk__move, 9, 43)
        self.assertRaises(ValueError, disk._Disk__move, 9, 0)
        self.assertRaises(ValueError, disk._Disk__move, 9, 39)

    def test_move_exact_size(self):
        """
        Checks if moving a file to a free space exactly the size of the file
        works correctly.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        disk._Disk__move(7, 2)
        self.assertEqual("00777111...2...333.44.5555.6666.....888899",
                         str(disk))
        disk._Disk__move(7, 8)
        self.assertEqual("00...1117772...333.44.5555.6666.....888899",
                         str(disk))
        disk._Disk__move(7, 12)
        self.assertEqual("00...111...2777333.44.5555.6666.....888899",
                         str(disk))
        disk._Disk__move(7, 31)
        self.assertEqual("00...111...2...333.44.5555.6666777..888899",
                         str(disk))

    def test_move_greater_size(self):
        """
        Checks if moving a file into a free space that is larger than the file
        size works correctly.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        disk._Disk__move(9, 2)
        self.assertEqual("0099.111...2...333.44.5555.6666.777.8888..",
                         str(disk))
        disk._Disk__move(9, 8)
        self.assertEqual("00...11199.2...333.44.5555.6666.777.8888..",
                         str(disk))
        disk._Disk__move(9, 12)
        self.assertEqual("00...111...299.333.44.5555.6666.777.8888..",
                         str(disk))
        disk._Disk__move(9, 40)
        self.assertEqual("00...111...2...333.44.5555.6666.777.888899",
                         str(disk))

    def test_move_middle_of_free_space(self):
        """
        Checks if moving a file into the middle of a free space works
        correctly.
        """
        disk_map = "2333133121414131402"
        disk = Disk.build_from_string(disk_map)
        disk._Disk__move(9, 13)
        self.assertEqual("00...111...2.99333.44.5555.6666.777.8888..",
                         str(disk))
