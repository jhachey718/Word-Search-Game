from copy import deepcopy
import random
import string
import window
from pathlib import Path


class WordSearch:

  # Contains a list of row and columns mapping to where each letter of a word is on a board
  class Word:

    def __init__(self):
      self.found = False
      self.indexes = []

    def equals(self, other):
      list1 = self.indexes
      list2 = other.indexes
      if len(list1) != len(list2):
        return False
      # Check if each element exists in both lists
      return all(item in list2 for item in list1)

  def __init__(self, board_size):
    self.board_size = board_size
    self.board = [['0' for _ in range(board_size)] for _ in range(board_size)]
    self.word_list = []
    self.index_list = []
    self.total_chars = 0
    self.WORDS = []
    self.words_found = 0
    self.MAX_CHARS = board_size * board_size - board_size * 2
    self.word_length_error = "Word must be at least 3 characters long"
    self.max_char_error = "Max amount of characters for board size reached!"
    self.word_limit = self.board_size * 2 if self.board_size > 15 else int(
        self.board_size * 1.5)

  # Any spot on the board that is not already occupied is replaces with random letters
  def fill_board(self):
    for i in range(self.board_size):
      for j in range(self.board_size):
        if self.board[i][j] == '0':
          self.board[i][j] = random.choice(string.ascii_lowercase)

  # Only for debugging purposes
  def print_word_search(self):
    for row in self.board:
      print(' '.join(row))

  # Picks a random word from the word list and attempts to add it to the board
  def generate_words(self, amount_to_generate):
    if len(self.WORDS) == 0:
      # Creating a path to the word list
      p = Path('..')
      p = p.cwd()
      word_file = str(p) + '/word_lists/words.txt'
      with open(word_file) as file:
        self.WORDS = file.read().splitlines()
    for _ in range(amount_to_generate):
      while (True):
        random_word = random.choice(self.WORDS)
        message = self.add_word(random_word)
        if message == "":
          break
        else:
          return message
    return ""

  # Ensures the word can fit on the board and adds it
  def add_word(self, word):
    word = str(word)
    if len(self.word_list) > self.word_limit:
      return "Word limit reached"
    if len(word) <= 2:
      return self.word_length_error
    if len(word) >= self.board_size - 1:
      return "Word must be at least one character shorter than board size"
    if len(word) + self.total_chars > self.MAX_CHARS:
      return self.max_char_error
    else:
      self.total_chars += len(word)
      self.word_list.append(word.lower().strip())
      return ""
  
  # Generates a random direction for a word to be placed
  def __generate_direction(self, word):
    # 0 1 2
    # 3 _ 4
    # 5 6 7
    direction = random.randint(0, 7)
    if len(word) in range(self.board_size - 2, self.board_size):
      if direction == 0:
        direction += 1
      if direction == 2 or direction == 5 or direction == 7:
        direction -= 1
    return direction

  # Tests if placement of a letter is valid
  def __test_place(self, word, temp_board, new_row, new_col, i):
    if temp_board[new_row][new_col] == '0' or temp_board[new_row][
      new_col] == word[i]:
      temp_board[new_row][new_col] = word[i]
      self.word_indexes.indexes.append([new_row, new_col])
      return True
    else:
      return False

  # Places all words in the word list
  def place_words(self):
    for word in self.word_list:
      is_placed = False

      while not is_placed:
        self.word_indexes = self.Word()
        temp_board = deepcopy(self.board)
        col = random.randint(0, self.board_size - 1)
        row = random.randint(0, self.board_size - 1)
        direction = self.__generate_direction(word)

        # Checks direction that was generate and determines whether or not it can be placed
        if direction == 0 and col - len(word) >= 0 and row - len(word) >= 0:
          for i in range(len(word)):
            new_col = col - i
            new_row = row - i
                # print(f"Placed {word}")
            is_placed = self.__test_place(word, temp_board, new_row, new_col, i)
            if not is_placed:
              break

        elif direction == 1 and row - len(word) >= 0:
          for i in range(len(word)):
            new_row = row - i
            is_placed = self.__test_place(word, temp_board, new_row, col, i)
            if not is_placed:
              break

        elif direction == 2 and col + len(word) <= self.board_size and row - len(
            word) >= 0:
          for i in range(len(word)):
            new_col = col + i
            new_row = row - i
            is_placed = self.__test_place(word, temp_board, new_row, new_col, i)
            if not is_placed:
              break

        elif direction == 3 and col - len(word) >= 0:
          for i in range(len(word)):
            new_col = col - i
            is_placed = self.__test_place(word, temp_board, row, new_col, i)
            if not is_placed:
              break

        elif direction == 4 and col + len(word) <= self.board_size:
          for i in range(len(word)):
            new_col = col + i
            is_placed = self.__test_place(word, temp_board, row, new_col, i)
            if not is_placed:
              break

        elif direction == 5 and col - len(word) >= 0 and row + len(
            word) <= self.board_size:
          for i in range(len(word)):
            new_col = col - i
            new_row = row + i
            is_placed = self.__test_place(word, temp_board, new_row, new_col, i)
            if not is_placed:
              break

        elif direction == 6 and row + len(word) <= self.board_size:
          for i in range(len(word)):
            new_row = row + i
            is_placed = self.__test_place(word, temp_board, new_row, col, i)
            if not is_placed:
              break

        elif direction == 7 and col + len(word) <= self.board_size and row + len(
            word) <= self.board_size:
          for i in range(len(word)):
            new_row = row + i
            new_col = col + i
            is_placed = self.__test_place(word, temp_board, new_row, new_col, i)
            if not is_placed:
              break

        if is_placed:
          # print("board updated")
          # Appends the word's row and column to the list
          self.index_list.append(self.word_indexes)
          # Copies over the temp board
          self.board = deepcopy(temp_board)
    # print(self.index_list)

  # Returns the index of the word if found
  def check_guess(self, selected_word):
    for index, word in enumerate(self.index_list):
      if not word.found and word.equals(selected_word):
        word.found = True
        self.words_found += 1
        return index
    return -1
