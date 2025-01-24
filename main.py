import numpy as np
from PIL import ImageGrab
import cv2
import keyboard
import time
from pynput import mouse
from screeninfo import get_monitors

def get_mouse_click_coordinates():
    coordinates = []

    def on_click(x, y, button, pressed):
        if pressed:
            # Add the coordinates to the list
            coordinates.append((x, y))
            # Stop the listener after capturing the click
            print(f'{x}, {y}')
            return False

    # Start listening for mouse events
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    return coordinates

# Get display width and height
monitor = get_monitors()[0]
display_width = monitor.width
display_height = monitor.height

# Game variables
init = False  # State of game
sleep_time = 0.25  # Wait time before next operation
cycle = 0  # Number of iterations
game_dimension = [0, 0, display_width, display_height]  # Coordinates of region of interest (ROI)
left_point = get_mouse_click_coordinates()  # Position of man's head on left (in ROI)
right_point = get_mouse_click_coordinates()  # Position of man's head on right (in ROI)
dir_man = 0  # Boolean variable to represent direction 0: left, 1: right

# Function to change direction
def toggle_direction(direction):
    return 1 if direction == 0 else 0

# Function to cut tree
def cut_tree(direction):
    keyboard.press_and_release('left' if direction == 0 else 'right')

# Function to check if branch is right above the head
def branch_about_to_hit(direction, left_point, right_point, screen):
    point = left_point if direction == 0 else right_point
    return screen[point[1], point[0]] < 200

# Main game loop
img = None
screen = None

def update_values():
    global img
    global screen
    img = ImageGrab.grab(bbox=game_dimension)
    screen = np.array(img.copy())
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

while True:
    # Fail-safe to kill the bot
    if keyboard.is_pressed('down'):
        break

    # Run only if up key is pressed
    if not keyboard.is_pressed('up'):
        break

    # Initialize position with position left
    if not init:
        print('GAME STARTED')
        keyboard.press_and_release('left')
        time.sleep(sleep_time)
        init = True
        cycle += 1
        continue

    # Capture screen and convert into 1D array (gray)
    update_values()

    # Change direction or cut tree
    branch_hit = branch_about_to_hit(dir_man, left_point, right_point, screen)
    if branch_hit:
        print(f'Branch about to hit on {("left" if dir_man == 0 else "right")} side!')
        dir_man = toggle_direction(dir_man)
        cut_tree(dir_man)
        print(f'Toggling direction, now it is: {("left" if dir_man == 0 else "right")}')
        time.sleep(sleep_time)
    else:
        cut_tree(dir_man)
        time.sleep(sleep_time)

    cycle += 1