const API_BASE_URL = '';

// DOM Elements
const form = document.getElementById('predictionForm');
const tickerInput = document.getElementById('tickerInput');
const predictBtn = document.getElementById('predictBtn');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const resultsContainer = document.getElementById('resultsContainer');
const stockChips = document.querySelectorAll('.stock-chip');

// Event Listeners
form.addEventListener('submit', handleSubmit);

stockChips.forEach(chip => {
    chip.addEventListener('click', () => {
        const ticker = chip.getAttribute('data-ticker');
        tickerInput.value = ticker;
        form.dispatchEvent(new Event('submit'));
    });
});

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();

    const ticker = tickerInput.value.trim().toUpperCase();

    if (!ticker) {
        showError('Please enter a stock ticker symbol');
        return;
    }

    await fetchPrediction(ticker);
}

// Fetch prediction from API
async function fetchPrediction(ticker) {
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticker })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch prediction');
        }

        displayResults(data);
    } catch (error) {
        showError(error.message);
    }
}

// Show loading state
function showLoading() {
    loadingState.style.display = 'block';
    errorState.style.display = 'none';
    resultsContainer.style.display = 'none';
    predictBtn.disabled = true;
}

// Show error state
function showError(message) {
    errorMessage.textContent = message;
    errorState.style.display = 'block';
    loadingState.style.display = 'none';
    resultsContainer.style.display = 'none';
    predictBtn.disabled = false;
}

// Display results
function displayResults(data) {
    loadingState.style.display = 'none';
    errorState.style.display = 'none';
    resultsContainer.style.display = 'block';
    predictBtn.disabled = false;

    // Update ticker and price info
    document.getElementById('resultTicker').textContent = data.ticker;

    const priceChange = data.priceChange >= 0 ? '+' : '';
    const priceColor = data.priceChange >= 0 ? 'var(--success)' : 'var(--danger)';

    document.getElementById('priceInfo').innerHTML = `
        <span style="color: ${priceColor}">
            $${data.currentPrice.toFixed(2)} 
            <small>(${priceChange}${data.priceChange.toFixed(2)} / ${priceChange}${data.percentChange.toFixed(2)}%)</small>
        </span>
    `;

    // Update prediction badge
    const predictionBadge = document.getElementById('predictionBadge');
    predictionBadge.textContent = data.prediction;
    predictionBadge.className = `prediction-badge ${data.prediction.toLowerCase()}`;

    // Update stats
    document.getElementById('predictionValue').textContent = data.prediction;
    document.getElementById('confidenceValue').textContent = `${(data.confidence * 100).toFixed(1)}%`;
    document.getElementById('precisionValue').textContent = `${(data.precision * 100).toFixed(1)}%`;

    const changeValue = document.getElementById('changeValue');
    changeValue.textContent = `${priceChange}${data.percentChange.toFixed(2)}%`;
    changeValue.style.color = priceColor;

    // Update indicators
    updateIndicator('sma10', data.indicators.sma10, data.currentPrice);
    updateIndicator('sma50', data.indicators.sma50, data.currentPrice);
    updateRSI(data.indicators.rsi);
    updateVolume(data.indicators.volume);

    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Update indicator bars
function updateIndicator(name, value, currentPrice) {
    const valueElement = document.getElementById(`${name}Value`);
    const barElement = document.getElementById(`${name}Bar`);

    valueElement.textContent = `$${value.toFixed(2)}`;

    // Calculate percentage for bar (relative to current price)
    const percentage = Math.min((value / currentPrice) * 100, 100);
    barElement.style.width = `${percentage}%`;
}

// Update RSI indicator
function updateRSI(rsi) {
    const valueElement = document.getElementById('rsiValue');
    const barElement = document.getElementById('rsiBar');

    valueElement.textContent = rsi.toFixed(2);
    barElement.style.width = `${rsi}%`;

    // Color based on RSI zones
    if (rsi < 30) {
        barElement.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    } else if (rsi > 70) {
        barElement.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    } else {
        barElement.style.background = 'var(--accent-gradient)';
    }
}

// Update volume indicator
function updateVolume(volume) {
    const valueElement = document.getElementById('volumeValue');
    const barElement = document.getElementById('volumeBar');

    // Format volume
    const formatted = formatVolume(volume);
    valueElement.textContent = formatted;

    // Animate bar height (random height for visual effect since we don't have historical data)
    const height = Math.random() * 60 + 40; // 40-100%
    barElement.style.height = `${height}%`;
}

// Format large numbers
function formatVolume(num) {
    if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    }
    if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    }
    if (num >= 1e3) {
        return (num / 1e3).toFixed(2) + 'K';
    }
    return num.toString();
}

// Add keyboard shortcut (Enter to submit)
tickerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        form.dispatchEvent(new Event('submit'));
    }
});

// Auto-focus input on load
window.addEventListener('load', () => {
    tickerInput.focus();
});
