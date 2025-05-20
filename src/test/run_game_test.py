import subprocess
import os
import sys
from pathlib import Path

project = "AttackerTestProject"

# Get run_game.py path from src/core/run_game.py

file = Path(__file__).parent.parent / "core" / "run_game.py"
if not file.exists():
    raise FileNotFoundError(f"File {file} does not exist.")

subprocess.Popen([sys.executable, file, project])