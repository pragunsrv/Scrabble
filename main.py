import random
import string

class Scrabble:
    def __init__(self):
        self.board = self.create_board()
        self.tiles = self.create_tiles()
        self.player_tiles = []

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

    def draw_tiles(self):
        self.player_tiles = [self.tiles.pop() for _ in range(7)]

    def display_board(self):
        for row in self.board:
            print(' '.join([cell if cell else '.' for cell in row]))

    def place_word(self, word, row, col, direction):
        if direction == 'H':
            for i, letter in enumerate(word):
                self.board[row][col + i] = letter
        elif direction == 'V':
            for i, letter in enumerate(word):
                self.board[row + i][col] = letter

    def play(self):
        self.draw_tiles()
        self.display_board()
        print("Player's tiles:", self.player_tiles)
        word = input("Enter word to place: ")
        row = int(input("Enter row: "))
        col = int(input("Enter column: "))
        direction = input("Enter direction (H/V): ")
        self.place_word(word, row, col, direction)
        self.display_board()

game = Scrabble()
game.play()
