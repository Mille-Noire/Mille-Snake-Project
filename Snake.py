# Import of Namespaces
import tkinter as tk
import sqlite3 as sqlite
import random

VERSION = "1.0"
COMPILATION_DT = "22.06.2023 15:28"

# Set Colors
MAP_BACKGROUND_COLOR = "#5a7500"
BUTTON_COLOR = "#b1ed00"
BUTTON_ALT_COLOR = "#727181"
BUTTON_ACTIVE_BG_COLOR = "#727181"
BUTTON_ACTIVE_FG_COLOR = "#b1ed00"
FONT_COLOR = "#b1ed00"
WINDOW_BACKGROUND_COLOR = "#202024"
SNAKE_COLOR = "#1e2800"
SNAKE_OUTLINE_COLOR = "#850000"
HEAD_COLOR = "#1e2800"
HEAD_OUTLINE_COLOR = "#b1ed00"
FOOD_COLOR = "#b1ed00"
FOOD_OUTLINE_COLOR = "#bfff00"

FONT = "Trebuchet MS"

# Set game_map Size (w & h have to be divisible by SEGMENT_SIZE)
SEGMENT_SIZE = 20
map_width = 400
map_height = 400

# Set game speed  in Ms (lower = faster)
game_speed = 300

points_multiplier = 1


def set_points_multiplier(speed):
    """Takes in the games speed and defines how many Points are added if the player collects the food"""
    global points_multiplier
    points_multiplier = round(((speed - 600) * -1) / 100)


set_points_multiplier(game_speed)

score = 0
high_scores = []
food_count = []
food_length = 1

# Create Main-Window
main = tk.Tk()
main.geometry("400x250")
main.minsize(400, 250)
main.resizable(False, False)
main.update()
main.title("Hauptmenü")
main.configure(bg=WINDOW_BACKGROUND_COLOR)
main.eval("tk::PlaceWindow . center")


