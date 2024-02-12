import pyautogui
import keyboard

def print_mouse_coordinates(e):
    x, y = pyautogui.position()
    print(f"Mouse Coordinates: {x},{y}")

# Register the callback function for the space key
keyboard.on_press_key('space', print_mouse_coordinates)

# Keep the script running
keyboard.wait('esc')  # You can change 'esc' to any key you want to use for exiting the script
