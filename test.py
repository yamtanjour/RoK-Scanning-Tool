from PIL import Image
from adb_connector import connect_ldplayer_adb
from navigation import tap, take_screenshot
import easyocr
import numpy as np 



reader = easyocr.Reader(['en'])
connect_ldplayer_adb()

tap(180, 750)
take_screenshot()
img = np.array(Image.open("player_profile.png"))
results = reader.readtext(img)
print(results)