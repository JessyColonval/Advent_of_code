from collections.abc import Sequence


def csv_to_list(file_name: str,
                sep: str = ',',
                by: str = "row") -> Sequence[Sequence[int]]:
    """
    Reads the contents of a csv file and returns it as an integer matrix.

    Parameters
    ----------
    file_name: str
        The file path.
    sep: str, default: 's'
        The character separating each value in the file.
    by: str, default: "row"
        The way the list will be built.
        When "row", then each list contains the values of each line.
        And when "column", then each list contains the values of each columns.

    Returns
    -------
    Sequence[Sequence[int]]
        An integer matrix containing the contents of each row in the file.
    """
    with open(file_name, "r", encoding="utf-8") as input_file:
        if by == "row":
            if sep is None:
                return [
                    [int(num) for num in row.strip()]
                    for row in input_file.readlines()
                ]
            else:
                return [
                    [int(num) for num in row.split(sep)]
                    for row in input_file.readlines()
                ]

        elif by == "column":
            lines = input_file.readlines()
            result = [[int(val)] for val in lines[0].split(sep)]
            for i in range(1, len(lines)):
                values = lines[i].split(sep)
                for j in range(0, len(values)):
                    result[j].append(int(values[j]))
            return result

    return None
