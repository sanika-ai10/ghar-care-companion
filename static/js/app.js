/**
 * Recovery Companion — Frontend Client
 * Handles file selection, language selection, API communication,
 * DOM rendering of the recovery plan, and browser speech synthesis.
 */

// Application State
const state = {
  selectedFile: null,
  selectedLanguage: 'English',
  demoMode: false,
  currentPlan: null,
  isSpeaking: false,
  speechUtterance: null,
};

// DOM Elements
const elements = {
  // Config & Header
  demoModeToggle: document.getElementById('demoModeToggle'),
  
  // Sections
  uploadSection: document.getElementById('uploadSection'),
  loadingSection: document.getElementById('loadingSection'),
  errorSection: document.getElementById('errorSection'),
  planSection: document.getElementById('planSection'),
  
  // Language & Upload
  langOptions: document.querySelectorAll('.lang-option'),
  dropzone: document.getElementById('dropzone'),
  dropzoneEmpty: document.getElementById('dropzoneEmpty'),
  dropzonePreview: document.getElementById('dropzonePreview'),
  fileInput: document.getElementById('fileInput'),
  imagePreview: document.getElementById('imagePreview'),
  fileName: document.getElementById('fileName'),
  fileSize: document.getElementById('fileSize'),
  removeFileBtn: document.getElementById('removeFileBtn'),
  useSampleBtn: document.getElementById('useSampleBtn'),
  submitBtn: document.getElementById('submitBtn'),
  
  // Loading & Error
  loadingStatusTitle: document.getElementById('loadingStatusTitle'),
  errorHeading: document.getElementById('errorHeading'),
  errorMessage: document.getElementById('errorMessage'),
  retryUploadBtn: document.getElementById('retryUploadBtn'),
  fallbackSampleBtn: document.getElementById('fallbackSampleBtn'),
  
  // Plan Toolbar & Status
  readAloudBtn: document.getElementById('readAloudBtn'),
  ttsStopBtn: document.getElementById('ttsStopBtn'),
  ttsBtnText: document.getElementById('ttsBtnText'),
  ttsStatusBar: document.getElementById('ttsStatusBar'),
  ttsStatusText: document.getElementById('ttsStatusText'),
  planDemoBadge: document.getElementById('planDemoBadge'),
  newPlanBtn: document.getElementById('newPlanBtn'),
  bottomNewPlanBtn: document.getElementById('bottomNewPlanBtn'),
  
  // Plan Display Elements
  patientNameHeader: document.getElementById('patientNameHeader'),
  dischargeDateBadge: document.getElementById('dischargeDateBadge'),
  docTypeBadge: document.getElementById('docTypeBadge'),
  careProfileContainer: document.getElementById('careProfileContainer'),
  diagnosisText: document.getElementById('diagnosisText'),
  procedureRow: document.getElementById('procedureRow'),
  procedureText: document.getElementById('procedureText'),
  plainSummaryText: document.getElementById('plainSummaryText'),
  
  // Medicines
  medicineCountBadge: document.getElementById('medicineCountBadge'),
  medFilters: document.getElementById('medFilters'),
  medicineList: document.getElementById('medicineList'),
  
  // Followups
  followupList: document.getElementById('followupList'),
  
  // Red Flags
  redFlagList: document.getElementById('redFlagList'),
  
  // Uncertainties
  uncertainItemList: document.getElementById('uncertainItemList'),
  missingInfoList: document.getElementById('missingInfoList'),
  
  // Monitoring & Extras
  monitoringList: document.getElementById('monitoringList'),
  dietActivityBox: document.getElementById('dietActivityBox'),
  dietList: document.getElementById('dietList'),
  contactsBox: document.getElementById('contactsBox'),
  contactList: document.getElementById('contactList'),
};

// Initialization
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await checkServerConfig();
});

