from navigation import tap, adb_command, take_screenshot
from ocr_reader import get_region, get_text
from adb_connector import connect_ldplayer_adb
import time
import easyocr
import PIL as Image
import numpy as np

NameList = []
PowerList = []
KPList = []
boxes = [] # [name, power, kill points, T4, T4P, T5, T5P, Deaths]

reader = easyocr.Reader(['en'])

def printstats(i):
    print("--------------------------------------------------")
    print(f"Governor: {NameList[i]}")
    print(f"Power: {PowerList[i]}")
    print(f"Kill Points: {KPList[i]}")
    print("--------------------------------------------------")

def get_regions():
    img = Image.open("player_profile.png")
    take_screenshot()
    results = reader.readtext(img)
    boxes.append(get_region(img, results, "civilization", 1))
    boxes.append(get_region(img, results, "power", 3))
    boxes.append(get_region(img, results, "kill points", 3))
    tap(1150, 300)
    take_screenshot()
    img = Image.open("player_profile.png")
    crop = img.crop((850, 320 , 1500, 700))
    results = reader.readtext(crop)
    boxes.append(get_region(crop, results, "Kill Statistics", 7))
    boxes.append(get_region(crop, results, "Kill Statistics", 8))
    boxes.append(get_region(crop, results, "Kill Statistics", 9))
    boxes.append(get_region(crop, results, "Kill Statistics", 10))
    tap(180, 750)
    take_screenshot()
    
    
    
adb_path = r"C:\LDPlayer\LDPlayer9\adb.exe"
connect_ldplayer_adb()



tap(700, 300)
time.sleep(2)
take_screenshot()
regions = detect_value_regions("player_profile.png")
capture_profile()
adb_command(f"input tap 50 650")
printstats(0)
tap(700, 400)
take_screenshot()
capture_profile()
adb_command(f"input tap 50 650")   
printstats(1)
tap(700, 500)
take_screenshot()
capture_profile()
adb_command(f"input tap 50 650")
printstats(2)
for i in range(3, 297):
    tap(700, 600)
    take_screenshot()
    capture_profile()
    adb_command(f"input tap 50 650")
    printstats(i)
    if NameList[i] == "N/A" or PowerList[i] == "N/A" or KPList[i] == "N/A":
        tap(700, 700)
        time.sleep(1)
        take_screenshot()
        capture_profile()
        adb_command(f"input tap 50 650")
        printstats(i)
    

for i in range (0, len(NameList)):
    printstats(i)