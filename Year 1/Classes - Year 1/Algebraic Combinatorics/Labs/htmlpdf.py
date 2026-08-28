from pathlib import Path
import subprocess

folder = Path("/mnt/c/Users/baneg/OneDrive/Desktop/git/PhD/Classes - Year 1/Algebraic Combinatorics/Labs")

for nb in folder.glob("*.ipynb"):
    print(f"Converting {nb.name}...")

    # Convert notebook -> HTML
    subprocess.run(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "html",
            str(nb)
        ],
        check=True
    )

    html = nb.with_suffix(".html")
    pdf = nb.with_suffix(".pdf")

    # Convert HTML -> PDF using Chromium
    subprocess.run(
        [
            "playwright",
            "pdf",
            str(html),
            str(pdf)
        ],
        check=True
    )

print("Done.")