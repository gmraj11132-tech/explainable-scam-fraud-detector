/**
 * ScamGuard XAI - Professional Client Controller
 * Multimodal AI Engine & Real-time Web Inspector
 */

let currentInputMode = 'text';
let lastScanId = null;

// Presets Cache
const PRESETS = {
  bank_kyc: "Dear SBI customer, your savings account will be blocked within 24 hours due to pending KYC. Update your PAN immediately at http://sbi-netbanking-kyc-verify.xyz to avoid permanent suspension.",
  electricity_cut: "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM from the power house because your previous month bill was not updated. Please contact our electricity officer at +91 9876543210 immediately.",
  kbc_lottery: "Congratulations! Your mobile number has won Rs 25 Lakh in KBC All India Lucky Draw 2026. Send your bank details to claim on WhatsApp: +91 9123456789.",
  job_offer: "Part-time job offer! Earn Rs 3,000 - 8,000 daily working from home on your phone. Just like and subscribe YouTube videos. Contact HR on WhatsApp: +91 9988776655.",
  legit_bank: "Dear customer, INR 1,500.00 debited from account ending in **4582 on 04-Oct-2026 at Amazon India. Available balance is INR 45,200.00. If not done by you, SMS BLOCK to 567676."
};

// API Key & GPT Engine Management
function getStoredApiKey() {
  return localStorage.getItem('scamguard_openai_key') || '';
}

function updateApiKeyStatus() {
  const key = getStoredApiKey();
  const statusElem = document.getElementById('api-status-text');
  const btn = document.getElementById('api-key-btn');
  if (key) {
    statusElem.textContent = 'GPT-4o Engine Active';
    btn.style.borderColor = 'rgba(16, 185, 129, 0.4)';
    btn.style.color = '#6ee7b7';
  } else {
    statusElem.textContent = 'AI Engine / GPT Key';
    btn.style.borderColor = 'rgba(99, 102, 241, 0.35)';
    btn.style.color = '#c7d2fe';
  }
}

function openApiKeyModal() {
  const modal = document.getElementById('api-modal');
  const input = document.getElementById('modal-api-key-input');
  input.value = getStoredApiKey();
  modal.style.display = 'flex';
}

function closeApiKeyModal() {
  document.getElementById('api-modal').style.display = 'none';
}

function saveApiKey() {
  const input = document.getElementById('modal-api-key-input');
  const key = input.value.trim();
  if (key) {
    localStorage.setItem('scamguard_openai_key', key);
    alert('OpenAI API Key saved! GPT-4o-mini & GPT-4o Vision are now active.');
  } else {
    localStorage.removeItem('scamguard_openai_key');
  }
  updateApiKeyStatus();
  closeApiKeyModal();
}

function clearApiKey() {
  localStorage.removeItem('scamguard_openai_key');
  document.getElementById('modal-api-key-input').value = '';
  updateApiKeyStatus();
  alert('API Key removed. Reverting to local ML & Live Web Inspector.');
  closeApiKeyModal();
}

// Main Tab Navigation
function switchMainTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(content => content.style.display = 'none');

  const selectedBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
  if (selectedBtn) selectedBtn.classList.add('active');

  const targetTab = document.getElementById(`tab-${tabId}`);
  if (targetTab) targetTab.style.display = 'block';

  if (tabId === 'history') {
    loadHistory();
  }
}

// Input Modality Switcher
function switchInputMode(mode) {
  currentInputMode = mode;
  document.querySelectorAll('.mode-pill').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.input-mode-panel').forEach(panel => panel.style.display = 'none');

  const selectedBtn = Array.from(document.querySelectorAll('.mode-pill')).find(b => b.getAttribute('onclick').includes(mode));
  if (selectedBtn) selectedBtn.classList.add('active');

  const targetPanel = document.getElementById(`input-mode-${mode}`);
  if (targetPanel) targetPanel.style.display = 'block';
}

// Update Active Model Tag in Card Header
function updateModelTag() {
  const select = document.getElementById('model-select');
  const tag = document.getElementById('active-model-tag');
  const key = getStoredApiKey();
  if (key) {
    tag.textContent = 'Engine: OpenAI GPT-4o';
  } else {
    tag.textContent = `Model: ${select.value}`;
  }
}

// 1-Click Preset Loader
function loadDemoPreset(presetKey) {
  switchInputMode('text');
  const textInput = document.getElementById('text-input');
  if (PRESETS[presetKey]) {
    textInput.value = PRESETS[presetKey];
    textInput.focus();
  }
}

