#!/usr/bin/env python3
"""
generate_blog.py
Konwertuje pliki .md z folderu blog/posts/ na HTML.
Uruchom z głównego folderu repo:
  python generate_blog.py

Obsługuje shortcody:
  [youtube: VIDEO_ID]   - embed YouTube
  [audio: path/do/pliku.mp3] - player audio
"""

import os, re, json
from pathlib import Path
import markdown

POSTS_DIR = Path('blog/posts')
OUTPUT_DIR = Path('blog')
OUTPUT_DIR.mkdir(exist_ok=True)

NAV = '''<nav>
  <div class="nav-inner">
    <a href="../index.html" class="logo">
      <img src="../graphics/logo_cichy_mechanik.png" alt="Cichy Mechanik">
    </a>
    <ul class="nav-links">
      <li><a href="../index.html#builds">Builds</a></li>
      <li><a href="../dzwieki.html">Posłuchaj</a></li>
      <li><a href="index.html" class="active">Blog</a></li>
      <li><a href="../o-mnie.html">O mnie</a></li>
      <li><a href="../index.html#kontakt">Kontakt</a></li>
    </ul>
  </div>
</nav>'''

SHARED_CSS = '''
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=DM+Mono:wght@300;400&family=Outfit:wght@300;400&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --cream: #faf9f6; --paper: #f4f1eb; --ink: #1a1915; --ink-soft: #5a5850;
    --ink-muted: #9a9890; --line: #e0ddd6;
    --serif: 'Cormorant Garamond', Georgia, serif;
    --mono: 'DM Mono', monospace;
    --sans: 'Outfit', sans-serif;
    --max: 1200px; --content: 680px;
  }
  html { scroll-behavior: smooth; }
  body { background: var(--cream); color: var(--ink); font-family: var(--mono); font-size: 14px; line-height: 1.8; -webkit-font-smoothing: antialiased; }
  nav { position: sticky; top: 0; z-index: 100; background: var(--cream); border-bottom: 0.5px solid var(--line); }
  .nav-inner { max-width: var(--max); margin: 0 auto; padding: 0 48px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
  .logo { font-family: var(--sans); font-size: 20px; font-weight: 300; color: var(--ink); text-decoration: none; display: flex; align-items: center; gap: 10px; }
  .logo img { height: 36px; width: auto; }
  .nav-links { display: flex; gap: 36px; list-style: none; }
  .nav-links a { font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase; color: var(--ink-soft); text-decoration: none; transition: color 0.2s; }
  .nav-links a:hover, .nav-links a.active { color: var(--ink); }
  footer { border-top: 0.5px solid var(--line); padding: 40px 0; margin-top: 80px; }
  .footer-inner { max-width: var(--max); margin: 0 auto; padding: 0 48px; display: flex; align-items: center; justify-content: space-between; }
  .footer-logo { font-family: var(--sans); font-size: 18px; font-weight: 300; letter-spacing: 0.5px; }
  .footer-links { display: flex; gap: 24px; list-style: none; }
  .footer-links a { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--ink-muted); text-decoration: none; }
  .footer-links a:hover { color: var(--ink); }
  .footer-note { font-size: 10px; color: var(--ink-muted); }
  @media (max-width: 768px) {
    .nav-inner, .footer-inner { padding: 0 24px; }
    .nav-links { display: none; }
    .footer-inner { flex-direction: column; gap: 16px; text-align: center; }
    .footer-links { justify-content: center; }
  }
'''

FOOTER = '''<footer>
  <div class="footer-inner">
    <div class="footer-logo">Cichy Mechanik</div>
    <ul class="footer-links">
      <li><a href="index.html">Blog</a></li>
      <li><a href="../regulamin.html">Regulamin</a></li>
      <li><a href="https://youtube.com/@cichymechanik" target="_blank">YouTube</a></li>
    </ul>
    <p class="footer-note">Żory · Śląsk · 2026</p>
  </div>
</footer>'''


def parse_frontmatter(text):
    """Parse YAML-ish frontmatter between --- lines"""
    meta = {}
    body = text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].strip()
    return meta, body


