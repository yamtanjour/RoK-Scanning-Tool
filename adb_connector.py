import os
import os
def get_ldplayer_adb(adb_path):
    """Finds LDPlayer's built-in ADB."""
    adb_path = os.environ.get("ADB_PATH") # Adjust path if necessary
    if os.path.exists(adb_path):
        print(f"✅ Found ADB at: {adb_path}")
        return adb_path
    print("❌ ADB not found! Ensure LDPlayer is installed.")
    return None

def connect_ldplayer_adb():
    """Connects ADB to LDPlayer using full path."""
    adb_path = get_ldplayer_adb()
    if adb_path:
        os.system(f'"{adb_path}" connect localhost:5555')
        print("✅ Connected to LDPlayer via ADB!")
    else:
        print("❌ Failed to connect ADB.")

