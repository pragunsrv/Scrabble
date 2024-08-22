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
        self.power_ups = {"Player 1": [], "Player 2": []}
        self.inventories = {"Player 1": [], "Player 2": []}
        self.challenges = {"Player 1": 3, "Player 2": 3}
        self.challenge_success = {"Player 1": 0, "Player 2": 0}
        self.time_limits = {"Player 1": 60, "Player 2": 60}  # 60 seconds per turn
        self.word_bonuses = {"Player 1": 0, "Player 2": 0}
        self.used_tiles = {"Player 1": [], "Player 2": []}

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

    def remove_tiles_from_player(self, word):
        for letter in word:
            if letter in self.player_tiles[self.current_player]:
                self.player_tiles[self.current_player].remove(letter)
            else:
                print("Tile not in player's possession.")
                return False
        return True

    def check_word(self, word):
        return word in self.word_list

    def exchange_tiles(self):
        tiles_to_exchange = input("Enter the letters to exchange: ").upper()
        if all(tile in self.player_tiles[self.current_player] for tile in tiles_to_exchange):
            self.save_game_state()
            for tile in tiles_to_exchange:
                self.tiles.append(tile)
                self.player_tiles[self.current_player].remove(tile)
            random.shuffle(self.tiles)
            self.draw_tiles(self.current_player)
            self.switch_player()
        else:
            print("You don't have these tiles.")

    def pass_turn(self):
        self.passes[self.current_player] += 1
        if self.passes[self.current_player] >= 2:
            self.end_game()
        else:
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

    def challenge_word(self):
        challenged_word = input(f"{self.current_player} is challenging the last word played. Enter the word: ").upper()
        if challenged_word in self.word_list:
            print("Challenge successful!")
            self.challenge_success[self.current_player] += 1
        else:
            print("Challenge failed.")
            self.challenges[self.current_player] -= 1

    def add_power_up(self, player, power_up):
        self.power_ups[player].append(power_up)

    def use_power_up(self, player, power_up):
        if power_up in self.power_ups[player]:
            if power_up == "DOUBLE_SCORE":
                self.scores[player] *= 2
            elif power_up == "EXTRA_TURN":
                self.current_player = player
            self.power_ups[player].remove(power_up)
        else:
            print(f"{player} does not have this power-up.")

    def check_tile_restrictions(self, word, row, col, direction):
        restricted_tiles = self.used_tiles[self.current_player]
        for letter in word:
            if letter in restricted_tiles:
                print(f"{letter} cannot be used again in this game.")
                return False
        return True

    def enforce_time_limit(self, player):
        import time
        start_time = time.time()
        elapsed_time = 0
        while elapsed_time < self.time_limits[player]:
            elapsed_time = time.time() - start_time
            remaining_time = self.time_limits[player] - elapsed_time
            print(f"Time left: {remaining_time:.2f} seconds")
            time.sleep(1)
        print("Time's up!")

    def trade_inventory_item(self, player, item, trade_with_player):
        if item in self.inventories[player]:
            self.inventories[player].remove(item)
            self.inventories[trade_with_player].append(item)
            print(f"{player} traded {item} with {trade_with_player}.")
        else:
            print(f"{player} does not have this item.")
