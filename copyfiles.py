import os, subprocess
from pathlib import Path

# ---- Configuration ----------------------------------------------------------
ROOT = Path(__file__).resolve().parent           # project root
EXCLUDE_DIRS  = {".venv", ".vscode"}
EXCLUDE_FILES = {"copy.py", "copy.bat", "build_static_game.py"}   #  ← added helper
INCLUDE_EXTENSIONS = {".py", ".html"}
# -----------------------------------------------------------------------------


def iter_source_files():
    """Yield (relative_path, full_path) for files we want to copy."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            p = Path(dirpath, name)
            if (
                p.suffix.lower() in INCLUDE_EXTENSIONS
                and name not in EXCLUDE_FILES
            ):
                yield p.relative_to(ROOT), p


def build_clipboard_blob():
    parts = []
    for rel_path, full_path in iter_source_files():
        header = f"\n# ===== {rel_path} =====\n"
        try:
            text = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = "<(Filen kunde inte tolkas som UTF-8 – hoppar över)>"
        parts.append(header + text)
    return "\n".join(parts)


def copy_to_clipboard(text: str):
    subprocess.run("clip", input=text.encode("utf-16le"), check=True)


if __name__ == "__main__":
    blob = build_clipboard_blob()
    copy_to_clipboard(blob)
