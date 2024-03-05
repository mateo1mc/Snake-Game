import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0
food_refresh_timer = None

# Creating a window screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.bgpic("background.gif")
wn.setup(width=600, height=700)
wn.tracer(0)

# head of the snake
head = turtle.Turtle()
head.shape("circle")
head.color("purple")
head.shapesize(1.2)
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# food in the game
food_colors = ["red", "white"]
current_food_color = "red"
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color(current_food_color)
food.penup()
food.goto(0, 100)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 307)
pen.write("Score : 0  |  High Score : 0", align="center", font=("candara", 24, "bold"))

# Create the message turtle
message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color("white")
message_pen.penup()
message_pen.hideturtle()
message_pen.goto(0, -333)

# Write the initial message
message_pen.write("Press 'w', 'a', 's', 'd' to play the game", align="center", font=("candara", 20, "bold"))

# Function to start the game
def start_game():
    message_pen.clear()
    main_gameplay()

# Assigning key to start the game
wn.listen()
wn.onkeypress(start_game, "w")  # You can use any key you prefer to start the game

segments = []

# assigning key directions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# Function to move
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    elif head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    elif head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

    # Screen wrapping logic
    if head.xcor() > 290:
        head.setx(-290)
    elif head.xcor() < -290:
        head.setx(290)
    elif head.ycor() > 290:
        head.sety(-290)
    elif head.ycor() < -290:
        head.sety(290)

# Function to change food color
def change_food_color():
    global current_food_color
    current_food_color = food_colors[1] if current_food_color == food_colors[0] else food_colors[0]
    food.color(current_food_color)
    wn.ontimer(change_food_color, 150)

# Start changing food color
change_food_color()

# Function to update food's position randomly
def update_food_position():
    global food_refresh_timer
    x = random.randint(-270, 270)
    y = random.randint(-270, 270)
    food.goto(x, y)
    if food_refresh_timer is not None:
        wn.after_cancel(food_refresh_timer)
    food_refresh_timer = wn.ontimer(update_food_position, 20000)  # Call the function again after 20 seconds

# Start updating food position
update_food_position()

# Assigning key directions
def handle_key_press():
    global delay
    global score
    global high_score

    # Buttons that you can play
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")
    wn.onkeypress(go_up, "W")
    wn.onkeypress(go_down, "S")
    wn.onkeypress(go_left, "A")
    wn.onkeypress(go_right, "D")
    wn.onkeypress(go_up, "Up")
    wn.onkeypress(go_down, "Down")
    wn.onkeypress(go_left, "Left")
    wn.onkeypress(go_right, "Right")


# Handle the first key press
handle_key_press()

# Add a global variable to track the game state
is_paused = False

# Function to toggle game state between paused and running
def toggle_pause():
    global is_paused
    is_paused = not is_paused

# Bind the space key to toggle_pause function
wn.onkeypress(toggle_pause, "space")

# Main Gameplay
def main_gameplay():
    global delay
    global score
    global high_score

    while True:
        wn.update()
        
        if is_paused:
            continue

        # Check for collision with wall
        if (
            head.xcor() > 290
            or head.xcor() < -290
            or head.ycor() > 290
            or head.ycor() < -290
        ):
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"

            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = 0.1

            pen.clear()
            pen.write(
                "Score : {}  |  High Score : {} ".format(score, high_score),
                align="center",
                font=("candara", 24, "bold"),
            )

        # Check for collision with food
        if head.distance(food) < 20:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            food.goto(x, y)

            # Add segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("circle")
            new_segment.color("purple")
            new_segment.penup()
            segments.append(new_segment)

            delay -= 0.001
            score += 10
            if score > high_score:
                high_score = score
            pen.clear()
            pen.write(
                "Score : {}  |  High Score : {} ".format(score, high_score),
                align="center",
                font=("candara", 24, "bold"),
            )

        # Move the end segments first in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for collision with the body segments
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "Stop"

                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()

                score = 0
                delay = 0.1
                pen.clear()
                pen.write(
                    "Score : {}  |  High Score : {} ".format(score, high_score),
                    align="center",
                    font=("candara", 24, "bold"),
                )

        time.sleep(delay)

# Start the main gameplay
main_gameplay()

wn.mainloop()
