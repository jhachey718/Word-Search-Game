from copy import deepcopy
import random
import string
import window


class WordSearch:
  class Word:
    def __init__ (self):
      self.indexes = []

    def equals(self, other):
      list1 = self.indexes
      list2 = other.indexes
      if len(list1) != len(list2):
          return False

      # Check if each element is equal
      for i in range(len(list1)):
          if len(list1[i]) != len(list2[i]):
              return False
          if  not list1[i] in list2:
              return False
      return True
  def __init__(self, board_size):
    self.window = window
    self.board_size = board_size
    self.board = [['0' for _ in range(board_size)] for _ in range(board_size)]
    self.word_list = []
    self.index_list = []
    self.total_chars = 0
    self.WORDS = []
    self.MAX_CHARS = board_size * board_size - board_size * 2
    self.word_length_error = "Word must be at least 3 characters long"
    self.max_char_error = "Max amount of characters for board size reached!"
    self.word_limit = self.board_size * 2 if self.board_size > 15 else int(
        self.board_size * 1.5)

  def fill_board(self):
    for i in range(self.board_size):
      for j in range(self.board_size):
        if self.board[i][j] == '0':
          self.board[i][j] = random.choice(string.ascii_lowercase)

  def print_word_search(self):
    for row in self.board:
      print(' '.join(row))

  def place_words(self):
    for word in self.word_list:
      is_placed = False

      while not is_placed:
        word_indexes = self.Word()
        temp_board = deepcopy(self.board)
        col = random.randint(0, self.board_size - 1)
        row = random.randint(0, self.board_size - 1)
        # 0 1 2
        # 3 _ 4
        # 5 6 7
        if len(word) in range(self.board_size - 2, self.board_size):
          direction = random.randint(0, 7)
          if direction == 0:
            direction += 1
          if direction == 2 or direction == 5 or direction == 7:
            direction -= 1
        else:
          direction = random.randint(0, 7)
        if direction == 0 and col - len(word) >= 0 and row - len(word) >= 0:
          for i in range(len(word)):
            new_col = col - i
            new_row = row - i
            if temp_board[new_row][new_col] == '0' or temp_board[new_row][new_col] == word[i]:
              temp_board[new_row][new_col] = word[i]
              word_indexes.indexes.append([new_row, new_col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 1 and row - len(word) >= 0:
          for i in range(len(word)):
            new_row = row - i
            if temp_board[new_row][col] == '0' or temp_board[new_row][col] == word[i]:
              temp_board[new_row][col] = word[i]
              word_indexes.indexes.append([new_row, col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 2 and col + len(word) <= self.board_size and row - len(
            word) >= 0:
          for i in range(len(word)):
            new_col = col + i
            new_row = row - i
            if temp_board[new_row][new_col] == '0' or temp_board[new_row][new_col] == word[i]:
              temp_board[new_row][new_col] = word[i]
              word_indexes.indexes.append([new_row, new_col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 3 and col - len(word) >= 0:
          for i in range(len(word)):
            new_col = col - i
            if temp_board[row][new_col] == '0' or temp_board[row][new_col] == word[i]:
              temp_board[row][new_col] = word[i]
              word_indexes.indexes.append([row, new_col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 4 and col + len(word) <= self.board_size:
          for i in range(len(word)):
            new_col = col + i
            if temp_board[row][new_col] == '0' or temp_board[row][new_col] == word[i]:
              temp_board[row][new_col] = word[i]
              word_indexes.indexes.append([row, new_col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 5 and col - len(word) >= 0 and row + len(
            word) <= self.board_size:
          for i in range(len(word)):
            new_col = col - i
            new_row = row + i
            if temp_board[new_row][new_col] == '0' or temp_board[new_row][new_col] == word[i]:
              temp_board[new_row][new_col] = word[i]
              word_indexes.indexes.append([new_row, new_col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 6 and row + len(word) <= self.board_size:
          for i in range(len(word)):
            new_row = row + i
            if temp_board[new_row][col] == '0' or temp_board[new_row][col] == word[i]:
              temp_board[new_row][col] = word[i]
              word_indexes.indexes.append([new_row, col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if direction == 7 and col + len(word) <= self.board_size and row + len(
            word) <= self.board_size:
          for i in range(len(word)):
            new_row = row + i
            new_col = col + i
            if temp_board[new_row][new_col] == '0' or temp_board[new_row][new_col] == word[i]:
              temp_board[new_row][new_col] = word[i]
              word_indexes.indexes.append([new_row, new_col])
              if i == len(word) - 1:
                is_placed = True
                # print(f"Placed {word}")
            else:
              break

        if is_placed:
          # print("board updated")
          self.index_list.append(word_indexes)
          self.board = deepcopy(temp_board)
    # print(self.index_list)

  def check_guess(self, selected_word):
    for index, word in enumerate(self.index_list):
      if word.equals(selected_word):
        return index
    return -1

  def generate_words(self, amount_to_generate):
    if len(self.WORDS) == 0:
      word_file = "words.txt"
      with open(word_file) as file:
        self.WORDS = file.read().splitlines()
    for _ in range(amount_to_generate):
      while (True):
        random_word = random.choice(self.WORDS)
        message = self.add_word(random_word)
        if message == "":
          break
        elif message == self.max_char_error:
          return message
    return ""

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
