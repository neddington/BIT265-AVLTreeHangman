import tkinter as tk
import random
from avl_tree import AVLTree


# Hardcoded list of words to choose from
words = ["apple", "banana", "cherry", "durian", "elderberry", "cheese"]

# Hangman figure
hangman = [
    " _____ ",
    " |     |",
    " O     |",
    "/|\\   |",
    "/ \\   |",
    "       |",
    "========="
]


class WordGuessingGame:
    def __init__(self, master):
        self.guess_label = None
        self.hangman_label = None
        self.buttons_frame = None
        self.hangman_image = None
        self.word_label = None
        self.master = master
        self.avl_tree = AVLTree()  # AVL tree to keep track of guessed letters
        self.word = random.choice(words)  # Choose a random word from the list
        self.word_state = ["_" for _ in range(len(self.word))]  # List to keep track of revealed letters
        self.guesses = set()  # Set to keep track of all guesses (for displaying at end)
        self.remaining_guesses = 6  # Number of incorrect guesses before losing
        # Create reset button

        self.reset_button = None

        self.setup_ui()

    def setup_ui(self):
        # Create UI elements
        self.word_label = tk.Label(self.master, text=" ".join(self.word_state))
        self.word_label.pack()
        self.guess_label = tk.Label(self.master, text=f"Remaining guesses: {self.remaining_guesses}")
        self.guess_label.pack()
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack()
        for letter in "abcdefghijklmnopqrstuvwxyz":
            # Create a button for each letter
            btn = tk.Button(self.buttons_frame, text=letter, command=lambda l=letter: self.make_guess(l))
            btn.pack(side=tk.LEFT)
        self.hangman_label = tk.Label(self.master, text="\n".join(hangman[:0]))
        self.hangman_label.pack()
        self.hangman_image = tk.Label(self.master, text="")
        self.hangman_image.pack()
        self.reset_button = tk.Button(self.master, text="New Game", command=self.reset_game, state=tk.DISABLED)

    def make_guess(self, letter):
        # Check if the letter has already been guessed
        if letter in self.avl_tree:
            return
        self.avl_tree.insert(letter)  # Insert the letter into the AVL tree
        self.guesses.add(letter)  # Add the letter to the set of all guesses
        if letter in self.word:
            # If the letter is in the word, reveal all occurrences of the letter
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.word_state[i] = letter
            self.word_label.config(text=" ".join(self.word_state))
            if "_" not in self.word_state:
                # If there are no underscores left in the word, the player has won
                self.end_game(True)
        else:
            # If the letter is not in the word, decrement the remaining guesses and update the UI
            self.remaining_guesses -= 1
            self.guess_label.config(text=f"Remaining guesses: {self.remaining_guesses}")
            if self.remaining_guesses == 0:
                # If there are no more remaining guesses, the player has lost
                self.end_game(False)
                hangman_images = [
                    "  +----+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========="
                ]
                self.hangman_image.config(text=hangman_images[0])
            else:
                # Update the hangman based on the remaining guesses
                hangman_images = [
                    "  +-----+\n  |   |\n      |\n      |\n      |\n      |\n========",
                    "  +-----+\n  |   |\n  O   |\n      |\n      |\n      |\n========",
                    "  +-----+\n  |   |\n  O   |\n  |   |\n      |\n      |\n========",
                    "  +-----+\n  |   |\n  O   |\n /|   |\n      |\n      |\n========",
                    "  +-----+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n========",
                    "  +-----+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n========",
                    "  +-----+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========"
                ]
                self.hangman_image.config(text=hangman_images[6 - self.remaining_guesses])

    def end_game(self, win):
        # Display the solution and all guesses, and disable all buttons
        solution_label = tk.Label(self.master, text=f"The word was: {self.word}")
        solution_label.pack()
        guesses_label = tk.Label(self.master, text=f"Your guesses: {', '.join(self.guesses)}")
        guesses_label.pack()
        self.reset_button.pack()
        self.reset_button.config(state=tk.NORMAL)
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)
        if win:
            # If the player won, display a message
            message_label = tk.Label(self.master, text="Congratulations, you won!")
            message_label.pack()
        else:
            # If the player lost, display a message
            message_label = tk.Label(self.master, text="Sorry, you lost.")
            message_label.pack()

        # Reveal all correct letters in the word
        revealed_word = ""
        for i in range(len(self.word)):
            if self.word[i] in self.avl_tree:
                revealed_word += self.word[i] + " "
            else:
                revealed_word += "_ "
        self.word_label.config(text=revealed_word)

    def reset_game(self):
        self.avl_tree = AVLTree()
        self.word = random.choice(words)
        self.word_state = ["_" for _ in range(len(self.word))]
        self.guesses = set()
        self.remaining_guesses = 6
        # update the text of the labels to their initial values
        self.word_label.config(text=" ".join(self.word_state))
        self.guess_label.config(text=f"Remaining guesses: {self.remaining_guesses}")
        self.hangman_label.config(text="\n".join(hangman[:0]))
        self.hangman_image.config(text="")
        # re-enable the buttons
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.reset_button.pack_forget()
        # remove the labels that were added at the end of the previous game
        for child in self.master.winfo_children():
            if isinstance(child, tk.Label) and child not in [self.word_label, self.guess_label, self.hangman_label,
                                                             self.hangman_image]:
                child.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x350")
    game = WordGuessingGame(root)
    root.mainloop()
