import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# ---------- THEME COLORS ----------
BG_COLOR = "#1c1c1c"        # Dark background
FG_COLOR = "#FFD700"        # Gold text
BTN_COLOR = "#333333"       # Button background
BTN_HOVER = "#444444"

process = None  # Global for subprocess

def start_scan():
    global process
    adb_path = input_path_var.get()
    num_players = input_num_var.get()
    
    if not adb_path or not num_players:
        messagebox.showerror("Missing Data", "Please fill all fields.")
        return

    env = os.environ.copy()
    env["ADB_PATH"] = adb_path
    env["NUM_PLAYERS"] = num_players

    # Clear output box
    output_box.delete("1.0", tk.END)

    process = subprocess.Popen(
        ["python", "main.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    def read_output():
        line = process.stdout.readline()
        if line:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)
        if process.poll() is None:
            root.after(100, read_output)

    read_output()

def stop_scan():
    global process
    if process:
        process.terminate()
        output_box.insert(tk.END, "\n[Scan stopped by user]\n")
        output_box.see(tk.END)
        process = None

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("RoK Scanning Tool")
root.configure(bg=BG_COLOR)
root.geometry("500x450")

# ---------- TITLE ----------
tk.Label(root, text="RoK Scanning Tool", font=("Helvetica", 18, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)

# ---------- ENTRIES ----------
tk.Label(root, text="ADB Path:", fg=FG_COLOR, bg=BG_COLOR).pack()
input_path_var = tk.StringVar(value="C:\\LDPlayer\\LDPlayer9\\adb.exe")
input_path = tk.Entry(root, width=50, textvariable=input_path_var)
input_path.pack(pady=5)

tk.Label(root, text="Num. of Players: (min. 4)", fg=FG_COLOR, bg=BG_COLOR).pack()
input_num_var = tk.StringVar(value="300")
input_num = tk.Entry(root, width=50, textvariable=input_num_var)
input_num.pack(pady=5)

# ---------- BUTTONS ----------
def style_button(btn):
    btn.configure(bg=BTN_COLOR, fg=FG_COLOR, activebackground=BTN_HOVER, font=("Helvetica", 10, "bold"))

btn_start = tk.Button(root, text="Start Scan", command=start_scan)
style_button(btn_start)
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text="Stop Scan", command=stop_scan)
style_button(btn_stop)
btn_stop.pack()

# ---------- OUTPUT BOX ----------
output_box = tk.Text(root, height=10, width=60, bg="#121212", fg="#00FF00")
output_box.pack(pady=10)

# ---------- MAIN LOOP ----------
root.mainloop()
