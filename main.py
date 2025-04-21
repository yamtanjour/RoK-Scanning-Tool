#!/usr/bin/env python3
import os
import sys
import time
import csv

from PIL import Image
import numpy as np
import easyocr

from navigation import tap, take_screenshot
from adb_connector import connect_ldplayer_adb
from ocr_reader import get_region, get_text

# ── CONFIG ──────────────────────────────────────────────────────────────────────
# How many players to scan; override via environment:
NUM_PLAYERS = int(os.environ.get("NUM_PLAYERS", "3"))

# ── GLOBALS ─────────────────────────────────────────────────────────────────────
# Will hold one [Name, Power, KillPoints, T4k, T4p, T5k, T5p, Deaths] per governor
PlayerList = []

# Once‑only bounding boxes for the 8 OCR regions
boxes = []

# Initialize the OCR reader (only English)
reader = easyocr.Reader(['en'], gpu=False)


def printstats(i: int):
    """Print the stats for the ith governor."""
    row = PlayerList[i]
    print("--------------------------------------------------")
    print(f"Governor:   {row[0]}")
    print(f"Power:      {row[1]}")
    print(f"Kill Points:{row[2]}")
    print(f"T4 Kills:   {row[3]}")
    print(f"T4 Points:  {row[4]}")
    print(f"T5 Kills:   {row[5]}")
    print(f"T5 Points:  {row[6]}")
    print(f"Deaths:     {row[7]}")
    print("--------------------------------------------------")


def get_regions():
    """
    Run once at startup to detect the 8 OCR regions on the screen.
    """
    # 1) Top profile bar
    take_screenshot()
    img = Image.open("player_profile.png")
    img_np = np.array(img)
    results = reader.readtext(img_np)

    boxes.append(get_region(img, results, "civilization", 1))    # Name
    boxes.append(get_region(img, results, "power", 3))            # Power
    boxes.append(get_region(img, results, "kill points", 3))     # Kill Points

    # 2) Kill‑stats section
    tap(1150, 300)
    time.sleep(1)
    take_screenshot()
    img = Image.open("player_profile.png")
    crop = img.crop((850, 320, 1500, 700))
    crop_np = np.array(crop)
    results = reader.readtext(crop_np)

    boxes.append(get_region(crop, results, "Kill Statistics",  9))  # T4 Kills
    boxes.append(get_region(crop, results, "Kill Statistics", 10))  # T4 Points
    boxes.append(get_region(crop, results, "Kill Statistics", 11))  # T5 Kills
    boxes.append(get_region(crop, results, "Kill Statistics", 12))  # T5 Points

    # 3) Deaths section
    tap(180, 750)
    time.sleep(1)
    take_screenshot()
    img = Image.open("player_profile.png")
    results = reader.readtext(np.array(img))
    boxes.append(get_region(img, results, "dead", 1))

    # Reset UI
    tap(50, 650)
    tap(50, 650)


def capture_profile():
    """
    OCR the 8 regions for the currently displayed governor and append the
    values list to PlayerList.
    """
    vals = []

    # Top bar: Name, Power, Kill Points
    take_screenshot()
    img = Image.open("player_profile.png")
    vals.append(get_text(img, boxes[0]))
    vals.append(get_text(img, boxes[1]))
    vals.append(get_text(img, boxes[2]))

    # Kill stats section
    tap(1150, 300)
    take_screenshot()
    img = Image.open("player_profile.png")
    crop = img.crop((850, 320, 1500, 700))
    vals.append(get_text(crop, boxes[3]))
    vals.append(get_text(crop, boxes[4]))
    vals.append(get_text(crop, boxes[5]))
    vals.append(get_text(crop, boxes[6]))

    # Deaths
    tap(180, 750)
    take_screenshot()
    img = Image.open("player_profile.png")
    vals.append(get_text(img, boxes[7]))

    # Reset UI
    tap(50, 650)
    tap(50, 650)

    PlayerList.append(vals)


# ── MAIN ────────────────────────────────────────────────────────────────────────

def main():
    # 1) Connect to LDPlayer via ADB
    connect_ldplayer_adb()
    # 2) Open first governor slot
    tap(700, 300)
    time.sleep(2)
    get_regions()
    # 4) Scan each governor slot
    tap(700, 300)
    time.sleep(1)
    capture_profile()
    tap(700, 400)
    time.sleep(1)
    capture_profile()
    tap(700, 500)
    time.sleep(1)
    capture_profile()
    for idx in range(4, NUM_PLAYERS):
        tap(700, 600)
        capture_profile()
        time.sleep(1)

    # 5) After scanning all, print stats
    for i in range(len(PlayerList)):
        printstats(i)

    # 6) Write CSV
    with open("PlayerList.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name", "Power", "Kill Points",
            "T4 Kills", "T4 Points",
            "T5 Kills", "T5 Points", "Deaths"
        ])
        writer.writerows(PlayerList)


if __name__ == "__main__":
    main()
