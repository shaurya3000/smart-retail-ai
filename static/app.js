document.addEventListener("DOMContentLoaded", () => {
  fetchDashboardStats();
  setupFaceRecognition();
  setupProductClassifier();
  setupSentimentAnalysis();
  setupChatbot();
});

// Fetch Stats and Update Dashboard Cards
async function fetchDashboardStats() {
  try {
    const response = await fetch("/dashboard/stats");
    if (!response.ok) return;
    const data = await response.json();

    document.getElementById("stat-total-visits").innerText = data.total_visits || 0;

    // Calculate Positive Ratio
    const pos = data.sentiment_breakdown.positive || 0;
    const neg = data.sentiment_breakdown.negative || 0;
    const neu = data.sentiment_breakdown.neutral || 0;
    const totalSent = pos + neg + neu;
    const ratio = totalSent > 0 ? Math.round((pos / totalSent) * 100) : 100;
    document.getElementById("stat-positive-ratio").innerText = `${ratio}%`;

    // Find top product
    const prodCounts = data.product_category_counts || {};
    let topProd = "Shoes";
    let maxC = -1;
    for (const [cat, count] of Object.entries(prodCounts)) {
      if (count > maxC) {
        maxC = count;
        topProd = cat;
      }
    }
    document.getElementById("stat-top-product").innerText = topProd.charAt(0).toUpperCase() + topProd.slice(1);

    // Total bot queries
    const botQueries = Object.values(data.top_chatbot_intents || {}).reduce((a, b) => a + b, 0);
    document.getElementById("stat-bot-queries").innerText = botQueries;

    // Render Visit Log Table
    renderVisitLogs(data.recent_visits || []);
  } catch (err) {
    console.error("Error fetching dashboard stats:", err);
  }
}

