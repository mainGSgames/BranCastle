from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import random
import uuid
from datetime import datetime
from google import genai
from pathlib import Path
import shutil

app = Flask(__name__)

# Configuration
CARDS_DIR = "cards"
NIGHT_CARDS_DIR = os.path.join(CARDS_DIR, "night")
DAY_CARDS_DIR = os.path.join(CARDS_DIR, "day")
BACKUP_DIR = "cards_backup"
CONFIG_FILE = "config.json"

# Ensure directories exist
for directory in [CARDS_DIR, NIGHT_CARDS_DIR, DAY_CARDS_DIR, BACKUP_DIR]:
    os.makedirs(directory, exist_ok=True)

# Game configuration
DEFAULT_CONFIG = {
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

GAME_CONTEXT = """
You are generating cards for \"Bran Castle - Dracula's Domains\", a gothic-horror co-operative board game for 1-6 players.
Cards remain active for exactly six turns (the length of one Day or Night
phase) unless the effect text states they are immediate.

GAME OVERVIEW:
- Players win by destroying all three vampire sisters and Count Dracula
  before drawing 60 cards.
- Players lose if any hero dies or if the pre-chosen draw limit of
  50 / 60 / 70 cards is reached.
- Each game turn: DAY phase (each hero gets 3 actions) ? NIGHT phase
  (draw 1 Night card).
- Heroes reduced to 1-2 HP become infected vampires and must be healed
  with Holy Water whilst in a coffin.

CARD DESIGN RULES:
-1. Effects must reference specific game mechanics (D6 rolls, room names,
    item names, sister names).
-2. Create tactical decisions – players should discuss their best response.
-3. Night cards are often immediate threats/challenges.
-4. Day cards offer risky opportunities or blessings; the active hero may
    be teleported between rooms.
-5. Keep text concise – max 2 sentences for story; then clear mechanics.
-6. Weather MUST influence the effect when relevant.
-7. Each Day or Night card lasts exactly 6 game rounds unless noted.
-8. There are six heroes (listed above) with their signature items.
  
VAMPIRE SISTERS (must be killed before Dracula appears):
- Mary (White) – Spreads mourning & guilt; each of her strikes makes
  heroes lose 1 Willpower. Weak to Garlic.
- Sade (Red) – Seductive domina who dominates minds; drains 2 Health
  in the Master Bedroom and 1 elsewhere. Weak to a Cross.
- Luci (Black) – Dream-weaver causing hallucinations; erodes 1 Sanity.
  Weak to Holy Water.

HEROES & STARTING ITEMS:
- Van Helsing (Cross), Dr Seward (Holy Water), Quincey Morris (Revolver)
- Lord Godalming (Wooden Club), Mina Harker (Garlic), Jonathan Harker (Key)

KEY MECHANICS:
- Memory Search – Flip two face-down cards; if they match, gain that item.
- Combat – Roll D6; results 5-6 hit vampires (items may modify).
- Movement – 1 action to move between connected rooms.
- Health / Sanity / Willpower – tracked on a D6 (1-6); death at 0.

WEATHER EFFECTS (entire round):
- FAIR – No effect.
- STORM – Day loses 1 round, Night gains 1 round, no crafting allowed.
- MIST – Memory Searches succeed only on a D6 roll of 6.
- THUNDER – Cannot stake vampires; Sisters deal +1 damage.

ROOMS IN GAME:
- 1 Catacombs Stairwell ? Dungeon / Crypt
- 2 First-Floor Stairwell ? Entrance Hall / Blood Storage (Dracula here ? +1 Power)
- 3 Second-Floor Stairwell ? Ballroom / Dining Room
- 4 Third-Floor Stairwell ? Great Hall / Library
- 5 Fourth-Floor Stairwell ? First Tower Bedroom / Master Bedroom / Second Tower Bedroom
- 6 Crypt – During Day you may attempt to impale sleeping vampires.
- 7 Dungeon – Dragged outside? You awake here.
- 8 Entrance Hall – All heroes start here at Daybreak.
- 9 Blood Storage – Dracula gains 1 Power when present.
- 10 Ballroom – When heroes meet here, each gains +1 Willpower.
- 11 Dining Room – Spend a turn feasting to heal +1 Health.
- 12 Great Hall – An open space for grand encounters.
- 13 Library – Tomes may reveal secrets (Memory Search gains +1?).
- 14 First Tower Bedroom – Rest heals 1 of Willpower / Sanity / Health.
- 15 Master Bedroom – Sade advances one step closer to resting heroes each
  turn; resting heals 2 points split as desired.
- 16 Second Tower Bedroom – Rest heals 1 of Willpower / Sanity / Health.

ITEMS IN GAME:
- Garlic – Blocks 1 Mary attack.
- Holy Water – Blocks 1 Luci attack, heals +1 HP or cures vampirism.
- Cross – Blocks 1 Sade attack and teleports Sade to the Crypt.
- Wooden Stakes (+Hammer) – Kill sleeping vampires on Will test 5-6.
- Silver-Tipped Stake – Only item that can kill Dracula.
- Revolver – On a 5-6 hit, the vampire is stunned for 1 turn.
"""

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            for key in DEFAULT_CONFIG:
                if key not in config:
                    config[key] = DEFAULT_CONFIG[key]
            return config
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_all_cards(card_type):
    directory = NIGHT_CARDS_DIR if card_type == "night" else DAY_CARDS_DIR
    cards = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                card = json.load(f)
                cards.append(card)
    return sorted(cards, key=lambda x: x.get('created_at', ''))

def get_card_by_id(card_id):
    for card_type in ['night', 'day']:
        directory = NIGHT_CARDS_DIR if card_type == "night" else DAY_CARDS_DIR
        filepath = os.path.join(directory, f"{card_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    return None

def save_card(card_data):
    directory = NIGHT_CARDS_DIR if card_data['type'] == "night" else DAY_CARDS_DIR
    filename = f"{card_data['id']}.json"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(card_data, f, indent=2)

def delete_card(card_id):
    for card_type in ['night', 'day']:
        directory = NIGHT_CARDS_DIR if card_type == "night" else DAY_CARDS_DIR
        filepath = os.path.join(directory, f"{card_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    return False

def generate_card_prompt(card_type, weather, existing_cards, active_heroes):
    # Get titles of existing cards to avoid duplicates
    recent = existing_cards[-10:]             # ðŸ‘ˆ de 10 senaste
    recent_dump = json.dumps(
        [{ "title": c["title"], "effect": c["effect"] } for c in recent],
        indent=2
    )
    
    
    # Build heroes context based on active heroes
    heroes_in_game = []
    if active_heroes.get('van_helsing'): heroes_in_game.append("Van Helsing (Cross)")
    if active_heroes.get('dr_seward'): heroes_in_game.append("Dr Seward (Holy Water)")
    if active_heroes.get('quincey_morris'): heroes_in_game.append("Quincey Morris (Revolver)")
    if active_heroes.get('lord_godalming'): heroes_in_game.append("Lord Godalming (Wooden Club)")
    if active_heroes.get('mina_harker'): heroes_in_game.append("Mina Harker (Garlic)")
    if active_heroes.get('jonathan_harker'): heroes_in_game.append("Jonathan Harker (Key)")
    
    heroes_context = f"Active heroes in this game: {', '.join(heroes_in_game)}"
    
    uniqueness_rules = """
RULES FOR UNIQUENESS
- Do NOT reuse a title that appears under RECENT_CARDS
- Avoid effects or stories with >80 % textual overlap to any RECENT_CARD
"""

    night_instructions = """
NIGHT CARD: Create an immediate threat or challenge. Examples:
- Sister attacks specific rooms
- Movement restrictions  
- Resource drain
- Weather interactions
"""
    
    day_instructions = """
DAY CARD: Create a risky opportunity or double-edged blessing. Examples:
- Found supplies with a catch
- Temporary advantages with costs
- Information about vampire locations
- Weather interactions
"""
    
    specific_instructions = night_instructions if card_type == "night" else day_instructions
    
    prompt = f"""{GAME_CONTEXT}

{heroes_context}

Generate a {card_type.upper()} card with weather: {weather}.

RECENT_CARDS:
{recent_dump}

{uniqueness_rules}

{specific_instructions}

Create a unique card that:
- References specific game elements and active heroes
- Has a brief story (max 2 sentences)
- Has clear mechanical effects
- Considers the current weather ({weather})
- Assigns a likelihood weight (1-10, where 10 is most common)

Respond in JSON:
{{
  "title": "Unique Card Title",
  "story": "Brief atmospheric text.",
  "effect": "Specific game effect",
  "weather": "{weather}",
  "likelihood": 5,
  "required_heroes": []
}}"""
    
    return prompt

@app.route('/')
def index():
    return render_template('editor.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    if request.method == 'GET':
        return jsonify(load_config())
    else:
        config = request.json
        save_config(config)
        return jsonify({"success": True})

@app.route('/api/cards/<card_type>')
def api_cards(card_type):
    if card_type not in ['night', 'day']:
        return jsonify({"error": "Invalid card type"}), 400
    
    cards = get_all_cards(card_type)
    config = load_config()
    active_heroes = config.get('active_heroes', DEFAULT_CONFIG['active_heroes'])
    
    # Filter cards based on required heroes
    filtered_cards = []
    for card in cards:
        required_heroes = card.get('required_heroes', [])
        if all(active_heroes.get(hero, False) for hero in required_heroes):
            filtered_cards.append(card)
    
    return jsonify(filtered_cards)

@app.route('/api/card/<card_id>', methods=['GET', 'PUT', 'DELETE'])
def api_card(card_id):
    if request.method == 'GET':
        card = get_card_by_id(card_id)
        if card:
            return jsonify(card)
        return jsonify({"error": "Card not found"}), 404
    
    elif request.method == 'PUT':
        card_data = request.json
        card_data['id'] = card_id
        card_data['updated_at'] = datetime.now().isoformat()
        save_card(card_data)
        return jsonify({"success": True})
    
    elif request.method == 'DELETE':
        if delete_card(card_id):
            return jsonify({"success": True})
        return jsonify({"error": "Card not found"}), 404

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    card_type = data.get('type', 'night')
    count = data.get('count', 1)
    
    config = load_config()
    api_key = config.get('api_key', '')
    
    if not api_key:
        return jsonify({"error": "API key not configured"}), 400
    
    client = genai.Client(api_key=api_key)
    
    existing_cards = get_all_cards(card_type)
    generated_cards = []
    
    for i in range(count):
        weather = random.choice(['FAIR', 'FAIR', 'FAIR', 'STORM', 'MIST', 'THUNDER', 'CLOUD'])
        prompt = generate_card_prompt(card_type, weather, existing_cards, config['active_heroes'])
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            card_text = response.text
            
            # Extract JSON from response
            start = card_text.find('{')
            end = card_text.rfind('}') + 1
            if start >= 0 and end > start:
                card_data = json.loads(card_text[start:end])
                
                # Add metadata
                card_data['id'] = str(uuid.uuid4())
                card_data['type'] = card_type
                card_data['created_at'] = datetime.now().isoformat()
                card_data['updated_at'] = card_data['created_at']
                
                # Ensure required fields
                card_data['likelihood'] = card_data.get('likelihood', 5)
                card_data['required_heroes'] = card_data.get('required_heroes', [])
                
                save_card(card_data)
                generated_cards.append(card_data)
                existing_cards.append(card_data)
                
        except Exception as e:
            print(f"Error generating card {i+1}: {str(e)}")
            continue
    
    return jsonify({
        "success": True,
        "generated": len(generated_cards),
        "cards": generated_cards
    })

@app.route('/api/draw/<card_type>')
def api_draw(card_type):
    """Draw a random card based on likelihood weights"""
    cards = get_all_cards(card_type)
    config = load_config()
    active_heroes = config.get('active_heroes', DEFAULT_CONFIG['active_heroes'])
    
    # Filter cards based on required heroes
    eligible_cards = []
    for card in cards:
        required_heroes = card.get('required_heroes', [])
        if all(active_heroes.get(hero, False) for hero in required_heroes):
            eligible_cards.append(card)
    
    if not eligible_cards:
        return jsonify({"error": "No eligible cards found"}), 404
    
    # Weight-based selection
    weights = [card.get('likelihood', 5) for card in eligible_cards]
    selected_card = random.choices(eligible_cards, weights=weights, k=1)[0]
    
    return jsonify(selected_card)

@app.route('/api/backup', methods=['POST'])
def api_backup():
    """Create a backup of all cards"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    
    try:
        shutil.copytree(CARDS_DIR, backup_path)
        return jsonify({"success": True, "backup": f"backup_{timestamp}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def api_stats():
    """Get statistics about the card collection"""
    night_cards = get_all_cards('night')
    day_cards = get_all_cards('day')
    
    config = load_config()
    active_heroes = config.get('active_heroes', DEFAULT_CONFIG['active_heroes'])
    
    # Count eligible cards
    eligible_night = sum(1 for card in night_cards 
                        if all(active_heroes.get(hero, False) 
                              for hero in card.get('required_heroes', [])))
    eligible_day = sum(1 for card in day_cards 
                      if all(active_heroes.get(hero, False) 
                            for hero in card.get('required_heroes', [])))
    
    return jsonify({
        "total_night": len(night_cards),
        "total_day": len(day_cards),
        "eligible_night": eligible_night,
        "eligible_day": eligible_day,
        "active_heroes": sum(1 for v in active_heroes.values() if v)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)