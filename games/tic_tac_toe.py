import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg='#f0f0f0')
        self.board = [''] * 9
        self.current_player = 'X'
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s turn", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        self.turn_label.pack(pady=10)

        self.board_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.board_frame.pack()

        for i in range(9):
            button = tk.Button(self.board_frame, text='', font=('Arial', 24, 'bold'), width=5, height=2,
                               bg='white', relief='raised', command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        self.reset_button = tk.Button(self.root, text="Reset Game", font=('Arial', 12), bg='#4CAF50', fg='white',
                                      command=self.reset_game)
        self.reset_button.pack(pady=10)

    def make_move(self, index):
        if self.board[index] == '':
            self.board[index] = self.current_player
            color = 'blue' if self.current_player == 'X' else 'red'
            self.buttons[index].config(text=self.current_player, fg=color)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif '' not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.turn_label.config(text=f"Player {self.current_player}'s turn")

    def check_winner(self):
        win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != '':
                return True
        return False

    def reset_game(self):
        self.board = [''] * 9
        self.current_player = 'X'
        self.turn_label.config(text=f"Player {self.current_player}'s turn")
        for button in self.buttons:
            button.config(text='', fg='black')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()