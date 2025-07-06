#!/usr/bin/env python3
"""
Builds a ready-to-serve static bundle of game.html plus the latest cards.

Run locally or in CI:
    python scripts/build_static_game.py

It creates /dist with:
    ├── game.html
    ├── cards/night/index.json  + all *.json
    ├── cards/day/index.json   + all *.json
    └── static/   (images & sfx)
"""
import json, shutil, os, pathlib

ROOT   = pathlib.Path(__file__).resolve().parent.parent
DIST   = ROOT / "dist"
CARDS  = ROOT / "cards"
STATIC = ROOT / "static"
TEMPL  = ROOT / "templates" / "game.html"

def fresh_dir(p: pathlib.Path):
    if p.exists(): shutil.rmtree(p)
    p.mkdir(parents=True)

def copy_cards(card_type: str):
    src = CARDS / card_type
    dst = DIST / "cards" / card_type
    shutil.copytree(src, dst)
    files = sorted(f.name for f in dst.glob("*.json") if f.name != "index.json")
    (dst / "index.json").write_text(json.dumps(files, separators=(",",":")))
    print(f"   • {card_type}: {len(files)} cards")

def main():
    print("🔨  Building static game bundle …")
    fresh_dir(DIST)
    fresh_dir(DIST / "cards")
    copy_cards("night")
    copy_cards("day")
    shutil.copy(TEMPL, DIST / "game.html")
    shutil.copytree(STATIC, DIST / "static")
    print("✅  /dist is ready")

if __name__ == "__main__":
    main()
