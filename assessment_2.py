# I acknowledge the use of ChatGPT (GPT-5.1, OpenAI, https://chat.openai.com)
# to help create and refine the code in this file.

import tkinter as tk
import random

class ClickGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Click the Target Game")

        self.score = 0
        self.time_left = 20

        # Score label
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

        # Time label
        self.time_label = tk.Label(root, text=f"Time Left: {self.time_left}", font=("Arial", 16))
        self.time_label.pack(pady=10)

        # Canvas where the player clicks the target
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.canvas.pack()
        # Restart & Quit buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        restart_button = tk.Button(button_frame, text="Restart Game", command=lambda: self.restart_game())
        restart_button.grid(row=0, column=0, padx=10)

        quit_button = tk.Button(button_frame, text="Quit", command=root.destroy)
        quit_button.grid(row=0, column=1, padx=10)


        # Target
        self.target = self.canvas.create_oval(10, 10, 50, 50, fill="red")

        # Bind mouse click
        self.canvas.tag_bind(self.target, "<Button-1>", self.hit_target)

        # Start timers
        self.move_target()
        self.countdown()

    def hit_target(self, event):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def restart_game(self):
    # Reset score and time
        self.score = 0
        self.time_left = 20

        # Update labels
        self.score_label.config(text=f"Score: {self.score}")
        self.time_label.config(text=f"Time Left: {self.time_left}")

        # Re-enable clicking
        self.canvas.tag_bind(self.target, "<Button-1>", self.hit_target)

        # Clear "Game Over" text if present
        self.canvas.delete("all")
        # Recreate target
        self.target = self.canvas.create_oval(10, 10, 50, 50, fill="red")
        self.canvas.tag_bind(self.target, "<Button-1>", self.hit_target)

        # Restart movement + timer
        self.move_target()
        self.countdown()
    

    def move_target(self):
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        self.canvas.coords(self.target, x, y, x + 40, y + 40)

        if self.time_left > 0:
            self.root.after(700, self.move_target)

    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time Left: {self.time_left}")
            self.root.after(1000, self.countdown)
        else:
            self.canvas.unbind("<Button-1>")
            self.game_over()

    def game_over(self):
        self.canvas.create_text(
            200, 150,
            text=f"Game Over!\nFinal Score: {self.score}",
            font=("Arial", 20),
            fill="blue"
        )

if __name__ == "__main__":
    root = tk.Tk()
    ClickGame(root)
    root.mainloop()