def process_shortcodes(html):
    """Replace [youtube: ID] and [audio: path] with embeds"""

    # YouTube
    def yt_replace(m):
        vid = m.group(1).strip()
        return f'''<div class="embed-yt">
  <iframe src="https://www.youtube.com/embed/{vid}" allowfullscreen loading="lazy"></iframe>
</div>'''
    html = re.sub(r'\[youtube:\s*([^\]]+)\]', yt_replace, html)

    # Audio
    def audio_replace(m):
        src = m.group(1).strip()
        return f'''<div class="embed-audio">
  <button class="audio-play" onclick="blogPlay(this, '{src}')">
    <span class="ap-icon">&#9654;</span>
    <span class="ap-pause" style="display:none;">&#9646;&#9646;</span>
  </button>
  <div class="audio-info">
    <div class="audio-label">Posłuchaj brzmienia</div>
    <div class="audio-bar"><div class="audio-fill" id="fill-{abs(hash(src))}"></div></div>
    <div class="audio-time" id="time-{abs(hash(src))}">0:00</div>
  </div>
  <audio src="../{src}" data-fill="fill-{abs(hash(src))}" data-time="time-{abs(hash(src))}"
    ontimeupdate="blogProgress(this)" onended="blogEnd(this)"></audio>
</div>'''
    html = re.sub(r'\[audio:\s*([^\]]+)\]', audio_replace, html)

    return html


def build_post_html(meta, content_html, slug):
    title = meta.get('title', 'Wpis')
    subtitle = meta.get('subtitle', '')
    date = meta.get('date', '')
    tags = [t.strip() for t in meta.get('tags', '').split(',') if t.strip()]

    tags_html = ''.join(f'<span class="post-tag">{t}</span>' for t in tags)
    subtitle_html = f'<p class="post-subtitle">{subtitle}</p>' if subtitle else ''
    date_html = f'<time class="post-date">{date}</time>' if date else ''

    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Cichy Mechanik</title>
