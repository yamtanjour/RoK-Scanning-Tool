import tkinter as tk
import subprocess

def start_scan():
    print("Starting scan...")
    subprocess.run(["python", "main.py"])

root = tk.Tk()
root.title("RoK Scanning Tool")

btn_scan = tk.Button(root, text="Start Scan", command=start_scan)
btn_scan.pack(pady=10)

btn_exit = tk.Button(root, text="Exit", command=root.quit)
btn_exit.pack(pady=5)

root.mainloop()
