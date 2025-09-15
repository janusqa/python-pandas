from pathlib import Path

import pandas as pd

# Define the root directory (one level up from src)
ROOT_DIR = Path(__file__).parent.parent  # If in a .py file
# For notebook, use:
ROOT_DIR = Path.cwd().parent

# Construct the full path
csv_path = ROOT_DIR / "data" / "your_file.csv"

# Read the CSV
df = pd.read_csv(csv_path)
