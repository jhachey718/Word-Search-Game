import tkinter as tk
import controller
import word_search


class WordSearchGUI:

  class Letter:

    def __init__(self, rectangle):
      self.rectangle = rectangle
      self.solved = False

  def __init__(self, master, wordsearch, clickndrag):
    self.master = master
    self.master.wait_visibility()
    self.word_search = wordsearch
    self.selected_word = self.word_search.Word()
    self.rectangle_list = [[
        self.Letter(0) for _ in range(self.word_search.board_size)
    ] for _ in range(self.word_search.board_size)]
    self.selected_rectangle_list = []
    self.drag_mode = clickndrag
    self.previous_row = 0
    self.previous_col = 0
    self.offset = 650 // self.word_search.board_size
    if self.word_search.board_size == 24:
      self.offset -= 1
    self.width = 1280
    self.height = 695
    self.word_bank = []
    self.font_size = 375 // self.word_search.board_size
    if self.font_size > 20:
      self.font_size = 20
    self.reset_button = tk.Button(self.master,
                                  text="Reset",
                                  font=("Calistoga", 15),
                                  background="#1B1B1B",
                                  foreground="#FDFFFC",
                                  activebackground="#282626",
                                  activeforeground="#FDFFF7",
                                  command=self.reset)
    self.settings_button = tk.Button(self.master,
                                     text="New Board",
                                     font=("Calistoga", 15),
                                     background="#1B1B1B",
                                     foreground="#FDFFFC",
                                     activebackground="#282626",
                                     activeforeground="#FDFFF7",
                                     command=self.settings)
    if not self.drag_mode:
      self.reset_button.place(relx=.18, y=self.height + 2)
      self.settings_button.place(relx=.28, y=self.height + 2)
    else:
      self.settings_button.place(relx=.23, y=self.height + 2)
    if self.offset % 2 != 0:
      self.offset += 1

    self.canvas = tk.Canvas(master,
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
    self.master.bind("<Button-1>", self.select)
    if not self.drag_mode:
      self.master.bind("<Key>", self.process_key)
    else:
      self.master.bind("<B1-Motion>", self.select)
      self.master.bind("<ButtonRelease-1>", self.end_selection)
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
        rect.solved = True
      current_text = self.canvas.itemcget(self.word_bank[index], "text")
      self.canvas.itemconfig(self.word_bank[index],
                             text=current_text + u'\u2713',
                             fill="#67e356")
      self.selected_rectangle_list.clear()
      self.selected_word = self.word_search.Word()
      if self.word_search.words_found == len(self.word_search.word_list):
        self.winning_message()
    elif self.drag_mode:
      self.reset()


  def end_selection(self, event):
    if self.in_bounds(self.row, self.col):
      letter = self.rectangle_list[self.row][self.col]
      self.canvas.itemconfig(letter.rectangle, fill='red')
      self.selected_rectangle_list.append(letter)
    self.check_word()

  def select(self, event):
    self.row = (event.y - 25) // self.offset
    self.col = (event.x - 25) // self.offset
    if self.in_bounds(self.row, self.col):
      letter = self.rectangle_list[self.row][self.col]
      if [self.row, self.col] not in self.selected_word.indexes:
        y = (event.y - 25) / self.offset - self.row
        x = (event.x - 25) / self.offset - self.col
        if not self.drag_mode or (x >= .3 and x <= .8 and y >= .3 and y <= .8):
          self.canvas.itemconfig(letter.rectangle, fill='red')
          self.selected_rectangle_list.append(letter)
          self.selected_word.indexes.append([self.row, self.col])
        if not self.drag_mode:
          self.check_word()

  def in_bounds(self, row, col):
    return row >= 0 and row < self.word_search.board_size and col >= 0 and \
    col < self.word_search.board_size

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
      font_difference = 17 if len(self.word_search.word_list) > 30 else 14
      multi_columns = True
    line_spacing = 500 // font_difference
    words_per_column = font_difference + 1
    for word in self.word_search.word_list:
      temp_font_difference = font_difference
      if len(word) > 8 and len(word) <= 11:
        temp_font_difference += 2
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

  def winning_message(self):
    self.win_window = tk.Toplevel(self.master)
    self.win_window.title("Word Search")
    self.win_window.geometry("400x200")
    self.win_window.wait_visibility()
    x = self.master.winfo_rootx(
    ) + self.master.winfo_width() // 2 - self.win_window.winfo_width() // 2
    y = self.master.winfo_rooty(
    ) + self.master.winfo_height() // 2 - self.win_window.winfo_height() // 2
    self.win_window.geometry(f"+{x}+{y}")
    self.win_window.resizable(False, False)
    self.win_window.configure(bg="#161616")
    label = tk.Label(self.win_window,
                     text="You Win!",
                     font=("Calistoga", 50),
                     fg="#67e356",
                     bg="#161616")
    label.place(anchor="center", relx=.5, rely=.5)

  def reset(self):
    for rect in self.selected_rectangle_list:
      if rect.solved:
        self.canvas.itemconfig(rect.rectangle, fill='green')
      else:
        self.canvas.itemconfig(rect.rectangle, fill='#1B1B1B')
    self.selected_rectangle_list.clear()
    self.selected_word = self.word_search.Word()

  def settings(self):
    self.master.destroy()
    root = tk.Tk()
    root.title("Settings")
    controller.Settings(root)

  def process_key(self, event):
    if event.char.lower() == 'r':
      self.reset()
