/**
 * PlantGuard AI - Frontend Interactivity & API Client
 */

// DOM Elements
const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const dropPrompt = document.getElementById("dropPrompt");
const previewContainer = document.getElementById("previewContainer");
const imagePreview = document.getElementById("imagePreview");
const removeImageBtn = document.getElementById("removeImageBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeBtnText = document.getElementById("analyzeBtnText");
const emptyResultState = document.getElementById("emptyResultState");
const loadingState = document.getElementById("loadingState");
const resultsContainer = document.getElementById("resultsContainer");

// Diagnostics Elements
const diagnosisBanner = document.getElementById("diagnosisBanner");
const healthBadge = document.getElementById("healthBadge");
const categoryBadge = document.getElementById("categoryBadge");
const diseaseHeading = document.getElementById("diseaseHeading");
const cropName = document.getElementById("cropName");
const pathogenName = document.getElementById("pathogenName");
const confidenceScore = document.getElementById("confidenceScore");
const confidenceBar = document.getElementById("confidenceBar");
const symptomsText = document.getElementById("symptomsText");
const organicList = document.getElementById("organicList");
const chemicalList = document.getElementById("chemicalList");
const preventionList = document.getElementById("preventionList");
const topCandidatesList = document.getElementById("topCandidatesList");

// Tabs
const tabOrganicBtn = document.getElementById("tabOrganicBtn");
const tabChemicalBtn = document.getElementById("tabChemicalBtn");
const tabPreventionBtn = document.getElementById("tabPreventionBtn");
const tabContentOrganic = document.getElementById("tabContentOrganic");
const tabContentChemical = document.getElementById("tabContentChemical");
const tabContentPrevention = document.getElementById("tabContentPrevention");

// Camera Elements
const webcamBtn = document.getElementById("webcamBtn");
const cameraModal = document.getElementById("cameraModal");
const closeCameraBtn = document.getElementById("closeCameraBtn");
const webcamVideo = document.getElementById("webcamVideo");
const webcamCanvas = document.getElementById("webcamCanvas");
const snapPhotoBtn = document.getElementById("snapPhotoBtn");

// Library Elements
const diseaseCardsGrid = document.getElementById("diseaseCardsGrid");
const librarySearchInput = document.getElementById("librarySearchInput");
const plantFilterSelect = document.getElementById("plantFilterSelect");
const categoryFilterSelect = document.getElementById("categoryFilterSelect");
const backendStatusText = document.getElementById("backendStatusText");

// API Configuration Modal Elements
const apiConfigBtn = document.getElementById("apiConfigBtn");
const apiConfigBtnLabel = document.getElementById("apiConfigBtnLabel");
const apiConfigModal = document.getElementById("apiConfigModal");
const closeApiConfigBtn = document.getElementById("closeApiConfigBtn");
const apiBaseUrlInput = document.getElementById("apiBaseUrlInput");
const saveApiBaseUrlBtn = document.getElementById("saveApiBaseUrlBtn");
const resetApiBaseUrlBtn = document.getElementById("resetApiBaseUrlBtn");

let currentFile = null;
let mediaStream = null;
let allDiseases = [];

// ==========================
// 0. API Base URL Resolver
// ==========================
const DEFAULT_PRODUCTION_API_URL = "https://plant-leaf-disease-detection-system-snr3.onrender.com";

function getApiBaseUrl() {
  const custom = localStorage.getItem("plantguard_backend_url");
  if (custom && custom.trim()) {
    return custom.trim().replace(/\/+$/, "");
  }
  // If running locally, use relative path
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    return "";
  }
  // If deployed on Vercel, default directly to live Render backend
  return DEFAULT_PRODUCTION_API_URL;
}

function apiUrl(endpoint) {
  const base = getApiBaseUrl();
  const clean = endpoint.startsWith("/") ? endpoint : "/" + endpoint;
  return base ? `${base}${clean}` : clean;
}

function updateApiConfigUI() {
  const custom = localStorage.getItem("plantguard_backend_url");
  const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
  const activeUrl = custom || (!isLocal ? DEFAULT_PRODUCTION_API_URL : "");

  if (activeUrl) {
    try {
      const u = new URL(activeUrl);
      if (apiConfigBtnLabel) apiConfigBtnLabel.textContent = `API: ${u.hostname.split('.')[0]}`;
    } catch {
      if (apiConfigBtnLabel) apiConfigBtnLabel.textContent = "API: Connected";
    }
    if (apiBaseUrlInput) apiBaseUrlInput.value = activeUrl;
  } else {
    if (apiConfigBtnLabel) apiConfigBtnLabel.textContent = "API: Local";
    if (apiBaseUrlInput) apiBaseUrlInput.value = "";
  }
}

