// Basit yerel yorum listesi (kalıcı değil). Gerçek yorumlar için backend gerekir.
const form = document.getElementById('commentForm');
const list = document.getElementById('commentList');

function nowTR() {
  const d = new Date();
  return d.toLocaleString('tr-TR', { dateStyle: 'short', timeStyle: 'short' });
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const comment = document.getElementById('comment').value.trim();
  if (!name || !comment) return;

  const li = document.createElement('li');
  li.className = 'comment-item';
  li.innerHTML = `
    <div class="meta">${name} • ${nowTR()}</div>
    <div class="text">${escapeHTML(comment)}</div>
  `;
  list.prepend(li);
  form.reset();
});

function escapeHTML(str) {
  const p = document.createElement('p');
  p.textContent = str;
  return p.innerHTML;
}