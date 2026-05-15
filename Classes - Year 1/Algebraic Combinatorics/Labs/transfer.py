from pathlib import Path
import shutil

# Windows Downloads folder
downloads = Path("/mnt/c/Users/baneg/Downloads/")

# Current WSL working directory
target = Path("/mnt/c/Users/baneg/OneDrive/Desktop/git/PhD/Classes - Year 1/Algebraic Combinatorics/Labs")

# Change filename here
filename = "Lab7-Cycle_index (1).ipynb"

src = downloads / filename
dst = target / filename

shutil.copy(src, dst)

print(f"Copied:\n{src}\n->\n{dst}")