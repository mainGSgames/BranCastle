#!/usr/bin/env python3
"""
Quick setup script for Bran Castle Card Manager
Creates necessary folders and example cards
"""

import os
import json
import uuid
from datetime import datetime

def create_folders():
    """Create necessary folder structure"""
    folders = [
        'templates',
        'cards',
        'cards/night',
        'cards/day',
        'cards_backup'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Created folder: {folder}")

def create_example_cards():
    """Create a few example cards to get started"""
    
    # Example Night Card
    night_card = {
        "id": str(uuid.uuid4()),
        "type": "night",
        "title": "Mary's Mourning",
        "story": "The white sister weeps in the Crypt. Her sorrow spreads like a plague.",
        "effect": "All heroes lose 1 Willpower. Heroes at stairs must move 1 step toward the Crypt.",
        "likelihood": 6,
        "required_heroes": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Example Day Card
    day_card = {
        "id": str(uuid.uuid4()),
        "type": "day",
        "title": "Blessed Ammunition",
        "story": "Hidden in the armory, silver bullets gleam with holy water.",
        "effect": "Quincey Morris gains 3 blessed bullets. These bullets stun vampires for 2 turns instead of 1.",
        "likelihood": 4,
        "required_heroes": ["quincey_morris"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Save example cards
    with open(f'cards/night/{night_card["id"]}.json', 'w') as f:
        json.dump(night_card, f, indent=2)
    print(f"✓ Created example night card: {night_card['title']}")
    
    with open(f'cards/day/{day_card["id"]}.json', 'w') as f:
        json.dump(day_card, f, indent=2)
    print(f"✓ Created example day card: {day_card['title']}")

def create_config():
    """Create default configuration file"""
    config = {
        "api_key": "",
        "deck_size": 60,
        "active_heroes": {
            "van_helsing": True,
            "dr_seward": True,
            "quincey_morris": True,
            "lord_godalming": True,
            "mina_harker": True,
            "jonathan_harker": True
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✓ Created default configuration file")

def main():
    print("🦇 Bran Castle Card Manager Setup 🦇")
    print("=" * 40)
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("⚠️  Warning: app.py not found in current directory!")
        print("   Make sure you've saved all the files before running the app.")
    
    # Create folders
    print("\nCreating folder structure...")
    create_folders()
    
    # Create example cards
    print("\nCreating example cards...")
    create_example_cards()
    
    # Create config
    print("\nCreating configuration...")
    create_config()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Make sure app.py is in this directory")
    print("2. Save editor.html and game.html in the templates/ folder")
    print("3. Run: pip install -r requirements.txt")
    print("4. Run: python app.py")
    print("5. Open http://localhost:5000 in your browser")
    print("6. Add your Gemini API key in Settings")
    print("\nHappy card generating! 🎴")

if __name__ == "__main__":
    main()