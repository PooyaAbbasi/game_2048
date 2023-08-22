""" running script 2048 game """
from logic import *
from variables import *


def check_win(board: list[list[int]]) -> bool:
    for row in board:
        if 2048 in row:
            return True
    else:
        return False


def is_game_over(board: list[list[int]]) -> bool:
    if check_vertically(board):
        return False
    elif check_horizontally(board):
        return False
    else:
        return True


def check_vertically(board) -> bool:
    for i in range(board_size):
        for j in range(board_size):
            if can_add_right_cell(board, i, j):
                return True
    else:
        return False


def check_horizontally(board) -> bool:
    return check_vertically(get_rotated_to_left(board))


has_moved: bool


if __name__ == "__main__":
    # running
    init_board(game_board, board_size)
    produce_random_new_2_in_opposite_of_direction(game_board, direction=None)
    print(f" \n {construction_message} \n")

    while True:

        print_board(game_board)
        command = input(" enter command: ")

        direction: Direction
        try:
            direction = Direction.get_direction_of(command)
        except InvalidDirection as direction_error:
            print(f" {direction_error}")
            continue

        has_moved = perform_command(direction, game_board)

        if check_win(game_board) is True:
            print(" :::::: YOU WIN ::::::::: ")

        if has_moved:
            try:
                produce_random_new_2_in_opposite_of_direction(game_board, direction)
            except NoEmptyCell:
                if is_game_over(game_board):
                    print(" ##### Game Over ##### ")
                    break
                else:
                    print("--- try another direction ---")
        else:
            if is_game_over(game_board):
                print(" ##### Game Over ##### ")
                break

        has_moved = False  # reinitialize has_moved
