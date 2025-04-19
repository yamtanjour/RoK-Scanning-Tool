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
        # Replace localhost:5555 with actual port if different (e.g., 127.0.0.1:5555 or 5557)
        os.system(f'"{adb_path}" kill-server')
        os.system(f'"{adb_path}" start-server')
        os.system(f'"{adb_path}" connect 127.0.0.1:5555')

        print("[OK] Connected to LDPlayer via ADB!")
    else:
        print("[ERROR] Failed to connect ADB.")