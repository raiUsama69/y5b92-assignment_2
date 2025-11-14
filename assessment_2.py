# I acknowledge the use of ChatGPT (GPT-5.1, OpenAI, https://chat.openai.com)
# to help create and refine the code in this file.

import tkinter as tk
import random

class ClickGame:
    def __init__(self, root):
        self.dark_mode = False
        self.paused = False
        # Load high score from file
        self.highscore = 0
        try:
            with open("highscore.txt", "r") as f:
                self.highscore = int(f.read().strip())
        except:
            self.highscore = 0

            
        self.highscore_label = tk.Label(root, text=f"High Score: {self.highscore}", font=("Arial", 16))
        self.highscore_label.pack(pady=5)

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

        dark_mode_button = tk.Button(button_frame, text="Dark Mode", command=lambda: self.toggle_dark_mode())
        dark_mode_button.grid(row=0, column=2, padx=10)

        pause_button = tk.Button(button_frame, text="Pause", command=lambda: self.pause_game())
        pause_button.grid(row=0, column=3, padx=10)

        resume_button = tk.Button(button_frame, text="Resume", command=lambda: self.resume_game())
        resume_button.grid(row=0, column=4, padx=10)




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
        if self.paused:
            return

        x = random.randint(0, 350)
        y = random.randint(0, 250)
        self.canvas.coords(self.target, x, y, x + 40, y + 40)

        if self.time_left > 0:
            self.root.after(700, self.move_target)

    def countdown(self):
        if self.paused:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time Left: {self.time_left}")
            self.root.after(1000, self.countdown)
        else:
            self.canvas.unbind("<Button-1>")
            self.game_over()


    def game_over(self):
        # Check and update high score
        if self.score > self.highscore:
            self.highscore = self.score
            self.highscore_label.config(text=f"High Score: {self.highscore}")

            # Save to file
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))

        self.canvas.create_text(
            200, 150,
            text=f"Game Over!\nFinal Score: {self.score}",
            font=("Arial", 20),
            fill="blue"
        )

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            # Dark mode colours
            bg = "#222222"
            fg = "white"
            canvas_bg = "#333333"
            target_color = "yellow"
        else:
            # Light mode colours
            bg = "white"
            fg = "black"
            canvas_bg = "white"
            target_color = "red"

        # Apply to window
        self.root.config(bg=bg)

        # Labels
        self.score_label.config(bg=bg, fg=fg)
        self.time_label.config(bg=bg, fg=fg)

        # Canvas
        self.canvas.config(bg=canvas_bg)

        # Change target colour
        self.canvas.itemconfig(self.target, fill=target_color)


    def pause_game(self):
        self.paused = True

    def resume_game(self):
        if self.paused:
            self.paused = False
            # Restart timers / movement from current state
            self.move_target()
            self.countdown()



# I will add sound functionality later

if __name__ == "__main__":
    
    root = tk.Tk()
    ClickGame(root)
    root.mainloop()
