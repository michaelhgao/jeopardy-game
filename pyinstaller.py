import subprocess
import sys

ENTRY_SCRIPT = "main.py"
DATA_FOLDER = "images"
DIST_FOLDER = "dist"
EXE_NAME = "JeopardyApp"

if sys.platform == "win32":
    add_data = f"{DATA_FOLDER};{DATA_FOLDER}"
else:
    add_data = f"{DATA_FOLDER}:{DATA_FOLDER}"

# Build command
cmd = [
    "pyinstaller",
    "--onefile",  # single executable
    "--windowed",  # no console window
    f"--name={EXE_NAME}",
    f"--add-data={add_data}",
    ENTRY_SCRIPT,
]

print("Running PyInstaller...")
print(" ".join(cmd))

subprocess.run(cmd, check=True)

print(
    f"Executable created in {DIST_FOLDER}/{EXE_NAME}.exe (Windows) or {DIST_FOLDER}/{EXE_NAME} (macOS/Linux)"
)
