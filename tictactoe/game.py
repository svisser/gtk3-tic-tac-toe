import enum


DEFAULT_WIDTH = 3
DEFAULT_HEIGHT = 3


class Cell(enum.Enum):
    EMPTY = " "
    X = "X"
    O = "O"


class Player(enum.Enum):
    X = "X"
    O = "O"

    def get_cell(self):
        return {
            Player.X: Cell.X,
            Player.O: Cell.O,
        }[self]

    def get_opposite_player(self):
        return {
            Player.X: Player.O,
            Player.O: Player.X,
        }[self]

    def __str__(self):
        return str(self.value)


class GameStatus(enum.Enum):
    ACTIVE = 0
    GAME_OVER = 1


class GameState(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_player = Player.X
        self.status = GameStatus.ACTIVE
        self.winning_player = None
        self.winning_cells = None
        self.symbols_placed = 0
        self.grid = [[Cell.EMPTY for _ in range(width)] for _ in range(height)]

    @classmethod
    def get_initial_state(cls):
        return cls(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def place_symbol(self, gx, gy):
        self.symbols_placed += 1
        self.grid[gy][gx] = self.current_player.get_cell()

        winner, cells = self.calculate_winner()
        if winner is not None:
            self.status = GameStatus.GAME_OVER
            self.winning_player = winner
            self.winning_cells = cells
            return

        if self.symbols_placed == self.width * self.height:
            self.status = GameStatus.GAME_OVER
            return

        self.current_player = self.current_player.get_opposite_player()

    def calculate_possibilities(self):
        for x in range(self.width):
            yield frozenset((x, y) for y in range(self.height))
        for y in range(self.height):
            yield frozenset((x, y) for x in range(self.width))
        yield frozenset((k, k) for k in range(self.width))
        yield frozenset((k, self.width - 1 - k) for k in range(self.width))

    def calculate_winner(self):
        for player in Player:
            symbol = player.get_cell()
            for cells in self.calculate_possibilities():
                if all(self.grid[cy][cx] == symbol for cx, cy in cells):
                    return player, cells
        return None, None
