from PIL import Image
from adb_connector import connect_ldplayer_adb
from navigation import tap

connect_ldplayer_adb()

tap(180, 750)