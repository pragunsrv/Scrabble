import random
import string

class Scrabble:
    def __init__(self):
        self.board = self.create_board()
        self.tiles = self.create_tiles()
        self.player_tiles = []
        self.word_list = self.load_word_list()

    def create_board(self):
        board = [['' for _ in range(15)] for _ in range(15)]
        return board

    def create_tiles(self):
        letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}
        tiles = []
        for letter, value in letter_values.items():
            tiles.extend([letter] * (8 if letter in 'EAIONRTLSU' else 1))
        random.shuffle(tiles)
        return tiles

    def load_word_list(self):
        # This is a placeholder for loading a word list
        return set(["CAT", "DOG", "FISH", "BIRD", "FROG"])

    def draw_tiles(self):
        self.player_tiles = [self.tiles.pop() for _ in range(7)]

    def display_board(self):
        for row in self.board:
            print(' '.join([cell if cell else '.' for cell in row]))

    def display_tiles(self):
        print("Player's tiles:", self.player_tiles)

    def place_word(self, word, row, col, direction):
        if not self.is_valid_placement(word, row, col, direction):
            print("Invalid word placement.")
            return
        if direction == 'H':
            for i, letter in enumerate(word):
                self.board[row][col + i] = letter
        elif direction == 'V':
            for i, letter in enumerate(word):
                self.board[row + i][col] = letter

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

    def update_score(self, word):
        score = 0
        letter_values = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}
        for letter in word:
            score += letter_values.get(letter, 0)
        return score

    def check_word(self, word):
        return word in self.word_list

    def play(self):
        self.draw_tiles()
        self.display_board()
        self.display_tiles()
        word = input("Enter word to place: ").upper()
        if not self.check_word(word):
            print("Word not in dictionary.")
            return
        row = int(input("Enter row: "))
        col = int(input("Enter column: "))
        direction = input("Enter direction (H/V): ").upper()
        self.place_word(word, row, col, direction)
        print(f"Word score: {self.update_score(word)}")
        self.display_board()
        self.display_tiles()

game = Scrabble()
game.play()
