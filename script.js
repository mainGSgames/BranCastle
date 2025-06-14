// --- Global State & Initialization ---
let apiKey = localStorage.getItem('geminiApiKey') || '';
let currentCardData = { night: null, day: null };
let selectedCard = null;
let cardStates = { night: 'back', day: 'back' };
let deckSize = 52; // Default deck size
let cardsLeft = null;
let settings = {
    autoPlayCardFlip: localStorage.getItem('autoPlayCardFlip') !== 'false'
};

document.addEventListener('DOMContentLoaded', () => {
    // Load settings
    if (apiKey) {
        document.getElementById('apiKey').value = apiKey;
    }
    document.getElementById('autoPlayCardFlip').checked = settings.autoPlayCardFlip;

    // Load and initialize card counter
    const storedDeckSize = localStorage.getItem('deckSize');
    if (storedDeckSize) {
        deckSize = parseInt(storedDeckSize, 10);
    }
    document.getElementById('deckSize').value = deckSize;

    const storedCardsLeft = localStorage.getItem('cardsLeft');
    // If cardsLeft is stored and valid, use it. Otherwise, initialize it to the deck size.
    if (storedCardsLeft !== null && !isNaN(parseInt(storedCardsLeft, 10))) {
        cardsLeft = parseInt(storedCardsLeft, 10);
    } else {
        cardsLeft = deckSize;
        localStorage.setItem('cardsLeft', cardsLeft); // Save the initial value
    }
    updateCounterDisplay();

    // Load card back images
    loadCardBackImage('day');
    loadCardBackImage('night');
});

function loadCardBackImage(cardType) {
    const cardBack = document.getElementById(`${cardType}CardBack`);
    const backImage = cardBack.querySelector('img');
    const imagePath = cardType === 'night' ? 'nightcard.png' : 'daycard.png';

    const img = new Image();
    img.onload = () => {
        backImage.src = imagePath;
        backImage.style.display = 'block';
        cardBack.style.background = 'none';
    };
    img.onerror = () => {
        backImage.style.display = 'none';
        cardBack.style.background = cardType === 'night'
            ? 'radial-gradient(circle at center, #1a0a2a 0%, #0a0a1a 50%, #000 100%)'
            : 'radial-gradient(circle at center, #2a1a0a 0%, #1a0a0a 50%, #000 100%)';
    };
    img.src = imagePath;
}

// --- Counter UI ---
function updateCounterDisplay() {
    const counterEl = document.getElementById('cardCounter');
    if (counterEl) {
        counterEl.textContent = `Cards Left: ${cardsLeft}`;
    }
}

// --- Settings & UI ---
function openSettings() { document.getElementById('settingsModal').style.display = 'flex'; }
function closeSettings() { document.getElementById('settingsModal').style.display = 'none'; }
function showLoading(show) { document.getElementById('loading').style.display = show ? 'flex' : 'none'; }

function saveSettings() {
    apiKey = document.getElementById('apiKey').value.trim();
    settings.autoPlayCardFlip = document.getElementById('autoPlayCardFlip').checked;

    localStorage.setItem('geminiApiKey', apiKey);
    localStorage.setItem('autoPlayCardFlip', String(settings.autoPlayCardFlip));

    // Handle deck size change
    const newDeckSizeInput = document.getElementById('deckSize').value;
    const newDeckSize = parseInt(newDeckSizeInput, 10) || 52; // Default to 52 if invalid
    
    // If deck size changes, reset the counter
    if (newDeckSize !== deckSize) {
        deckSize = newDeckSize;
        cardsLeft = deckSize; 
    }
    
    localStorage.setItem('deckSize', deckSize);
    localStorage.setItem('cardsLeft', cardsLeft);
    updateCounterDisplay();

    showError('Settings saved successfully!', false);
    closeSettings();
}

function showError(message, isError = true) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.style.background = isError ? 'rgba(255, 0, 0, 0.1)' : 'rgba(0, 255, 0, 0.1)';
    errorDiv.style.borderColor = isError ? '#ff6b6b' : '#4caf50';
    errorDiv.style.color = isError ? '#ff6b6b' : '#4caf50';
    setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
}

// --- Card Interaction Logic ---
function selectCard(cardType) {
    if (selectedCard === cardType && cardStates[cardType] === 'front') {
        showCardBack(cardType);
        resetToTwoCards();
        return;
    }
    if (selectedCard && selectedCard !== cardType) {
        showCardBack(selectedCard);
    }
    selectAndCenterCard(cardType);
    generateCard(cardType);
}