if (apiConfigBtn) {
  apiConfigBtn.addEventListener("click", () => {
    updateApiConfigUI();
    apiConfigModal.classList.remove("hidden");
  });
}

if (closeApiConfigBtn) {
  closeApiConfigBtn.addEventListener("click", () => {
    apiConfigModal.classList.add("hidden");
  });
}

if (saveApiBaseUrlBtn) {
  saveApiBaseUrlBtn.addEventListener("click", () => {
    const val = apiBaseUrlInput.value.trim();
    if (val) {
      localStorage.setItem("plantguard_backend_url", val);
    } else {
      localStorage.removeItem("plantguard_backend_url");
    }
    apiConfigModal.classList.add("hidden");
    updateApiConfigUI();
    checkBackendHealth();
    loadDiseaseEncyclopedia();
  });
}

if (resetApiBaseUrlBtn) {
  resetApiBaseUrlBtn.addEventListener("click", () => {
    localStorage.removeItem("plantguard_backend_url");
    apiBaseUrlInput.value = "";
    apiConfigModal.classList.add("hidden");
    updateApiConfigUI();
    checkBackendHealth();
    loadDiseaseEncyclopedia();
  });
}

// ==========================
// 1. Initialization & Health
// ==========================
async function checkBackendHealth() {
  try {
    const targetUrl = apiUrl("/api/health");
    const res = await fetch(targetUrl);
    if (!res.ok) throw new Error("Backend offline");
    const data = await res.json();
    if (data.model_loaded) {
      backendStatusText.textContent = `PyTorch Neural Engine (${data.device})`;
      backendStatusText.parentElement.classList.remove("text-slate-300");
      backendStatusText.parentElement.classList.add("text-emerald-400");
    } else {
      backendStatusText.textContent = "Simulation Mode (Ready for training)";
    }
  } catch (err) {
    backendStatusText.textContent = "Backend Offline / Check API";
  }
}

async function loadDiseaseEncyclopedia() {
  try {
    const res = await fetch(apiUrl("/api/diseases"));
    if (!res.ok) throw new Error("Could not load encyclopedia");
    const data = await res.json();
    allDiseases = data.diseases || [];

    // Populate plant filter dropdown
    plantFilterSelect.innerHTML = `<option value="">All Crops (${data.available_plants.length})</option>`;
    data.available_plants.forEach(plant => {
      const opt = document.createElement("option");
      opt.value = plant;
      opt.textContent = plant;
      plantFilterSelect.appendChild(opt);
    });

    // Populate category filter dropdown
    categoryFilterSelect.innerHTML = `<option value="">All Categories (${data.available_categories.length})</option>`;
    data.available_categories.forEach(cat => {
      const opt = document.createElement("option");
      opt.value = cat;
      opt.textContent = cat;
      categoryFilterSelect.appendChild(opt);
    });

    renderEncyclopediaCards(allDiseases);
  } catch (err) {
    diseaseCardsGrid.innerHTML = `<p class="col-span-full text-slate-500 text-sm text-center">Unable to load disease encyclopedia from API.</p>`;
  }
}

function renderEncyclopediaCards(diseases) {
  if (!diseases.length) {
    diseaseCardsGrid.innerHTML = `<p class="col-span-full text-slate-400 text-sm text-center py-8">No diseases match your filters.</p>`;
    return;
  }

  diseaseCardsGrid.innerHTML = diseases.map(item => `
    <div class="disease-card bg-slate-800/60 border border-slate-700/60 rounded-2xl p-5 flex flex-col justify-between space-y-4">
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs px-2.5 py-0.5 rounded-full ${item.is_healthy ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'}">
            ${item.is_healthy ? 'Healthy Leaf' : item.category}
          </span>
          <span class="text-xs text-slate-400 font-mono">${item.plant}</span>
        </div>
        <h4 class="font-bold text-base text-slate-100">${item.condition}</h4>
        <p class="text-xs text-slate-400 line-clamp-3">${item.visual_symptoms}</p>
      </div>

      <div class="pt-3 border-t border-slate-700/50 flex items-center justify-between text-xs text-slate-400">
        <span>Pathogen: <em class="text-slate-300">${item.pathogen !== 'None' ? item.pathogen : 'None'}</em></span>
        <button onclick="inspectDisease(${item.class_name ? "'" + item.condition + "'" : ''})" class="text-emerald-400 hover:text-emerald-300 font-medium">
          Details →
        </button>
      </div>
    </div>
  `).join("");
}

