import random


class Game:
    def __init__(self, game_data):
        self.turn = game_data["turn"]
        self.you = Snake(game_data["you"], game_data["you"]["id"])
        self.board = Board(game_data["board"], game_data["you"]["id"])
        self.game = game_data["game"]
        print(self.board)

    def naive_move(self):
        first_choices = []
        second_choices = []
        choices = {}
        for choice in {"up", "down", "left", "right"}:
            free = 0
            if self.board.your_head.next[choice].free:
                for further in {"up", "down", "left", "right"}:
                    if self.board.your_head.next[choice].next[further].free:
                        free += 1
                    if self.board.your_head.next[choice].next[further].head:
                        free -= 0.5
                    if self.board.your_head.next[choice].next[further].food:
                        if self.you.health < 50:
                            free += 0.2
                        else:
                            free -= 0.2
            if self.board.your_head.next[choice].food:
                if self.you.health < 50:
                    free += 0.4
                else:
                    free -= 0.4

            choices[choice] = free

        print(choices)
        best_free = 0
        best_choices = []
        for choice in choices:
            if choices[choice] > best_free:
                best_choices = [choice]
                best_free = choices[choice]
            elif choices[choice] == best_free:
                best_choices.append(choice)

        move = random.choice(best_choices)
        print(f"Moving {move} ({best_free} free spaces)")

        return move


class Board:
    def __init__(self, board_data, you_id):
        self.snakes = [Snake(s, you_id) for s in board_data["snakes"]]
        self.food = [Food(f["x"], f["y"]) for f in board_data["food"]]
        self.width = board_data["width"]
        self.height = board_data["height"]
        self._make_board()

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

        self.board = board
        self._link_cells()
        self._mark_your_head()

    def _link_cells(self):
        for j in range(self.height):
            for i in range(self.width):
                if j == 0:
                    self.board[j][i].next["up"] = Wall(i, j - 1)
                else:
                    self.board[j][i].next["up"] = self.board[j - 1][i]
                if j == self.height - 1:
                    self.board[j][i].next["down"] = Wall(i, j + 1)
                else:
                    self.board[j][i].next["down"] = self.board[j + 1][i]
                if i == 0:
                    self.board[j][i].next["left"] = Wall(i - 1, j)
                else:
                    self.board[j][i].next["left"] = self.board[j][i - 1]
                if i == self.width - 1:
                    self.board[j][i].next["right"] = Wall(i + 1, j)
                else:
                    self.board[j][i].next["right"] = self.board[j][i + 1]

    def _mark_your_head(self):
        for snake in self.snakes:
            if snake.you:
                self.your_head = snake.body[0]
                break


class Snake:
    def __init__(self, snake_data, you_id):
        self.you = you_id == snake_data["id"]
        self.id = snake_data["id"]
        self.name = snake_data["name"]
        self.body = [
            SnakePart(part["x"], part["y"], idx, self.you)
            for idx, part in enumerate(snake_data["body"])
        ]
        self.health = snake_data["health"]


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.free = True
        self.food = False
        self.head = False
        self.next = {}


class SnakePart(Cell):
    def __init__(self, x, y, idx, you):
        super().__init__(x, y)
        self.idx = idx
        self.you = you
        self.free = False
        self.head = True

    @property
    def head(self):
        return self.idx == 0

    def __str__(self):
        if self.you:
            return "Y" if self.head else "y"
        else:
            return "S" if self.head else "s"


class Food(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.food = True

    def __str__(self):
        return "o"


class EmptyCell(Cell):
    def __str__(self):
        return " "


class Wall(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.free = False

    def __str__(self):
        return "X"
