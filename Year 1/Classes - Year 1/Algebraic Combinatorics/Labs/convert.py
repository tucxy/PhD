from pathlib import Path
import subprocess

folder = Path("/mnt/c/Users/baneg/OneDrive/Desktop/git/PhD/Classes - Year 1/Algebraic Combinatorics/Labs")

for nb in folder.glob("*.ipynb"):
    print(f"Converting {nb.name}...")

    subprocess.run(
        ["jupyter", "nbconvert", "--to", "pdf", str(nb)],
        check=True
    )

print("Done.")