async function checkServerConfig() {
  try {
    const res = await fetch('/api/config');
    if (res.ok) {
      const config = await res.json();
      state.demoMode = Boolean(config.demo_mode);
      if (elements.demoModeToggle) {
        elements.demoModeToggle.checked = state.demoMode;
      }
    }
  } catch (err) {
    console.warn('Could not fetch server config, defaulting to local state:', err);
  }
}

function setupEventListeners() {
  // Demo Mode Switch
  if (elements.demoModeToggle) {
    elements.demoModeToggle.addEventListener('change', (e) => {
      state.demoMode = e.target.checked;
    });
  }

  // Language Radio Pill Selector
  elements.langOptions.forEach((option) => {
    option.addEventListener('click', () => {
      elements.langOptions.forEach((o) => o.classList.remove('active'));
      option.classList.add('active');
      const radio = option.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
        state.selectedLanguage = radio.value;
      }
    });
  });

  // Dropzone Interaction
  elements.dropzone.addEventListener('click', (e) => {
    if (e.target.id === 'removeFileBtn') return;
    elements.fileInput.click();
  });

  elements.fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFileSelected(file);
  });

  // Drag and Drop
  ['dragenter', 'dragover'].forEach((eventName) => {
    elements.dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      elements.dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach((eventName) => {
    elements.dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      elements.dropzone.classList.remove('dragover');
    });
  });

  elements.dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelected(files[0]);
    }
  });

  // Remove File Button
  elements.removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    clearSelectedFile();
  });

  // Use Sample Document Button
  elements.useSampleBtn.addEventListener('click', () => {
    loadSamplePlan(state.selectedLanguage);
  });

  // Submit Button
  elements.submitBtn.addEventListener('click', submitDocument);

  // Error Section Action Buttons
  elements.retryUploadBtn.addEventListener('click', () => {
    showUploadSection();
    elements.fileInput.click();
  });

  elements.fallbackSampleBtn.addEventListener('click', () => {
    loadSamplePlan(state.selectedLanguage);
  });

  // Navigation / Retake Buttons
  [elements.newPlanBtn, elements.bottomNewPlanBtn].forEach((btn) => {
    if (btn) {
      btn.addEventListener('click', () => {
        stopSpeech();
        showUploadSection();
      });
    }
  });

  // Medicine Filter Tabs
  if (elements.medFilters) {
    elements.medFilters.addEventListener('click', (e) => {
      const btn = e.target.closest('.med-filter-btn');
      if (!btn) return;
      document.querySelectorAll('.med-filter-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      filterMedicines(filter);
    });
  }

  // TTS Read Aloud Buttons
  elements.readAloudBtn.addEventListener('click', toggleSpeech);
  elements.ttsStopBtn.addEventListener('click', stopSpeech);
}

// File Selection Handlers
function handleFileSelected(file) {
  if (!file.type.startsWith('image/')) {
    alert('Please select an image file (JPEG, PNG, WEBP).');
    return;
  }
  state.selectedFile = file;

  // Update preview
  elements.fileName.textContent = file.name;
  elements.fileSize.textContent = formatBytes(file.size);

  const reader = new FileReader();
  reader.onload = (e) => {
    elements.imagePreview.src = e.target.result;
    elements.dropzoneEmpty.classList.add('hidden');
    elements.dropzonePreview.classList.remove('hidden');
  };
  reader.readAsDataURL(file);
}

