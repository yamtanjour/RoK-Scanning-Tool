# RoK Scanning Tool

Python tool for capturing Rise of Kingdoms profiles through an Android emulator and extracting Name, Power, Kill Points, T4/T5 Kills and Points, and Deaths with EasyOCR.

## Scope and verification

This guide was checked against the Python source at commit `c73a03b2f307c0cda463c145026a15d695aaea4b`. Commands below are derived from the existing entry points, imports and ADB calls; **they have not been tested end to end with an emulator**. Setup commands are a proposed local installation procedure, not an existing installer.

The repository has no dependency manifest, version lock, automated test suite or documented emulator preset. Consequently, an identical dependency environment and successful scanning on every installation cannot currently be guaranteed.

## Prerequisites

- Git and Python 3 with pip and venv.
- A desktop session with Tkinter for the optional GUI.
- Python packages: Pillow (`PIL`), NumPy and EasyOCR, as imported by the source.
- An Android emulator with Rise of Kingdoms installed, a working login, and ADB enabled.
- A writable checkout: screenshots, debug crops and CSV output are written to the current working directory.

**Not established by the repository:** minimum Python version, exact package versions, supported OS versions, emulator versions and hardware requirements. Tracked `cpython-312.pyc` files suggest Python 3.12 was used at some point; they do not prove support for a particular Python release. Windows is the most directly suggested environment because the GUI defaults to a Windows BlueStacks executable. LDPlayer and BlueStacks are mentioned, but neither has a documented tested configuration.

## Installation (Windows PowerShell)

Run these commands in PowerShell. Use the activated environment for all subsequent commands.

```powershell
git clone https://github.com/yamtanjour/RoK-Scanning-Tool.git
cd RoK-Scanning-Tool
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Pillow numpy easyocr
python -c "import PIL, numpy, easyocr; print('Imports OK')"
```

There is no `requirements.txt`, so do not use `pip install -r requirements.txt`. Package versions above are intentionally unpinned because none are established by the repository. EasyOCR may need to download model weights during first initialization; model files are not included. Allow that initialization to finish before judging the scan.

Optional GUI check:

```powershell
python -m tkinter
```

This should open Tkinter's demonstration window. Close it before continuing. If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of `python` for the CLI commands below. The GUI launches the literal command `python main.py`, so its child process must also resolve to the intended Python installation.

## ADB and emulator setup

1. Start one emulator instance and enable its ADB access in the emulator settings.
2. Locate the actual ADB executable. The GUI's default below is only a path suggestion; check your installation.
3. Configure that instance to accept a local ADB connection at `127.0.0.1:5555`.

**Not established by the repository:** emulator settings menu names, how to change its port, Android version, DPI, and exact resolution. Consult your installed emulator's documentation for those settings. A different endpoint is not fully supported without a source change: `navigation.py` reads `ADB_HOST`/`ADB_PORT`, but `adb_connector.py` always connects to `127.0.0.1:5555`.

```powershell
$env:ADB_PATH = "C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
$env:ADB_HOST = "127.0.0.1"
$env:ADB_PORT = "5555"
Test-Path $env:ADB_PATH
& $env:ADB_PATH start-server
& $env:ADB_PATH connect 127.0.0.1:5555
& $env:ADB_PATH devices
```

Replace the executable path if necessary. `Test-Path` must return `True`; the device list must include `127.0.0.1:5555` with status `device`. The program's own “Connected” message is not proof: it does not check ADB return codes. At startup it also runs `kill-server`, restarting the shared ADB server.

Verify capture before scanning (these mirror `navigation.py`):

```powershell
& $env:ADB_PATH -s 127.0.0.1:5555 shell screencap -p /sdcard/screen.png
& $env:ADB_PATH -s 127.0.0.1:5555 pull /sdcard/screen.png adb-check.png
```

Open `adb-check.png` and verify that it is the intended game instance. This diagnostic file is not consumed by the scanner.

### Required game layout

Set the game UI to English: the readers use `['en']` and locate the English anchors `civilization`, `power`, `kill points`, `Kill Statistics`, and `dead`.

Before starting, open the governor/player list whose first three rows can be opened at `(700, 300)`, `(700, 400)`, and `(700, 500)`. This starting screen is inferred from `main.py`; its exact in-game name and route are not documented. Do not start with a profile already open.

The code also taps `(1150, 300)`, `(180, 750)`, and `(50, 650)`, and crops the rectangle `(850, 320, 1500, 700)`. These are Android screenshot pixels, not desktop window coordinates. The intended full crop needs an image at least 1500 pixels wide, and the tap at y=750 must be inside it. **That is a geometric lower bound, not a verified resolution preset.** Compare your screenshot and the tracked `player_profile.png`; if the layout differs, adjust the coordinates/crop in `main.py` before scanning. Do not change resolution or UI scale during a run; OCR regions are detected only once.

## Start and example workflow

