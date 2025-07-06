# 🦇 Bran Castle Card Manager - Quick Start 🦇

## 5-Minute Setup

1. **Install Python 3.8+** and **pip**

2. **Create a new folder and navigate to it**:
```bash
mkdir bran-castle-cards
cd bran-castle-cards
```

3. **Save all the files**:
   - `app.py` (main application)
   - `requirements.txt`
   - `setup.py`
   - Create `templates/` folder and save:
     - `templates/editor.html`
     - `templates/game.html`

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Run setup** (creates folders and example cards):
```bash
python setup.py
```

6. **Start the application**:
```bash
python app.py
```

7. **Open in browser**: http://localhost:5000

## First Time Use

1. **Click "Settings"**
2. **Add your Gemini API key** (get one at https://makersuite.google.com/app/apikey)
3. **Save Settings**
4. **Click "Generate Cards"**
5. **Choose Night or Day, set quantity (start with 5-10)**
6. **Click Generate**

## Playing the Game

1. **Click "Play Game"** from the editor
2. **Click card backs** to draw cards
3. **Press R** to reset the deck when empty

## Key Features

- **Edit cards**: Click any card in the editor
- **Set likelihood**: 1-10 (higher = more common)
- **Hero requirements**: Cards can require specific heroes
- **Backup**: Click "Backup Cards" regularly

## Keyboard Shortcuts

**Editor**:
- No shortcuts (use mouse)

**Game**:
- **N**: Draw Night card
- **D**: Draw Day card  
- **R**: Reset deck
- **ESC**: Return to card backs

## Tips

- Generate cards in small batches (5-10)
- Review and edit generated cards for balance
- Use hero requirements for variety
- Create backups before major changes

Enjoy creating your haunted deck! 🎴