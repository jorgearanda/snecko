class Game:
    def __init__(self, game_data):
        self.turn = game_data["turn"]
        self.you = Snake(game_data["you"])
        self.board = Board(game_data["board"])
        self.game = game_data["game"]


class Board:
    def __init__(self, board_data):
        self.snakes = [Snake(s) for s in board_data["snakes"]]
        self.food = [Food(f) for f in board_data["food"]]
        self.width = board_data["width"]
        self.height = board_data["height"]
        self.board = self._make_board()

    def print_board(self):
        print("X" * (self.width + 2))
        for row in self.board:
            print("X" + "".join([str(cell) for cell in row]) + "X")
        print("X" * (self.width + 2))

    def _make_board(self):
        board = [[Empty(i, j) for i in range(self.width)] for j in range(self.height)]
        for snake in self.snakes:
            for part in snake.body:
                board[part.y][part.x] = part
        for food in self.food:
            board[food.y][food.x] = food

        return board


class Snake:
    def __init__(self, snake_data):
        self.id = snake_data["id"]
        self.name = snake_data["name"]
        self.body = [
            SnakePart(idx, part) for idx, part in enumerate(snake_data["body"])
        ]
        self.health = snake_data["health"]


class SnakePart:
    def __init__(self, idx, snake_part_data):
        self.idx = idx
        self.x = snake_part_data["x"]
        self.y = snake_part_data["y"]

    def __str__(self):
        return "S" if self.idx == 0 else "s"


class Food:
    def __init__(self, food_data):
        self.x = food_data["x"]
        self.y = food_data["y"]

    def __str__(self):
        return "o"


class Empty:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return " "
