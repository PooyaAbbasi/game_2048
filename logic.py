""" game logic function """

from random import choice
from variables import *

board_size_ = board_size
last_index = board_size_ - 1
first_index = 0


def init_board(board: list[list[int]], size: int = board_size_):
    """ init the board to size * size matrix with all 0 elements """
    for _ in range(size):
        row: list[int] = []
        for __ in range(size):
            row.append(0)
        board.append(row)


def print_board(board):
    print("*" * 20)
    for row in board:
        for cell in row:
            print(f"{str(cell): ^6}|", end="")
        print("")
    print("*" * 20)


def produce_random_new_2_in_opposite_of_direction(board: list[list[int]],
                                                  direction: Direction = None
                                                  ) -> None:
    """ produce new 2 randomly in an empty cells which placed in opposite of direction
     :raise NoEmptyCell exception if there is no zero cell in opposite side of direction """

    if direction is None:
        produce_first_2(board)
    else:
        opposite_side = get_opposite_direction(direction)
        all_empty_cells_from_side = get_all_empty_cells_from(opposite_side, board)
        if all_empty_cells_from_side:
            row_index, column_index = choice(all_empty_cells_from_side)
            board[row_index][column_index] = 2
        else:
            raise NoEmptyCell("there is no more empty cell !")


def produce_first_2(board: list[list[int]], size=board_size_):
    """ produces first 2 in beginning of the game from Left direction """
    random_cell_of_left = choice(list(range(size)))
    board[random_cell_of_left][0] = 2


def get_opposite_direction(direction: Direction):
    match direction:

        case direction.RIGHT:
            return direction.LEFT

        case direction.LEFT:
            return direction.RIGHT

        case direction.DOWN:
            return direction.UP

        case direction.UP:
            return direction.DOWN
        case _:
            raise ValueError("invalid direction")


def get_all_empty_cells_from(direction: Direction, board: list[list[int]]) -> list:
    """ get empty cells from side of direction like [(1, 3), (2, 3)]"""
    match direction:
        case Direction.UP | Direction.DOWN:
            return get_up_or_down_empty_cells(board, direction)
        case Direction.LEFT | Direction.RIGHT:
            return get_right_or_left_empty_cells(board, direction)
    pass


def get_up_or_down_empty_cells(board: list[list[int]],
                               direction: Direction) -> list[tuple[int, int]]:
    """
    :return:
        empty cells in list of tuples of positions.
    :raise:
        InvalidDirection if direction is not UP or DOWN
    """

    if direction == Direction.DOWN:
        row_index = last_index
    elif direction == Direction.UP:
        row_index = first_index
    else:
        raise InvalidDirection(f" expected UP or DOWN got {direction}")

    empty_cells = []
    for column_index in range(board_size_):
        if board[row_index][column_index] == 0:
            empty_cells.append((row_index, column_index))
    return empty_cells


def get_right_or_left_empty_cells(board: list[list[int]],
                                  direction: Direction) -> list[tuple[int, int]]:
    """
    :return:
        vertically empty cells in list of tuples of positions.
    :raise:
        InvalidDirection if direction is not LEFT or RIGHT
    """
    if direction == Direction.LEFT:
        column_index = first_index
    elif direction == Direction.RIGHT:
        column_index = last_index
    else:
        raise InvalidDirection(f" LEFT or RIGHT excepted got {direction} ")

    empty_cells = []
    for row_index in range(board_size_):
        if board[row_index][column_index] == 0:
            empty_cells.append((row_index, column_index))
    return empty_cells


has_moved: bool
# has_moved to specify any cell in the board has moved or not


def perform_command(direction: Direction, board: list[list[int]]) -> bool:
    global has_moved
    has_moved = False  # reinitialize has moved
    match direction:
        case Direction.UP:
            perform_up_command(board)
            pass
        case Direction.DOWN:
            perform_down_command(board)
            pass
        case Direction.LEFT:
            perform_left_command(board)
            pass
        case Direction.RIGHT:
            perform_right_command(board)
            pass
    return has_moved


def perform_left_command(board: list[list[int]]):
    row_index = first_index

    for row in get_rows_gen(board):
        # for each row first compress to direction command
        # get the first cell from direction side to pars
        # if cell is zero means there is no more nonzero cell
        # because it has been compressed before so go next row

        compress_to_left(board, row_index)
        cell = {"row": row_index, "column": first_index, "value": 0}
        value_of_cell = board[cell["row"]][cell["column"]]
        cell["value"] = value_of_cell

        while cell["column"] < board_size_:
            cell["value"] = board[cell["row"]][cell["column"]]
            if cell["value"] == 0:
                break
            elif cell["value"] > 0:

                if can_add_right_cell(board, cell["row"], cell["column"]):
                    global has_moved
                    has_moved = True
                    add_right_cell_and_leave_it_zero(board, cell["row"], cell["column"])
                    compress_to_left(board, cell["row"])

                cell["column"] += 1

        row_index += 1


def compress_to_left(board: list[list[int]], row_index: int) -> None:
    board[row_index] = get_compressed_to_left(board[row_index])


