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
    self.master.configure(bg="#5B8E7D")
    self.amount_to_generate = 0
    self.board_size_input = self.create_input_field(5, self.validate_int)
    self.board_size_input.place(
        relx=.5,
        rely=.20,
        anchor="center",
    )
    self.confirm_board_size = self.create_button("Confirm Board Sizes",
                                                 self.get_input_board_size)
    self.confirm_board_size.place(relx=.5, rely=.30, anchor="center")
    self.word_input = self.create_input_field(15, self.validate_word)
    self.word_input.place(relx=.5, rely=.45, anchor="center")
    self.confirm_word = self.create_button("Add Word", self.get_input_word)
    self.confirm_word.place(relx=.5, rely=.55, anchor="center")
    self.random_words = self.create_button("Generate Words",
                                           self.generate_random_words)
    self.random_words.place(relx=.65, rely=.7, anchor="center")
    self.amount_random_words = self.create_input_field(5, self.validate_int)
    self.amount_random_words.place(relx=.35, rely=.7, anchor="center")

    self.create = self.create_button("Create", self.create_window)
    self.create.place(relx=.5, rely=.85, anchor="center")

  def get_input_board_size(self):
    if self.board_size_input.get().isdigit():
      board_size = int(self.board_size_input.get())
      if board_size in range(10, 26):
        self.word_search = word_search.WordSearch(board_size)
        self.word_search_created = True
      else:
        self.show_error("Board size must be between 10 and 25")

  def get_input_word(self):
    if self.word_search_created:
      self.show_error(self.word_search.add_word(self.word_input.get()))
      self.word_input.delete(0, tk.END)
    else:
      self.show_error("Set a board size before adding words!")

  def create_input_field(self, width, validatecommand):
    validation = self.master.register(validatecommand)
    return tk.Entry(self.master,
                    background="#0B132B",
                    foreground="#FDFFFC",
                    width=width,
                    justify="center",
                    font=("Calistoga", 15),
                    validate="key",
                    validatecommand=(validation, "%P"))

  def create_button(self, text, command):
    return tk.Button(self.master,
                     text=text,
                     background="#0B132B",
                     foreground="#FDFFFC",
                     activebackground="#1F2644",
                     activeforeground="#FDFFF7",
                     command=command,
                     font=("Calistoga", 15))

  def show_error(self, msg):
    if msg != "":
      messagebox.showerror("Error", msg)

  def generate_random_words(self):
    if self.amount_random_words.get() == "0" or "":
      self.show_error("Invalid amount of words to generate")
    if not self.word_search_created:
      self.show_error("Input board size before generating words.")
    else:
      self.amount_to_generate = int(self.amount_random_words.get())
      excessive_words = self.amount_to_generate + len(
          self.word_search.word_list) - (self.word_search.board_size * 2)
      if excessive_words > 0:
        if self.amount_to_generate - excessive_words != 0:
          self.show_error("Can only generate " +
                        str(self.amount_to_generate - excessive_words) +
                        " more words. Try again.")
        else:
          self.show_error("Can't generate anymore words.")
      else:
        self.show_error(self.word_search.generate_words(self.amount_to_generate))

  def create_window(self):
    if self.word_search_created and len(self.word_search.word_list) > 0:
      self.word_search.word_list = sorted(self.word_search.word_list,
                                          key=len,
                                          reverse=True)
      self.word_search.place_words()
      self.word_search.fill_board()
      self.master.destroy()
      root = tk.Tk()
      root.title("Word Search")
      root.geometry("1280x750")
      root.resizable(False, False)
      root.configure(bg="#5B8E7D")
      self.word_search_gui = window.WordSearchGUI(root, self.word_search)
    elif not self.word_search_created:
      self.show_error("Set a board size before creating a window!")
    else:
      self.show_error("Add words to your word search!")

  def validate_word(self, input):
    return input.isalpha() or input == ""

  def validate_int(self, input):
    return input.isdigit() or input == ""