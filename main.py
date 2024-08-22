import random
import string

class Scrabble:
    def __init__(self):
        self.board = self.create_board()
        self.tiles = self.create_tiles()
        self.player_tiles = {"Player 1": [], "Player 2": []}
        self.word_list = self.load_word_list()
        self.scores = {"Player 1": 0, "Player 2": 0}
        self.current_player = "Player 1"
        self.multiplier_board = self.create_multiplier_board()
        self.turns_without_progress = 0
        self.passes = {"Player 1": 0, "Player 2": 0}
        self.dictionary_mode = False
        self.game_history = []
        self.undo_stack = []
        self.redo_stack = []

    def create_board(self):
        board = [['' for _ in range(15)] for _ in range(15)]
        return board

    def create_multiplier_board(self):
        multiplier_board = [
            ["TW", "", "", "DL", "", "", "", "TW", "", "", "", "DL", "", "", "TW"],
            ["", "DW", "", "", "", "TL", "", "", "", "TL", "", "", "", "DW", ""],
            ["", "", "DW", "", "", "", "DL", "", "DL", "", "", "", "DW", "", ""],
            ["DL", "", "", "DW", "", "", "", "DL", "", "", "", "DW", "", "", "DL"],
            ["", "", "", "", "DW", "", "", "", "", "", "DW", "", "", "", ""],
            ["", "TL", "", "", "", "TL", "", "", "", "TL", "", "", "", "TL", ""],
            ["", "", "DL", "", "", "", "DL", "", "DL", "", "", "", "DL", "", ""],
            ["TW", "", "", "DL", "", "", "", "DW", "", "", "", "DL", "", "", "TW"],
            ["", "", "DL", "", "", "", "DL", "", "DL", "", "", "", "DL", "", ""],
            ["", "TL", "", "", "", "TL", "", "", "", "TL", "", "", "", "TL", ""],
            ["", "", "", "", "DW", "", "", "", "", "", "DW", "", "", "", ""],
            ["DL", "", "", "DW", "", "", "", "DL", "", "", "", "DW", "", "", "DL"],
            ["", "", "DW", "", "", "", "DL", "", "DL", "", "", "", "DW", "", ""],
            ["", "DW", "", "", "", "TL", "", "", "", "TL", "", "", "", "DW", ""],
            ["TW", "", "", "DL", "", "", "", "TW", "", "", "", "DL", "", "", "TW"]
        ]
        return multiplier_board

    def create_tiles(self):
        letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}
        tiles = []
        for letter, value in letter_values.items():
            tiles.extend([letter] * (8 if letter in 'EAIONRTLSU' else 1))
        tiles.extend([' '] * 2)  # Add blank tiles
        random.shuffle(tiles)
        return tiles

    def load_word_list(self):
        return set([
            "CAT", "DOG", "FISH", "BIRD", "FROG", "HOUSE", "COMPUTER", "PYTHON", "JAZZ", "QUIZ",
            "XYLOPHONE", "ZEBRA", "GIRAFFE", "ELEPHANT", "TIGER", "LION", "MONKEY", "KANGAROO",
            "DOLPHIN", "SHARK", "WHALE", "HIPPOPOTAMUS", "RHINOCEROS", "CROCODILE", "ALLIGATOR",
            "DINGO", "KOALA", "WOMBAT", "CASSOWARY", "EMU", "PLATYPUS", "EAGLE", "HAWK", "CONDOR",
            "CHEETAH", "LEOPARD", "PANTHER", "JAGUAR", "HYENA", "CAPE", "ANTHILL", "NIGHTINGALE"
        ])

    def draw_tiles(self, player):
        while len(self.player_tiles[player]) < 7:
            if self.tiles:
                self.player_tiles[player].append(self.tiles.pop())
            else:
                break

    def display_board(self):
        for row in self.board:
            print(' '.join([cell if cell else '.' for cell in row]))

    def display_tiles(self):
        print(f"{self.current_player}'s tiles:", self.player_tiles[self.current_player])

    def switch_player(self):
        self.current_player = "Player 2" if self.current_player == "Player 1" else "Player 1"

    def place_word(self, word, row, col, direction):
        if not self.is_valid_placement(word, row, col, direction):
            print("Invalid word placement.")
            return False
        self.apply_multipliers(word, row, col, direction)
        self.save_game_state()
        if direction == 'H':
            for i, letter in enumerate(word):
                if self.board[row][col + i] == '' or self.board[row][col + i] == letter:
                    self.board[row][col + i] = letter
                else:
                    print("Tile conflict! Choose another placement.")
                    self.undo_last_move()
                    return False
        elif direction == 'V':
            for i, letter in enumerate(word):
                if self.board[row + i][col] == '' or self.board[row + i][col] == letter:
                    self.board[row + i][col] = letter
                else:
                    print("Tile conflict! Choose another placement.")
                    self.undo_last_move()
                    return False
        self.remove_tiles_from_player(word)
        self.undo_stack.append(self.redo_stack)
        self.redo_stack = []
        return True

    def is_valid_placement(self, word, row, col, direction):
        if direction == 'H':
            if col + len(word) > 15:
                return False
            for i in range(len(word)):
                if self.board[row][col + i] and self.board[row][col + i] != word[i]:
                    return False
        elif direction == 'V':
            if row + len(word) > 15:
                return False
            for i in range(len(word)):
                if self.board[row + i][col] and self.board[row + i][col] != word[i]:
                    return False
        return True

    def apply_multipliers(self, word, row, col, direction):
        word_score = 0
        word_multiplier = 1
        letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}
        for i, letter in enumerate(word):
            letter_score = letter_values.get(letter, 0)
            if direction == 'H':
                multiplier = self.multiplier_board[row][col + i]
            elif direction == 'V':
                multiplier = self.multiplier_board[row + i][col]
            if multiplier == "DL":
                letter_score *= 2
            elif multiplier == "TL":
                letter_score *= 3
            elif multiplier == "DW":
                word_multiplier *= 2
            elif multiplier == "TW":
                word_multiplier *= 3
            word_score += letter_score
        word_score *= word_multiplier
        self.scores[self.current_player] += word_score

    def update_score(self, word):
        return self.scores[self.current_player]

    def check_word(self, word):
        if self.dictionary_mode:
            print("Checking word in extended dictionary...")
            return word in self.word_list
        return word in self.word_list

    def remove_tiles_from_player(self, word):
        for letter in word:
            if letter in self.player_tiles[self.current_player]:
                self.player_tiles[self.current_player].remove(letter)

    def exchange_tiles(self):
        for _ in range(len(self.player_tiles[self.current_player])):
            if self.tiles:
                self.tiles.append(self.player_tiles[self.current_player].pop(0))
                self.player_tiles[self.current_player].append(self.tiles.pop())
        random.shuffle(self.tiles)

    def pass_turn(self):
        self.passes[self.current_player] += 1
        self.switch_player()

    def undo_last_move(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            last_move = self.undo_stack[-1]
            self.board = last_move['board']
            self.player_tiles = last_move['player_tiles']
            self.scores = last_move['scores']
            self.current_player = last_move['current_player']

    def redo_last_move(self):
        if self.redo_stack:
            last_redo = self.redo_stack.pop()
            self.undo_stack.append(last_redo)
            self.board = last_redo['board']
            self.player_tiles = last_redo['player_tiles']
            self.scores = last_redo['scores']
            self.current_player = last_redo['current_player']

    def save_game_state(self):
        state = {
            'board': [row[:] for row in self.board],
            'player_tiles': {k: v[:] for k, v in self.player_tiles.items()},
            'scores': self.scores.copy(),
            'current_player': self.current_player
        }
        self.undo_stack.append(state)

    def end_game(self):
        print("Game over!")
        if self.scores["Player 1"] > self.scores["Player 2"]:
            print("Player 1 wins!")
        elif self.scores["Player 1"] < self.scores["Player 2"]:
            print("Player 2 wins!")
        else:
            print("It's a tie!")
        self.display_scores()

    def display_scores(self):
        print("Final Scores:")
        print("Player 1:", self.scores["Player 1"])
        print("Player 2:", self.scores["Player 2"])

    def play(self):
        while True:
            self.display_board()
            self.display_tiles()
            print(f"{self.current_player}'s turn.")
            word = input("Enter a word (or 'pass', 'exchange', 'quit'): ").upper()
            if word == 'PASS':
                self.pass_turn()
            elif word == 'EXCHANGE':
                self.exchange_tiles()
            elif word == 'QUIT':
                self.end_game()
                break
            elif self.check_word(word):
                direction = input("Enter direction (H for horizontal, V for vertical): ").upper()
                row = int(input("Enter row (0-14): "))
                col = int(input("Enter column (0-14): "))
                if self.place_word(word, row, col, direction):
                    self.scores[self.current_player] = self.update_score(word)
                    self.switch_player()
                else:
                    print("Invalid placement, try again.")
            else:
                print("Invalid word, try again.")