// ==========================
// 2. File Upload & Drag-and-Drop
// ==========================
function handleFileSelection(file) {
  if (!file || !file.type.startsWith("image/")) {
    alert("Please select a valid image file (JPG, PNG, WEBP).");
    return;
  }
  currentFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.src = e.target.result;
    dropPrompt.classList.add("hidden");
    previewContainer.classList.remove("hidden");
    analyzeBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length) {
    handleFileSelection(e.target.files[0]);
  }
});

["dragenter", "dragover"].forEach(name => {
  dropZone.addEventListener(name, (e) => {
    e.preventDefault();
    dropZone.classList.add("border-emerald-400", "bg-emerald-950/30");
  });
});

["dragleave", "drop"].forEach(name => {
  dropZone.addEventListener(name, (e) => {
    e.preventDefault();
    dropZone.classList.remove("border-emerald-400", "bg-emerald-950/30");
  });
});

dropZone.addEventListener("drop", (e) => {
  if (e.dataTransfer.files.length) {
    handleFileSelection(e.dataTransfer.files[0]);
  }
});

removeImageBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  currentFile = null;
  fileInput.value = "";
  imagePreview.src = "";
  previewContainer.classList.add("hidden");
  dropPrompt.classList.remove("hidden");
  analyzeBtn.disabled = true;
});

// ==========================
// 3. Camera Snapshot
// ==========================
webcamBtn.addEventListener("click", async () => {
  try {
    cameraModal.classList.remove("hidden");
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
    webcamVideo.srcObject = mediaStream;
  } catch (err) {
    alert("Unable to access camera. Please verify camera permissions in your browser.");
    cameraModal.classList.add("hidden");
  }
});

function stopCamera() {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
  }
  cameraModal.classList.add("hidden");
}

closeCameraBtn.addEventListener("click", stopCamera);

snapPhotoBtn.addEventListener("click", () => {
  if (!webcamVideo.videoWidth) return;
  webcamCanvas.width = webcamVideo.videoWidth;
  webcamCanvas.height = webcamVideo.videoHeight;
  const ctx = webcamCanvas.getContext("2d");
  ctx.drawImage(webcamVideo, 0, 0);

  webcamCanvas.toBlob(blob => {
    const file = new File([blob], "leaf_camera_capture.jpg", { type: "image/jpeg" });
    handleFileSelection(file);
    stopCamera();
  }, "image/jpeg", 0.95);
});

// ==========================
// 4. Quick Sample Generator
// ==========================
document.querySelectorAll(".sample-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const sample = btn.getAttribute("data-sample");
    // Draw synthetic plant leaf canvas for instant testing
    const canvas = document.createElement("canvas");
    canvas.width = 300;
    canvas.height = 300;
    const ctx = canvas.getContext("2d");

    // Background
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(0, 0, 300, 300);

    // Leaf shape
    ctx.beginPath();
    ctx.ellipse(150, 150, 80, 120, Math.PI / 4, 0, 2 * Math.PI);
    ctx.fillStyle = sample.includes("healthy") ? "#16a34a" : "#ca8a04";
    ctx.fill();

    // Leaf veins
    ctx.strokeStyle = "#15803d";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(70, 70);
    ctx.lineTo(230, 230);
    ctx.stroke();

    if (!sample.includes("healthy")) {
      // Lesions
      ctx.fillStyle = "#78350f";
      for (let i = 0; i < 7; i++) {
        ctx.beginPath();
        ctx.arc(100 + i * 15, 120 + (i % 3) * 20, 6 + (i % 4), 0, Math.PI * 2);
        ctx.fill();
      }
    }

    canvas.toBlob(blob => {
      const file = new File([blob], `${sample}.png`, { type: "image/png" });
      handleFileSelection(file);
    });
  });
});

