import tkinter as tk
import random

class SimplePong:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Pong")
        self.root.configure(bg='#1a1a1a')
        self.score = 0
        self.canvas = tk.Canvas(root, width=400, height=300, bg='black', highlightthickness=0)
        self.canvas.pack(pady=10)

        self.paddle = self.canvas.create_rectangle(350, 250, 370, 300, fill='#00ff00', outline='#00ff00')
        self.ball = self.canvas.create_oval(190, 140, 210, 160, fill='#ff0000', outline='#ff0000')

        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = random.choice([-4, 4])
        self.paddle_dy = 0

        self.score_label = tk.Label(root, text="Score: 0", font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='white')
        self.score_label.pack()

        self.instructions = tk.Label(root, text="Use Up/Down arrows to move paddle", font=('Arial', 10), bg='#1a1a1a', fg='gray')
        self.instructions.pack(pady=5)

        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)

        self.game_loop()

    def key_press(self, event):
        if event.keysym == 'Up':
            self.paddle_dy = -6
        elif event.keysym == 'Down':
            self.paddle_dy = 6

    def key_release(self, event):
        if event.keysym in ['Up', 'Down']:
            self.paddle_dy = 0

    def game_loop(self):
        self.move_ball()
        self.move_paddle()
        self.root.after(30, self.game_loop)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_pos = self.canvas.coords(self.ball)
        if ball_pos[1] <= 0 or ball_pos[3] >= 300:
            self.ball_dy = -self.ball_dy
        if ball_pos[0] <= 0:
            self.ball_dx = -self.ball_dx
        if ball_pos[2] >= 400:
            # Miss
            self.canvas.coords(self.ball, 190, 140, 210, 160)
            self.ball_dx = random.choice([-4, 4])
            self.ball_dy = random.choice([-4, 4])
            self.score = max(0, self.score - 1)
            self.score_label.config(text=f"Score: {self.score}")

        paddle_pos = self.canvas.coords(self.paddle)
        if (ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2] and
            ball_pos[3] >= paddle_pos[1] and ball_pos[1] <= paddle_pos[3]):
            self.ball_dx = -self.ball_dx
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

    def move_paddle(self):
        paddle_pos = self.canvas.coords(self.paddle)
        if (paddle_pos[1] + self.paddle_dy >= 0 and paddle_pos[3] + self.paddle_dy <= 300):
            self.canvas.move(self.paddle, 0, self.paddle_dy)

if __name__ == "__main__":
    root = tk.Tk()
    game = SimplePong(root)
    root.mainloop()