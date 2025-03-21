import os
import time
import pygetwindow as gw
from PIL import ImageGrab
from adb_connector import connect_ldplayer_adb

def adb_command(command):
    """
    Sends an ADB command to the LDPlayer emulator.
    Adjust the adb_path if needed.
    """
    adb_path = r"C:\LDPlayer\LDPlayer9\adb.exe"  # Ensure this path is correct for your setup
    os.system(f'"{adb_path}" -s localhost:5555 shell {command}')
    time.sleep(1)

def tap(x_position, y_position):
    print(f"👆 Tapping on player at X={x_position}, Y={y_position}")
    adb_command(f"input tap {x_position} {y_position}")
    time.sleep(2)  # Wait for profile to load


def take_screenshot(filename="player_profile.png"):
    """
    Captures a screenshot on the device using ADB and pulls it to the local machine.
    Uses the existing adb_command function.
    """
    adb_path = r"C:\LDPlayer\LDPlayer9\adb.exe"  # Use the same path as in adb_command
    
    # Ensure device is connected
    os.system(f'"{adb_path}" connect localhost:5555')
    time.sleep(1)
    
    # Capture screenshot on the device
    adb_command("screencap -p /sdcard/screen.png")
    
    # Pull the screenshot file from the device to the local machine
    os.system(f'"{adb_path}" -s localhost:5555 pull /sdcard/screen.png {filename}')
    print(f"✅ Screenshot saved as: {filename}")

