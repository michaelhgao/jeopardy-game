import os
import shutil
import subprocess
import sys

ENTRY_SCRIPT = "main.py"
DATA_FOLDER = "images"
DIST_FOLDER = "dist"
EXE_NAME = "JeopardyApp"

# Clean old builds
for folder in ("build", "dist"):
    if os.path.exists(folder):
        shutil.rmtree(folder)

if sys.platform == "win32":
    add_data = f"{DATA_FOLDER};{DATA_FOLDER}"
else:
    add_data = f"{DATA_FOLDER}:{DATA_FOLDER}"

# Build command
cmd = [
    "pyinstaller",
    "--noconsole",
    "--onedir",
    f"--name={EXE_NAME}",
    f"--add-data={add_data}",
    ENTRY_SCRIPT,
]

print("Running PyInstaller...")
print(" ".join(cmd))

subprocess.run(cmd, check=True)

base = os.path.join("dist", EXE_NAME)
os.makedirs(os.path.join(base, "images"), exist_ok=True)
os.makedirs(os.path.join(base, "saves"), exist_ok=True)

print(
    f"Executable created in {DIST_FOLDER}/{EXE_NAME}.exe (Windows) or {DIST_FOLDER}/{EXE_NAME} (macOS/Linux)"
)
