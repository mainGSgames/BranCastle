// --- Prompt Configuration ---
// This is the main file to edit for game rules and card generation instructions.
// You can change any text inside the backticks (` `).

const GAME_CONTEXT = `
You are generating cards for "Bran Castle - Dracula's Domains", a gothic horror co-operative board game for 1-5 players.

GAME OVERVIEW:
- Players win by destroying all three vampire sisters AND Count Dracula before drawing 60 cards
- Players lose if any hero dies OR 60 cards are drawn
- Each turn: DAY phase (3 actions per hero) then NIGHT phase (draw Night card)
- Heroes become infected vampires at 1-2 HP and must be healed

VAMPIRE SISTERS (must be killed before Dracula appears):
- Mary (White): Causes mourning/guilt, forces heroes to skip turns or lose willpower
- Sade (Red): Dominates minds, drains willpower, turns heroes against each other
- Luci (Black): Dream-weaver, causes hallucinations, makes memory searches harder

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
- CLOUD: Resolved Night card shuffled back into deck

ITEMS IN GAME:
- Garlic: Block 1 vampire attack
- Holy Water: Heal 1 HP or cure vampirism
- Cross: Teleport vampire to different room
- Wooden Stakes: Kill sleeping vampires (need Hammer too)
- Silver-Tipped Stake: Only item that can kill Dracula
- Revolver/Club: Combat items with special abilities

CARD DESIGN RULES:
1. Effects must reference specific game mechanics (D6 rolls, room names, item names, sister names)
2. Create tactical decisions - players should debate best response
3. Night cards are immediate threats/challenges
4. Day cards offer risky opportunities or brief respites
5. Keep text concise - maximum 2 sentences for story, clear mechanical effect
6. Weather MUST affect card resolution when relevant



`;function getCardPrompt(cardType, weather) {
    const nightInstructions = `
NIGHT CARD: Create an immediate threat or challenge. Examples:
- Sister attacks: "Sade appears in [Room], all heroes there lose 2 Willpower"  
- Movement restrictions: "Luci's dreams block the Catacombs until a hero rolls 5+"
- Resource drain: "Mary's mourning - discard 2 items or each hero loses 1 Sanity"
- Weather interaction: If STORM, could affect action economy; if MIST, affect searches


`;    const dayInstructions = `
DAY CARD: Create a risky opportunity or double-edged blessing. Examples:
- Found supplies: "Gain Holy Water, but make a Sanity check (4+) or become infected"
- Temporary advantage: "While Day lasts, +1 to combat rolls but -1 to Willpower"  
- Information: "Glimpse Mary in the Library, but all heroes lose 1 Sanity from her wail"
- Weather interaction: If THUNDER, no staking benefit; if CLOUD, effect might not last



`;    const specificInstructions = cardType === 'night' ? nightInstructions : dayInstructions;

    return `${GAME_CONTEXT}

Generate a ${cardType === 'night' ? 'Night' : 'Day'} card for the game with current weather: ${weather}.

${specificInstructions}

IMPORTANT: 
- Reference specific game elements (room names, sister names, item names, dice rolls)
- Story text: MAX 2 sentences, evocative but brief
- Effect text: Clear, specific, mechanically unambiguous
- Current weather (${weather}) must influence the effect when logical

Respond in this exact JSON format:
{
  "title": "Card Title (3-5 words)",
  "story": "Brief atmospheric text. One or two sentences maximum.",
  "effect": "Specific game effect referencing exact mechanics, rooms, items, or dice rolls",
  "weather": "${weather}"
}`;
}