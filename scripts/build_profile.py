"""Regenerate the portrait and bio card from the committed avatar."""
from pathlib import Path
from html import escape
from PIL import Image, ImageOps, ImageEnhance
ROOT = Path(__file__).resolve().parents[1]

def frame(width, height, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>', f'<rect width="{width}" height="{height}" rx="14" fill="#0d1117"/>']

im = Image.open(ROOT / 'avatar.png').convert('RGB')
im = ImageOps.fit(im, (76, 46))
im = ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.6)
ramp = '@%#*+=-:. '
s = frame(370, 410, 'Zia Abdullah — animated ASCII portrait')
s += ['<text x="20" y="28" fill="#39d353" font-family="monospace" font-size="12">zia@github:~$ whoami</text><defs>']
for row in range(46):
    s.append(f'<clipPath id="r{row}"><rect x="14" y="{48+row*7.3}" width="342" height="8"><animate attributeName="width" from="0" to="342" dur="0.35s" begin="{row*.045:.3f}s" fill="freeze"/></rect></clipPath>')
s.append('</defs>')
for row in range(46):
    line = ''.join(ramp[im.getpixel((col,row))* (len(ramp)-1)//255] for col in range(76))
    s.append(f'<text xml:space="preserve" x="14" y="{55+row*7.3}" clip-path="url(#r{row})" fill="#c9d1d9" font-family="monospace" font-size="7.3">{escape(line)}</text>')
s.append('</svg>')
(ROOT/'zia-ascii.svg').write_text('\n'.join(s))
s = frame(490, 410, 'Zia Abdullah — Full-Stack Developer and Technical SEO Specialist')
s += ['<style>@keyframes reveal{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}.line{animation:reveal .5s both}@media(prefers-reduced-motion:reduce){.line{animation:none}}</style>', '<text x="24" y="34" fill="#39d353" font-size="17" font-family="monospace">zia@github</text>', '<path d="M24 49H466" stroke="#30363d"/>']
rows = [('Name','Zia Abdullah'),('Role','Full-Stack Developer'),('Focus','Technical SEO'),('Stack','Next.js / React'),('Build','Modern SaaS products'),('','AI-powered platforms'),('','High-performance websites'),('Location','Lahore'),('Web','ziaabdullah.com')]
for i,(key,val) in enumerate(rows):
    y=80+i*32
    s.append(f'<g class="line" style="animation-delay:{.2+i*.12:.2f}s" font-family="monospace" font-size="14"><text x="24" y="{y}" fill="#58a6ff">{escape(key)}</text><text x="128" y="{y}" fill="#c9d1d9">{escape(val)}</text></g>')
s.append('</svg>')
(ROOT/'info-card.svg').write_text('\n'.join(s))