<link rel="icon" href="../graphics/favicon.png">
<style>
{SHARED_CSS}

  .post-wrap {{ max-width: var(--content); margin: 0 auto; padding: 64px 48px 80px; }}

  .post-back {{ display: inline-flex; align-items: center; gap: 8px; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--ink-muted); text-decoration: none; margin-bottom: 48px; transition: color 0.2s; }}
  .post-back:hover {{ color: var(--ink); }}

  .post-header {{ margin-bottom: 48px; padding-bottom: 32px; border-bottom: 0.5px solid var(--line); }}
  .post-tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }}
  .post-tag {{ font-size: 9px; letter-spacing: 2px; text-transform: uppercase; padding: 3px 10px; border: 0.5px solid var(--line); border-radius: 2px; color: var(--ink-muted); }}
  .post-title {{ font-family: var(--serif); font-size: clamp(32px, 5vw, 52px); font-weight: 300; line-height: 1.1; margin-bottom: 12px; }}
  .post-subtitle {{ font-size: 15px; color: var(--ink-soft); margin-bottom: 16px; font-style: italic; font-family: var(--serif); }}
  .post-date {{ font-size: 11px; color: var(--ink-muted); letter-spacing: 1px; }}

  /* Post body */
  .post-body {{ }}
  .post-body p {{ margin-bottom: 1.6rem; color: var(--ink-soft); }}
  .post-body h2 {{ font-family: var(--serif); font-size: 28px; font-weight: 300; margin: 2.5rem 0 1rem; color: var(--ink); }}
  .post-body h3 {{ font-family: var(--serif); font-size: 22px; font-weight: 300; margin: 2rem 0 0.8rem; color: var(--ink); }}
  .post-body strong {{ color: var(--ink); font-weight: 400; }}
  .post-body em {{ font-style: italic; }}
  .post-body ul, .post-body ol {{ margin: 0 0 1.6rem 1.5rem; color: var(--ink-soft); }}
  .post-body li {{ margin-bottom: 0.4rem; }}
  .post-body a {{ color: var(--ink); }}
  .post-body blockquote {{ border-left: 2px solid var(--line); padding: 0 0 0 20px; margin: 2rem 0; font-family: var(--serif); font-size: 20px; font-weight: 300; color: var(--ink-soft); font-style: italic; line-height: 1.5; }}
  .post-body hr {{ border: none; border-top: 0.5px solid var(--line); margin: 2.5rem 0; }}
  .post-body code {{ font-family: var(--mono); font-size: 12px; background: var(--paper); padding: 2px 6px; border-radius: 2px; color: var(--ink); }}

  /* YouTube embed */
  .embed-yt {{ margin: 2rem 0; width: 100%; aspect-ratio: 16/9; background: #0d0d0d; border-radius: 4px; overflow: hidden; }}
  .embed-yt iframe {{ width: 100%; height: 100%; border: none; display: block; }}

  /* Audio player */
  .embed-audio {{ display: flex; align-items: center; gap: 16px; margin: 2rem 0; padding: 16px 20px; background: var(--paper); border-radius: 4px; border: 0.5px solid var(--line); }}
  .audio-play {{ width: 40px; height: 40px; border-radius: 50%; border: 0.5px solid var(--line); background: var(--cream); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 14px; color: var(--ink); flex-shrink: 0; transition: background 0.15s; }}
  .audio-play:hover {{ background: var(--ink); color: var(--cream); }}
  .audio-play.playing {{ background: var(--ink); color: var(--cream); }}
  .audio-info {{ flex: 1; min-width: 0; }}
  .audio-label {{ font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--ink-muted); margin-bottom: 6px; }}
  .audio-bar {{ width: 100%; height: 2px; background: var(--line); border-radius: 1px; cursor: pointer; }}
  .audio-fill {{ height: 100%; background: var(--ink); border-radius: 1px; width: 0%; transition: width 0.1s linear; pointer-events: none; }}
  .audio-time {{ font-size: 10px; color: var(--ink-muted); margin-top: 4px; }}

  @media (max-width: 768px) {{
    .post-wrap {{ padding: 40px 24px 60px; }}
  }}
</style>
</head>
<body>
{NAV}
<div class="post-wrap">
  <a href="index.html" class="post-back">← Wszystkie wpisy</a>
  <header class="post-header">
    <div class="post-tags">{tags_html}</div>
    <h1 class="post-title">{title}</h1>
    {subtitle_html}
    {date_html}
  </header>
  <div class="post-body">
    {content_html}
  </div>
</div>
{FOOTER}
<script>
let blogAudio = null;
let blogBtn = null;

function blogPlay(btn, src) {{
  if (blogAudio && !blogAudio.paused && blogBtn !== btn) {{
    blogAudio.pause();
    blogBtn.classList.remove('playing');
    blogBtn.querySelector('.ap-icon').style.display = '';
    blogBtn.querySelector('.ap-pause').style.display = 'none';
  }}
  if (!blogAudio || blogBtn !== btn) {{
    blogAudio = btn.nextElementSibling.nextElementSibling.nextElementSibling;
    blogBtn = btn;
  }}
  if (blogAudio.paused) {{
    blogAudio.play();
    btn.classList.add('playing');
    btn.querySelector('.ap-icon').style.display = 'none';
    btn.querySelector('.ap-pause').style.display = '';
  }} else {{
    blogAudio.pause();
    btn.classList.remove('playing');
    btn.querySelector('.ap-icon').style.display = '';
    btn.querySelector('.ap-pause').style.display = 'none';
  }}
}}

function blogProgress(audio) {{
  if (!audio.duration) return;
  const pct = (audio.currentTime / audio.duration * 100).toFixed(1);
  const fill = document.getElementById(audio.dataset.fill);
  const time = document.getElementById(audio.dataset.time);
  if (fill) fill.style.width = pct + '%';
  if (time) {{
    const s = Math.floor(audio.currentTime);
    time.textContent = Math.floor(s/60) + ':' + String(s%60).padStart(2,'0');
  }}
}}

function blogEnd(audio) {{
  const fill = document.getElementById(audio.dataset.fill);
  if (fill) fill.style.width = '0%';
  if (blogBtn) {{
    blogBtn.classList.remove('playing');
    blogBtn.querySelector('.ap-icon').style.display = '';
    blogBtn.querySelector('.ap-pause').style.display = 'none';
  }}
}}
</script>
</body>
</html>'''


def build_index_html(posts):
    posts_html = ''
    for p in sorted(posts, key=lambda x: x['date'], reverse=True):
        tags_html = ''.join(f'<span class="post-tag">{t}</span>' for t in p['tags'])
        posts_html += f'''  <a href="{p['slug']}.html" class="post-item">
    <div class="post-item-meta">
      <div class="post-item-tags">{tags_html}</div>
      <time class="post-item-date">{p['date']}</time>
    </div>
    <h2 class="post-item-title">{p['title']}</h2>
    {f'<p class="post-item-sub">{p["subtitle"]}</p>' if p['subtitle'] else ''}
  </a>
'''

    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — Cichy Mechanik</title>
<link rel="icon" href="../graphics/favicon.png">
<style>
{SHARED_CSS}

  .wrap {{ max-width: var(--max); margin: 0 auto; padding: 0 48px; }}
  .hero {{ padding: 64px 0 48px; border-bottom: 0.5px solid var(--line); }}
  .hero-eyebrow {{ font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--ink-muted); margin-bottom: 16px; }}
  .hero-title {{ font-family: var(--serif); font-size: clamp(36px, 5vw, 56px); font-weight: 300; line-height: 1.1; }}
  .hero-title em {{ font-style: italic; color: var(--ink-soft); }}

  .post-list {{ max-width: 720px; margin: 0; padding: 0; }}

  .post-item {{ display: block; padding: 36px 0; border-bottom: 0.5px solid var(--line); text-decoration: none; color: inherit; transition: opacity 0.15s; }}
  .post-item:hover {{ opacity: 0.7; }}
  .post-item:first-child {{ padding-top: 48px; }}

  .post-item-meta {{ display: flex; align-items: center; gap: 16px; margin-bottom: 12px; }}
  .post-item-tags {{ display: flex; gap: 6px; }}
  .post-tag {{ font-size: 9px; letter-spacing: 2px; text-transform: uppercase; padding: 2px 8px; border: 0.5px solid var(--line); border-radius: 2px; color: var(--ink-muted); }}
  .post-item-date {{ font-size: 10px; color: var(--ink-muted); letter-spacing: 1px; margin-left: auto; }}

  .post-item-title {{ font-family: var(--serif); font-size: 26px; font-weight: 300; line-height: 1.2; color: var(--ink); margin-bottom: 6px; }}
  .post-item-sub {{ font-size: 13px; color: var(--ink-muted); font-style: italic; font-family: var(--serif); }}

  @media (max-width: 768px) {{
    .wrap {{ padding: 0 24px; }}
  }}
</style>
</head>
<body>
{NAV}
<div class="wrap">
  <div class="hero">
    <p class="hero-eyebrow">Blog</p>
    <h1 class="hero-title">Mechanika<br>i <em>obsesja.</em></h1>
  </div>
  <div class="post-list">
{posts_html}  </div>
</div>
{FOOTER}
</body>
</html>'''


def main():
    md = markdown.Markdown(extensions=['fenced_code', 'nl2br'])
    posts_meta = []

    for md_file in sorted(POSTS_DIR.glob('*.md')):
        slug = md_file.stem
        text = md_file.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(text)

        md.reset()
        content_html = md.convert(body)
        content_html = process_shortcodes(content_html)

        html = build_post_html(meta, content_html, slug)
        out_path = OUTPUT_DIR / f'{slug}.html'
        out_path.write_text(html, encoding='utf-8')

        tags = [t.strip() for t in meta.get('tags', '').split(',') if t.strip()]
        posts_meta.append({
            'slug': slug,
            'title': meta.get('title', slug),
            'subtitle': meta.get('subtitle', ''),
            'date': meta.get('date', ''),
            'tags': tags,
        })
        print(f'  ✓ {slug}.html')

    index_html = build_index_html(posts_meta)
    (OUTPUT_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print(f'  ✓ blog/index.html')
    print(f'\nGotowe. {len(posts_meta)} wpisów.')


if __name__ == '__main__':
    main()
