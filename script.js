// Handles dashboard navigation, prediction, and Ollama AI advice
document.addEventListener("DOMContentLoaded", () => {
  const predictionBtn = document.getElementById("predictionBtn");
  const statisticsBtn = document.getElementById("statisticsBtn");
  const factTile = document.getElementById("factTile");

  // === Navigation Buttons ===
  if (predictionBtn) predictionBtn.addEventListener("click", () => (window.location.href = "/form"));
  if (statisticsBtn) statisticsBtn.addEventListener("click", () => (window.location.href = "/statistics"));
  if (factTile) fetchFact();

  // === Form Handling ===
  const predictBtn = document.getElementById("predict-btn");
  const askBtn = document.getElementById("ask-btn");

  if (predictBtn) {
    predictBtn.addEventListener("click", async () => {
      const form = document.getElementById("predict-form");
      const formData = new FormData(form);
      const jsonData = {};
      formData.forEach((v, k) => (jsonData[k] = v));

      const resultBox = document.getElementById("result-text");
      resultBox.innerHTML = "⏳ Predicting...";

      try {
        const res = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(jsonData),
        });

        const data = await res.json();

        if (data.error) {
          resultBox.className = "alert alert-danger";
          resultBox.innerHTML = `${data.error}`;
        } else {
          const risk = data.prediction === 1 ? "High Risk" : "Low Risk";
          const prob = (data.probability * 100).toFixed(2);
          resultBox.className = "alert alert-info";
          resultBox.innerHTML = `<strong>${risk}</strong><br>Probability: ${prob}%`;
        }
      } catch (err) {
        resultBox.className = "alert alert-danger";
        resultBox.innerHTML = "Prediction failed. Check console for details.";
        console.error(err);
      }
    });
  }

  if (askBtn) {
    askBtn.addEventListener("click", async () => {
      const form = document.getElementById("predict-form");
      const formData = new FormData(form);
      const jsonData = {};
      formData.forEach((v, k) => (jsonData[k] = v));

      const adviceBox = document.getElementById("advice-text");
      adviceBox.innerHTML = "Asking AI for advice...";

      try {
        const res = await fetch("/ask_ai", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ inputs: jsonData }),
        });

        const data = await res.json();
        adviceBox.className = "alert alert-secondary";
        adviceBox.innerHTML = data.ai_response || "No advice received.";
      } catch (err) {
        adviceBox.className = "alert alert-danger";
        adviceBox.innerHTML = "Could not reach AI.";
        console.error(err);
      }
    });
  }
});

// === Fact Fetching (for dashboard) ===
async function fetchFact() {
  const factTile = document.getElementById("factTile");
  factTile.innerHTML = "<p>Fetching an interesting fact...</p>";

  try {
    const response = await fetch("/get_fact");
    const data = await response.json();
    factTile.innerHTML = `
      <h5 class="fw-semibold">Health Fact</h5>
      <p class="mt-2">${data.fact}</p>
    `;
  } catch (err) {
    factTile.innerHTML = "<p>Unable to fetch fact. Make sure Ollama is running.</p>";
  }
}
