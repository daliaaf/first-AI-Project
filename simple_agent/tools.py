# tools.py
from pathlib import Path
import math

MEMORY_FILE = Path("memory.txt")

def remember(content: str) -> str:
    """
    Append a memory entry to memory.txt with a separator line.
    """
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)  # usually ".", but safe
    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(content.strip() + "\n---\n")
    return f"Stored memory entry ({len(content)} chars) in {MEMORY_FILE.resolve()}"


def recall() -> str:
    """
    Read and return all stored memory.
    If no memory exists, return a friendly message.
    """
    if not MEMORY_FILE.exists():
        return "No memory stored yet."
    text = MEMORY_FILE.read_text(encoding="utf-8").strip()
    if not text:
        return "No memory stored yet."
    return f"Stored memory entries:\n{text}"

def write_file(path: str, content: str) -> str:
    p = Path(path)
    p.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} characters to {p.resolve()}"


def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return f"ERROR: file {p} does not exist."
    return p.read_text(encoding="utf-8")


def list_files() -> str:
    p = Path(".")
    files = [str(child) for child in p.iterdir() if child.is_file()]
    if not files:
        return "No files in current directory."
    return "\n".join(files)


def append_file(path: str, content: str) -> str:
    """
    Append content to a file. Create the file if it does not exist.
    """
    p = Path(path)
    with p.open("a", encoding="utf-8") as f:
        f.write(content)
    return f"Appended {len(content)} characters to {p.resolve()}"


def calculate(expression: str) -> str:
    """
    Evaluate a math expression safely using Python's math module.
    Example expressions: '2+2', 'sqrt(16) + 3', 'sin(0.5)**2'
    """
    try:
        allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
        # Disallow builtins
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"ERROR: could not evaluate '{expression}': {e}"


def search_in_file(path: str, query: str) -> str:
    """
    Search for a query string in a file and return matching lines.
    """
    p = Path(path)
    if not p.exists():
        return f"ERROR: file {p} does not exist."

    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    matches = [f"{idx+1}: {line}" for idx, line in enumerate(lines) if query.lower() in line.lower()]

    if not matches:
        return f"No matches for '{query}' in {p}."
    return f"Matches for '{query}' in {p}:\n" + "\n".join(matches)
