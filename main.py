from navigation import tap, adb_command, take_screenshot
from ocr_reader import extract_values, detect_value_regions
from adb_connector import connect_ldplayer_adb
import time

NameList = []
PowerList = []
KPList = []


def capture_profile():
    extract_values("player_profile.png", regions)
    gov, power, kill = extract_values("player_profile.png", regions)
    NameList.append(gov)
    PowerList.append(power)
    KPList.append(kill)
    
adb_path = r"C:\LDPlayer\LDPlayer9\adb.exe"
connect_ldplayer_adb()


tap(700, 300)
take_screenshot()
regions = detect_value_regions("player_profile.png")
capture_profile()
adb_command(f"input tap 50 650")
tap(700, 400)
take_screenshot()
capture_profile()
adb_command(f"input tap 50 650")
tap(700, 500)
take_screenshot()
capture_profile()
adb_command(f"input tap 50 650")
for i in range(1, 3):
    tap(700, 600)
    time.sleep(1)
    take_screenshot()
    capture_profile()
    adb_command(f"input tap 50 650")
    print("closing Player")
    time.sleep(1)
    

for i in range (0, len(NameList)):
    print(f"Governor: {NameList[i]}")
    print(f"Power: {PowerList[i]}")
    print(f"Kill Points: {KPList[i]}")
    print("--------------------------------------------------")