function selectAndCenterCard(cardType) {
    selectedCard = cardType;
    const nightContainer = document.querySelector('.night-card');
    const dayContainer = document.querySelector('.day-card');
    if (cardType === 'night') {
        nightContainer.classList.add('selected');
        dayContainer.classList.add('hidden');
    } else {
        dayContainer.classList.add('selected');
        nightContainer.classList.add('hidden');
    }
}

function resetToTwoCards() {
    selectedCard = null;
    document.querySelector('.night-card').classList.remove('selected', 'hidden');
    document.querySelector('.day-card').classList.remove('selected', 'hidden');
}

function showCardFront(cardType) {
    if (cardStates[cardType] === 'front') return;
    cardStates[cardType] = 'front';
    const card = document.getElementById(`${cardType}Card`);
    card.classList.add('flipped');
    card.closest('.card-container').classList.add('expanded');
    if (settings.autoPlayCardFlip) playCardFlipSound();
}

function showCardBack(cardType) {
    if (cardStates[cardType] === 'back') return;
    cardStates[cardType] = 'back';
    const card = document.getElementById(`${cardType}Card`);
    card.classList.remove('flipped');
    card.closest('.card-container').classList.remove('expanded');
    currentCardData[cardType] = null;
    const cardContent = document.getElementById(`${cardType}CardContent`);
    const defaultTitle = cardType.charAt(0).toUpperCase() + cardType.slice(1) + ' Card';
    const defaultStory = cardType === 'night' ? 'Click to reveal the nightmares that await...' : 'Click to discover what the day brings...';
    cardContent.innerHTML = `<div class="card-title">${defaultTitle}</div><div class="card-story">${defaultStory}</div>`;
    if (settings.autoPlayCardFlip) playCardFlipSound();
}

function playCardFlipSound() {
    const flipAudio = document.getElementById('flipAudio');
    flipAudio.currentTime = 0;
    flipAudio.play().catch(e => console.log('Card flip sound failed:', e));
}

// --- Core API and Generation Logic ---
async function generateCard(cardType) {
    if (!apiKey) {
        showError('Please set your Gemini API key in settings');
        openSettings();
        resetToTwoCards();
        return;
    }

    if (cardsLeft <= 0) {
        showError('The deck is empty. Reset the deck size in settings to play again.', false);
        resetToTwoCards();
        return;
    }

    showLoading(true);
    const weather = determineWeather();
    // This function now comes from prompts.js
    const prompt = getCardPrompt(cardType, weather); 

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [
                    {
                        role: "user",
                        parts: [{ text: prompt }]
                    }
                ],
                generationConfig: {
                    temperature: 0.8,
                    topK: 64,
                    topP: 0.9,
                    maxOutputTokens: 2000,
                    responseMimeType: "text/plain"
                }
            })
        });
        if (!response.ok) throw new Error((await response.json()).error?.message || 'API request failed');
        const data = await response.json();
        const candidate = data.candidates?.[0];
        if (!candidate) throw new Error('No candidates in API response');
        if (candidate.finishReason === 'MAX_TOKENS') throw new Error('Response was truncated due to token limit. Try again.');
        
        const content = candidate.content?.parts?.[0]?.text;
        if (!content) throw new Error('No text content in API response');
        
        const jsonStr = content.substring(content.indexOf('{'), content.lastIndexOf('}') + 1);
        const cardData = JSON.parse(jsonStr);

        // Decrement counter on successful generation
        cardsLeft--;
        localStorage.setItem('cardsLeft', cardsLeft);
        updateCounterDisplay();
        
        currentCardData[cardType] = cardData;
        displayCard(cardData, cardType);

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to generate card: ${error.message}`);
        showCardBack(cardType);
        resetToTwoCards();
    } finally {
        showLoading(false);
    }
}

function determineWeather() {
    const random = Math.random();
    if (random < 0.67) return 'FAIR';
    const badWeathers = ['STORM', 'MIST', 'THUNDER', 'CLOUD'];
    return badWeathers[Math.floor(Math.random() * badWeathers.length)];
}

function displayCard(cardData, cardType) {
    const cardContent = document.getElementById(`${cardType}CardContent`);
    cardContent.innerHTML = `
        <div class="card-title">${cardData.title}</div>
        <div class="card-story">${cardData.story}</div>
        <div class="card-effect"><strong>Effect:</strong> ${cardData.effect}</div>
        <div class="weather-indicator">Weather: ${cardData.weather}</div>`;
    showCardFront(cardType);
}

// --- Keyboard shortcuts ---
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (document.getElementById('settingsModal').style.display === 'flex') closeSettings();
        else if (selectedCard) {
            showCardBack(selectedCard);
            resetToTwoCards();
        }
    } else if (e.key === 'm' || e.key === 'M') selectCard('night');
    else if (e.key === 'd' || e.key === 'D') selectCard('day');
});