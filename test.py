from navigation import tap, adb_command, adb_screenshot
from ocr_reader import extract_values, detect_value_regions
from adb_connector import connect_ldplayer_adb
import time

time.sleep(1)
connect_ldplayer_adb()
adb_screenshot()