/* nav.js — centralna nawigacja Cichy Mechanik
   Dodaj do każdej strony:
     <div id="nav"></div>
     <script src="/nav.js"></script>
   lub dla podstron:
     <script src="../nav.js"></script>
*/

(function() {
  const here = location.pathname;

  // Wykryj głębokość ścieżki żeby ustawić poprawne linki
  const depth = (here.match(/\//g) || []).length;
  const root = depth <= 1 ? '' : '../';

  const links = [
    { href: root + 'index.html#builds', label: 'Builds' },
    { href: root + 'dzwieki.html',      label: 'Posłuchaj' },
    { href: root + 'blog/index.html',   label: 'Blog' },
    { href: root + 'o-mnie.html',       label: 'O mnie' },
    { href: root + 'index.html#kontakt',label: 'Kontakt' },
    { href: 'https://youtube.com/@cichymechanik', label: 'YouTube ↗', external: true },
  ];

  const navLinks = links.map(l => {
    const active = !l.external && here.includes(l.href.replace(root,'').split('#')[0]) && l.href !== root + 'index.html#kontakt' && l.href !== root + 'index.html#builds'
      ? ' class="active"' : '';
    const target = l.external ? ' target="_blank"' : '';
    return `<li><a href="${l.href}"${active}${target}>${l.label}</a></li>`;
  }).join('\n      ');

  const html = `<nav>
  <div class="nav-inner">
    <a href="${root}index.html" class="logo">
      <img src="${root}graphics/logo_cichy_mechanik.png" alt="Cichy Mechanik"
        onerror="this.style.display='none'">
    </a>
    <ul class="nav-links">
      ${navLinks}
    </ul>
    <button class="nav-mobile-toggle" onclick="this.nextElementSibling.classList.toggle('open')" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <ul class="nav-links-mobile">
      ${navLinks}
    </ul>
  </div>
</nav>`;

  const el = document.getElementById('nav');
  if (el) el.outerHTML = html;
})();
