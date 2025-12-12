import tkinter as tk
from tkinter import messagebox
import random
import time

class MemoryMatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match")
        self.root.configure(bg='#e3f2fd')
        self.cards = list(range(1, 9)) * 2
        random.shuffle(self.cards)
        self.buttons = []
        self.flipped = []
        self.matched = []
        self.start_time = time.time()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Memory Match", font=('Arial', 18, 'bold'), bg='#e3f2fd', fg='#1976d2')
        self.title_label.pack(pady=10)

        self.board_frame = tk.Frame(self.root, bg='#e3f2fd')
        self.board_frame.pack()

        for i in range(16):
            button = tk.Button(self.board_frame, text='', font=('Arial', 16, 'bold'), width=6, height=3,
                               bg='#bbdefb', relief='raised', command=lambda i=i: self.flip_card(i))
            button.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(button)

        self.time_label = tk.Label(self.root, text="Time: 0s", font=('Arial', 14), bg='#e3f2fd', fg='#388e3c')
        self.time_label.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="New Game", font=('Arial', 12), bg='#4CAF50', fg='white',
                                      command=self.reset_game)
        self.reset_button.pack(pady=10)

        self.update_time()

    def update_time(self):
        elapsed = int(time.time() - self.start_time)
        self.time_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_time)

    def flip_card(self, index):
        if index in self.flipped or index in self.matched:
            return
        self.buttons[index].config(text=str(self.cards[index]), bg='#fff9c4')
        self.flipped.append(index)
        if len(self.flipped) == 2:
            self.root.after(1000, self.check_match)

    def check_match(self):
        i1, i2 = self.flipped
        if self.cards[i1] == self.cards[i2]:
            self.matched.extend(self.flipped)
            for idx in self.flipped:
                self.buttons[idx].config(bg='#c8e6c9', state='disabled')
            if len(self.matched) == 16:
                elapsed = int(time.time() - self.start_time)
                messagebox.showinfo("Congratulations!", f"You matched all cards in {elapsed} seconds!")
        else:
            for idx in self.flipped:
                self.buttons[idx].config(text='', bg='#bbdefb')
        self.flipped = []

    def reset_game(self):
        self.cards = list(range(1, 9)) * 2
        random.shuffle(self.cards)
        self.flipped = []
        self.matched = []
        self.start_time = time.time()
        for button in self.buttons:
            button.config(text='', bg='#bbdefb', state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryMatch(root)
    root.mainloop()