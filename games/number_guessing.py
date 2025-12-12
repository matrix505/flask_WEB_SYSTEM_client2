import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessing:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.configure(bg='#fff3e0')
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_guess = 1
        self.max_guess = 100
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Number Guessing Game", font=('Arial', 18, 'bold'), bg='#fff3e0', fg='#e65100')
        self.title_label.pack(pady=10)

        self.label = tk.Label(self.root, text=f"Guess a number between {self.min_guess} and {self.max_guess}:", font=('Arial', 14), bg='#fff3e0')
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=('Arial', 12), width=20)
        self.entry.pack()

        self.button_frame = tk.Frame(self.root, bg='#fff3e0')
        self.button_frame.pack(pady=5)

        self.guess_button = tk.Button(self.button_frame, text="Guess", font=('Arial', 12, 'bold'), bg='#2196F3', fg='white',
                                      command=self.guess)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        self.new_game_button = tk.Button(self.button_frame, text="New Game", font=('Arial', 12), bg='#4CAF50', fg='white',
                                         command=self.reset_game)
        self.new_game_button.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(self.root, text="", font=('Arial', 12, 'bold'), bg='#fff3e0', fg='#d32f2f')
        self.result_label.pack(pady=5)

        self.attempts_label = tk.Label(self.root, text="Attempts: 0", font=('Arial', 14), bg='#fff3e0', fg='#1b5e20')
        self.attempts_label.pack(pady=5)

    def guess(self):
        try:
            guess = int(self.entry.get())
            if guess < self.min_guess or guess > self.max_guess:
                self.result_label.config(text=f"Please enter a number between {self.min_guess} and {self.max_guess}.")
                return
            self.attempts += 1
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
            if guess < self.secret_number:
                self.min_guess = guess + 1
                self.result_label.config(text="Too low!")
                self.label.config(text=f"Guess a number between {self.min_guess} and {self.max_guess}:")
            elif guess > self.secret_number:
                self.max_guess = guess - 1
                self.result_label.config(text="Too high!")
                self.label.config(text=f"Guess a number between {self.min_guess} and {self.max_guess}:")
            else:
                messagebox.showinfo("Congratulations!", f"You guessed it in {self.attempts} attempts!")
                self.reset_game()
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_guess = 1
        self.max_guess = 100
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="")
        self.label.config(text=f"Guess a number between {self.min_guess} and {self.max_guess}:")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessing(root)
    root.mainloop()