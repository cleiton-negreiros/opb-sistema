// ============================================
// API HELPER
// ============================================
async function apiCall(endpoint, method, body) {
    const baseUrl = document.getElementById('cfg-api-url')?.value || 'http://localhost:5000';
    const url = baseUrl + endpoint;
    const options = { method: method || 'GET', headers: { 'Content-Type': 'application/json' } };
    if (body) options.body = JSON.stringify(body);
    try {
        const res = await fetch(url, options);
        const data = await res.json();
        return data;
    } catch (err) {
        showToast('Erro na API: ' + err.message, 'error');
        return { error: err.message };
    }

function escapeHtml(t) { const d = document.createElement('div'); d.textContent = t; return d.innerHTML; }
