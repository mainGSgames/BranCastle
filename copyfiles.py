import os
import subprocess
from pathlib import Path

# ---- Konfiguration ----------------------------------------------------------
# Rotmapp = den mapp där detta skript ligger
ROOT = Path(__file__).resolve().parent

# Kataloger att ignorera  (kan utökas vid behov)
EXCLUDE_DIRS = {".venv", ".vscode"}

# Filer att ignorera
EXCLUDE_FILES = {"copy.py", "copy.bat"}

# Filtyper vi vill ha med
INCLUDE_EXTENSIONS = {".py", ".html"}
# -----------------------------------------------------------------------------


def iter_source_files():
    """Gå igenom projektträdets filer vi bryr oss om."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Ta bort exkluderade mappar direkt – så slipper vi ens gå ned i dem
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for name in filenames:
            p = Path(dirpath, name)
            if (
                p.suffix.lower() in INCLUDE_EXTENSIONS
                and name not in EXCLUDE_FILES
            ):
                yield p.relative_to(ROOT), p


def build_clipboard_blob():
    """Sätt ihop en stor textblob med fil-rubriker."""
    parts = []
    for rel_path, full_path in iter_source_files():
        header = f"\n# ===== {rel_path} =====\n"
        try:
            text = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fångar udda fil med annan encoding – hoppar över med lite sarkasm
            text = "<(Filen kunde inte tolkas som UTF-8 – hoppar över)>"
        parts.append(header + text)
    return "\n".join(parts)


def copy_to_clipboard(text: str):
    """Copy text to Windows clipboard using 'clip' with UTF-16LE encoding."""
    subprocess.run("clip", input=text.encode("utf-16le"), check=True)


if __name__ == "__main__":
    blob = build_clipboard_blob()
    copy_to_clipboard(blob)
