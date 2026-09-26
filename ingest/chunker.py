# chunker.py
# Splits the document(s) into chunks.
## CUSTOMIZED to Colorado ECMC Rules & Regulations Documention format

import re
from dataclasses import dataclass

from ingest.loader import Doc

# Start of a section in the PDFs (i.e. "301. GENERAL REQUIREMENTS..." in ECMC Rules 300 series)
SECTION =  re.compile(r"^\d{3,4}\.\s+[A-Z]")
# Start of a list item or definition (list markers and defined terms are natural cut points).
BREAK = re.compile(r"""^(
      \(\d{1,3}\)                                   # (1)  (2)
    | [a-zA-Z]{1,4}\.\s                             # a.  A.  i.  aa.  iv.
    | \d{1,3}\.\s                                   # 1.  2.
    | [A-Z][A-Z0-9 &(),/–-]{2,}\s(means|shall\ mean|is|are)\b   # DEFINED TERM means ...
)""", re.VERBOSE)


@dataclass # imported class from the dataclasses library. Quick decorator function to create named fields (i.e. doc.path)
class Chunk:
    index: int # chunk's position in the document: 0, 1, 2, ...
    text: str


def split_blocks(text: str) -> list[str]:
    """ Join wrapped lines into blocks, start a new block at each rule, list or definition.
        Highly customized to the formatting in Colorado ECMC Rules & Regulations.
    """
    blocks: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue # Skip empty lines
        if not blocks or SECTION.match(line) or BREAK.match(line):
            blocks.append(line)
        else:
            blocks[-1] += " " + line # a wrapped line in a block
    return blocks


def chunk_doc(doc: Doc, max_chars: int) -> list[Chunk]:
    """Blocks are combined into chunks ~size of max_chars."""
    pieces: list[str] = []
    title = ""
    current = ""
    for block in split_blocks(doc.text):
        is_section = bool(SECTION.match(block))
        if is_section:
            title = block[:150]
        if current and (is_section or len(current) + len(block) > max_chars):
            pieces.append(current.strip())
            current = "" if is_section else title + "\n"
        current += block + "\n"
    if current.strip():
        pieces.append(current.strip())
    return [Chunk(i, text) for i, text in enumerate(pieces)]

