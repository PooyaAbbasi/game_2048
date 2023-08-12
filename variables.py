from enum import Enum

class Direction(Enum):
    LEFT = 'l'
    RIGHT = 'r'
    UP = 'u'
    DOWN = 'd'

    @staticmethod
    def get_direction_of(user_command: str) -> "Direction":
        user_command = user_command.strip()
        match user_command:
            case 'l' | 'L':
                return Direction.LEFT
            case 'r' | 'R':
                return Direction.RIGHT
            case 'd' | 'D':
                return Direction.DOWN
            case 'u' | 'U':
                return Direction.UP

            case _:
                raise InvalidDirection(f'excepted {valid_directions} , got {user_command}')

class InvalidDirection(Exception):
    pass


game_board: list[list[int]] = []

construction_message = (
    """ directions :
 r or R : move Right 
 l or L : move Left  
 u ro U : move up  
 d or D : move down  """)

board_size: int = 4

valid_directions = ('r', 'R',  # Right
                    'l', 'L',  # Left
                    'd', 'D',  # Down
                    'u', 'U')  # Up