// ==========================
// 5. Run Diagnosis API Call
// ==========================
analyzeBtn.addEventListener("click", async () => {
  if (!currentFile) return;

  // Toggle Loading State
  emptyResultState.classList.add("hidden");
  resultsContainer.classList.add("hidden");
  loadingState.classList.remove("hidden");
  analyzeBtn.disabled = true;
  analyzeBtnText.textContent = "Diagnosing...";

  try {
    const formData = new FormData();
    formData.append("file", currentFile);

    const response = await fetch(apiUrl("/api/predict"), {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Diagnosis failed");
    }

    const data = await response.json();
    displayResults(data);
  } catch (error) {
    alert("Error during diagnosis: " + error.message);
    emptyResultState.classList.remove("hidden");
  } finally {
    loadingState.classList.add("hidden");
    analyzeBtn.disabled = false;
    analyzeBtnText.textContent = "Run Diagnosis";
  }
});

function displayResults(data) {
  const diag = data.diagnosis;
  resultsContainer.classList.remove("hidden");

  // Health / Danger Styling
  if (diag.is_healthy) {
    diagnosisBanner.className = "p-5 rounded-2xl border border-emerald-500/40 bg-emerald-950/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4";
    healthBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
    healthBadge.textContent = "Healthy Crop";
    confidenceBar.className = "bg-emerald-400 h-1.5 rounded-full";
  } else {
    diagnosisBanner.className = "p-5 rounded-2xl border border-rose-500/40 bg-rose-950/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4";
    healthBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/40";
    healthBadge.textContent = `${diag.severity || 'Infected'}`;
    confidenceBar.className = "bg-rose-400 h-1.5 rounded-full";
  }

  categoryBadge.textContent = diag.category;
  diseaseHeading.textContent = diag.condition;
  cropName.textContent = diag.plant;
  pathogenName.textContent = diag.pathogen;

  confidenceScore.textContent = `${diag.confidence}%`;
  confidenceBar.style.width = `${diag.confidence}%`;

  symptomsText.textContent = diag.visual_symptoms;

  // Render Treatment lists
  organicList.innerHTML = diag.organic_treatment && diag.organic_treatment.length
    ? diag.organic_treatment.map(item => `<li>${item}</li>`).join("")
    : "<li>No specific organic treatments required. Maintain standard plant hygiene.</li>";

  chemicalList.innerHTML = diag.chemical_treatment && diag.chemical_treatment.length
    ? diag.chemical_treatment.map(item => `<li>${item}</li>`).join("")
    : "<li>No chemical fungicide or pesticide indicated.</li>";

  preventionList.innerHTML = diag.prevention && diag.prevention.length
    ? diag.prevention.map(item => `<li>${item}</li>`).join("")
    : "<li>Rotate crops and sanitize field equipment regularly.</li>";

  // Top candidates
  topCandidatesList.innerHTML = (data.top_candidates || []).map(cand => `
    <div class="flex items-center justify-between text-xs py-1">
      <span class="text-slate-300">${cand.plant} - ${cand.condition}</span>
      <div class="flex items-center space-x-2">
        <div class="w-24 bg-slate-800 rounded-full h-1.5 overflow-hidden">
          <div class="bg-emerald-400 h-1.5 rounded-full" style="width: ${cand.confidence}%"></div>
        </div>
        <span class="font-mono text-slate-400 w-12 text-right">${cand.confidence}%</span>
      </div>
    </div>
  `).join("");
}

// ==========================
// 6. Tabs Management
// ==========================
function switchTab(activeBtn, activeContent) {
  [tabOrganicBtn, tabChemicalBtn, tabPreventionBtn].forEach(btn => {
    btn.classList.remove("border-emerald-400", "text-emerald-400");
    btn.classList.add("border-transparent", "text-slate-400");
  });
  [tabContentOrganic, tabContentChemical, tabContentPrevention].forEach(c => c.classList.add("hidden"));

  activeBtn.classList.remove("border-transparent", "text-slate-400");
  activeBtn.classList.add("border-emerald-400", "text-emerald-400");
  activeContent.classList.remove("hidden");
}

tabOrganicBtn.addEventListener("click", () => switchTab(tabOrganicBtn, tabContentOrganic));
tabChemicalBtn.addEventListener("click", () => switchTab(tabChemicalBtn, tabContentChemical));
tabPreventionBtn.addEventListener("click", () => switchTab(tabPreventionBtn, tabContentPrevention));

// ==========================
// 7. Library Search & Filters
// ==========================
function applyFilters() {
  const q = librarySearchInput.value.toLowerCase();
  const plant = plantFilterSelect.value;
  const cat = categoryFilterSelect.value;

  const filtered = allDiseases.filter(d => {
    const matchesQ = !q || d.plant.toLowerCase().includes(q) || d.condition.toLowerCase().includes(q) || d.visual_symptoms.toLowerCase().includes(q);
    const matchesPlant = !plant || d.plant === plant;
    const matchesCat = !cat || d.category === cat;
    return matchesQ && matchesPlant && matchesCat;
  });

  renderEncyclopediaCards(filtered);
}

librarySearchInput.addEventListener("input", applyFilters);
plantFilterSelect.addEventListener("change", applyFilters);
categoryFilterSelect.addEventListener("change", applyFilters);

// Boot
updateApiConfigUI();
checkBackendHealth();
loadDiseaseEncyclopedia();

