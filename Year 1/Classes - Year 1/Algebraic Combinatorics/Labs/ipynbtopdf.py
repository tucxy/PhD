from pathlib import Path
import subprocess

folder = Path.cwd()

for nb in folder.glob("*.ipynb"):

    print(f"\nConverting {nb.name}...")

    result = subprocess.run(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "pdf",
            str(nb)
        ],
        text=True,
        capture_output=True
    )

    print(result.stdout)
    print(result.stderr)

print("Done.")