import tkinter as tk
import word_search
import window
import controller

word_search = word_search.WordSearch(25)
word_search.add_word("hellolplplplplplpllplpl")
word_search.generate_words(30)
word_search.word_list = sorted(word_search.word_list, key=len, reverse=True)
word_search.place_words()
# word_search.fill_board()
root = tk.Tk()
settings = controller.Settings(root)
settings.word_search = word_search
settings.word_search_created = True
settings.drag_mode = tk.BooleanVar(value=True)
settings.create_window()
root.mainloop()