def get_compressed_to_left(row: list[int]) -> list[int]:
    """ compress all nonzero cells in queue to left
    by removing middle zeroes and append them to right
    :return compressed row
    """

    global has_moved
    column_index = first_index
    while column_index < board_size_:
        if is_there_nonzero_right_of(column_index, row):
            if row[column_index] == 0:
                row.pop(column_index)
                row.append(0)
                has_moved = True
            elif row[column_index] > 0:
                column_index += 1
                pass
        else:
            break
    return row


def is_there_nonzero_right_of(index: int, row: list[int]):
    for i in range(index, board_size_):
        if row[i] > 0:
            return True
    else:
        return False


def can_add_right_cell(board, row, column):
    """ check if the column is not at last index, if it isn't.
        row and column are current cell position
    :return: True if the current cell and next right cell one are same , else False
    """
    if column == last_index:
        return False
    elif board[row][column] == board[row][column + 1]:
        return True
    else:
        return False


def add_right_cell_and_leave_it_zero(board: list[list[int]], row_index: int, column_index: int):
    board[row_index][column_index] *= 2
    board[row_index][column_index + 1] = 0
    pass


def perform_right_command(board: list[list[int]]):
    # works like performing left command
    row_index = first_index

    for row in get_rows_gen(board):

        board[row_index] = get_compressed_to_right(row)
        cell = {"row": row_index, "column": last_index, "value": 0}
        value_of_cell = board[cell["row"]][cell["column"]]
        cell["value"] = value_of_cell

        while cell["column"] >= first_index:
            if cell["value"] == 0:
                break
            elif cell["value"] > 0:
                if can_add_left_cell(board, row=cell["row"],
                                     column=cell["column"]):
                    global has_moved
                    has_moved = True
                    add_left_cell_and_leave_it_zero(board, cell["row"], cell["column"])
                    compress_to_right(board, row_index)

                cell["column"] -= 1
                cell["value"] = board[cell["row"]][cell["column"]]

        row_index += 1


def compress_to_right(board: list[list[int]], row_index: int) -> None:
    board[row_index] = get_compressed_to_right(board[row_index])


def get_compressed_to_right(row: list[int]) -> list[int]:
    """ compress all nonzero cells in queue to right
        by removing middle zeroes and append them to left
        :return compressed row
        """
    global  has_moved
    column_index = last_index
    while column_index >= first_index:
        if is_there_nonzero_left_of(column_index, row):
            if row[column_index] == 0:
                row.pop(column_index)
                row = [0] + row
                has_moved = True
            elif row[column_index] > 0:
                column_index -= 1
                pass

        else:
            break
    return row
    pass


def is_there_nonzero_left_of(index: int, row: list[int]):
    for i in range(index, first_index - 1, -1):
        if row[i] > 0:
            return True
    else:
        return False


def can_add_left_cell(board: list[list[int]], row: int, column: int):
    if column == first_index:
        return False
    elif board[row][column] == board[row][column - 1]:
        return True
    else:
        return False


def add_left_cell_and_leave_it_zero(board: list[list[int]], row: int, column: int):
    board[row][column] *= 2
    board[row][column - 1] = 0
    pass


def perform_up_command(board: list[list[int]]):
    # it is enough to rotate board to left
    # then perform left command on it

    rotated_to_left = get_rotated_to_left(board)
    perform_left_command(rotated_to_left)
    performed_board = get_rotated_back_to_right(rotated_to_left)
    replace_to_main_board(performed_board, board)
    pass


def perform_down_command(board: list[list[int]]):
    # it is enough to rotate board to left
    # then perform right command on it

    rotated_to_left = get_rotated_to_left(board)
    perform_right_command(rotated_to_left)
    performed_board = get_rotated_back_to_right(rotated_to_left)
    replace_to_main_board(performed_board, board)


def get_rotated_to_left(board: list[list[int]]) -> list[list[int]]:
    """ the result board should have the columns of the current board from last to first (reversely)
    """
    board_to_rotate_left = []
    for column_line in get_columns_gen(board):
        board_to_rotate_left = [column_line] + board_to_rotate_left

    return board_to_rotate_left


def get_rotated_back_to_right(rotated_board: list[list[int]]) -> list[list[int]]:
    """ to rotate back we have to pick up columns from first to last and reverse them
    then add them to result board
    """
    board_to_rotate_right = []
    for column_line in get_columns_gen(rotated_board):
        column_line.reverse()
        board_to_rotate_right.append(column_line)

    return board_to_rotate_right


def replace_to_main_board(performed_board, main_board):
    for i in range(board_size_):
        main_board[i] = performed_board[i]


def get_rows_gen(board: list[list[int]]):
    yield from board


def get_columns_gen(board: list[list[int]]):
    for row_index in range(board_size_):
        vertical_line = []
        for column_index in range(board_size_):
            vertical_line.append(board[column_index][row_index])

        yield vertical_line


class NoMoreNonzeroCell(Exception):
    pass


class NoEmptyCell(Exception):
    pass