// Clear Inputs
function clearInputs() {
  document.getElementById('text-input').value = '';
  document.getElementById('url-input').value = '';
  document.getElementById('image-input').value = '';
  document.getElementById('image-preview-box').style.display = 'none';
  document.getElementById('result-content').style.display = 'none';
  document.getElementById('result-placeholder').style.display = 'block';
}

// Image Preview Handler
function previewSelectedImage(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = document.getElementById('image-preview');
      img.src = e.target.result;
      document.getElementById('image-preview-box').style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

// Trigger ML & XAI Scan
async function triggerScan() {
  const btn = document.getElementById('btn-scan');
  const modelName = document.getElementById('model-select').value;
  const apiKey = getStoredApiKey();
  
  btn.disabled = true;
  btn.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="animation: spin 1s linear infinite;"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>
    <span>Analyzing Feature Vectors & Web Context...</span>
  `;

  try {
    let response, data;

    if (currentInputMode === 'text') {
      const text = document.getElementById('text-input').value.trim();
      if (!text) {
        alert('Please enter or select a message to analyze.');
        return;
      }
      response = await fetch('/api/analyze/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, model: modelName, api_key: apiKey })
      });
      data = await response.json();

    } else if (currentInputMode === 'url') {
      const url = document.getElementById('url-input').value.trim();
      if (!url) {
        alert('Please enter a website URL to analyze.');
        return;
      }
      response = await fetch('/api/analyze/url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, api_key: apiKey })
      });
      data = await response.json();

    } else if (currentInputMode === 'image') {
      const fileInput = document.getElementById('image-input');
      if (!fileInput.files || !fileInput.files[0]) {
        alert('Please choose a screenshot image to upload.');
        return;
      }
      const formData = new FormData();
      formData.append('image', fileInput.files[0]);
      formData.append('model', modelName);
      if (apiKey) {
        formData.append('api_key', apiKey);
      }

      response = await fetch('/api/analyze/image', {
        method: 'POST',
        body: formData
      });
      data = await response.json();
    }

    if (!response.ok) {
      throw new Error(data.error || 'Failed to complete scan.');
    }

    renderScanResults(data);

  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <span>Execute Forensic Analysis</span>
    `;
  }
}

