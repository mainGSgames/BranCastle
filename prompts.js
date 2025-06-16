// --- Prompt Configuration ---
// This is the main file to edit for game rules and card generation instructions.
// You can change any text inside the backticks (` `).

const GAME_CONTEXT = `
You are generating cards for "Bran Castle - Dracula's Domains", a gothic horror co-operative board game for 1-5 players.

GAME OVERVIEW:
- Players win by destroying all three vampire sisters AND Count Dracula before drawing 60 cards
- Players lose if any hero dies OR 50,60, or 70 cards are drawn, determines the number before the game starts
- Each turn: DAY phase (3 actions per hero) then NIGHT phase (draw Night card)
- Heroes become infected vampires at 1-2 HP and must be healed of holy water in the coffin  

VAMPIRE SISTERS (must be killed before Dracula appears):
- Mary (White): Causes mourning/guilt, forces heroes to lose willpower by one
- Mary is weak against garlic 
- Sade (Red): Dominates minds, drains two health in the in master bedroom and one outside, Sade is sexy seduction domina
- Sade is weak against a cross
- Luci (Black): Dream-weaver, causes hallucinations, she wants to harm sanity by one 
- Luci is weak against holy water

HEROES & STARTING ITEMS:
- Van Helsing (Cross), Dr Seward (Holy Water), Quincey Morris (Revolver)
- Lord Godalming (Wooden Club), Mina Harker (Garlic), Jonathan Harker (Key)

KEY MECHANICS:
- Memory Search: Flip 2 face-down cards, if match = gain that item
- Combat: Roll D6, 5-6 hits vampires (some items modify rolls)
- Movement: 1 action to move between connected rooms
- Health/Sanity/Willpower: Tracked on D6 (1-6), death at 0

WEATHER EFFECTS (affect entire round):
- FAIR: No effect
- STORM: Day loses 1 round, Night gains 1 round, no crafting allowed
- MIST: Memory searches only succeed on D6 roll of 6
- THUNDER: Cannot stake vampires, Sisters deal +1 damage


ROOMS IN GAME:
- List room names here.
- Catacombs stairwell nr1: leads to Dungeon or Crypt
- First Floor stairwell nr2: leads to Entrance or Blood Storage, if Dracula is here i got one power
- Second Floor stairwell nr3: leads to Ballroom or Dining Room
- Third Floor stairwell nr4: leads to Great Hall or Library
- Fourth Floor stairwell nr5: leads to First Tower Bedroom or Master Bedroom or Second Tower Bedroom
- Crypt nr6: During six day trips you have a chance to impale vampires
- Dungeon nr7: If Dracula's servants take you outside the castle, you go into the dungeon
- Entrance Hall nr8: Starting position when the game starts in the daytime
- Blood Storage nr9: Dracula gets a power point here
- Ballroom 10: If heroes meet here, they will get a Willpower 
- Dining Room nr11: Stand over a turn and eat and you get a health
- Great Hall nr12 
- Library nr13: In card you can 
- First Tower Bed Room nr14: one rest in First Tower Bedroom heals one optional strength of Willpower, Sanity or Health
- Master Bedroom nr15: The vampire Sade comes at you for every rest one step closer every turn, one turn rest in Master Bedroom heals two optional strength of Willpower, Sanity or Health
- Second Tower Bed Room nr16: one rest in Second Tower Bedroom heals one optional strength of Willpower, Sanity or Health 




ITEMS IN GAME:
- Garlic: Block 1 Mary vampire attack
- Holy Water: Block 1 Luci vampire attack, Heal 1 HP or cure vampirism
- Cross: Block 1 Sade vampire attack and teleport Sade vampire to Crypt room
- Wooden Stakes: Kill sleeping vampires (need Hammer too) and a Will test 5-6 succeed
- Silver-Tipped Stake: Only item that can kill Dracula
- Revolver: Combat items with special abilities, D6 5-6 vampires is stunned for one turn

CARD DESIGN RULES:
-1. Effects must reference specific game mechanics (D6 rolls, room names, item names, sister names)
-2. Create tactical decisions - players should debate best response
-3. Night cards are sometimes immediate threats/challenges
-4. Day cards offer risky opportunities or good events (for the players), current player might be transfered from one room to another
-5. Keep text concise - maximum 2 sentences for story, clear mechanical effect
-6. Weather MUST affect card resolution when relevant
-7. There are six game rounds on a day card.
-8. There are six game rounds on one night card.
-10. A current hero must have a name
`;function getCardPrompt(cardType, weather) {
    const nightInstructions = `
NIGHT CARD: Create an immediate threat or challenge. Examples:
- Sister attacks: "Sade appears in [Room], all heroes there lose 1 Willpower"  
- Movement restrictions: "Luci's dreams block the Catacombs until a hero rolls 5+"
- Resource drain: "Mary's mourning - discard 2 items or each hero loses 1 Sanity"
- Weather interaction: If STORM, could affect action economy; if MIST, affect searches


`;    const dayInstructions = `
DAY CARD: Create a risky opportunity or double-edged blessing. Examples:
- Found supplies: "Gain Holy Water, but make a Sanity check (4+) or become infected"
- Temporary advantage: "While Day lasts, +1 to combat rolls but -1 to Willpower"  
- Information: "All vampires sleep in their coffins, time to kill them"
- Weather interaction: If THUNDER, no staking benefit; if CLOUD, effect might not last



`;    const specificInstructions = cardType === 'night' ? nightInstructions : dayInstructions;

    return `${GAME_CONTEXT}

Generate a ${cardType === 'night' ? 'Night' : 'Day'} card for the game with current weather: ${weather}.

${specificInstructions}

IMPORTANT: 
- Reference specific game elements (room names, sister names, heroes name, item names, dice rolls, will test)
- Story text: MAX 2 sentences, evocative but brief
- Effect text: Clear, specific, mechanically unambiguous
- Current weather (${weather}) must influence the effect when logical
- Concider referencing real historical facts from Bran Castle history and lore

Respond in this exact JSON format:
{
  "title": "Card Title (3-5 words)",
  "story": "Brief atmospheric text. One or two sentences maximum.",
  "effect": "Specific game effect referencing exact mechanics, rooms, items, or dice rolls",
  "weather": "${weather}"
}`;
}