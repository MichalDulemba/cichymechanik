(function() {
  const here = location.pathname;
  const isBlog = here.includes('/blog/');
  const root = isBlog ? '../' : '';

  const links = [
    { href: root + 'index.html#builds', label: 'Builds' },
    { href: root + 'dzwieki.html',       label: 'Posłuchaj' },
    { href: root + 'blog/index.html',    label: 'Blog' },
    { href: root + 'o-mnie.html',        label: 'O mnie' },
    { href: root + 'index.html#kontakt', label: 'Kontakt' },
    { href: 'https://youtube.com/@cichymechanik', label: 'YouTube ↗', external: true },
  ];

  function isActive(l) {
    if (l.external) return false;
    const clean = l.href.split('#')[0].replace(root, '');
    if (clean === 'index.html') return false;
    return here.includes(clean);
  }

  const li = links.map(l => {
    const a = isActive(l) ? ' class="active"' : '';
    const t = l.external ? ' target="_blank" rel="noopener"' : '';
    return `<li><a href="${l.href}"${a}${t}>${l.label}</a></li>`;
  }).join('');

  const css = `<style id="nav-style">
nav{position:sticky;top:0;z-index:100;background:var(--cream,#faf9f6);border-bottom:.5px solid var(--line,#e0ddd6)}
.nav-inner{max-width:1200px;margin:0 auto;padding:0 48px;height:56px;display:flex;align-items:center;justify-content:space-between;position:relative}
.logo{font-family:'Outfit',sans-serif;font-size:20px;font-weight:300;letter-spacing:.5px;color:var(--ink,#1a1915);text-decoration:none;display:flex;align-items:center;gap:10px}
.logo img{height:36px;width:auto}
.nav-links{display:flex;gap:36px;list-style:none;margin:0;padding:0}
.nav-links a{font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--ink-soft,#5a5850);text-decoration:none;transition:color .2s}
.nav-links a:hover,.nav-links a.active{color:var(--ink,#1a1915)}
.nav-toggle{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px}
.nav-toggle span{display:block;width:22px;height:1.5px;background:var(--ink,#1a1915)}
.nav-drawer{display:none;position:absolute;top:56px;left:0;right:0;background:var(--cream,#faf9f6);border-bottom:.5px solid var(--line,#e0ddd6);padding:20px 24px;flex-direction:column;gap:16px;list-style:none;margin:0;z-index:99}
.nav-drawer.open{display:flex}
.nav-drawer a{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--ink-soft,#5a5850);text-decoration:none}
.nav-drawer a:hover{color:var(--ink,#1a1915)}
@media(max-width:768px){.nav-links{display:none}.nav-inner{padding:0 24px}.nav-toggle{display:flex}}
</style>`;

  const html = `${css}
<nav>
  <div class="nav-inner">
    <a href="${root}index.html" class="logo">
      <img src="${root}graphics/logo_cichy_mechanik.png" alt="Cichy Mechanik"
           onerror="this.style.display='none'">
    </a>
    <ul class="nav-links">${li}</ul>
    <button class="nav-toggle" id="nav-toggle" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <ul class="nav-drawer" id="nav-drawer">${li}</ul>
  </div>
</nav>`;

  const el = document.getElementById('nav');
  if (el) el.outerHTML = html;

  document.addEventListener('click', function(e) {
    const btn = document.getElementById('nav-toggle');
    const drawer = document.getElementById('nav-drawer');
    if (!btn || !drawer) return;
    if (btn.contains(e.target)) {
      drawer.classList.toggle('open');
    } else if (!drawer.contains(e.target)) {
      drawer.classList.remove('open');
    }
  });
})();