function clearSelectedFile() {
  state.selectedFile = null;
  elements.fileInput.value = '';
  elements.imagePreview.src = '';
  elements.dropzonePreview.classList.add('hidden');
  elements.dropzoneEmpty.classList.remove('hidden');
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Submit Document to Backend API
async function submitDocument() {
  // If demo mode is active and no file was uploaded, use sample response
  if (state.demoMode && !state.selectedFile) {
    await loadSamplePlan(state.selectedLanguage);
    return;
  }

  if (!state.selectedFile && !state.demoMode) {
    alert('Please take or upload a photo of your medical document, or enable Demo Mode.');
    return;
  }

  showLoadingSection();

  const formData = new FormData();
  if (state.selectedFile) {
    formData.append('file', state.selectedFile);
  }
  formData.append('language', state.selectedLanguage);
  if (state.demoMode) {
    formData.append('demo_mode', 'true');
  }

  try {
    const response = await fetch('/api/extract', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();

    if (response.ok && result.status === 'success') {
      renderRecoveryPlan(result.data, Boolean(result.demo_mode));
    } else {
      // Handles requirement 6: "Please retake the photo"
      const errorMsg = result.detail || result.message || 'Please retake the photo';
      showErrorSection(errorMsg);
    }
  } catch (err) {
    console.error('Extraction request failed:', err);
    showErrorSection('Please retake the photo. Ensure adequate lighting and camera focus.');
  }
}

// Direct Sample Plan Loader
async function loadSamplePlan(language) {
  showLoadingSection();
  try {
    const res = await fetch(`/api/sample/${language.toLowerCase()}`);
    if (res.ok) {
      const json = await res.json();
      renderRecoveryPlan(json.data, true);
    } else {
      showErrorSection('Failed to load sample plan. Please try again.');
    }
  } catch (err) {
    console.error('Sample fetch error:', err);
    showErrorSection('Could not connect to server.');
  }
}

// View State Switchers
function showUploadSection() {
  elements.uploadSection.classList.remove('hidden');
  elements.loadingSection.classList.add('hidden');
  elements.errorSection.classList.add('hidden');
  elements.planSection.classList.add('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showLoadingSection() {
  elements.uploadSection.classList.add('hidden');
  elements.loadingSection.classList.remove('hidden');
  elements.errorSection.classList.add('hidden');
  elements.planSection.classList.add('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showErrorSection(message) {
  elements.uploadSection.classList.add('hidden');
  elements.loadingSection.classList.add('hidden');
  elements.errorSection.classList.remove('hidden');
  elements.planSection.classList.add('hidden');

  if (message.toLowerCase().includes('retake')) {
    elements.errorHeading.textContent = 'Please retake the photo';
    elements.errorMessage.textContent = message;
  } else {
    elements.errorHeading.textContent = 'Unable to Process Document';
    elements.errorMessage.textContent = message;
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showPlanSection() {
  elements.uploadSection.classList.add('hidden');
  elements.loadingSection.classList.add('hidden');
  elements.errorSection.classList.add('hidden');
  elements.planSection.classList.remove('hidden');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Render Recovery Plan
function renderRecoveryPlan(plan, isDemo = false) {
  state.currentPlan = plan;

  // Demo badge visibility
  if (isDemo) {
    elements.planDemoBadge.classList.remove('hidden');
  } else {
    elements.planDemoBadge.classList.add('hidden');
  }

  // 1. Patient & Summary
  const name = plan.patient_first_name ? plan.patient_first_name : 'Patient';
  elements.patientNameHeader.textContent = `${name}'s Recovery Plan`;

  elements.dischargeDateBadge.textContent = plan.discharge_date
    ? `Discharged: ${plan.discharge_date}`
    : 'Discharged Recently';

  const docTypeNames = {
    discharge_summary: 'Discharge Summary',
    prescription: 'Prescription',
    lab_report: 'Lab Report',
    other: 'Medical Document',
  };
  elements.docTypeBadge.textContent = docTypeNames[plan.document_type] || 'Medical Document';

  // Care profile tags
  elements.careProfileContainer.innerHTML = '';
  if (Array.isArray(plan.care_profile)) {
    plan.care_profile.forEach((tag) => {
      const span = document.createElement('span');
      span.className = 'care-tag';
      span.textContent = formatCareTag(tag);
      elements.careProfileContainer.appendChild(span);
    });
  }

  elements.diagnosisText.textContent = plan.diagnosis_plain || 'Not specified in document';

  if (plan.procedure_plain) {
    elements.procedureRow.classList.remove('hidden');
    elements.procedureText.textContent = plan.procedure_plain;
  } else {
    elements.procedureRow.classList.add('hidden');
  }

  elements.plainSummaryText.textContent = plan.summary_plain || '';

  // 2. Medicines
  window.__patientName = plan.patient_first_name || 'The patient';
  renderMedicines(plan.medicines || []);

  // 3. Follow-ups
  renderFollowups(plan.follow_ups || []);

  // 4. Warning Signs (Red Flags)
  renderRedFlags(plan.red_flags || []);

  // 5. Uncertainties & Missing Info
  renderUncertainties(plan.uncertain_items || [], plan.missing_info || []);

  // 6. Monitoring & Contacts
  renderMonitoring(plan.monitoring || []);
  renderDietAndActivity(plan.diet_and_activity || []);
  renderContacts(plan.contacts || []);

  // Switch to plan view
  showPlanSection();
}

function formatCareTag(tag) {
  const map = {
    post_surgery: 'Post Surgery 🏥',
    cardiac: 'Cardiac Care ❤️',
    hypertension: 'Blood Pressure 🩺',
    diabetes: 'Diabetes Care 🩸',
    respiratory: 'Respiratory 🫁',
    kidney: 'Kidney Care 💧',
    infection: 'Infection Recovery 🩹',
    maternity: 'Maternity 👶',
    orthopedic: 'Bone & Joints 🦴',
    neurological: 'Neurology 🧠',
    other: 'General Care 📋',
  };
  return map[tag] || tag.replace('_', ' ');
}

// Render Medicines
function renderMedicines(medicines) {
  elements.medicineCountBadge.textContent = `${medicines.length} Medicine${medicines.length === 1 ? '' : 's'}`;
  elements.medicineList.innerHTML = '';

  if (!medicines || medicines.length === 0) {
    elements.medicineList.innerHTML = '<p class="text-muted">No medicines listed in this document.</p>';
    return;
  }

  medicines.forEach((med, idx) => {
    const card = document.createElement('div');
    card.className = `med-card ${med.is_critical ? 'critical' : ''}`;
    card.dataset.index = idx;
    card.dataset.times = JSON.stringify(med.times_of_day || []);
    card.dataset.asNeeded = med.as_needed ? 'true' : 'false';

    // Clock times / Frequency chips
    const clockTimesStr = (med.suggested_clock_times || []).join(', ');
    const timesChip = clockTimesStr ? `⏰ ${clockTimesStr}` : `🔄 ${med.frequency_as_written || 'As directed'}`;

    // Food instruction
    const foodLabels = {
      before: '🍽️ Before Food (AC)',
      after: '🍽️ After Food (PC)',
      with: '🍽️ With Meals',
      any: '🍽️ With or without food',
      unknown: '🍽️ Check with pharmacist',
    };
    const foodChip = foodLabels[med.with_food] || '🍽️ With food';

    card.innerHTML = `
      <div class="med-header">
        <div>
          <h4 class="med-name">${escapeHtml(med.name_as_written)}</h4>
          <span class="file-size">${escapeHtml(med.form || '')} • ${escapeHtml(med.dose || '')}</span>
        </div>
        <div class="med-badges">
          ${med.is_critical ? '<span class="badge-critical">⚠️ Important: Do not miss</span>' : ''}
          ${med.confidence === 'low' ? '<span class="badge-confidence-low">Confirm with Doctor</span>' : ''}
        </div>
      </div>

      <div class="med-schedule-row">
        <span class="time-chip">${escapeHtml(timesChip)}</span>
        <span class="food-chip">${escapeHtml(foodChip)}</span>
        ${med.duration_as_written ? `<span class="time-chip">📅 ${escapeHtml(med.duration_as_written)}</span>` : ''}
      </div>

      <p class="med-purpose"><strong>Why you take this:</strong> ${escapeHtml(med.purpose_plain || 'Not specified')}</p>

      ${med.special_instructions_plain ? `
        <div class="med-notes">
          💡 <strong>Special note:</strong> ${escapeHtml(med.special_instructions_plain)}
        </div>
      ` : ''}
    `;

    addDoseButtons(card, med);
    elements.medicineList.appendChild(card);
  });
}

// Filter Medicines by Time of Day
function filterMedicines(filter) {
  const cards = elements.medicineList.querySelectorAll('.med-card');
  cards.forEach((card) => {
    if (filter === 'all') {
      card.classList.remove('hidden');
      return;
    }

    const times = JSON.parse(card.dataset.times || '[]');
    const isAsNeeded = card.dataset.asNeeded === 'true';

    if (filter === 'as_needed') {
      card.classList.toggle('hidden', !isAsNeeded);
    } else if (filter === 'morning') {
      card.classList.toggle('hidden', !times.includes('morning'));
    } else if (filter === 'afternoon') {
      card.classList.toggle('hidden', !times.includes('afternoon'));
    } else if (filter === 'evening_night') {
      card.classList.toggle('hidden', !times.includes('evening') && !times.includes('night'));
    }
  });
}

// Render Followups
function renderFollowups(followups) {
  elements.followupList.innerHTML = '';
  if (!followups || followups.length === 0) {
    elements.followupList.innerHTML = '<p class="text-muted">No specific follow-up appointments mentioned in document.</p>';
    return;
  }

  followups.forEach((f) => {
    const card = document.createElement('div');
    card.className = 'followup-card';

    const timing = f.date
      ? `📅 ${f.date}`
      : (f.date_as_written ? `⏱️ ${f.date_as_written}` : (f.relative_days_from_discharge ? `⏱️ In ${f.relative_days_from_discharge} days` : ''));

    card.innerHTML = `
      <h4 class="followup-title">${escapeHtml(f.what_plain || 'Follow-up visit')}</h4>
      <div class="followup-meta">
        ${timing ? `<span><strong>When:</strong> ${escapeHtml(timing)}</span>` : ''}
        ${f.doctor_or_clinic ? `<span><strong>Where:</strong> ${escapeHtml(f.doctor_or_clinic)}</span>` : ''}
      </div>
      ${f.what_to_bring_plain ? `
        <div class="followup-bring">
          💼 <strong>What to bring:</strong> ${escapeHtml(f.what_to_bring_plain)}
        </div>
      ` : ''}
    `;
    elements.followupList.appendChild(card);
  });
}

// Render Warning Signs (Red Flags)
function renderRedFlags(redFlags) {
  elements.redFlagList.innerHTML = '';
  if (!redFlags || redFlags.length === 0) {
    elements.redFlagList.innerHTML = '<p class="text-muted">No explicit emergency red flags noted in document.</p>';
    return;
  }

  redFlags.forEach((rf) => {
    const item = document.createElement('div');
    const isEmergency = rf.urgency === 'emergency';
    item.className = `red-flag-item ${isEmergency ? 'emergency' : 'call_doctor'}`;

    const badgeLabel = isEmergency ? '🚨 Emergency' : '📞 Call Doctor';

    item.innerHTML = `
      <div class="rf-header">
        <span class="rf-badge ${isEmergency ? 'emergency' : 'call_doctor'}">${badgeLabel}</span>
      </div>
      <p class="rf-symptom">⚠️ ${escapeHtml(rf.symptom_plain)}</p>
      <p class="rf-action"><strong>Action:</strong> ${escapeHtml(rf.action)}</p>
    `;
    elements.redFlagList.appendChild(item);
  });
}

// Render Uncertainties & Missing Info
function renderUncertainties(uncertainItems, missingInfo) {
  elements.uncertainItemList.innerHTML = '';
  elements.missingInfoList.innerHTML = '';

  if (uncertainItems.length === 0) {
    elements.uncertainItemList.innerHTML = '<p class="file-size" style="color: #64748b;">No unclear items detected in this document.</p>';
  } else {
    uncertainItems.forEach((item) => {
      const box = document.createElement('div');
      box.className = 'uncertain-item-box';
      box.innerHTML = `
        <p class="uncertain-source">"${escapeHtml(item.text)}":</p>
        <p class="uncertain-reason">⚠️ ${escapeHtml(item.reason)}</p>
      `;
      elements.uncertainItemList.appendChild(box);
    });
  }

  if (missingInfo.length === 0) {
    elements.missingInfoList.innerHTML = '<p class="file-size" style="color: #64748b;">All expected recovery details were present.</p>';
  } else {
    missingInfo.forEach((info) => {
      const box = document.createElement('div');
      box.className = 'missing-item-box';
      box.innerHTML = `<span>ℹ️ ${escapeHtml(info)}</span>`;
      elements.missingInfoList.appendChild(box);
    });
  }
}

// Render Monitoring & Diet
function renderMonitoring(monitoring) {
  elements.monitoringList.innerHTML = '';
  if (!monitoring || monitoring.length === 0) {
    elements.monitoringList.innerHTML = '<p class="text-muted" style="grid-column: 1/-1;">No home monitoring tests prescribed.</p>';
    return;
  }

  monitoring.forEach((m) => {
    const card = document.createElement('div');
    card.className = 'mon-card';
    card.innerHTML = `
      <p class="mon-label">${escapeHtml(m.label_plain || m.parameter)}</p>
      <p class="mon-freq">${escapeHtml(m.frequency_as_written || 'Daily')}</p>
      ${m.target_range ? `<p class="mon-range">Target: ${escapeHtml(m.target_range)}</p>` : ''}
      ${m.alert_thresholds ? `<p class="file-size" style="color: #b91c1c;">Alert if: ${escapeHtml(m.alert_thresholds)}</p>` : ''}
    `;
    elements.monitoringList.appendChild(card);
  });
}

function renderDietAndActivity(dietList) {
  elements.dietList.innerHTML = '';
  if (!dietList || dietList.length === 0) {
    elements.dietActivityBox.classList.add('hidden');
    return;
  }
  elements.dietActivityBox.classList.remove('hidden');
  dietList.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    elements.dietList.appendChild(li);
  });
}

function renderContacts(contacts) {
  elements.contactList.innerHTML = '';
  if (!contacts || contacts.length === 0) {
    elements.contactsBox.classList.add('hidden');
    return;
  }
  elements.contactsBox.classList.remove('hidden');
  contacts.forEach((c) => {
    const a = document.createElement('a');
    a.className = 'contact-chip';
    a.href = `tel:${c.number.replace(/[^0-9+]/g, '')}`;
    a.innerHTML = `📞 <strong>${escapeHtml(c.label)}:</strong> ${escapeHtml(c.number)}`;
    elements.contactList.appendChild(a);
  });
}

// Speech Synthesis ("Read Aloud") Implementation
function toggleSpeech() {
  if (state.isSpeaking) {
    stopSpeech();
  } else {
    startSpeech();
  }
}

function startSpeech() {
  if (!('speechSynthesis' in window)) {
    alert('Speech synthesis is not supported on your browser.');
    return;
  }

  if (!state.currentPlan) return;

  window.speechSynthesis.cancel();

  const script = buildSpeechScript(state.currentPlan);
  const utterance = new SpeechSynthesisUtterance(script);
  state.speechUtterance = utterance;

  // Language mapping
  const langCodeMap = {
    English: 'en-IN',
    Hindi: 'hi-IN',
    Kannada: 'kn-IN',
  };
  const targetLang = langCodeMap[state.selectedLanguage] || 'en-IN';
  utterance.lang = targetLang;
  utterance.rate = 0.95; // slightly slower for patient clarity

  // Try to find matching voice
  const voices = window.speechSynthesis.getVoices();
  const matchedVoice = voices.find(
    (v) => v.lang.startsWith(targetLang) || v.lang.startsWith(targetLang.split('-')[0])
  );
  if (matchedVoice) {
    utterance.voice = matchedVoice;
  }

  utterance.onstart = () => {
    state.isSpeaking = true;
    updateSpeechUI(true);
  };

  utterance.onend = () => {
    state.isSpeaking = false;
    updateSpeechUI(false);
  };

  utterance.onerror = (e) => {
    console.warn('Speech synthesis error:', e);
    state.isSpeaking = false;
    updateSpeechUI(false);
  };

  window.speechSynthesis.speak(utterance);
}

function stopSpeech() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  state.isSpeaking = false;
  updateSpeechUI(false);
}

function updateSpeechUI(isSpeaking) {
  if (isSpeaking) {
    elements.readAloudBtn.classList.add('hidden');
    elements.ttsStopBtn.classList.remove('hidden');
    elements.ttsStatusBar.classList.remove('hidden');
    elements.ttsStatusText.textContent = `Reading plan aloud in ${state.selectedLanguage}...`;
  } else {
    elements.readAloudBtn.classList.remove('hidden');
    elements.ttsStopBtn.classList.add('hidden');
    elements.ttsStatusBar.classList.add('hidden');
  }
}

function buildSpeechScript(plan) {
  const parts = [];

  // Intro
  const name = plan.patient_first_name || 'Patient';
  parts.push(`Recovery plan for ${name}.`);

  if (plan.diagnosis_plain) {
    parts.push(`Diagnosis: ${plan.diagnosis_plain}.`);
  }

  if (plan.summary_plain) {
    parts.push(plan.summary_plain);
  }

  // Medicines summary
  if (Array.isArray(plan.medicines) && plan.medicines.length > 0) {
    parts.push(`Here is your medicine schedule with ${plan.medicines.length} medicines:`);
    plan.medicines.forEach((m) => {
      const timing = (m.suggested_clock_times || []).join(' and ') || m.frequency_as_written || '';
      parts.push(`${m.name_as_written}. Take ${m.dose || ''} at ${timing}. Purpose: ${m.purpose_plain || 'as directed'}.`);
    });
  }

  // Warning signs
  if (Array.isArray(plan.red_flags) && plan.red_flags.length > 0) {
    parts.push('Important warning signs to watch out for:');
    plan.red_flags.forEach((rf) => {
      parts.push(`${rf.symptom_plain}. Action: ${rf.action}.`);
    });
  }

  // Follow up
  if (Array.isArray(plan.follow_ups) && plan.follow_ups.length > 0) {
    parts.push('Follow-up instructions:');
    plan.follow_ups.forEach((f) => {
      parts.push(`${f.what_plain}. ${f.date_as_written || f.date || ''}.`);
    });
  }

  if (Array.isArray(plan.uncertain_items) && plan.uncertain_items.length > 0) {
    parts.push('Please remember to confirm any unclear handwriting with your doctor or pharmacist.');
  }

  return parts.join(' ');
}

// Helpers
function escapeHtml(text) {
  if (text === null || text === undefined) return '';
  const div = document.createElement('div');
  div.textContent = String(text);
  return div.innerHTML;
}


// ---- Dose tracking: "Taken" buttons (saved in this browser, per day) ----
function doseKey(med, time) {
  const today = new Date().toLocaleDateString('en-CA');
  return `dose:${today}:${med.name_as_written}:${time}`;
}
function loadDose(key) {
  try { return localStorage.getItem(key); } catch (e) { return null; }
}
function saveDose(key, value) {
  try {
    if (value) localStorage.setItem(key, value);
    else localStorage.removeItem(key);
  } catch (e) { /* storage unavailable: ignore */ }
}
function addDoseButtons(card, med) {
  window.__planLoadedAt = Date.now();
  ensureFamilyBar();
  const times = (med.suggested_clock_times && med.suggested_clock_times.length)
    ? med.suggested_clock_times
    : (med.as_needed ? ['As needed'] : []);
  if (!times.length) return;

  const box = document.createElement('div');
  box.className = 'dose-box';
  const title = document.createElement('div');
  title.className = 'dose-title';
  title.textContent = med.as_needed ? 'Log a dose' : "Today's doses";
  box.appendChild(title);

  const row = document.createElement('div');
  row.className = 'dose-row';
  times.forEach((t) => {
    const key = doseKey(med, t);
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'dose-btn';
    btn.dataset.time = t;
    btn.dataset.med = med.name_as_written;
    const render = () => {
      const takenAt = loadDose(key);
      btn.classList.toggle('taken', !!takenAt);
      btn.textContent = takenAt ? `✅ ${t} taken at ${takenAt}` : `${t} - Tap when taken`;
    };
    btn.addEventListener('click', () => {
      if (loadDose(key)) {
        saveDose(key, null);
      } else {
        saveDose(key, new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        sendFamilyAlert('taken', med.name_as_written, t);
      }
      render();
    });
    render();
    row.appendChild(btn);
  });
  box.appendChild(row);
  card.appendChild(box);
}


// ---- Family alerts (sent to Telegram through /api/notify) ----
function familyAlertsOn() {
  try { return localStorage.getItem('familyAlerts') !== 'off'; } catch (e) { return true; }
}
function setFamilyStatus(msg) {
  const el = document.getElementById('familyStatus');
  if (el) el.textContent = msg;
}
async function sendFamilyAlert(kind, medName, time) {
  if (!familyAlertsOn()) return;
  try {
    const res = await fetch('/api/notify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kind, patient: window.__patientName || 'The patient', medicine: medName, time }),
    });
    setFamilyStatus(res.ok ? 'Family alert sent ✓' : 'Could not send family alert');
  } catch (e) {
    setFamilyStatus('Could not send family alert');
  }
}
function ensureFamilyBar() {
  if (document.getElementById('familyBar')) return;
  const bar = document.createElement('div');
  bar.id = 'familyBar';
  bar.className = 'family-bar';
  bar.innerHTML = `
    <label class="family-toggle"><input type="checkbox" id="familyToggle"> Tell my family when I take or miss a dose</label>
    <button type="button" id="familyDemoBtn" class="family-demo-btn">Demo: simulate a missed dose</button>
    <span id="familyStatus" class="family-status"></span>`;
  elements.medicineList.before(bar);
  const tog = bar.querySelector('#familyToggle');
  tog.checked = familyAlertsOn();
  tog.addEventListener('change', () => {
    try { localStorage.setItem('familyAlerts', tog.checked ? 'on' : 'off'); } catch (e) {}
  });
  bar.querySelector('#familyDemoBtn').addEventListener('click', () => {
    const btn = Array.from(document.querySelectorAll('.dose-btn:not(.taken)'))
      .find((b) => /^\d/.test(b.dataset.time || ''));
    if (!btn) { setFamilyStatus('No pending dose to simulate'); return; }
    sendFamilyAlert('missed', btn.dataset.med, btn.dataset.time);
  });
}


// ---- Automatic missed-dose check (runs while this page is open) ----
const MISSED_GRACE_MIN = (() => {
  const g = parseInt(new URLSearchParams(location.search).get('grace'), 10);
  return Number.isFinite(g) && g >= 0 ? g : 30;
})();
function checkMissedDoses() {
  if (!familyAlertsOn()) return;
  const now = Date.now();
  const today = new Date().toLocaleDateString('en-CA');
  document.querySelectorAll('.dose-btn:not(.taken)').forEach((btn) => {
    const m = /^(\d{1,2}):(\d{2})$/.exec(btn.dataset.time || '');
    if (!m) return;
    const due = new Date();
    due.setHours(parseInt(m[1], 10), parseInt(m[2], 10), 0, 0);
    if (due.getTime() < (window.__planLoadedAt || 0)) return;
    if (now < due.getTime() + MISSED_GRACE_MIN * 60000) return;
    const sentKey = `missedSent:${today}:${btn.dataset.med}:${btn.dataset.time}`;
    if (loadDose(sentKey)) return;
    saveDose(sentKey, '1');
    sendFamilyAlert('missed', btn.dataset.med, btn.dataset.time);
  });
}
setInterval(checkMissedDoses, 30000);
