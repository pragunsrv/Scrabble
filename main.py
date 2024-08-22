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
        self.special_tile_effects = {"*": "Double letter score"}
        self.tile_replacement = {"Player 1": [], "Player 2": []}
        self.tile_bank = {}
        self.clues = {"Player 1": [], "Player 2": []}
        self.clue_timer = {"Player 1": 10, "Player 2": 10}
        self.restricted_words = set()
        self.dynamic_multiplier_board = self.create_dynamic_multiplier_board()
        self.custom_tournaments = []
        self.custom_difficulties = {"Normal": 1, "Hard": 2, "Extreme": 3}
        self.current_difficulty = 1
        self.challenge_count = {"Player 1": 0, "Player 2": 0}
        self.game_rules = {"Standard": True, "Extended": False}
        self.game_modes = ["Classic", "Speed", "Tactical"]
        self.power_up_effects = {"Swap": "Allows swapping up to 3 tiles", "Hint": "Gives a hint for the next word"}
        self.custom_word_list = []
        self.tournament_history = []
        self.ai_opponents = []
        self.ai_difficulty = {"Easy": 1, "Medium": 2, "Hard": 3}
        self.current_ai_difficulty = 1
        self.hints_used = {"Player 1": 0, "Player 2": 0}
        self.swap_history = {"Player 1": [], "Player 2": []}
        self.bonus_streak_count = {"Player 1": 0, "Player 2": 0}
        self.undo_limit = 3
        self.undo_history = {"Player 1": [], "Player 2": []}
        self.special_tile_placements = []
        self.custom_rules = {"Double Score on Q": True, "No Proper Nouns": False}
        self.history_log = []
        self.special_tile_usage = {"*": 0}

    def create_board(self):
        return [['' for _ in range(15)] for _ in range(15)]

    def create_multiplier_board(self):
        return [
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

    def create_dynamic_multiplier_board(self):
        return [
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
            "CAT", "DOG", "FISH", "BIRD", "BEAR", "PANTHER", "LION", "TIGER", "ELEPHANT", "GIRAFFE", "ZEBRA", "HIPPO", "KANGAROO", "KOALA", "WOLF",
            "PYTHON", "JAVA", "SCRABBLE", "DEVELOPER", "GITHUB", "PROGRAMMING", "EXAMPLE", "COMPUTERIZED", "PYTHONIC", "REPOSITORY", "OCEAN", "MOUNTAIN", 
            "FOREST", "DESERT", "ISLAND", "JUNGLE", "PLAIN", "RIVER", "LAKE", "POND", "VALLEY", "CAVE", "FOSSIL", "DINO", "ASTEROID", "GALAXY", "UNIVERSE"
        ])

    def display_board(self):
        for row in self.board:
            print(' '.join([cell if cell else '.' for cell in row]))

    def display_tiles(self):
        for player, tiles in self.player_tiles.items():
            print(f"{player}'s Tiles: {' '.join(tiles)}")

    def place_word(self, word, row, col, direction):
        if direction == 'H':
            if col + len(word) > len(self.board[0]):
                return False
            if any(self.board[row][col + i] not in ('', letter) for i, letter in enumerate(word)):
                return False
            for i, letter in enumerate(word):
                self.board[row][col + i] = letter
        elif direction == 'V':
            if row + len(word) > len(self.board):
                return False
            if any(self.board[row + i][col] not in ('', letter) for i, letter in enumerate(word)):
                return False
            for i, letter in enumerate(word):
                self.board[row + i][col] = letter
        else:
            return False
        return True

    def calculate_score(self, word, row, col, direction):
        letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}
        word_score = 0
        word_multiplier = 1
        if direction == 'H':
            for i, letter in enumerate(word):
                letter_score = letter_values.get(letter, 0)
                word_score += letter_score
                if self.multiplier_board[row][col + i] == 'DW':
                    word_multiplier *= 2
                elif self.multiplier_board[row][col + i] == 'TW':
                    word_multiplier *= 3
        elif direction == 'V':
            for i, letter in enumerate(word):
                letter_score = letter_values.get(letter, 0)
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
                self.undo_last_move()
                return False
        self.draw_tiles(self.current_player)
        return True

    def draw_tiles(self, player):
        needed_tiles = 7 - len(self.player_tiles[player])
        if needed_tiles > 0:
            new_tiles = [self.tiles.pop() for _ in range(needed_tiles)]
            self.player_tiles[player].extend(new_tiles)

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
            pass
        elif self.difficulty == "Easy":
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
                self.calculate_score(word, row, col, direction)
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
        pass

    def add_word_restrictions(self):
        pass

    def manage_swap(self):
        if self.swap_count[self.current_player] < self.swap_limit:
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
            pass
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
            pass
        elif self.difficulty == "Easy":
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
    def switch_player(self):
        self.current_player = "Player 1" if self.current_player == "Player 2" else "Player 2"

    def manage_special_tiles(self):
        pass

    def manage_tile_replacement(self):
        pass

    def provide_clues(self):
        pass

    def handle_restricted_words(self):
        pass

if __name__ == "__main__":
    game = Scrabble()
    game.run()
