import os
import time


adb_path = r"C:\LDPlayer\LDPlayer9\adb.exe"

def adb_command(command):
    os.system(f'"{adb_path}" -s localhost:5555 shell {command}')
    time.sleep(1)

def tap(x_position, y_position):
    print(f"Tapping on player at X={x_position}, Y={y_position}")
    adb_command(f"input tap {x_position} {y_position}")
    time.sleep(1)


def take_screenshot(filename="player_profile.png"):
    
    # Capture screenshot on the device
    adb_command("screencap -p /sdcard/screen.png")
    
    # Pull the screenshot file from the device to local machine
    os.system(f'"{adb_path}" -s localhost:5555 pull /sdcard/screen.png {filename}')

