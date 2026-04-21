const API = "http://127.0.0.1:8000";

async function loadSummary() {
    try {
        const response = await fetch(API + "/session-summary");
        const data = await response.json();

        document.getElementById("duration").innerText = data.duration;
        document.getElementById("events").innerText = data.total_events;
        document.getElementById("avgScore").innerText = data.avg_score;
        document.getElementById("maxScore").innerText = data.max_score;
        document.getElementById("statusSummary").innerText = data.most_common_status;

    } catch (error) {
        console.error("Error loading summary:", error);
    }
}

window.onload = loadSummary;