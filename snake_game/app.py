# Author: Sam Yong Zhi
# Purpose: Coding artefact for SMU MITB AI track application
# Description: Running the script will open up the classic snake game. The game is created using Python 3.8 and using Tkinter for GUI and Pillow (PIL fork) for opening/loading the images.
# Remarks: Following a video guide online, I have written the codes from scratch and added my own comments.
# URL of the video is https://www.youtube.com/watch?v=yB1aSBM8fvI


import tkinter as tk
from PIL import Image, ImageTk
from random import randint

# move_per_second can be changed to change the speed of the game
moves_per_second = 15

# constants
MOVE_INCREMENT = 20
GAME_SPEED = 1000 // moves_per_second

# Create Snake class which inherits tk.Canvas followed by inserting the game logics/methods
class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=600, height=620, background="black", highlightthickness=0
        )

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()

        self.score = 0
        self.direction = "Right"

        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()
        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)

    # open or "load" the images used in the game
    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    # place the images into the application window
    def create_objects(self):
        # score display
        self.create_text(
            100, 12, text=f"Score {self.score} (speed: {moves_per_second})", tag="score", fill="#fff", font=("TkDefaultFont",14)
        )

        # position of snake
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position,
                              image=self.snake_body, tag="snake")
        # position of food
        self.create_image(*self.food_position, image=self.food, tag="food")

        # drawing the boundaries
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    # method for moving the snake
    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        # moving the head of the snake and removing the "tail" of the snake
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        # updating the canvas using the tags
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position) # updates the element to a new set of coordinates

    # method for perfoming actions
    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return # if true, game will stop here

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    # method for checking collisions against borders or the body of the snake
    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return(
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    # method for key press while preventing the player from reversing the snake immediately
    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites):
            self.direction = new_direction

    # if head of snake is equal to position of food, we add to the "tail" of snake
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            # increase game speed after every 5 points interval
            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed: {moves_per_second})", tag="score")

    # setting new food position and ensuring food does not get created at spaces already occupied by the body of the snake
    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    # end game screen
    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=("TkDefaultFont", 24)
        )

# create main application window
root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

# instance of Snake class
board = Snake()

# putting the canvas into the application window
board.pack()

# run application
root.mainloop()
