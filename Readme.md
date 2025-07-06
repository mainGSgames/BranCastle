# Bran Castle Card Manager

A comprehensive card management system for the board game "Bran Castle - Dracula's Domains". This application allows you to pre-generate, manage, and play with cards stored as JSON files.

## Features

- **Card Editor**: Generate, edit, and delete cards with AI assistance
- **Bulk Generation**: Generate multiple cards at once
- **Card Filtering**: Filter cards based on active heroes in the game
- **Likelihood System**: Set card drawing probabilities (1-10 weight)
- **Unique IDs**: Each card has a trackable UUID
- **Hero Requirements**: Cards can require specific heroes to be in play
- **Backup System**: Create backups of your card collection
- **Game Mode**: Play with your pre-generated cards

## Installation

1. **Install Python** (3.8 or higher)

2. **Install required packages**:
```bash
pip install flask google-generativeai
```

3. **Get a Gemini API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Save it for configuration

## File Structure

```
bran-castle-cards/
├── app.py                 # Main Flask application
├── templates/
│   ├── editor.html       # Card editor interface
│   └── game.html         # Game playing interface
├── cards/                # Card storage (created automatically)
│   ├── night/           # Night cards (JSON files)
│   └── day/             # Day cards (JSON files)
├── cards_backup/         # Backup folder (created automatically)
└── config.json          # Configuration file (created automatically)
```

## Quick Start

1. **Create the folder structure**:
```bash
mkdir bran-castle-cards
cd bran-castle-cards
mkdir templates
```

2. **Save the files**:
   - Save `app.py` in the main folder
   - Save `editor.html` and `game.html` in the `templates` folder

3. **Run the application**:
```bash
python app.py
```

4. **Open in browser**:
   - Go to `http://localhost:5000`
   - The editor will open automatically

5. **Configure settings**:
   - Click the "Settings" button
   - Enter your Gemini API key
   - Set deck size (default: 60)
   - Choose which heroes are in your game

6. **Generate cards**:
   - Click "Generate Cards"
   - Choose card type (Night/Day)
   - Set number of cards to generate
   - Click "Generate"

## Using the Editor

### Generating Cards
1. Click "Generate Cards"
2. Select card type and quantity
3. The AI will generate unique cards based on:
   - Current game rules
   - Active heroes
   - Existing cards (to avoid duplicates)
   - Weather conditions

### Editing Cards
1. Click on any card in the grid
2. Modify:
   - Title
   - Story text
   - Game effect
   - Weather condition
   - Likelihood (1-10)
   - Required heroes
3. Save or delete the card

### Card Properties
- **ID**: Unique identifier (UUID)
- **Title**: Card name
- **Story**: Atmospheric flavor text (max 2 sentences)
- **Effect**: Game mechanics
- **Weather**: FAIR, STORM, MIST, THUNDER, or CLOUD
- **Likelihood**: Drawing weight (1-10, higher = more common)
- **Required Heroes**: Which heroes must be active for this card

## Playing the Game

1. Click "Play Game" from the editor
2. Click on Night or Day card backs to draw
3. Cards are drawn based on:
   - Likelihood weights
   - Active hero requirements
4. Card counter tracks remaining cards
5. Reset deck when empty

### Keyboard Shortcuts
- **N**: Draw Night card
- **D**: Draw Day card
- **R**: Reset deck
- **Escape**: Return cards to back

## Managing Heroes

In Settings, toggle which heroes are in your game:
- Van Helsing (Cross)
- Dr Seward (Holy Water)
- Quincey Morris (Revolver)
- Lord Godalming (Wooden Club)
- Mina Harker (Garlic)
- Jonathan Harker (Key)

Cards can be set to require specific heroes, ensuring appropriate cards are drawn.

## Backup System

Click "Backup Cards" to create a timestamped backup of all cards in the `cards_backup` folder.

## Card Storage

Cards are stored as individual JSON files:
```json
{
  "id": "unique-uuid",
  "type": "night",
  "title": "Mary's Lament",
  "story": "Mournful cries echo through the castle walls.",
  "effect": "All heroes in the Crypt lose 1 Willpower. Heroes at stairs move 1 step toward Mary.",
  "weather": "MIST",
  "likelihood": 6,
  "required_heroes": ["mina_harker"],
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

## Tips

1. **Start Small**: Generate 5-10 cards at a time and review them
2. **Balance**: Mix high and low likelihood cards
3. **Hero-Specific**: Create cards requiring specific heroes for variety
4. **Weather Variety**: Ensure good distribution of weather effects
5. **Regular Backups**: Backup before major changes

## Troubleshooting

- **No cards appearing**: Check if heroes in settings match card requirements
- **Generation fails**: Verify API key is correct and has quota
- **Cards not saving**: Ensure write permissions in the folder

## Customization

Edit the `GAME_CONTEXT` in `app.py` to modify:
- Game rules
- Card generation guidelines
- Character descriptions
- Room layouts
- Item effects

The AI will use this context when generating new cards.