### Recommended first run: CLI, three profiles

Keep the same PowerShell session and working directory used above. Back up the included `PlayerList.csv` and any images you want to retain: the scanner overwrites them.

```powershell
$env:NUM_PLAYERS = "3"
python main.py
```

There are no implemented command-line flags, file-selection prompts or player-ID inputs. Configuration is through environment variables and the current emulator screen.

The script connects, opens the first profile to locate OCR regions, then captures the first three slots. It prints eight fields per captured profile and, after all captures finish, writes `PlayerList.csv`. Check those three CSV rows manually against the game before attempting a longer run. OCR results remain strings, including thousands separators; they are not numerically validated. Use Ctrl+C in the CLI to interrupt; interrupted runs may not write a new CSV.

### Optional GUI

```powershell
python gui.py
```

Enter the full existing ADB executable path and a numeric player count, then click **Start Scan**. The initial values are the BlueStacks path above and `300`. **Stop Scan** terminates the child process, so a partial CSV is not guaranteed. The GUI only checks whether fields are empty, not whether the count is valid. Its output-reading code can block the interface while waiting for a line; use the CLI first for diagnosis.

### Player-count limitation

The GUI label says “min. 4”, but the implementation behaves differently:

- The first three profiles are always captured, even if `NUM_PLAYERS` is less than 3.
- The remaining loop is `range(4, NUM_PLAYERS)`. Therefore 3 and 4 both produce three capture calls; values greater than 4 produce `NUM_PLAYERS - 1` calls.
- Every additional capture taps `(700, 600)`. There is no explicit swipe/scroll command. Whether that advances to a new player depends on the game UI and is not established by the repository; duplicate profiles are possible.

Do not interpret the requested count or CSV row count as proof of that many distinct governors.

## Outputs and source map

| File | Role / behavior |
| --- | --- |
| `main.py` | CLI entry point, fixed taps/crop, once-only region detection, CSV writing |
| `gui.py` | Tkinter launcher; supplies ADB_PATH and NUM_PLAYERS |
| `adb_connector.py` | Validates path existence; restarts server and connects to fixed endpoint |
| `navigation.py` | Requires ADB_PATH at import; taps and screenshot/pull commands |
| `ocr_reader.py` | Anchor/offset region selection and OCR of cropped regions |
| `PlayerList.csv` | Overwritten at successful completion; header: Name, Power, Kill Points, T4 Kills, T4 Points, T5 Kills, T5 Points, Deaths |
| `player_profile.png` | Latest pulled screenshot; overwritten repeatedly |
| `debug_region_from_*.png` | Regions saved during initial calibration |
| `debug_cropped.png` | Reused by every default get_text call; only the latest crop survives |

Other tracked crops are examples/artifacts; current `main.py` does not generate separate `Name_cropped.png`, `T4Kills_cropped.png`, etc. `test.py` is a live diagnostic script that connects, taps, captures and runs OCR, **not an automated unit test**. It also requires ADB_PATH.

## Troubleshooting

| Symptom | Check / action |
| --- | --- |
| ADB_PATH error before startup | Set ADB_PATH before launching Python: navigation.py validates it during import. Use a full path to an existing executable. |
| ADB connection refused / offline / wrong device | Confirm emulator ADB access and port, run the devices command above, and require the exact serial 127.0.0.1:5555 with status device. Other ports need a connector source change as described above. |
| “Connected” printed but taps fail | The message is unconditional after os.system calls. Inspect ADB output and devices rather than trusting it. |
| Missing or stale player_profile.png | Repeat the screenshot/pull preflight. ADB failures are not checked, so an old tracked screenshot can otherwise be read silently. |
| StopIteration during get_region | An English anchor was not detected. Check game language, starting screen, layout, loading state and screenshot. |
| “Offset leads to invalid index.” | Anchor was found but the expected following OCR entry was absent; inspect screenshot and debug regions, then review anchor offsets in main.py. |
| N/A or incorrect values | N/A means the crop produced no text. Check crops, resolution, text clarity and fixed coordinates. Validate results manually; there is no confidence/number validation. |
| Model download or package import error | Check the active Python environment, installation output, network and model cache access. Exact tested dependency versions and offline model setup are not provided. |
| CSV not updated / PermissionError | CSV is written only at the end. Close it in spreadsheet software, check directory permissions, and inspect the terminal for an earlier failure. |
| Too few rows or duplicate players | See the player-count limitation; verify the fourth-slot behavior before larger scans. |
| GUI appears frozen / logs delayed | Try the CLI. GUI uses blocking readline and a piped child stdout, which can delay feedback. |

## Validation limits

The entry points, dependencies, environment variable names, file paths, CSV schema, ADB command structure and count behavior above were checked against source. An emulator session, dependency installation, OCR accuracy, resolution calibration and long-run navigation still require local validation. There are no proven performance figures or supported emulator presets in this repository.
