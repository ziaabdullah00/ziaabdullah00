"""Build a unified animated terminal introduction from the public avatar."""
from pathlib import Path
from html import escape
from PIL import Image, ImageOps, ImageEnhance
ROOT = Path(__file__).resolve().parents[1]
# Focus on the face; an oval character boundary removes the busy surroundings.
im = Image.open(ROOT/'avatar.png').convert('RGB').crop((120, 35, 330, 275))
im = ImageOps.grayscale(im).resize((68, 68))
im = ImageEnhance.Contrast(ImageOps.autocontrast(im)).enhance(1.3)
ramp = ' .:-=+*#%@'
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="410" viewBox="0 0 860 410" role="img">', '<title>Zia Abdullah — Full-Stack Developer &amp; Technical SEO Specialist</title>', '<rect x="1" y="1" width="858" height="408" rx="10" fill="#11151b" stroke="#30363d"/>', '<path d="M1 45H859" stroke="#30363d"/>', '<circle cx="22" cy="23" r="4" fill="#ef736b"/><circle cx="38" cy="23" r="4" fill="#ddb968"/><circle cx="54" cy="23" r="4" fill="#83ba8b"/>', '<text x="80" y="28" fill="#a3abb6" font-family="monospace" font-size="12">zia@github — ~/about</text>', '<style>@keyframes print{from{opacity:0}to{opacity:1}}.row{animation:print .12s both}.copy{animation:print .65s both}@media(prefers-reduced-motion:reduce){.row,.copy{animation:none}}</style>']
for row in range(68):
    chars=[]
    for col in range(68):
        inside=((col-33.5)/30)**2+((row-33.5)/34)**2<=1
        value=im.getpixel((col,row))
        chars.append(ramp[(255-value)*9//255] if inside else ' ')
    s.append(f'<text class="row" xml:space="preserve" x="26" y="{66+row*4.65:.2f}" fill="#b8c0ca" font-family="monospace" font-size="6.4" textLength="260" lengthAdjust="spacingAndGlyphs" style="animation-delay:{row*.016:.3f}s">{escape("".join(chars))}</text>')
s.extend(['<g class="copy" style="animation-delay:.15s">', '<text x="335" y="99" fill="#b6c994" font-family="monospace" font-size="13">$ whoami</text>', '<text x="333" y="151" fill="#f0f0e8" font-family="Georgia,serif" font-size="43">Zia Abdullah.</text>', '<text x="335" y="186" fill="#e1e4e8" font-family="sans-serif" font-size="19">Full-Stack Developer</text>', '<text x="335" y="213" fill="#aeb6c0" font-family="sans-serif" font-size="18">&amp; Technical SEO Specialist</text>', '<path d="M335 238H811" stroke="#30363d"/>', '<text x="335" y="269" fill="#b6c994" font-family="monospace" font-size="12">BUILDING</text>', '<text x="335" y="297" fill="#d2d7de" font-family="sans-serif" font-size="17">SaaS products · AI-powered platforms</text>', '<text x="335" y="322" fill="#d2d7de" font-family="sans-serif" font-size="17">Fast, search-friendly websites.</text>', '<text x="335" y="371" fill="#aeb6c0" font-family="monospace" font-size="13">Next.js / React</text>', '<text x="710" y="371" fill="#aeb6c0" font-family="monospace" font-size="13">Lahore, PK</text>', '</g></svg>'])
(ROOT/'profile-terminal.svg').write_text('\n'.join(s)+'\n')
