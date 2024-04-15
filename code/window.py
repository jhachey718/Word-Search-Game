import tkinter as tk
import controller
import word_search


class WordSearchGUI:

  class Letter:

    def __init__(self, rectangle):
      self.rectangle = rectangle
      self.solved = False

  def __init__(self, master, wordsearch, settings):
    # Setting up window
    self.__settings = settings
    self.master = master
    self.master.update()
    self.word_search = wordsearch
    self.selected_word = self.word_search.Word()
    self.letter_list = [[
        self.Letter(0) for _ in range(self.word_search.board_size)
    ] for _ in range(self.word_search.board_size)]
    self.selected_rectangle_list = []
    self.drag_mode = settings.drag_mode.get()
    self.offset = 1070 // self.word_search.board_size - 2
    if self.word_search.board_size < 16:
      self.offset -= 2
    if self.word_search.board_size < 13:
     self.offset -= 1

    self.width = self.master.winfo_width()
    self.height = self.master.winfo_height() - 75
    print(self.width, self.height)
    self.word_bank = []
    self.font_size = 375 // self.word_search.board_size

    if self.font_size > 20:
      self.font_size = 20

    # Creating reset button and button to create a new board
    self.__reset_button = settings.create_button(self.master, "Reset",
                                                 self.__reset, self.font_size)
    self.__settings_button = settings.create_button(self.master, "New Board",
                                                    self.__settings,
                                                    self.font_size)

    # Places buttons
    if not self.drag_mode:
      self.__reset_button.place(relx=.25, y=self.height + 2)
      self.__settings_button.place(relx=.35, y=self.height + 2)
    else:
      self.__settings_button.place(relx=.30, y=self.height + 2)

    if self.offset % 2 != 0:
      self.offset += 1

    # Canvas for word search and word bank to be drawn on
    self.canvas = tk.Canvas(master,
                            width=self.width,
                            height=self.height,
                            background="#161616",
                            highlightthickness=0)
    self.canvas.pack()
    self.__draw_grid()

    # Binding left click to start a selection of letters
    self.master.bind("<Button-1>", self.__select)

    # Binding 'r' to reset the board if not in drag mode
    if not self.drag_mode:
      self.master.bind("<Key>", self.__process_key)
    else:
      self.master.bind("<B1-Motion>", self.__select)
      self.master.bind("<ButtonRelease-1>", self.__end_selection)
    self.__generate_word_bank()

  def __draw_grid(self):
    for i in range(self.word_search.board_size):
      for j in range(self.word_search.board_size):
        self.x0 = j * self.offset + 50
        self.x1 = (j + 1) * self.offset + 50
        self.y0 = i * self.offset + 50
        self.y1 = (i + 1) * self.offset + 50
        self.letter_list[i][j] = self.Letter(
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

  ## Returns true if a given row and column is within the bounds of the board
  ## Else returns false
  def __in_bounds(self, row, col):
    return row >= 0 and row < self.word_search.board_size and col >= 0 and \
    col < self.word_search.board_size

  # Generates word bank with word search word list
  def __generate_word_bank(self):
    # Range of pixels that will form the rectangle
    x0 = self.width / 2 + 335
    y0 = self.height - 20
    x1 = x0 + 425
    y1 = 50
    # Creates rectangle for words to be placed on
    self.canvas.create_rectangle(x0,
                                 y0,
                                 x1,
                                 y1,
                                 fill="#1B1B1B",
                                 outline="#FDFFFC")
    # Setting up counters
    i = 1
    j = 0

    column = 0
    multi_columns = False
    words_per_column = 0
    font_difference = 12

    # Determines if multiple columns is necessary based on word list length
    if len(self.word_search.word_list) > 25:
      multi_columns = True
    line_spacing = 500 // font_difference
    words_per_column = font_difference + 12

    for word in self.word_search.word_list:
      temp_font_difference = font_difference

      # Determines font size for individual word based on word length
      if len(word) > 11 and len(word) <= 17 and multi_columns:
        temp_font_difference += 2

      if len(word) > 17:
        if not multi_columns:
          temp_font_difference += 2
        else:
          temp_font_difference += 7

      # Sets up two columns to allow for more words
      if multi_columns:
        if j == 0:
          column = 12 / 45

        elif j == words_per_column:
          column = 33 / 45
          i = 1

        # Creates text box for each wor
        self.word_bank.append(
            self.canvas.create_text(x0 + (x1 - x0) * column,
                                    y1 + line_spacing * i,
                                    text=word,
                                    fill="#FDFFFC",
                                    justify="center",
                                    font=("Calistoga",
                                          250 // temp_font_difference)))
        j += 1

      else:
        # Creates text box for each word
        self.word_bank.append(
            self.canvas.create_text(x0 + (x1 - x0) / 2,
                                    y1 + line_spacing * i,
                                    text=word,
                                    fill="#FDFFFC",
                                    justify="center",
                                    font=("Calistoga",
                                          250 // temp_font_difference)))
      i += 1

  def __select(self, event):
    # Retrieves row and column of the rectangle that was clicked
    self.row = (event.y - 50) // self.offset
    self.col = (event.x - 50) // self.offset

    if self.__in_bounds(self.row, self.col):
      # Creates a letter object to store rectangle and solved state
      letter = self.letter_list[self.row][self.col]

      # Check if letter has already been selected
      if [self.row, self.col] not in self.selected_word.indexes:
        # Retrieves exact point the mouse was clicked
        y = (event.y - 50) / self.offset - self.row
        x = (event.x - 50) / self.offset - self.col

        # Checks to see if the mouse was dragged near the center of the rectangle
        if not self.drag_mode or (x >= .3 and x <= .8 and y >= .3 and y <= .8):
          self.canvas.itemconfig(letter.rectangle, fill='red')
          self.selected_word.indexes.append([self.row, self.col])
          self.selected_rectangle_list.append(letter)

        if not self.drag_mode:
          self.__check_word(len(self.selected_word.indexes))

  # Ends a selection after a mouse release and checks if the word is valid
  def __end_selection(self, event):
    if self.__in_bounds(self.row, self.col):
      letter = self.letter_list[self.row][self.col]
      self.canvas.itemconfig(letter.rectangle, fill='red')
      self.selected_rectangle_list.append(letter)
    self.__check_word(len(self.selected_word.indexes))

  def __check_word(self, length):
    # Determines if the indices of the selected letters match with the word list
    index = self.word_search.check_guess(self.selected_word)

    if index != -1:
      for i in range(0, length):
        self.canvas.itemconfig(self.selected_rectangle_list[i].rectangle,
                               fill='green')
        self.selected_rectangle_list[i].solved = True
      current_text = self.canvas.itemcget(self.word_bank[index], "text")
      self.canvas.itemconfig(self.word_bank[index],
                             text=current_text + u'\u2713',
                             fill="#67e356")
      self.selected_rectangle_list.clear()
      self.selected_word = self.word_search.Word()

      if self.word_search.words_found == len(self.word_search.word_list):
        self.__winning_message()
    elif self.drag_mode:
      self.__reset()

  # Creates a window with a message after the user has found every word
  def __winning_message(self):
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

  def __process_key(self, event):
    if event.char.lower() == 'r':
      self.__reset()

  # Returns any currently selected letter on the board to their original state
  def __reset(self):
    for rect in self.selected_rectangle_list:

      if rect.solved:
        self.canvas.itemconfig(rect.rectangle, fill='green')
      else:
        self.canvas.itemconfig(rect.rectangle, fill='#1B1B1B')

    self.selected_rectangle_list.clear()
    self.selected_word = self.word_search.Word()

  # Destroys current word search window and creates a new setting window
  def __settings(self):
    self.master.destroy()
    root = tk.Tk()
    root.title("Settings")
    controller.Settings(root)
