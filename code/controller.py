import tkinter as tk
from tkinter import messagebox
import word_search
import window


class Settings:

  def __init__(self, master):
    self.master = master
    self.word_search_created = False
    self.master.geometry("500x500")
    self.master.resizable(False, False)
    self.master.configure(bg="#161616")
    self.amount_to_generate = 0
    self.drag_mode = tk.BooleanVar()

    # Creates and places the widgets necessary for creating a custom word search
    self.board_size_input = self.create_input_field(5, self.validate_int)
    self.board_size_input.place(
        relx=.5,
        rely=.20,
        anchor="center",
    )
    self.confirm_board_size = self.create_button(self.master,
                                                 "Confirm Board Size",
                                                 self.__get_input_board_size, 15)
    self.confirm_board_size.place(relx=.5, rely=.30, anchor="center")

    self.word_input = self.create_input_field(15, self.validate_word)
    self.word_input.place(relx=.5, rely=.45, anchor="center")

    self.confirm_word = self.create_button(self.master, "Add Word",
                                           self.__get_input_word, 15)
    self.confirm_word.place(relx=.5, rely=.55, anchor="center")

    self.random_words = self.create_button(self.master, "Generate Words",
                                           self.generate_random_words, 15)
    self.random_words.place(relx=.65, rely=.7, anchor="center")

    self.amount_random_words = self.create_input_field(5, self.validate_int)
    self.amount_random_words.place(relx=.35, rely=.7, anchor="center")

    self.drag_mode_button = self.create_radiobutton("Click n Drag Mode",
                                                    self.drag_mode, True)
    self.drag_mode_button.place(relx=.3, rely=.82, anchor="center")

    self.select_mode_button = self.create_radiobutton("Individual Select Mode",
                                                      self.drag_mode, False)
    self.select_mode_button.place(relx=.3, rely=.88, anchor="center")

    self.create = self.create_button(self.master, "Create",
                                     self.create_word_search, 15)
    self.create.place(relx=.7, rely=.85, anchor="center")

  # General templates for creating differenct types of widgets
  def create_button(self, root, text, command, font_size):
    return tk.Button(root,
                     text=text,
                     background="#1B1B1B",
                     foreground="#FDFFFC",
                     activebackground="#282626",
                     activeforeground="#FDFFF7",
                     command=command,
                     font=("Calistoga", font_size))

  def create_radiobutton(self, text, var, value):
    return tk.Radiobutton(self.master,
                          text=text,
                          variable=var,
                          value=value,
                          background="#1B1B1B",
                          foreground="#FDFFFC",
                          activebackground="#282626",
                          activeforeground="#FDFFF7",
                          selectcolor="#1B1B1B",
                          font=("Calistoga", 12),
                          highlightthickness=0)

  def create_input_field(self, width, validatecommand):
    validation = self.master.register(validatecommand)
    return tk.Entry(
        self.master,
        background="#1B1B1B",
        foreground="#FDFFFC",
        width=width,
        justify="center",
        font=("Calistoga", 15),
        validate="key",
        validatecommand=(validation, "%P"),
    )

  # Retrieving valid inputs from the user
  def __get_input_board_size(self):
    if self.board_size_input.get().isdigit():
      board_size = int(self.board_size_input.get())
      if board_size in range(10, 26):
        self.word_search = word_search.WordSearch(board_size)
        self.word_search_created = True
      else:
        self.__show_error("Board size must be between 10 and 25")

  def __get_input_word(self):
    if self.word_search_created:
      self.__show_error(self.word_search.add_word(self.word_input.get()))
      self.word_input.delete(0, tk.END)
    else:
      self.__show_error("Set a board size before adding words!")

  def __show_error(self, msg):
    if msg != "":
      messagebox.showerror("Error", msg)

  def generate_random_words(self):
    # Ensures word search is created
    if not self.word_search_created:
      self.__show_error("Input board size before generating words.")

    # Ensures requested amount of words is valid for the board size
    if self.amount_random_words.get() == "0" or "":
      self.__show_error("Invalid amount of words to generate")
      return

    self.amount_to_generate = int(self.amount_random_words.get())
    excessive_words = self.amount_to_generate + len(
        self.word_search.word_list) - (self.word_search.word_limit)
    if excessive_words > 0:
      if self.amount_to_generate - excessive_words != 0:
        self.__show_error("Can only generate " +
                          str(self.amount_to_generate - excessive_words) +
                          " more words. Try again.")
      else:
        self.__show_error("Can't generate anymore words.")
    else:
      # Amount is validated and passed to the word search to generate the words
      self.__show_error(
          self.word_search.generate_words(self.amount_to_generate))

  def create_word_search(self):
    
    if self.word_search_created and len(self.word_search.word_list) > 0:
      self.word_search.word_list = sorted(self.word_search.word_list,
                                          key=len,
                                          reverse=True)
      # Places words from word list onto the board 
      self.word_search.place_words()
      # Fills the remaining spaces with random characters
      self.word_search.fill_board()
      self.create_window()

    elif not self.word_search_created:
      self.__show_error("Set a board size before creating a window!")
    else:
      self.__show_error("Add words to your word search!")

  def create_window(self):
    # Settings window is no longer needed so it is destroyed
    self.master.destroy()
    # Creates a new root window for the word search
    root = tk.Tk()
    root.title("Word Search")
    root.geometry("1645x1170")
    root.resizable(False, False)
    root.configure(bg="#161616")
    # Passes the root window and word search to be assembled into the GUI
    self.word_search_gui = window.WordSearchGUI(root, self.word_search, self)

  def validate_word(self, input):
    return input.isalpha() or input == ""

  def validate_int(self, input):
    return input.isdigit() or input == ""
