import pyautogui
import time

# Function to print mouse position to console every 3 seconds
def print_mouse_position():
    while True:
        x, y = pyautogui.position()  # Get current mouse position
        print(f"Mouse position: x = {x}, y = {y}", end='\r')  # Overwrite the previous line
        time.sleep(3)  # Wait for 3 seconds before updating

# Start printing mouse position every 3 seconds
print_mouse_position()
