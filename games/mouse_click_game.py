import tkinter as tk
from tkinter import messagebox, ttk
import time
import json
import os

class MouseClickGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Click Challenge")
        self.root.configure(bg='#e91e63')
        self.root.geometry("500x600")

        # Game variables
        self.time_limit = 10  # seconds
        self.remaining_time = self.time_limit
        self.click_count = 0
        self.game_running = False
        self.highscore = self.load_highscore()

        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="Mouse Click Challenge", font=('Arial', 20, 'bold'),
                                   bg='#e91e63', fg='white')
        self.title_label.pack(pady=20)

        # Highscore display
        self.highscore_label = tk.Label(self.root, text=f"Highscore: {self.highscore} clicks",
                                       font=('Arial', 14), bg='#e91e63', fg='yellow')
        self.highscore_label.pack(pady=5)

        # Time display
        self.time_label = tk.Label(self.root, text=f"Time: {self.remaining_time}s",
                                  font=('Arial', 16, 'bold'), bg='#e91e63', fg='white')
        self.time_label.pack(pady=10)

        # Click counter
        self.click_label = tk.Label(self.root, text="Clicks: 0", font=('Arial', 18, 'bold'),
                                   bg='#e91e63', fg='white')
        self.click_label.pack(pady=10)

        # Click button (large and prominent)
        self.click_button = tk.Button(self.root, text="CLICK ME!", font=('Arial', 24, 'bold'),
                                     bg='#ffeb3b', fg='#e91e63', width=15, height=3,
                                     command=self.register_click, state='disabled')
        self.click_button.pack(pady=20)

        # Control buttons
        self.button_frame = tk.Frame(self.root, bg='#e91e63')
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start Game", font=('Arial', 12, 'bold'),
                                     bg='#4caf50', fg='white', command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset Highscore", font=('Arial', 12),
                                     bg='#f44336', fg='white', command=self.reset_highscore)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Instructions
        self.instruction_label = tk.Label(self.root,
                                         text="Click the button as fast as you can!\nGame lasts 10 seconds.",
                                         font=('Arial', 10), bg='#e91e63', fg='white', justify='center')
        self.instruction_label.pack(pady=10)

        # Progress bar for time remaining
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.progress['value'] = 100

    def start_game(self):
        if self.game_running:
            return

        self.game_running = True
        self.click_count = 0
        self.remaining_time = self.time_limit
        self.click_label.config(text="Clicks: 0")
        self.time_label.config(text=f"Time: {self.remaining_time}s")
        self.click_button.config(state='normal', bg='#ffeb3b')
        self.start_button.config(state='disabled')
        self.progress['value'] = 100

        self.update_timer()

    def update_timer(self):
        if not self.game_running:
            return

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"Time: {self.remaining_time}s")
            self.progress['value'] = (self.remaining_time / self.time_limit) * 100
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def register_click(self):
        if not self.game_running:
            return

        self.click_count += 1
        self.click_label.config(text=f"Clicks: {self.click_count}")

        # Visual feedback
        self.click_button.config(bg='#ffc107')
        self.root.after(50, lambda: self.click_button.config(bg='#ffeb3b') if self.game_running else None)

    def end_game(self):
        self.game_running = False
        self.click_button.config(state='disabled', bg='#cccccc')
        self.start_button.config(state='normal')

        # Check for highscore
        if self.click_count > self.highscore:
            self.highscore = self.click_count
            self.save_highscore()
            self.highscore_label.config(text=f"Highscore: {self.highscore} clicks")
            messagebox.showinfo("New Highscore!", f"Congratulations!\nNew highscore: {self.click_count} clicks!")
        else:
            messagebox.showinfo("Time's Up!", f"Game Over!\nYou clicked {self.click_count} times.\nHighscore: {self.highscore} clicks")

    def load_highscore(self):
        try:
            if os.path.exists('click_highscore.json'):
                with open('click_highscore.json', 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
        except:
            pass
        return 0

    def save_highscore(self):
        try:
            with open('click_highscore.json', 'w') as f:
                json.dump({'highscore': self.highscore}, f)
        except:
            pass

    def reset_highscore(self):
        if messagebox.askyesno("Reset Highscore", "Are you sure you want to reset the highscore to 0?"):
            self.highscore = 0
            self.save_highscore()
            self.highscore_label.config(text=f"Highscore: {self.highscore} clicks")

if __name__ == "__main__":
    root = tk.Tk()
    game = MouseClickGame(root)
    root.mainloop()