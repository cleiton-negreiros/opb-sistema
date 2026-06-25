// ============================================
// TOAST
// ============================================
function showToast(msg, type='info') {
    let c = document.getElementById('toastContainer');
    if (!c) {
        c = document.createElement('div');
        c.id = 'toastContainer';
        c.className = 'toast-container';
        document.body.appendChild(c);
    }
    const t = document.createElement('div');
    t.className = 'toast ' + type;
    t.innerHTML = msg;
    c.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}
