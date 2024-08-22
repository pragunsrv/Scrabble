import random
import string
import time

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
        self.time_limits = {"Player 1": 60, "Player 2": 60}
        self.word_bonuses = {"Player 1": 0, "Player 2": 0}
        self.used_tiles = {"Player 1": [], "Player 2": []}
        self.game_mode = "Classic"
        self.round_timer = {"Player 1": None, "Player 2": None}
        self.word_restrictions = []
        self.difficulty = "Normal"
        self.rounds_played = 0
        self.max_rounds = 10
        self.leaderboard = []
        self.tournament_mode = False
        self.tournament_scores = {"Player 1": 0, "Player 2": 0}
        self.recent_words = []
        self.bonus_points = 50
        self.swap_limit = 3
        self.swap_count = {"Player 1": 0, "Player 2": 0}
        self.streak = {"Player 1": 0, "Player 2": 0}
        self.bonus_streak_threshold = 3
        self.auto_save = False
        self.save_file = "scrabble_save.txt"
        self.timed_mode = False
        self.remaining_time = {"Player 1": 300, "Player 2": 300}
        self.special_tiles = ["*"]
        self.special_tile_positions = []

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
        tiles.extend([' '] * 2)
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
        if direction == 'H':
            for i, letter in enumerate(word):
                letter_score = letter_values.get(letter, 0)
                if self.multiplier_board[row][col + i] == 'DL':
                    word_score += letter_score * 2
                elif self.multiplier_board[row][col + i] == 'TL':
                    word_score += letter_score * 3
                else:
                    word_score += letter_score
                if self.multiplier_board[row][col + i] == 'DW':
                    word_multiplier *= 2
                elif self.multiplier_board[row][col + i] == 'TW':
                    word_multiplier *= 3
        elif direction == 'V':
            for i, letter in enumerate(word):
                letter_score = letter_values.get(letter, 0)
                if self.multiplier_board[row + i][col] == 'DL':
                    word_score += letter_score * 2
                elif self.multiplier_board[row + i][col] == 'TL':
                    word_score += letter_score * 3
                else:
                    word_score += letter_score
                if self.multiplier_board[row + i][col] == 'DW':
                    word_multiplier *= 2
                elif self.multiplier_board[row + i][col] == 'TW':
                    word_multiplier *= 3
        self.scores[self.current_player] += word_score * word_multiplier

    def remove_tiles_from_player(self, word):
        for letter in word:
            if letter in self.player_tiles[self.current_player]:
                self.player_tiles[self.current_player].remove(letter)
            else:
                print(f"Tile {letter} not found in player tiles.")
                self.undo_last_move()
                return False
        self.draw_tiles(self.current_player)
        return True

    def save_game_state(self):
        self.game_history.append((
            [row.copy() for row in self.board],
            self.player_tiles.copy(),
            self.scores.copy(),
            self.current_player,
            self.tiles.copy()
        ))
        if len(self.game_history) > 10:
            self.game_history.pop(0)

    def undo_last_move(self):
        if self.game_history:
            state = self.game_history.pop()
            self.board, self.player_tiles, self.scores, self.current_player, self.tiles = state
            self.switch_player()
        else:
            print("No moves to undo.")

    def redo_last_move(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.board, self.player_tiles, self.scores, self.current_player, self.tiles = state
            self.switch_player()
        else:
            print("No moves to redo.")

    def use_power_up(self, power_up):
        if power_up in self.power_ups[self.current_player]:
            self.power_ups[self.current_player].remove(power_up)
            print(f"{power_up} used.")
        else:
            print("Power-up not available.")

    def challenge_word(self, word):
        if word in self.word_list:
            print("Challenge unsuccessful.")
            self.challenges[self.current_player] -= 1
        else:
            print("Challenge successful.")
            self.scores[self.current_player] += 20
            self.challenge_success[self.current_player] += 1

    def apply_difficulty(self):
        if self.difficulty == "Hard":
            # Apply harder rules
            pass
        elif self.difficulty == "Easy":
            # Apply easier rules
            pass

    def start_game(self):
        print("Starting game...")
        while not self.is_game_over():
            self.display_board()
            self.display_tiles()
            word = input(f"{self.current_player}, enter your word: ").upper()
            row = int(input("Enter the row: "))
            col = int(input("Enter the column: "))
            direction = input("Enter direction (H/V): ").upper()
            if self.place_word(word, row, col, direction):
                print(f"{self.current_player} placed {word} at ({row}, {col})")
            self.switch_player()
            self.turns_without_progress += 1
            self.check_passes()
            self.apply_difficulty()

    def check_passes(self):
        if all(pass_count >= 3 for pass_count in self.passes.values()):
            print("Game over due to multiple passes.")
            self.end_game()

    def is_game_over(self):
        if not any(self.tiles):
            if all(len(tiles) == 0 for tiles in self.player_tiles.values()):
                return True
        return False

    def end_game(self):
        print("Game over!")
        winner = max(self.scores, key=self.scores.get)
        print(f"The winner is {winner} with a score of {self.scores[winner]}")

    def auto_save_game(self):
        if self.auto_save:
            with open(self.save_file, "w") as file:
                file.write(str(self.game_history))

    def load_game(self):
        try:
            with open(self.save_file, "r") as file:
                self.game_history = eval(file.read())
                self.board, self.player_tiles, self.scores, self.current_player, self.tiles = self.game_history[-1]
        except FileNotFoundError:
            print("No save file found.")

    def handle_tournament(self):
        if self.tournament_mode:
            # Tournament logic
            pass

    def adjust_time_limits(self):
        if self.timed_mode:
            current_time = time.time()
            for player, limit in self.time_limits.items():
                self.remaining_time[player] -= (current_time - self.round_timer[player])
                self.round_timer[player] = current_time
                if self.remaining_time[player] <= 0:
                    print(f"{player} ran out of time!")
                    self.end_game()

    def play_turn(self):
        self.start_game()
        self.handle_tournament()
        self.auto_save_game()
        self.adjust_time_limits()

    def apply_special_tiles(self, word, row, col, direction):
        # Apply special tiles logic
        pass

    def add_word_restrictions(self):
        # Add logic for word restrictions
        pass

    def manage_swap(self):
        if self.swap_count[self.current_player] < self.swap_limit:
            # Swap logic
            pass
        else:
            print("Swap limit reached.")

    def manage_streaks(self):
        if self.streak[self.current_player] >= self.bonus_streak_threshold:
            self.scores[self.current_player] += self.bonus_points
            self.streak[self.current_player] = 0

    def update_leaderboard(self):
        self.leaderboard.append((self.current_player, self.scores[self.current_player]))
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x[1], reverse=True)

    def check_end_of_tournament(self):
        if self.tournament_mode:
            if self.rounds_played >= self.max_rounds:
                self.end_game()
                print("Tournament ended.")

    def run(self):
        self.load_game()
        self.play_turn()
        self.update_leaderboard()
        self.check_end_of_tournament()

if __name__ == "__main__":
    game = Scrabble()
    game.run()
