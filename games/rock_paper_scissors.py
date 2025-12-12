import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.configure(bg='#e8f5e8')
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.user_score = 0
        self.comp_score = 0
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Rock Paper Scissors", font=('Arial', 18, 'bold'), bg='#e8f5e8', fg='#2e7d32')
        self.title_label.pack(pady=10)

        self.label = tk.Label(self.root, text="Choose your move:", font=('Arial', 14), bg='#e8f5e8')
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(self.root, bg='#e8f5e8')
        self.button_frame.pack()

        for choice in self.choices:
            button = tk.Button(self.button_frame, text=choice, font=('Arial', 12, 'bold'), width=12, height=2,
                               bg='#4CAF50', fg='white', relief='raised', command=lambda c=choice: self.play(c))
            button.pack(side=tk.LEFT, padx=10, pady=5)

        self.score_label = tk.Label(self.root, text="Score: You 0 - 0 Computer", font=('Arial', 14, 'bold'), bg='#e8f5e8', fg='#1b5e20')
        self.score_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=('Arial', 12), bg='#e8f5e8', fg='#d32f2f')
        self.result_label.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reset Score", font=('Arial', 12), bg='#ff9800', fg='white',
                                      command=self.reset_score)
        self.reset_button.pack(pady=10)

    def play(self, user_choice):
        comp_choice = random.choice(self.choices)
        result = self.determine_winner(user_choice, comp_choice)
        self.result_label.config(text=f"You: {user_choice} vs Computer: {comp_choice}\n{result}")
        self.update_score(result)

    def determine_winner(self, user, comp):
        if user == comp:
            return "It's a tie!"
        elif (user == 'Rock' and comp == 'Scissors') or \
             (user == 'Paper' and comp == 'Rock') or \
             (user == 'Scissors' and comp == 'Paper'):
            return "You win!"
        else:
            return "Computer wins!"

    def update_score(self, result):
        if "You win" in result:
            self.user_score += 1
        elif "Computer wins" in result:
            self.comp_score += 1
        self.score_label.config(text=f"Score: You {self.user_score} - {self.comp_score} Computer")

    def reset_score(self):
        self.user_score = 0
        self.comp_score = 0
        self.score_label.config(text="Score: You 0 - 0 Computer")
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()