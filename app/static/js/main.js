// Live AI Priority Prediction (AJAX)
let debounceTimer;

function triggerPredict() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(async () => {
    const title = document.getElementById('title')?.value || '';
    const description = document.getElementById('description')?.value || '';

    if (title.length < 3) return;

    try {
      const form = new FormData();
      form.append('title', title);
      form.append('description', description);

      const res = await fetch('/tickets/predict', { method: 'POST', body: form });
      const data = await res.json();

      const box = document.getElementById('ai-prediction');
      if (box) {
        box.style.display = 'block';
        document.getElementById('pred-priority').textContent = data.priority;
        document.getElementById('pred-priority').className = 'badge-priority badge-' + data.priority.toLowerCase();
        document.getElementById('pred-conf').textContent = data.confidence + '% confidence';

        const bar = document.getElementById('pred-bar');
        if (bar) {
          bar.style.width = data.confidence + '%';
          bar.style.background = data.priority === 'High' ? '#ef4444' : data.priority === 'Medium' ? '#f59e0b' : '#06d6a0';
        }
      }
    } catch (e) { console.log('Predict error:', e); }
  }, 400);
}

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    document.querySelectorAll('.alert-custom').forEach(el => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    });
  }, 4000);
});