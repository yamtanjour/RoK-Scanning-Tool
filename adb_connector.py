import os

def get_ldplayer_adb(adb_path):
    """Finds LDPlayer's built-in ADB."""
    if os.path.exists(adb_path):
        print(f"[OK] Found ADB at: {adb_path}")
        return adb_path
    print("[ERROR] ADB not found! Ensure LDPlayer is installed.")
    return None

def connect_ldplayer_adb():
    """Connects ADB to LDPlayer using full path."""
    adb_path = os.environ.get("ADB_PATH")
    if not adb_path:
        raise ValueError("ADB_PATH not set in environment.")
    adb_path = get_ldplayer_adb(adb_path)
    if adb_path:
        os.system(f'"{adb_path}" connect localhost:5555')
        print("[OK] Connected to LDPlayer via ADB!")
    else:
        print("[ERROR] Failed to connect ADB.")