import tkinter as tk
import controller
import word_search


class WordSearchGUI:

  class Letter:

    def __init__(self, rectangle):
      self.selected = False
      self.rectangle = rectangle

  def __init__(self, master, wordsearch):
    self.master = master
    self.word_search = wordsearch
    self.selected_indexes = []
    self.selected_word = ""
    self.rectangle_list = [[
        self.Letter(0) for _ in range(self.word_search.board_size)
    ] for _ in range(self.word_search.board_size)]
    self.selected_rectangle_list = []
    self.previous_row = 0
    self.previous_col = 0
    self.offset = 665 // self.word_search.board_size
    self.width = 1280
    self.height = 695
    self.word_bank = []
    self.font_size = 375 // self.word_search.board_size
    if self.font_size > 20:
      self.font_size = 20
    self.reset_button = tk.Button(self.master,
                                  text="Reset",
                                  font=("Calistoga", 15),
                                  command=self.reset)
    self.settings_button = tk.Button(self.master,
                                     text="New Board",
                                     font=("Calistoga", 15),
                                     command=self.settings)
    self.reset_button.place(relx=.18, y=self.height + 2)
    self.settings_button.place(relx=.28, y=self.height + 2)
    if self.offset % 2 != 0:
      self.offset += 1

    self.canvas = tk.Canvas(
        master,
        width=self.width,
        height=self.height,
        background="#161616",
        highlightthickness=0)
    # 0B132B - oxford blue
    # FDFFFC - baby powder
    # F4A259 - sandy brown
    # 5B8E7D - viridian
    # BC4B51 - shimmer
    # 048A81 - dark cyan

    self.canvas.pack()

    self.draw_grid()
    self.master.bind("<Key>", self.process_key)
    self.master.bind("<Button-1>", self.select)
    # self.master.bind("<Configure> ", self.resize)
    self.generate_word_bank()

  # def resize(self, event):
  #   self.canvas.config(width=event.width, height=event.height)

  def draw_grid(self):
    for i in range(self.word_search.board_size):
      for j in range(self.word_search.board_size):
        self.x0 = j * self.offset + 25
        self.x1 = (j + 1) * self.offset + 25
        self.y0 = i * self.offset + 25
        self.y1 = (i + 1) * self.offset + 25
        self.rectangle_list[i][j] = self.Letter(
            self.canvas.create_rectangle(self.x0,
                                         self.y0,
                                         self.x1,
                                         self.y1,
                                         outline="#FDFFFC",
                                         fill="#1B1B1B"))
        self.canvas.create_text(self.x0 + self.offset // 2,
                                self.y0 + self.offset // 2,
                                text=self.word_search.board[i][j],
                                fill="#FDFFFC",
                                font=("Calistoga", self.font_size))

  def check_word(self):
    index = self.word_search.check_guess(self.selected_word)
    if index != -1:
      for rect in self.selected_rectangle_list:
        self.canvas.itemconfig(rect.rectangle, fill='green')
      current_text = self.canvas.itemcget(self.word_bank[index], "text")
      self.canvas.itemconfig(self.word_bank[index],
                             text=current_text + u'\u2713',
                             fill="#67e356")
      self.selected_rectangle_list.clear()
      self.selected_word = ""

  def select(self, event):
    self.row = (event.y - 25) // self.offset
    self.col = (event.x - 25) // self.offset
    if self.row < 0 or self.row >= self.word_search.board_size or self.col < 0 or \
    self.col >= self.word_search.board_size:
      return
    letter = self.rectangle_list[self.row][self.col]
    if not letter.selected:
      letter.selected = True
      self.canvas.itemconfig(letter.rectangle, fill='red')
      self.selected_rectangle_list.append(letter)
      self.selected_word += str(self.row) + str(self.col)
      self.check_word()

  def generate_word_bank(self):
    x0 = self.width / 2 + 125
    y0 = self.height - 50
    x1 = x0 + 425
    y1 = 50
    self.canvas.create_rectangle(x0,
                                 y0,
                                 x1,
                                 y1,
                                 fill="#1B1B1B",
                                 outline="#FDFFFC")
    i = 1
    j = 0
    column = 0
    multi_columns = False
    words_per_column = 0
    font_difference = 10
    if len(self.word_search.word_list) > 10:
      font_difference = len(self.word_search.word_list)
    if len(self.word_search.word_list) > 15:
      font_difference = 17 if len(self.word_search.word_list) > 30 else 12
      multi_columns = True
    line_spacing = 500 // font_difference
    words_per_column = font_difference + 1
    for word in self.word_search.word_list:
      temp_font_difference = font_difference
      if len(word) > 11 and len(word) <= 17 and multi_columns:
        temp_font_difference += 4
      if len(word) > 17:
        if not multi_columns:
          temp_font_difference += 2
        else:
          temp_font_difference += 10

      if multi_columns:
        if j == 0:
          column = 10 / 45

        elif j == words_per_column:
          column = 1 / 2
          i = 1

        elif j == 2 * words_per_column:
          column = 45 / 60
          i = 1

        self.word_bank.append(
            self.canvas.create_text(x0 + (x1 - x0) * column,
                                    y1 + line_spacing * i,
                                    text=word,
                                    fill="#FDFFFC",
                                    anchor="n",
                                    font=("Calistoga",
                                          250 // temp_font_difference)))
        j += 1

      else:
        self.word_bank.append(
            self.canvas.create_text(x0 + (x1 - x0) / 2,
                                    y1 + line_spacing * i,
                                    text=word,
                                    fill="#FDFFFC",
                                    anchor="n",
                                    justify="center",
                                    font=("Calistoga",
                                          250 // temp_font_difference)))
      i += 1

  def reset(self):
    for rect in self.selected_rectangle_list:
      self.canvas.itemconfig(rect.rectangle, fill='#0B132B')
      rect.selected = False
    self.selected_rectangle_list.clear()
    self.selected_word = ""

  def settings(self):
    self.master.destroy()
    root = tk.Tk()
    root.title("Settings")
    controller.Settings(root)

  def process_key(self, event):
    if event.char.lower() == 'r':
      self.reset()
