// API URL — change this when deployed!
//const API_URL = "http://127.0.0.1:8000"; // Local server
const API_URL = "https://grammar-guru.onrender.com" // Live server

// ─── Character counter ───
function updateCharCount() {
    const text = document.getElementById("inputText").value;
    const count = text.length;
    const charCount = document.getElementById("charCount");
    charCount.textContent = `${count} / 1000 characters`;

    if (count > 900) {
        charCount.classList.add("warning");
    } else {
        charCount.classList.remove("warning");
    }
}

// ─── Loading messages ───
let loadingTimers = [];

function startLoadingMessages(loading) {
    // Clear any existing timers
    loadingTimers.forEach(timer => clearTimeout(timer));
    loadingTimers = [];

    // Message 1 — immediate
    loading.textContent = "🔍 Checking your grammar...";

    // Message 2 — after 5 seconds
    loadingTimers.push(setTimeout(() => {
        if (loading.style.display === "block") {
            loading.textContent = "⏳ Server is waking up, please wait...";
        }
    }, 5000));

    // Message 3 — after 15 seconds
    loadingTimers.push(setTimeout(() => {
        if (loading.style.display === "block") {
            loading.textContent = "☕ Almost there, just a few more seconds...";
        }
    }, 15000));

    // Message 4 — after 30 seconds
    loadingTimers.push(setTimeout(() => {
        if (loading.style.display === "block") {
            loading.textContent = "🙏 Thank you for your patience, server is starting up...";
        }
    }, 30000));

    // Message 5 — after 60 seconds
    loadingTimers.push(setTimeout(() => {
        if (loading.style.display === "block") {
            loading.textContent = "🚀 Almost ready! Server takes 1-2 min on first load...";
        }
    }, 60000));
}

function stopLoadingMessages() {
    loadingTimers.forEach(timer => clearTimeout(timer));
    loadingTimers = [];
}


// ─── Main function ───
async function checkGrammar() {
    const text = document.getElementById("inputText").value.trim();
    const btn = document.getElementById("checkBtn");
    const loading = document.getElementById("loading");
    const errorBox = document.getElementById("errorBox");
    const results = document.getElementById("results");

    // Hide previous results
    results.style.display = "none";
    errorBox.style.display = "none";
    hideScoreCards();

    // Validate
    if (!text) {
        showError("Please enter some text first!");
        return;
    }

    if (text.length < 10) {
        showError("Text too short! Please write at least 10 characters.");
        return;
    }

    // Show loading
    btn.disabled = true;
    btn.textContent = "⏳ Checking...";
    loading.style.display = "block";
    startLoadingMessages(loading);

    try {
        // Call API
        const response = await fetch(`${API_URL}/check-grammar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        // Check for error
        if (data.error) {
            showError(data.error);
            return;
        }

        // Show results
        displayResults(data);

    } catch (error) {
        showError("Could not connect to server. Please try again in a minute!");
    } finally {
        // Reset button and stop timers
        btn.disabled = false;
        btn.textContent = "✅ Check Grammar";
        loading.style.display = "none";
        stopLoadingMessages();
    }
}


// ─── Display results ───
function displayResults(data) {
    // Corrected text
    document.getElementById("correctedText").textContent = data.corrected;

    // Mistakes list
    const mistakesList = document.getElementById("mistakesList");
    mistakesList.innerHTML = "";

    if (data.mistakes.length === 0) {
        mistakesList.innerHTML = `
            <div class="no-mistakes">
                🎉 No mistakes found! Perfect writing!
            </div>`;
    } else {
        data.mistakes.forEach(mistake => {
            mistakesList.innerHTML += `
                <div class="mistake-item">
                    <span class="wrong">${mistake.mistake}</span>
                    → <span class="correct">${mistake.correction}</span>
                    <div class="explanation">💡 ${mistake.explanation}</div>
                </div>`;
        });
    }

    // Show results section
    document.getElementById("results").style.display = "block";

    // Score card
    const score = data.score.replace("/100", "");
    document.getElementById("scoreNumber").textContent = score;
    document.getElementById("scoreCard").style.display = "block";

    // Mistake count
    document.getElementById("mistakeNumber").textContent = data.mistakes.length;
    document.getElementById("mistakeCount").style.display = "block";

    // Summary
    document.getElementById("summaryText").textContent = data.summary;
    document.getElementById("summaryCard").style.display = "block";
}


// ─── Show error ───
function showError(message) {
    const errorBox = document.getElementById("errorBox");
    errorBox.textContent = message;
    errorBox.style.display = "block";
}


// ─── Hide score cards ───
function hideScoreCards() {
    document.getElementById("scoreCard").style.display = "none";
    document.getElementById("mistakeCount").style.display = "none";
    document.getElementById("summaryCard").style.display = "none";
}