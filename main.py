from navigation import tap, take_screenshot
from ocr_reader import get_region, get_text
from adb_connector import connect_ldplayer_adb
import time
import easyocr
from PIL import Image
import numpy as np
import csv
import os
num_players = os.environ.get("NUM_PLAYERS")

Names = []
Power = []
KillPoints = []
T4Kills = []
T4Points = []
T5Kills = []
T5Points = []
Deaths = []

boxes = [] # [name, power, kill points, T4, T4P, T5, T5P, Deaths]

reader = easyocr.Reader(['en'])

def printstats(i):
    print("--------------------------------------------------")
    print(f"Governor: {Names[i]}")
    print(f"Power: {Power[i]}")
    print(f"Kill Points: {KillPoints[i]}")
    print(f"T4 Kills: {T4Kills[i]}")
    print(f"T4 Points: {T4Points[i]}")
    print(f"T5 Kills: {T5Kills[i]}")
    print(f"T5 Points: {T5Points[i]}")
    print(f"Deaths: {Deaths[i]}")
    print("--------------------------------------------------")

def get_regions():
    take_screenshot()
    img = Image.open("player_profile.png")
    img_np = np.array(img)  # Convert Pillow Image to numpy array
    results = reader.readtext(img_np)  # Pass numpy array to readtext()
    boxes.append(get_region(img, results, "civilization", 1))
    boxes.append(get_region(img, results, "power", 3))
    boxes.append(get_region(img, results, "kill points", 3))
    tap(1150, 300)
    time.sleep(1)
    take_screenshot()
    img = Image.open("player_profile.png")
    crop = img.crop((850, 320, 1500, 700))
    crop_np = np.array(crop)  # Convert cropped image to numpy array
    results = reader.readtext(crop_np)  # Pass numpy array to readtext()
    boxes.append(get_region(crop, results, "Kill Statistics", 9))
    boxes.append(get_region(crop, results, "Kill Statistics", 10))
    boxes.append(get_region(crop, results, "Kill Statistics", 11))
    boxes.append(get_region(crop, results, "Kill Statistics", 12))
    tap(180, 750)
    time.sleep(1)
    take_screenshot()
    img = Image.open("player_profile.png")
    img_np = np.array(img)  # Convert Pillow Image to numpy array
    results = reader.readtext(img_np)  # Pass numpy array to readtext()
    boxes.append(get_region(img, results, "dead", 1))
    tap(50, 650)
    tap(50, 650)


def capture_profile(j):
    global Names, Power, KillPoints, T4Kills, T4Points, T5Kills, T5Points, Deaths
    take_screenshot()
    img = Image.open("player_profile.png")
    Names.append(get_text(img, boxes[0]))
    Power.append(get_text(img, boxes[1]))
    KillPoints.append(get_text(img, boxes[2]))
    tap(1150, 300)
    time.sleep(1)
    take_screenshot()
    img = Image.open("player_profile.png")
    crop = img.crop((850, 320, 1500, 700)) 
    T4Kills.append(get_text(crop, boxes[3], key="T4Kills"))
    T4Points.append(get_text(crop, boxes[4], key="T4Points"))
    T5Kills.append(get_text(crop, boxes[5], key="T5Kills"))
    T5Points.append(get_text(crop, boxes[6], key="T5Points"))
    tap(180, 750)
    time.sleep(1)
    take_screenshot()
    img = Image.open("player_profile.png")
    Deaths.append(get_text(img, boxes[7], key="Deaths"))
    tap(50, 650)
    tap(50, 650)
    printstats(j)
    time.sleep(1)

# start of the proram
connect_ldplayer_adb()

tap(700, 300)
time.sleep(2)
get_regions()
tap(700, 300)
capture_profile(0)
tap(700, 400)
capture_profile(1)
tap(700, 500)
capture_profile(2)
for i in range(3, int(num_players) - 1):
    tap(700, 600)
    capture_profile(i)
    if Names[i] == "N/A" or Power[i] == "N/A" or KillPoints[i] == "N/A":
        tap(700, 700)
        time.sleep(1)
        capture_profile(i)

for i in range (0, len(Names)):
    printstats(i)
    

rows = zip(Names, Power, KillPoints, T4Kills, T4Points, T5Kills, T5Points, Deaths)

with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Player Name', 'Power', 'Kill Points', 'T4 Kills', 'T4 Kill Points', 'T5 Kills', 'T5 Kill Points', 'Deaths'])  # header
    writer.writerows(rows)

