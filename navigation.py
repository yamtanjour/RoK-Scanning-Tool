import os
import time

# 1. Read the user‑supplied ADB path
adb_path = os.environ.get("ADB_PATH")
if not adb_path or not os.path.isfile(adb_path):
    raise RuntimeError(
        f"Please set ADB_PATH to your emulator’s adb.exe; got: {adb_path!r}"
    )

# 2. Use the same host:port you connect to (127.0.0.1:5555)
ADB_HOST = os.environ.get("ADB_HOST", "127.0.0.1")
ADB_PORT = os.environ.get("ADB_PORT", "5555")
DEVICE_ADDR = f"{ADB_HOST}:{ADB_PORT}"

def _adb_command(cmd: str):
    
    full_cmd = f'"{adb_path}" -s {DEVICE_ADDR} shell {cmd}'
    # print(f"Running: {full_cmd}")  # <— you can uncomment this for debug
    os.system(full_cmd)
    time.sleep(1)

def tap(x_position: int, y_position: int):
    
    print(f"Tapping on player at X={x_position}, Y={y_position}")
    _adb_command(f"input tap {x_position} {y_position}")

def take_screenshot(filename: str = "player_profile.png"):
    
    # 1) Capture on device
    _adb_command("screencap -p /sdcard/screen.png")
    # 2) Pull down to the working directory, using the same DEVICE_ADDR
    pull_cmd = f'"{adb_path}" -s {DEVICE_ADDR} pull /sdcard/screen.png {filename}'
    os.system(pull_cmd)