// Render Results with Vector Icons & Reasoning Details
function renderScanResults(result) {
  lastScanId = result.scan_id;
  
  document.getElementById('result-placeholder').style.display = 'none';
  const resultContent = document.getElementById('result-content');
  resultContent.style.display = 'block';

  // 1. Verdict Badge with Icon
  const badgeContainer = document.getElementById('verdict-badge-container');
  let iconSvg = '';
  if (result.verdict_badge === 'danger') {
    iconSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
  } else if (result.verdict_badge === 'warning') {
    iconSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
  } else {
    iconSvg = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`;
  }

  const modelInfoTag = result.model_used ? `<span class="version-pill" style="margin-left: 8px;">${result.model_used}</span>` : '';
  badgeContainer.innerHTML = `<span class="verdict-badge ${result.verdict_badge}">${iconSvg}<span>${result.verdict}</span></span>${modelInfoTag}`;

  // 2. Risk Score & Meter
  const riskNum = document.getElementById('risk-number');
  const riskBar = document.getElementById('risk-bar');
  const targetScore = result.risk_score;

  animateValue(riskNum, 0, targetScore, 600);
  riskNum.className = `risk-number ${result.verdict_badge}`;
  
  riskBar.style.width = `${targetScore}%`;
  riskBar.style.backgroundColor = targetScore >= 65 ? '#ef4444' : targetScore >= 30 ? '#f59e0b' : '#10b981';

  // 3. Reasoning Summary Box (if present from GPT)
  let reasoningBox = document.getElementById('reasoning-summary-box');
  if (!reasoningBox) {
    reasoningBox = document.createElement('div');
    reasoningBox.id = 'reasoning-summary-box';
    reasoningBox.style.cssText = 'background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 10px; padding: 12px 14px; margin-bottom: 18px; font-size: 0.8rem; color: #c7d2fe; line-height: 1.5;';
    const meterBox = document.querySelector('.risk-meter-box');
    meterBox.parentNode.insertBefore(reasoningBox, meterBox.nextSibling);
  }
  if (result.reasoning_summary) {
    reasoningBox.style.display = 'block';
    reasoningBox.innerHTML = `<b>AI Forensic Summary:</b> ${result.reasoning_summary}`;
  } else if (result.live_web && result.live_web.page_title) {
    reasoningBox.style.display = 'block';
    reasoningBox.innerHTML = `<b>Live Web Telemetry:</b> Title: <i>"${result.live_web.page_title}"</i> | Reachable: ${result.live_web.is_reachable ? 'Yes' : 'No'} | Redirects: ${result.live_web.is_redirected ? 'Yes' : 'None'}`;
  } else {
    reasoningBox.style.display = 'none';
  }

  // 4. Token Attribution Heatmap
  const tokenCloud = document.getElementById('token-cloud');
  const tokenBox = document.getElementById('token-attribution-box');
  
  if (result.token_weights && result.token_weights.length > 0) {
    tokenBox.style.display = 'block';
    tokenCloud.innerHTML = result.token_weights.map(t => {
      const isScam = t.impact === 'scam';
      const sign = isScam ? '+' : '';
      return `<span class="token-tag ${t.impact}" title="Weight: ${t.weight}">
        <span>${t.word}</span> <span style="opacity: 0.8; font-size: 0.7rem;">(${sign}${t.weight})</span>
      </span>`;
    }).join(' ');
  } else {
    tokenBox.style.display = 'none';
  }

  // 5. Psychological & Deception Signals
  const signalsList = document.getElementById('signals-list');
  if (result.signals && result.signals.length > 0) {
    signalsList.innerHTML = result.signals.map(s => `
      <div class="signal-card ${s.severity}">
        <div class="signal-text">
          <h4>${s.title} (${s.severity} Severity)</h4>
          <p>${s.description}</p>
          ${s.matched_terms ? `<p style="font-size: 0.72rem; color: #f87171; margin-top: 4px;">Triggered Substrings: <code>${s.matched_terms.join(', ')}</code></p>` : ''}
        </div>
      </div>
    `).join('');
  } else if (result.warning_signals && result.warning_signals.length > 0) {
    signalsList.innerHTML = result.warning_signals.map(ws => `
      <div class="signal-card High">
        <div class="signal-text">
          <h4>Security Indicator</h4>
          <p>${ws}</p>
        </div>
      </div>
    `).join('');
  } else {
    signalsList.innerHTML = `
      <div class="signal-card" style="border-left: 3px solid #10b981;">
        <div class="signal-text">
          <h4>No High-Risk Deception Signatures Detected</h4>
          <p>Text adheres to expected syntactic and conversational norms.</p>
        </div>
      </div>
    `;
  }

  // 6. Actionable Recommendations
  const recsList = document.getElementById('recs-list');
  recsList.innerHTML = (result.recommendations || []).map(r => `<li>${r}</li>`).join('');

  if (window.innerWidth < 960) {
    resultContent.scrollIntoView({ behavior: 'smooth' });
  }
}

// Animate Numerical Value
function animateValue(elem, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    elem.textContent = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      elem.textContent = end;
    }
  };
  window.requestAnimationFrame(step);
}

// User Feedback Reporting
async function sendFeedback(type) {
  if (!lastScanId) {
    alert('Please execute a scan first before submitting feedback.');
    return;
  }
  try {
    const res = await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scan_id: lastScanId, feedback_type: type })
    });
    const d = await res.json();
    alert(d.message || 'Telemetry feedback recorded successfully.');
  } catch (e) {
    alert('Could not record feedback.');
  }
}

// Load Forensics Scan History
async function loadHistory() {
  const tbody = document.getElementById('history-table-body');
  try {
    const res = await fetch('/api/history');
    const scans = await res.json();

    if (!scans || scans.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">No entries in SQLite database yet.</td></tr>';
      return;
    }

    tbody.innerHTML = scans.map(s => `
      <tr>
        <td>#${s.id}</td>
        <td style="font-size: 0.75rem; color: var(--text-muted);">${s.timestamp}</td>
        <td><span class="preset-chip" style="padding: 2px 8px; font-size: 0.7rem;">${s.input_type.toUpperCase()}</span></td>
        <td style="max-width: 260px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${s.content_preview}">
          ${s.content_preview}
        </td>
        <td><b style="color: #ffffff;">${s.risk_score}</b>/100</td>
        <td><span class="verdict-badge ${s.verdict_badge}" style="font-size: 0.7rem; padding: 2px 8px;">${s.verdict}</span></td>
        <td style="font-size: 0.74rem;">${s.model_name}</td>
      </tr>
    `).join('');

  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #ef4444;">Error loading telemetry logs.</td></tr>';
  }
}

// Spin Animation Injection
const styleSheet = document.createElement("style");
styleSheet.innerText = `
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
`;
document.head.appendChild(styleSheet);

document.addEventListener('DOMContentLoaded', () => {
  updateApiKeyStatus();
  updateModelTag();
});