def set_snake_position():
    """Sets the snakes position to a random point inside the map"""
    global snake_x, snake_y
    snake_x = random.randint(0, map_width // SEGMENT_SIZE - 1) * SEGMENT_SIZE
    snake_y = random.randint(0, map_height // SEGMENT_SIZE - 1) * SEGMENT_SIZE
    if snake_x >= map_width - 100:
        set_snake_position()


# Set initial Snake-Coordinates
snake_x = random.randint(0, map_width // SEGMENT_SIZE - 1) * SEGMENT_SIZE
snake_y = random.randint(0, map_height // SEGMENT_SIZE - 1) * SEGMENT_SIZE
if snake_x >= map_width - 100:
    set_snake_position()

# Initialise Snake
snake_segments = [(snake_x, snake_y)]

# Set initial food coordinates
food_x = random.randint(0, map_width // SEGMENT_SIZE - 1) * SEGMENT_SIZE
food_y = random.randint(0, map_height // SEGMENT_SIZE - 1) * SEGMENT_SIZE


def set_food_position():
    """Sets the foods position to a random point inside the map"""
    global food_x, food_y
    food_x = random.randint(0, map_width // SEGMENT_SIZE - 1) * SEGMENT_SIZE
    food_y = random.randint(0, map_height // SEGMENT_SIZE - 1) * SEGMENT_SIZE
    if (food_x, food_y) in snake_segments:
        set_food_position()


# Set initial directions
direction = "Right"
delta_x = SEGMENT_SIZE
delta_y = 0
direction_has_changed = False


def set_direction(new_direction, x, y):
    """Takes the new direction after pressing a button and makes the snake move in the new direction"""
    global direction, delta_x, delta_y, direction_has_changed
    direction = new_direction
    delta_x = x
    delta_y = y
    direction_has_changed = False


game_over = False


def start_new_game():
    """Opens the game-window and initializes a new game"""
    global game_over, game_map
    main.withdraw()
    game_over = False

    def on_window_close():
        """Closes the window and resets the games parameters and sets a new position for snake and food"""
        global snake_segments, score, food_count, food_length
        set_snake_position()
        set_food_position()
        snake_segments = [(snake_x, snake_y)]
        score = 0
        label_score.config(text=f"Punkte: {score}")
        set_direction("Right", SEGMENT_SIZE, 0)
        food_count = []
        food_length = 1
        main.deiconify()
        game_window.destroy()

    def handle_keypress(event):
        """Listens to keydown-events and determines a new direction for the snake"""
        global direction, direction_has_changed, delta_x, delta_y
        if direction_has_changed:
            if (event.keysym == "Up" or event.keysym == "w") and direction != "Down":
                main.after(game_speed, lambda: set_direction("Up", 0, -SEGMENT_SIZE))
            elif (event.keysym == "Down" or event.keysym == "s") and direction != "Up":
                main.after(game_speed, lambda: set_direction("Down", 0, SEGMENT_SIZE))
            elif (event.keysym == "Left" or event.keysym == "a") and direction != "Right":
                main.after(game_speed, lambda: set_direction("Left", -SEGMENT_SIZE, 0))
            elif (event.keysym == "Right" or event.keysym == "d") and direction != "Left":
                main.after(game_speed, lambda: set_direction("Right", SEGMENT_SIZE, 0))
            direction_has_changed = True
        else:
            if (event.keysym == "Up" or event.keysym == "w") and direction != "Down":
                direction = "Up"
                delta_x = 0
                delta_y = -SEGMENT_SIZE
            elif (event.keysym == "Down" or event.keysym == "s") and direction != "Up":
                direction = "Down"
                delta_x = 0
                delta_y = SEGMENT_SIZE
            elif (event.keysym == "Left" or event.keysym == "a") and direction != "Right":
                direction = "Left"
                delta_x = -SEGMENT_SIZE
                delta_y = 0
            elif (event.keysym == "Right" or event.keysym == "d") and direction != "Left":
                direction = "Right"
                delta_x = SEGMENT_SIZE
                delta_y = 0
            direction_has_changed = True

    # Create game_window
    global game_window, score
    game_window = tk.Toplevel(main)
    game_window.geometry(f'{map_width + 60}x{map_height + 60}')
    game_window.minsize(map_width + 60, map_height + 60)
    game_window.resizable(False, False)
    game_window.title("Snake")
    game_window.configure(bg=WINDOW_BACKGROUND_COLOR)
    game_window.protocol("WM_DELETE_WINDOW", on_window_close)
    # Create the window in the middle of the screen
    main.eval(f"tk::PlaceWindow {str(game_window)} center")
    # Create game_map
    game_map = tk.Canvas(game_window, width=map_width, height=map_height)
    game_map.config(bg=WINDOW_BACKGROUND_COLOR, borderwidth=1, relief="sunken", highlightthickness=0)
    game_map.place(relx=0.5, rely=0.5, anchor="center")

    label_score = tk.Label(game_window, text=f"Punkte: {score}", bg=WINDOW_BACKGROUND_COLOR,
                           fg=FONT_COLOR, font=(FONT, 10))
    label_score.pack(padx=25, pady=3, side="top", anchor="w")

    def move_snake():
        """Renders every element on the map, everytime the snake moves"""
        global snake_segments, food_x, food_y, game_over, score, direction_has_changed, food_count, food_length
        direction_has_changed = False

        if len(food_count) > 0:
            for c in range(len(food_count)):
                # Check how many moves where made since the last food was collected
                if c < food_length:
                    food_count[c] += 1
                # Remove counter after usage
                else:
                    food_count.remove(food_count[c])

        # Move Snake on the map
        head_x = snake_segments[0][0] + delta_x
        head_y = snake_segments[0][1] + delta_y

        # Check for collision with game_map
        if head_x < 0 or head_x >= map_width or head_y < 0 or head_y >= map_height:
            game_over = True

        # Check if food is collected
        if head_x == food_x and head_y == food_y:
            # Snake is growing, the last segment isn't removed
            set_food_position()
            score = len(snake_segments) * points_multiplier
            label_score.config(text=f"Punkte: {score}")
            food_length = len(snake_segments)
            food_count.append(0)
        else:
            # Snake isn't growing, the last segment is removed
            snake_segments.pop()

        # Check for collision with self
        if (head_x, head_y) in snake_segments[1:]:
            game_over = True

        # Add new head-segment in moving direction
        snake_segments.insert(0, (head_x, head_y))

        if not game_over:
            # Refresh game_map
            game_map.delete("all")
            game_map.create_rectangle(0, 0, map_width, map_height, fill=MAP_BACKGROUND_COLOR)
            first = True
            # Draw Snake
            for segment in snake_segments:
                if first:
                    # Draw head-segment
                    x, y = segment
                    game_map.create_rectangle(x + 1, y + 1, x + SEGMENT_SIZE - 1, y + SEGMENT_SIZE - 1,
                                              fill=HEAD_COLOR, outline=HEAD_OUTLINE_COLOR)
                    game_map.create_rectangle(x + 8, y + 8, x + 12, y + 12,
                                              fill=SNAKE_COLOR, outline=SNAKE_OUTLINE_COLOR)
                    first = False
                else:
                    # Draw body-segments
                    x, y = segment
                    game_map.create_rectangle(x + 2, y + 2, x + SEGMENT_SIZE - 2, y + SEGMENT_SIZE - 2,
                                              fill=SNAKE_COLOR, outline=SNAKE_OUTLINE_COLOR)
                    game_map.create_rectangle(x + 15, y + 15, x + SEGMENT_SIZE / 4, y + SEGMENT_SIZE / 4,
                                              fill=SNAKE_COLOR, outline=HEAD_OUTLINE_COLOR)
                if len(food_count) > 0:
                    for count in food_count:
                        if count > food_length or count < 1:
                            continue
                        # Draw body-segment with food
                        if count % 2 == 0:
                            x, y = snake_segments[count]
                            game_map.create_rectangle(x + 2, y + 2, x + SEGMENT_SIZE - 2, y + SEGMENT_SIZE - 2,
                                                      fill=SNAKE_COLOR, outline=SNAKE_OUTLINE_COLOR)
                            game_map.create_rectangle(x + 15, y + 15, x + SEGMENT_SIZE / 4, y + SEGMENT_SIZE / 4,
                                                      fill=FOOD_OUTLINE_COLOR, outline=HEAD_OUTLINE_COLOR)
                        else:
                            x, y = snake_segments[count]
                            game_map.create_rectangle(x + 2, y + 2, x + SEGMENT_SIZE - 2, y + SEGMENT_SIZE - 2,
                                                      fill=SNAKE_COLOR, outline=SNAKE_OUTLINE_COLOR)
                            game_map.create_rectangle(x + 15, y + 15, x + SEGMENT_SIZE / 4, y + SEGMENT_SIZE / 4,
                                                      fill=FOOD_COLOR, outline=HEAD_COLOR)
            draw_food(game_map, food_x, food_y)
            # Next move
            main.after(game_speed, move_snake)
        else:
            # Game over
            button_restart = tk.Button(game_window, text="SPIEL NEUSTARTEN",
                                       command=lambda: restart_game(button_restart, button_back),
                                       width=20, bg=BUTTON_COLOR, font=(FONT, 10),
                                       activebackground=BUTTON_ACTIVE_BG_COLOR,
                                       activeforeground=BUTTON_ACTIVE_FG_COLOR)
            button_restart.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
            button_back = tk.Button(game_window, text="ZURÜCK ZUM MENÜ",
                                    command=close_game_window,
                                    width=20, bg=BUTTON_COLOR, font=(FONT, 10),
                                    activebackground=BUTTON_ACTIVE_BG_COLOR,
                                    activeforeground=BUTTON_ACTIVE_FG_COLOR)
            button_back.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            game_map.create_text(map_width / 2, map_height / 2, text="GAME OVER!", fill="white",
                                 font=(FONT, 24), anchor=tk.CENTER)
            game_map.create_text(map_width / 2, map_height / 2 + 30,
                                 text=f"Finaler Punktestand: {score}",
                                 fill="white", font=(FONT, 16), anchor=tk.CENTER)
            set_snake_position()
            snake_segments = [(snake_x, snake_y)]
            set_food_position()
            save_score("Placeholder", score)

    game_window.bind("<KeyPress>", handle_keypress)
    if game_over:
        return
    else:
        move_snake()

    def restart_game(button1, button2):
        """Resets the games parameters and sets a new position for snake and food"""
        global game_map, game_over, score, food_count, food_length
        game_map.delete("all")
        game_over = False
        score = 0
        label_score.config(text=f"Score: {score}")
        set_direction("Right", SEGMENT_SIZE, 0)
        food_count = []
        food_length = 1
        move_snake()
        button1.destroy()
        button2.destroy()

    def close_game_window():
        """Closes the game-window"""
        on_window_close()


def draw_food(gm, fx, fy):
    """Takes the game-map and the food-coordinates and draws a new food-element on the game-map-canvas"""
    gm.create_rectangle(fx, fy, fx + SEGMENT_SIZE, fy + SEGMENT_SIZE, outline=FOOD_OUTLINE_COLOR)
    gm.create_rectangle(fx + 15, fy + 15, fx + SEGMENT_SIZE / 4, fy + SEGMENT_SIZE / 4,
                        fill=FOOD_COLOR, outline=FOOD_OUTLINE_COLOR)


def save_score(name, h_score):
    """Takes the name(str) and score(int) and writes it into the database"""
    connection = None
    try:
        connection = sqlite.connect("G:\\Meine Ablage\\BBS\\LF5_Softwareentwicklung"
                                    "\\Projektarbeit\\Snake\\SnakeScores.db")
    except Exception as e:
        print(e)

    # Create a cursor
    cursor = connection.cursor()

    # Create new table (If no Table exists)
    connection.execute('''CREATE TABLE IF NOT EXISTS scores
                      (name Text, score INT)''')

    new_high_score = [(f"{name}", h_score)]
    cursor.executemany('''
                    INSERT INTO scores (name, score) VALUES(?, ?)
                    ''', new_high_score)
    connection.commit()

    # Close database objects
    cursor.close()
    connection.close()


def load_scores():
    """Loads the scores from the database"""
    global high_scores
    # Connect to (or create new) database
    connection = None
    try:
        connection = sqlite.connect("G:\\Meine Ablage\\BBS\\LF5_Softwareentwicklung"
                                    "\\Projektarbeit\\Snake\\SnakeScores.db")
    except Exception as e:
        print(e)

    # Create a cursor
    cursor = connection.cursor()

    # Create new table (If no Table exists)
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                          (name Text, score INT)''')
    connection.commit()

    # Read all rows in the scores table
    cursor.execute("SELECT * FROM scores")
    rows = cursor.fetchall()

    for row in rows:
        high_scores.append(row)

    # Close database objects
    cursor.close()
    connection.close()


def open_scores():
    """Opens the scores-window"""
    global high_scores
    p = 0
    main.withdraw()
    # Create settings-Window
    score_window = tk.Toplevel(main)
    load_scores()

    if high_scores:
        high_score = ""
        for s in high_scores:
            if p < 1:
                p += 1
                high_score += f"{p}: {s}"
            else:
                p += 1
                high_score += f"\n{p}: {s}"
    else:
        high_score = "Noch keine HIGH SCORES vorhanden."

    def on_window_close():
        """Closes the scores-window"""
        score_window.destroy()
        main.deiconify()

    score_window.geometry('400x250')
    score_window.minsize(400, 250)
    score_window.resizable(False, False)
    score_window.title("HIGH SCORES")
    score_window.configure(bg=WINDOW_BACKGROUND_COLOR)
    score_window.protocol("WM_DELETE_WINDOW", on_window_close)
    main.eval(f"tk::PlaceWindow {str(score_window)} center")
    button_return = tk.Button(score_window, text="↲", fg=WINDOW_BACKGROUND_COLOR,
                              command=on_window_close,
                              width=2, height=1, bg=BUTTON_ALT_COLOR,
                              activebackground=BUTTON_ACTIVE_BG_COLOR,
                              activeforeground=BUTTON_ACTIVE_FG_COLOR)
    button_return.grid(column=0, row=0, sticky=tk.W, padx=15, pady=15)
    label_high_score = tk.Label(score_window, text=high_score, bg=WINDOW_BACKGROUND_COLOR,
                                fg=FONT_COLOR, font=(FONT, 10))
    label_high_score.grid(column=0, row=1, sticky=tk.W, padx=50)


def open_settings():
    """Opens the settings-window"""
    global game_speed
    main.withdraw()
    speeds = ("1", "2", "3", "4", "5")

    def on_window_close():
        """Closes the settings-window"""
        settings_window.destroy()
        main.deiconify()

    def option_changed(*args):
        """Displays the new game-speed and sets the new points-multiplier accordingly"""
        global game_speed
        temp = int(game_speed_var.get())
        game_speed = (temp - 6) * -100
        set_points_multiplier(game_speed)

    # Create settings-Window
    settings_window = tk.Toplevel(main)
    settings_window.geometry('300x200')
    settings_window.minsize(300, 200)
    settings_window.resizable(False, False)
    settings_window.title("Settings")
    settings_window.configure(bg=WINDOW_BACKGROUND_COLOR)
    settings_window.protocol("WM_DELETE_WINDOW", on_window_close)
    main.eval(f"tk::PlaceWindow {str(settings_window)} center")
    button_return = tk.Button(settings_window, text="↲", fg=WINDOW_BACKGROUND_COLOR,
                              command=on_window_close,
                              width=2, height=1, bg=BUTTON_ALT_COLOR,
                              activebackground=BUTTON_ACTIVE_BG_COLOR,
                              activeforeground=BUTTON_ACTIVE_FG_COLOR)
    button_return.grid(column=0, row=0, sticky=tk.W, padx=15, pady=15)
    game_speed_var = tk.StringVar(settings_window)
    game_speed_var.set(f"{round(((game_speed - 600) * -1) / 100)}")
    game_speed_menu = tk.OptionMenu(settings_window, game_speed_var, *speeds,
                                    command=option_changed)
    game_speed_menu.config(bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR, activebackground=WINDOW_BACKGROUND_COLOR,
                           activeforeground=FONT_COLOR, borderwidth=5, relief="raised", highlightthickness=0)
    game_speed_menu["menu"].config(bg=WINDOW_BACKGROUND_COLOR, fg=FONT_COLOR)
    game_speed_menu.grid(column=1, row=1, sticky=tk.W, padx=0)
    label_game_speed = tk.Label(settings_window, text="Geschwindigkeit: ", bg=WINDOW_BACKGROUND_COLOR,
                                fg=FONT_COLOR, font=(FONT, 10))
    label_game_speed.grid(column=0, row=1, sticky=tk.W, padx=50)


def quit_game():
    """Closes the main-window"""
    main.destroy()


# Button creation & placement
button_start = tk.Button(main, text="NEUES SPIEL",
                         command=start_new_game,
                         width=20, bg=BUTTON_COLOR, font=(FONT, 10),
                         activebackground=BUTTON_ACTIVE_BG_COLOR,
                         activeforeground=BUTTON_ACTIVE_FG_COLOR)
button_start.place(relx=0.5, rely=0.2, anchor="center")
button_scores = tk.Button(main, text="HIGH SCORES",
                          command=open_scores,
                          width=20, bg=BUTTON_COLOR, font=(FONT, 10),
                          activebackground=BUTTON_ACTIVE_BG_COLOR,
                          activeforeground=BUTTON_ACTIVE_FG_COLOR)
button_scores.place(relx=0.5, rely=0.5, anchor="center")
button_end = tk.Button(main, text="BEENDEN",
                       command=quit_game,
                       width=20, bg=BUTTON_COLOR, font=(FONT, 10),
                       activebackground=BUTTON_ACTIVE_BG_COLOR,
                       activeforeground=BUTTON_ACTIVE_FG_COLOR)
button_end.place(relx=0.5, rely=0.8, anchor="center")
button_settings = tk.Button(main, text="⚙", fg=WINDOW_BACKGROUND_COLOR,
                            command=open_settings,
                            width=2, height=1, bg=BUTTON_ALT_COLOR,
                            activebackground=BUTTON_ACTIVE_BG_COLOR,
                            activeforeground=BUTTON_ACTIVE_FG_COLOR)
button_settings.grid(column=0, row=0, sticky=tk.W, padx=15, pady=15)

# Creation & placement of Versions-Label
label_version = tk.Label(main, text=f"Version: {VERSION}", bg=WINDOW_BACKGROUND_COLOR,
                         fg=FONT_COLOR, font=(FONT, 8))
label_version.place(relx=0.98, rely=0.95, anchor="se")
label_compiled = tk.Label(main, text=f"Letzte Änderung: {COMPILATION_DT}", bg=WINDOW_BACKGROUND_COLOR,
                          fg=FONT_COLOR, font=(FONT, 8))
label_compiled.place(relx=0.02, rely=0.95, anchor="sw")

# Start of Eventloop
main.mainloop()
