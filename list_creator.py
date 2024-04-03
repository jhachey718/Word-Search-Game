# Open the text file for reading
with open('words.txt', 'r') as file:
    # Read the content of the file
    text = file.read()

# Split the text into words
words = text.splitlines()

# Filter out words with less than 3 letters
filtered_words = [word for word in words if len(word) >= 3]

# Join the filtered words with each word separated by a new line
filtered_text = '\n'.join(filtered_words)

# Open the same or a different file for writing
with open('output.txt', 'w') as file:
    # Write the filtered text to the file
    file.write(filtered_text)