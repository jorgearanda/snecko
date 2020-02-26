class Game:
    def __init__(self, game_data):
        self.turn = game_data["turn"]
        self.you = Snake(game_data["you"])
        self.board = Board(game_data["board"], game_data["you"]["id"])
        self.game = game_data["game"]


class Board:
    def __init__(self, board_data, you_id):
        self.snakes = [Snake(s, you_id) for s in board_data["snakes"]]
        self.food = [Food(f["x"], f["y"]) for f in board_data["food"]]
        self.width = board_data["width"]
        self.height = board_data["height"]
        self.board = self._make_board()

    def print_board(self):
        print("X" * (self.width + 2))
        for row in self.board:
            print("X" + "".join([str(cell) for cell in row]) + "X")
        print("X" * (self.width + 2))

    def _make_board(self):
        board = [
            [EmptyCell(i, j) for i in range(self.width)] for j in range(self.height)
        ]
        for snake in self.snakes:
            for part in snake.body:
                board[part.y][part.x] = part
        for food in self.food:
            board[food.y][food.x] = food

        return board


class Snake:
    def __init__(self, snake_data, you_id):
        self.you = you_id == snake_data["id"]
        self.id = snake_data["id"]
        self.name = snake_data["name"]
        self.body = [
            SnakePart(part["x"], part["y"], idx)
            for idx, part in enumerate(snake_data["body"])
        ]
        self.health = snake_data["health"]


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.free = True


class SnakePart(Cell):
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
        self.free = False

    @property
    def head(self):
        return self.idx == 0

    def __str__(self):
        return "S" if self.head else "s"


class Food(Cell):
    def __str__(self):
        return "o"


class EmptyCell(Cell):
    def __str__(self):
        return " "


class Wall(Cell):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.free = False

    def __str__(self):
        return "X"
