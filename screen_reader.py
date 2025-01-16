import pytesseract
import pyautogui
from PIL import Image, ImageEnhance
import keyboard
import threading
import time

# Make sure Tesseract is correctly configured
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path if necessary

# Initialize global variables
market_price_reading = False
stop_thread = False

# Path for the output txt file
output_txt_file = "market_prices.txt"

screen_width, screen_height = pyautogui.size()
print(f"Screen size: {screen_width}x{screen_height}")

# Clear contents of the text file upon app start
open(output_txt_file, "w").write("") 

# Function to get user input for tier, enchantment, and quality
def get_user_input():
    print("\n--- Item Selection ---")
    tier = input("Enter item tier (4-8): ")
    while tier not in ["4", "5", "6", "7", "8"]:
        print("Invalid input. Please enter a number between 4 and 8.")
        tier = input("Enter item tier (4-8): ")

    enchantment = input("Enter enchantment level (0-4): ")
    while enchantment not in ["0", "1", "2", "3", "4"]:
        print("Invalid input. Please enter a number between 0 and 4.")
        enchantment = input("Enter enchantment level (0-4): ")

    quality = input("Enter item quality (0-4): ")
    while quality not in ["0", "1", "2", "3", "4"]:
        print("Invalid input. Please enter a number between 0 and 5.")
        quality = input("Enter item quality (0-4): ")

    print(f"\nSelected Tier: {tier}, Enchantment: {enchantment}, Quality: {quality}")

    # Append the user input to the output file
    with open(output_txt_file, "a") as file:
        file.write(f"Item Details - Tier: {tier}, Enchantment: {enchantment}, Quality: {quality}\n")

    return tier, enchantment, quality

# Function to capture market prices using Tesseract
def capture_market_prices():
    try:
        # Capture two different regions of the screen
        region_1 = (666, 453, 200, 500)  # Define first region (x, y, width, height)
        region_2 = (1017, 450, 100, 500)  # Define second region (x, y, width, height)

        # Capture the first region
        screenshot_1 = pyautogui.screenshot(region=region_1)
        enhanced_image_1 = enhance_image(screenshot_1)
        
        enhanced_image_1.save("region_1_image.png")

        # Capture the second region
        screenshot_2 = pyautogui.screenshot(region=region_2)
        enhanced_image_2 = enhance_image(screenshot_2)
        
        enhanced_image_2.save("region_2_image.png")

        # Use pytesseract to extract text from both regions
        text_1 = pytesseract.image_to_string(enhanced_image_1, lang='eng').strip()
        text_2 = pytesseract.image_to_string(enhanced_image_2, lang='eng').strip()

        print(f"Captured text 1: {text_1}")  # Debug print
        print(f"Captured text 2: {text_2}")  # Debug print

        # If there is any text extracted, process it
        if text_1 or text_2:
            with open(output_txt_file, "a") as file:
                if text_1:
                    file.write(f"{text_1}\n")
                if text_2:
                    file.write(f"{text_2}\n")

        return text_1, text_2
    except Exception as e:
        print(f"Error in capture_market_prices: {e}")
        return "", ""

# Function to enhance the image (optional)
def enhance_image(image):
    # Convert to grayscale (useful for OCR)
    gray_image = image.convert('L')

    # Enhance the image (optional, adjust as needed)
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)  # You can change the factor

    return enhanced_image

# Function to toggle market price reading
def market_price_reader():
    global stop_thread
    while not stop_thread:
        if market_price_reading:
            market_prices = capture_market_prices()
            if market_prices:
                print(f"Market Prices captured: {market_prices}")
            else:
                print("No market data found.")
        time.sleep(3)  # Ensure it checks every 3 seconds

# Function to listen for keyboard inputs (Alt+T to toggle, Alt+Q to quit)
def listen_for_keys():
    global market_price_reading, stop_thread
    while True:
        if keyboard.is_pressed('alt+t'):  # Toggle market price reading on/off
            market_price_reading = not market_price_reading
            if market_price_reading:
                print("Market price reading started.")
            else:
                print("Market price reading stopped.")
            time.sleep(0.5)  # Debounce key press

        if keyboard.is_pressed('alt+q'):  # Quit the application
            print("Exiting...")
            stop_thread = True
            break
        time.sleep(0.1)  # Reduce CPU usage

# Main function
def main():
    # Get tier, enchantment, and quality from user
    tier, enchantment, quality = get_user_input()

    print("\nPress 'Alt+T' to start/stop market price reading.")
    print("Press 'Alt+Q' to quit the application.")

    # Start the thread to read market prices
    price_reader_thread = threading.Thread(target=market_price_reader)
    price_reader_thread.start()

    # Start listening for key presses
    listen_for_keys()

    # Wait for the thread to finish before exiting
    price_reader_thread.join()

    print(f"Market prices saved to {output_txt_file}")

# Run the program
if __name__ == "__main__":
    main()
