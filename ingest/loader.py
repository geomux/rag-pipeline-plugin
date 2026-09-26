# loader.py
# Reads files in the docs/ folder into memory

import re
from dataclasses import dataclass
from pathlib import Path
from pypdf import PdfReader

EXTENSIONS = {".pdf"}

FOOTER = re.compile(r"^\d{3,4}-\d+ As of \w+ \d{1,2}, \d{4}\s*$", re.MULTILINE)

@dataclass # creates named fields (i.e. doc.path) without writing __init__
class Doc:
    path: str # relative to the docs folder, always "/" separated
    text: str

def read_pdf(file: Path) -> str:
    """Extract a PDF's text on eage page with the page footers removed"""
    text = "\n".join(page.extract_text() or "" for page in PdfReader(file).pages)
    return FOOTER.sub("", text)

def load_docs(folder):
    """Loads every PDF as a Doc"""
    root = Path(folder)
    return [
        Doc(f.relative_to(root).as_posix(), read_pdf(f)) # as_posix(): same "/" paths on Windows/Linux
        for f in sorted(root.rglob("*"))
        if f.suffix.lower() in EXTENSIONS
    ]
              