/**
 * LoadWise AI – Frontend JavaScript
 * Smart Building Load Balancing Advisor
 */

// ── Tab Switching ──────────────────────────────────────────
function switchAgent(n) {
  document.querySelectorAll('.agent-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.agent-tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + n).classList.add('active');
  document.querySelector('[data-agent="' + n + '"]').classList.add('active');
}

// ── Set Example Question ───────────────────────────────────
function setQ(id, text) {
  document.getElementById(id).value = text;
}

// ── Copy Result to Clipboard ───────────────────────────────
function copyResult(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target.closest('.btn-copy');
    const orig = btn.innerHTML;
    btn.innerHTML = '<i class="bi bi-check2"></i> Copied!';
    setTimeout(() => { btn.innerHTML = orig; }, 2000);
  });
}

// ── Collect Form Data: Agent 1 ─────────────────────────────
function collectAgent1() {
  const systems = [...document.querySelectorAll('.a1-sys:checked')].map(c => c.value);
  return {
    building_type:  document.getElementById('a1_building_type').value,
    floors:         document.getElementById('a1_floors').value,
    daily_kwh:      document.getElementById('a1_daily_kwh').value,
    hourly_usage:   document.getElementById('a1_hourly').value,
    smart_meter:    document.getElementById('a1_meter').value,
    dept_data:      document.getElementById('a1_dept').value,
    equipment_logs: document.getElementById('a1_equip').value,
    systems:        systems,
    question:       document.getElementById('a1_question').value
  };
}

// ── Collect Form Data: Agent 2 ─────────────────────────────
function collectAgent2() {
  return {
    building_type:   document.getElementById('a2_building_type').value,
    hourly_readings: document.getElementById('a2_hourly').value,
    daily_profile:   document.getElementById('a2_profile').value,
    max_demand:      document.getElementById('a2_max_demand').value,
    historical_data: document.getElementById('a2_historical').value,
    question:        document.getElementById('a2_question').value
  };
}

// ── Collect Form Data: Agent 3 ─────────────────────────────
function collectAgent3() {
  return {
    building_type:  document.getElementById('a3_building_type').value,
    working_hours:  document.getElementById('a3_hours').value,
    schedules:      document.getElementById('a3_schedules').value,
    critical_equip: document.getElementById('a3_critical').value,
    flexible_loads: document.getElementById('a3_flexible').value,
    occupancy:      document.getElementById('a3_occupancy').value,
    seasonal:       document.getElementById('a3_seasonal').value,
    peak_period:    document.getElementById('a3_peak').value,
    question:       document.getElementById('a3_question').value
  };
}

// ── Collect Form Data: Agent 4 ─────────────────────────────
function collectAgent4() {
  return {
    building_type:        document.getElementById('a4_building_type').value,
    floors:               document.getElementById('a4_floors').value,
    annual_kwh:           document.getElementById('a4_annual').value,
    current_systems:      document.getElementById('a4_systems').value,
    budget_range:         document.getElementById('a4_budget').value,
    sustainability_goals: document.getElementById('a4_sustainability').value,
    pain_points:          document.getElementById('a4_pain').value,
    question:             document.getElementById('a4_question').value
  };
}

// ── Run Agent API Call ─────────────────────────────────────
async function runAgent(n) {
  const collectors = { 1: collectAgent1, 2: collectAgent2, 3: collectAgent3, 4: collectAgent4 };
  const data = collectors[n]();

  if (!data.question || !data.question.trim()) {
    alert('Please enter a question or analysis request.');
    return;
  }

  const btn      = document.getElementById('btn' + n);
  const loading  = document.getElementById('loading' + n);
  const emptyMsg = document.getElementById('result' + n + '-empty');
  const panel    = document.getElementById('result' + n);
  const textEl   = document.getElementById('result' + n + '-text');

  // Show loading state
  btn.disabled = true;
  loading.classList.add('show');
  emptyMsg.style.display = 'none';
  panel.classList.remove('show');

  try {
    const res = await fetch('/api/agent' + n, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(data)
    });

    if (!res.ok) throw new Error('Server error: ' + res.status);
    const json = await res.json();

    textEl.innerText = json.result || 'No response received.';
    loading.classList.remove('show');
    panel.classList.add('show');

  } catch (err) {
    loading.classList.remove('show');
    emptyMsg.style.display = '';
    emptyMsg.innerHTML = `
      <i class="bi bi-exclamation-circle text-danger" style="font-size:2rem;"></i>
      <p class="mt-2 mb-0 text-danger" style="font-size:.875rem;">
        <strong>Error:</strong> ${err.message}<br>
        <span style="font-size:.8rem;">Check your IBM watsonx.ai credentials and try again.</span>
      </p>`;
  } finally {
    btn.disabled = false;
  }
}

// ── Keyboard Shortcut: Ctrl+Enter to Submit ────────────────
document.addEventListener('keydown', function (e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const activePanel = document.querySelector('.agent-panel.active');
    if (activePanel) {
      const id = activePanel.id.replace('panel-', '');
      runAgent(parseInt(id));
    }
  }
});
