import random
from collections import defaultdict, namedtuple

Point = namedtuple("Point", ["x", "y"])

class Bot:
    def __init__(self, width, height):
        self.memory = defaultdict(list)
        self.matched = set()
        self.width = width
        self.height = height
        self.last_flipped = None

    def observe(self, point, value):
        if point not in self.memory[value]:
            self.memory[value].append(point)

    def mark_as_matched(self, p1, p2):
        self.matched.update([p1, p2])

    def play(self):
        for value, points in self.memory.items():
            unpaired = [p for p in points if p not in self.matched]
            if len(unpaired) >= 2:
                if self.last_flipped is None:
                    self.last_flipped = unpaired[0]
                    return self.last_flipped
                else:
                    p = unpaired[1]
                    self.last_flipped = None
                    return p

        if self.last_flipped:
            for value, points in self.memory.items():
                if self.last_flipped in points:
                    for p in points:
                        if p != self.last_flipped and p not in self.matched:
                            self.last_flipped = None
                            return p

        while True:
            p = Point(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if p not in self.matched:
                if self.last_flipped is None:
                    self.last_flipped = p
                return p

def generate_board(size):
    total = size * size
    if total % 2 != 0:
        total -= 1  
    num_pairs = total // 2
    symbols = [chr(65 + i) for i in range(num_pairs)] * 2
    random.shuffle(symbols)

    board = []
    idx = 0
    for _ in range(size):
        row = []
        for _ in range(size):
            if idx < len(symbols):
                row.append(symbols[idx])
                idx += 1
            else:
                row.append(" ")  
        board.append(row)
    return board

def display_board(board, revealed):
    print("\n  " + " ".join(str(i) for i in range(len(board))))
    for y, row in enumerate(board):
        line = f"{y} " + " ".join(cell if revealed[y][x] or cell == " " else "■" for x, cell in enumerate(row))
        print(line)

def get_player_move(revealed, board):
    size = len(board)
    while True:
        try:
            x, y = map(int, input("Zadej souřadnice (x y): ").split())
            if 0 <= x < size and 0 <= y < size and not revealed[y][x] and board[y][x] != " ":
                return Point(x, y)
            else:
                print("Neplatné souřadnice nebo karta už byla otočena.")
        except:
            print("Zadej dvě čísla oddělená mezerou.")

def main():
    size = 5
    board = generate_board(size)
    revealed = [[False] * size for _ in range(size)]
    matched = set()
    bot = Bot(size, size)
    player_score = bot_score = 0
    winning_score = 3

    print(" Vítej ve hře PEXESO (5x5) proti AI botovi! Vyhrává ten, kdo získá 3 páry.")
    display_board(board, revealed)

    turn = "player"
    while player_score < winning_score and bot_score < winning_score:
        print(f"\n Na tahu je: {'Ty' if turn == 'player' else 'BOT'}")

        if turn == "player":
            p1 = get_player_move(revealed, board)
            revealed[p1.y][p1.x] = True
            v1 = board[p1.y][p1.x]
            display_board(board, revealed)

            p2 = get_player_move(revealed, board)
            revealed[p2.y][p2.x] = True
            v2 = board[p2.y][p2.x]
            display_board(board, revealed)

            if v1 == v2 and p1 != p2:
                print(" Správně! Máš pár!")
                matched.update([p1, p2])
                player_score += 1
            else:
                print(" Špatně. Zkusíš to příště.")
                revealed[p1.y][p1.x] = False
                revealed[p2.y][p2.x] = False
                turn = "bot"

        else:
            p1 = bot.play()
            v1 = board[p1.y][p1.x]
            bot.observe(p1, v1)

            p2 = bot.play()
            v2 = board[p2.y][p2.x]
            bot.observe(p2, v2)

            print(f" Bot otočil {p1} → {v1} a {p2} → {v2}")

            if v1 == v2 and p1 != p2:
                print(" Bot našel pár!")
                matched.update([p1, p2])
                bot.mark_as_matched(p1, p2)
                revealed[p1.y][p1.x] = True
                revealed[p2.y][p2.x] = True
                bot_score += 1
            else:
                print(" Bot nenašel pár.")
                turn = "player"

        print(f"\n Skóre – Ty: {player_score}, Bot: {bot_score}")

    print("\n Konec hry!")
    if player_score > bot_score:
        print(" Vyhrál jsi!")
    elif bot_score > player_score:
        print(" Vyhrál bot!")
    else:
        print(" Remíza!")

if __name__ == "__main__":
    main()