function renderVisitLogs(visits) {
  const tbody = document.getElementById("visit-log-rows");
  tbody.innerHTML = "";
  if (visits.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No visits logged yet.</td></tr>`;
    return;
  }
  visits.forEach(v => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong style="color: var(--primary-light);">${v.customer_id}</strong></td>
      <td>${v.name}</td>
      <td><span class="sentiment-badge sentiment-positive">${v.membership}</span></td>
      <td style="color: var(--text-muted);">${v.timestamp}</td>
      <td><span style="color: var(--accent-emerald);">Logged</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// Module A: Face Recognition Setup
function setupFaceRecognition() {
  const dropzone = document.getElementById("face-dropzone");
  const fileInput = document.getElementById("face-file-input");
  const sampleBtn = document.getElementById("btn-sample-face");
  const webcamBtn = document.getElementById("btn-webcam");

  dropzone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) processFaceImage(e.target.files[0]);
  });

  sampleBtn.addEventListener("click", async () => {
    const blob = await createSampleImageBlob("#6366f1", "CUSTOMER FACE");
    processFaceImage(blob);
  });

  webcamBtn.addEventListener("click", async () => {
    const blob = await createSampleImageBlob("#10b981", "WEBCAM SNAPSHOT");
    processFaceImage(blob);
  });
}

async function processFaceImage(fileOrBlob) {
  const preview = document.getElementById("face-preview");
  const resultCard = document.getElementById("face-result-card");
  
  preview.src = URL.createObjectURL(fileOrBlob);
  preview.style.display = "block";

  const formData = new FormData();
  formData.append("file", fileOrBlob, "face.jpg");

  try {
    const response = await fetch("/recognize-face", {
      method: "POST",
      body: formData
    });
    const res = await response.json();

    resultCard.style.display = "block";
    if (res.customer) {
      document.getElementById("customer-name").innerText = res.customer.name;
      document.getElementById("customer-badge").innerText = res.customer.membership;
      document.getElementById("customer-details").innerText = `ID: ${res.customer.customer_id} | Total Visits: ${res.customer.visit_count}`;
      document.getElementById("customer-msg").innerText = res.message;
    }
    fetchDashboardStats();
  } catch (err) {
    console.error("Face recognition error:", err);
  }
}

// Module B: Product Classification Setup
function setupProductClassifier() {
  const dropzone = document.getElementById("product-dropzone");
  const fileInput = document.getElementById("product-file-input");

  dropzone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) processProductImage(e.target.files[0]);
  });
}

async function processProductImage(fileOrBlob) {
  const preview = document.getElementById("product-preview");
  const resultBox = document.getElementById("product-result-box");
  const probList = document.getElementById("prob-bars");
  const categoryHint = document.getElementById("product-category-hint").value;

  preview.src = URL.createObjectURL(fileOrBlob);
  preview.style.display = "block";

  const formData = new FormData();
  formData.append("file", fileOrBlob, fileOrBlob.name || "product.jpg");
  if (categoryHint) {
    formData.append("category_hint", categoryHint);
  }

  try {
    const response = await fetch("/classify-product", {
      method: "POST",
      body: formData
    });
    const res = await response.json();

    resultBox.style.display = "block";
    document.getElementById("pred-cat-name").innerText = res.category.toUpperCase();
    document.getElementById("pred-confidence").innerText = `${(res.confidence * 100).toFixed(1)}% Confidence`;

    probList.innerHTML = "";
    for (const [cat, prob] of Object.entries(res.top_categories)) {
      const pct = (prob * 100).toFixed(1);
      const item = document.createElement("div");
      item.className = "prob-item";
      item.innerHTML = `
        <div class="prob-header">
          <span style="text-transform: capitalize;">${cat}</span>
          <span>${pct}%</span>
        </div>
        <div class="bar-container">
          <div class="bar-fill" style="width: ${pct}%"></div>
        </div>
      `;
      probList.appendChild(item);
    }
    fetchDashboardStats();
  } catch (err) {
    console.error("Product classification error:", err);
  }
}

// Module C: Sentiment Analysis Setup
function setupSentimentAnalysis() {
  const btn = document.getElementById("btn-analyze-sentiment");
  const input = document.getElementById("sentiment-input");
  const resultCard = document.getElementById("sentiment-result-card");

  btn.addEventListener("click", async () => {
    const text = input.value.trim();
    if (!text) return;

    try {
      const response = await fetch("/analyze-sentiment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const res = await response.json();

      resultCard.style.display = "block";
      const badge = document.getElementById("sentiment-label");
      badge.innerText = res.sentiment;
      badge.className = `sentiment-badge sentiment-${res.sentiment}`;
      
      document.getElementById("sentiment-score").innerText = `${(res.confidence * 100).toFixed(1)}%`;
      document.getElementById("sentiment-cleaned").innerText = `Cleaned Tokens: "${res.cleaned_text}"`;
      
      fetchDashboardStats();
    } catch (err) {
      console.error("Sentiment analysis error:", err);
    }
  });
}

// Module D: Support Chatbot Setup
function setupChatbot() {
  const sendBtn = document.getElementById("btn-chat-send");
  const input = document.getElementById("chat-input");

  const sendMessage = async () => {
    const msg = input.value.trim();
    if (!msg) return;

    appendBubble(msg, "user");
    input.value = "";

    try {
      const response = await fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
      });
      const res = await response.json();
      
      appendBubble(res.reply, "bot", `${res.intent} • ${res.source}`);
      fetchDashboardStats();
    } catch (err) {
      appendBubble("Sorry, unable to process your query right now.", "bot", "error");
    }
  };

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
}

function appendBubble(text, sender, meta = "") {
  const chatMessages = document.getElementById("chat-messages");
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;
  bubble.innerText = text;
  
  if (meta && sender === "bot") {
    const metaSpan = document.createElement("div");
    metaSpan.className = "chat-meta";
    metaSpan.innerText = meta;
    bubble.appendChild(metaSpan);
  }
  
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Helper: Generate synthetic sample image Blob using HTML5 Canvas
function createSampleImageBlob(color, text) {
  return new Promise((resolve) => {
    const canvas = document.createElement("canvas");
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, 256, 256);
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 16px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(text, 128, 128);
    canvas.toBlob((blob) => resolve(blob), "image/jpeg");
  });
}
