const chatEl = document.getElementById('chat');
const formEl = document.getElementById('chatForm');
const inputEl = document.getElementById('message');
const resetBtn = document.getElementById('resetBtn');

function renderMessage(role, content) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.textContent = content;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

const API_BASE = 'http://127.0.0.1:5000';

async function loadHistory() {
  const res = await fetch(`${API_BASE}/api/history`, {
    credentials: 'include'
  });
  const data = await res.json();
  chatEl.innerHTML = '';
  for (const m of data.history || []) {
    renderMessage(m.role, m.content);
  }
}

async function sendMessage(text) {
  renderMessage('user', text);
  renderMessage('assistant', '...');
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    // Replace the last assistant placeholder with actual reply
    const nodes = chatEl.querySelectorAll('.msg.assistant');
    const last = nodes[nodes.length - 1];
    if (last) last.textContent = data.reply;
  } catch (e) {
    const nodes = chatEl.querySelectorAll('.msg.assistant');
    const last = nodes[nodes.length - 1];
    if (last) last.textContent = '오류가 발생했어요. 다시 시도해주세요.';
  }
}

formEl.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = (inputEl.value || '').trim();
  if (!text) return;
  inputEl.value = '';
  sendMessage(text);
});

resetBtn.addEventListener('click', async () => {
  await fetch(`${API_BASE}/api/reset`, { method: 'POST', credentials: 'include' });
  loadHistory();
});

loadHistory();


