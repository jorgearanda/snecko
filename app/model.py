class Game:
    def __init__(self, game_data):
        self.turn = game_data["turn"]
        self.you = Snake(game_data["you"])
        self.board = game_data["board"]
        self.game = game_data["game"]


class Board:
    def __init__(self, board_data):
        self.snakes = [Snake(s) for s in board_data["snakes"]]
        self.food = [Food(f) for f in board_data["food"]]
        self.width = board_data["width"]
        self.height = board_data["height"]


class Snake:
    def __init__(self, snake_data):
        self.name = snake_data["name"]
        self.body = snake_data["body"]
        self.id = snake_data["id"]
        self.health = snake_data["health"]


class Food:
    def __init(self, food_data):
        self.x = food_data["x"]
        self.y = food_data["y"]
