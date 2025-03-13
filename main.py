import pyautogui
import time

# Inform the user to prepare the game window
print("Prepare your game window so that the player profile is visible in the defined region.")
time.sleep(5)  # Wait 5 seconds for you to position the window

# Define the region to capture: (x, y, width, height)
region = (600, 200, 800, 800)

# Capture the screenshot of the specified region
screenshot = pyautogui.screenshot(region=region)
screenshot.save("player_profile1.png")

print("Screenshot saved as player_profile.png")
