import random
import string
import tkinter as tk
from copy import deepcopy

board_size = 10


class WordSearchGUI:

  def __init__(self, master, grid):
    self.master = master
    self.grid = grid
    self.rows = len(grid)
    self.cols = len(grid[0])
    self.selected_word = ""

    self.canvas = tk.Canvas(master,
                            width=self.cols * 50,
                            height=self.rows * 50)
    self.canvas.pack()

    self.draw_grid()
    self.canvas.bind("<Button-1>", self.start_selection)
    self.canvas.bind("<B1-Motion>", self.select_letters)
    self.canvas.bind("<ButtonRelease-1>", self.end_selection)

  def draw_grid(self):
    for i in range(self.rows):
      for j in range(self.cols):
        self.canvas.create_rectangle(j * 50,
                                     i * 50, (j + 1) * 50, (i + 1) * 50,
                                     outline="black")
        self.canvas.create_text(j * 50 + 25,
                                i * 50 + 25,
                                text=self.grid[i][j],
                                font=("Arial", 20))

  def start_selection(self, event):
    self.start_row = event.y // 50
    self.start_col = event.x // 50
    y = event.y / 50 - self.start_row
    x = event.x / 50 - self.start_col
    if x >= .3 and x <= .8 and y >= .3 and y <= .8:
      self.selected_word = self.grid[event.y // 50][event.x // 50]
      print("" + str(event.y / 50) + " " + str(event.x / 50))

  def select_letters(self, event):
    current_row = event.y // 50
    current_col = event.x // 50
    y = event.y / 50 - current_row
    x = event.x / 50 - current_col
    if (current_row != self.start_row or current_col) != self.start_col and \
    x >= .3 and x <= .8 and y >= .3 and y <= .8:
      self.selected_word += self.grid[current_row][current_col]
      self.start_row = current_row
      self.start_col = current_col

  def end_selection(self, event):
    print("Selected Word:", self.selected_word)


def generate_board():
  return [['0' for _ in range(board_size)] for _ in range(board_size)]


def fill_board(board):
  for i in range(board_size):
    for j in range(board_size):
      if board[i][j] == '0':
        board[i][j] = random.choice(string.ascii_lowercase)
  return board


def print_board(board):
  for row in board:
    print(' '.join(row))


board = generate_board()
word_list = []
word = ""
while word != '0':
  word = str(input("Enter a word or 0 when done: "))
  if len(word_list) >= board_size // 2 and word != '0':
    print("Word limit for board size reached")
  elif not word.isdigit() and len(word) <= board_size - 1:
    word_list.append(word.lower().strip())
  elif word != '0':
    print("Invalid word")
temp_board = 0

for word in word_list:
  is_placed = False

  while not is_placed:
    temp_board = deepcopy(board)
    col = random.randint(0, board_size - 1)
    row = random.randint(0, board_size - 1)
    # 0 1 2
    # 3 _ 4
    # 5 6 7
    if len(word) in range(board_size - 2, board_size):
      direction = random.randint(0, 7)
      if direction == 0:
        direction += 1
      if direction == 2 or direction == 5 or direction == 7:
        direction -= 1
    else:
      direction = random.randint(0, 7)
    if direction == 0 and col - len(word) >= 0 and row - len(word) >= 0:
      for i in range(len(word)):
        if temp_board[row - i][col - i] == '0':
          temp_board[row - i][col - i] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 1 and row - len(word) >= 0:
      for i in range(len(word)):
        if temp_board[row - i][col] == '0':
          temp_board[row - i][col] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 2 and col + len(word) <= board_size and row - len(
        word) >= 0:
      for i in range(len(word)):
        if temp_board[row - i][col + i] == '0':
          temp_board[row - i][col + i] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 3 and col - len(word) >= 0:
      for i in range(len(word)):
        if temp_board[row][col - i] == '0':
          temp_board[row][col - i] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 4 and col + len(word) <= board_size:
      for i in range(len(word)):
        if temp_board[row][col + i] == '0':
          temp_board[row][col + i] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 5 and col - len(word) >= 0 and row + len(
        word) <= board_size:
      for i in range(len(word)):
        if temp_board[row + i][col - i] == '0':
          temp_board[row + i][col - i] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 6 and row + len(word) <= board_size:
      for i in range(len(word)):
        if temp_board[row + i][col] == '0':
          temp_board[row + i][col] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if direction == 7 and col + len(word) <= board_size and row + len(
        word) <= board_size:
      for i in range(len(word)):
        if temp_board[row + i][col + i] == '0':
          temp_board[row + i][col + i] = word[i]
          if i == len(word) - 1:
            is_placed = True
            # print(f"Placed {word}")
        else:
          break

    if is_placed:
      print("board updated")
      board = deepcopy(temp_board)

fill_board(board)

root = tk.Tk()
root.title("Word Search")
word_search_gui = WordSearchGUI(root, board)
root.mainloop()
# print_board(board)
# print("Col: " + str(col))
# print("Row: " + str(row))
# print(board[col][row])
