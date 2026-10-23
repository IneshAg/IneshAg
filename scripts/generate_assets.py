"""Generate the animated SVG assets for the IneshAg profile README.

Usage: python3 scripts/generate_assets.py assets
"""
import os, sys, random
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"
BG = "#07070f"
VIOLET, CYAN, PINK = "#a855f7", "#22d3ee", "#f472b6"


def write(name, body, w, h):
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}" font-family="{FONT}">{body}</svg>')


def stars(w, h, n, seed):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r, d = rnd.uniform(0.6, 1.8), rnd.uniform(0, 4)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" class="tw" style="animation-delay:{d:.1f}s"/>')
    return "".join(out)


def hero():
    w, h = 1000, 360
    return f'''
<defs>
  <linearGradient id="nameSpread" x1="0" x2="1" spreadMethod="reflect">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <radialGradient id="b1"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="b2"><stop offset="0" stop-color="{CYAN}" stop-opacity=".40"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="b3"><stop offset="0" stop-color="{PINK}" stop-opacity=".35"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".05"/>
  </pattern>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
  <clipPath id="r"><rect width="{w}" height="{h}" rx="24"/></clipPath>
  <style>
    .tw {{ animation: tw 4s ease-in-out infinite; opacity: .2 }}
    @keyframes tw {{ 50% {{ opacity: .9 }} }}
    .f1 {{ animation: f1 14s ease-in-out infinite }} @keyframes f1 {{ 50% {{ transform: translate(120px, 40px) }} }}
    .f2 {{ animation: f2 18s ease-in-out infinite }} @keyframes f2 {{ 50% {{ transform: translate(-140px, -30px) }} }}
    .f3 {{ animation: f3 16s ease-in-out infinite }} @keyframes f3 {{ 50% {{ transform: translate(60px, -50px) }} }}
    .in {{ opacity: 0; animation: in .9s ease-out forwards }}
    .d1 {{ animation-delay: .1s }} .d2 {{ animation-delay: .4s }} .d3 {{ animation-delay: .7s }} .d4 {{ animation-delay: 1s }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(14px) }} to {{ opacity: 1; transform: none }} }}
    .scan {{ animation: scan 6s linear infinite }} @keyframes scan {{ from {{ transform: translateY(-40px) }} to {{ transform: translateY({h}px) }} }}
    .blink {{ animation: bl 1s steps(1) infinite }} @keyframes bl {{ 50% {{ opacity: 0 }} }}
  </style>
</defs>
<g clip-path="url(#r)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <circle class="f1" cx="180" cy="80" r="260" fill="url(#b1)"/>
  <circle class="f2" cx="860" cy="300" r="280" fill="url(#b2)"/>
  <circle class="f3" cx="620" cy="40" r="200" fill="url(#b3)"/>
  {stars(w, h, 60, 7)}
  <rect class="scan" width="{w}" height="40" fill="#fff" opacity=".03"/>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="none" stroke="url(#nameSpread)" stroke-width="2" opacity=".8"/>

<g class="in d1"><text x="{w/2}" y="92" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{CYAN}" letter-spacing="6">&lt; HELLO WORLD, I'M /&gt;</text></g>
<g class="in d2">
  <text x="{w/2}" y="178" text-anchor="middle" font-size="84" font-weight="900" fill="url(#nameSpread)" filter="url(#glow)" opacity=".7" letter-spacing="-2">INESH AGARWAL</text>
  <text x="{w/2}" y="178" text-anchor="middle" font-size="84" font-weight="900" fill="url(#nameSpread)" letter-spacing="-2">INESH AGARWAL</text>
</g>
<g class="in d3"><text x="{w/2}" y="226" text-anchor="middle" font-size="22" font-weight="600" fill="#e5e7eb" letter-spacing="4">MOBILE  ✦  FULL-STACK  ✦  ML  ✦  BUILDER</text></g>
<g class="in d4">
  <rect x="{w/2-214}" y="262" width="434" height="44" rx="22" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".15"/>
  <circle cx="{w/2-182}" cy="284" r="6" fill="#22c55e"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <text x="{w/2-160}" y="290" font-family="{MONO}" font-size="15" fill="#e5e7eb">now shipping → <tspan fill="{CYAN}" font-weight="700">OneTake</tspan> on iOS + Android<tspan class="blink" fill="{CYAN}">▌</tspan></text>
</g>
''', w, h


def stats():
    w, h = 1000, 170
    items = [("TOP 15", "of 4,400+ teams", "Guidewire DEVTrails '26", VIOLET),
             ("1,900+", "participants", "Techformers 1.0 organizer", CYAN),
             ("2", "native platforms", "OneTake · iOS + Android", PINK),
             ("⭐", "Super Contributor", "Hacktoberfest", "#facc15")]
    cw = (w - 20 * 3) / 4
    cards = []
    for i, (big, mid, small, c) in enumerate(items):
        x = i * (cw + 20)
        cards.append(f'''
<g class="pop" style="animation-delay:{i*0.15:.2f}s">
  <rect x="{x+1:.0f}" y="1" width="{cw-2:.0f}" height="{h-2}" rx="18" fill="{BG}" stroke="{c}" stroke-opacity=".55" stroke-width="1.5"/>
  <rect x="{x+1:.0f}" y="1" width="{cw-2:.0f}" height="{h-2}" rx="18" fill="{c}" fill-opacity=".07"/>
  <text x="{x+cw/2:.0f}" y="76" text-anchor="middle" font-size="44" font-weight="900" fill="{c}" filter="url(#g)">{escape(big)}</text>
  <text x="{x+cw/2:.0f}" y="76" text-anchor="middle" font-size="44" font-weight="900" fill="{c}">{escape(big)}</text>
  <text x="{x+cw/2:.0f}" y="108" text-anchor="middle" font-size="16" font-weight="700" fill="#f3f4f6">{escape(mid)}</text>
  <text x="{x+cw/2:.0f}" y="136" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="#9ca3af">{escape(small)}</text>
</g>''')
    return f'''
<defs><filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<style>.pop {{ opacity: 0; animation: pop .7s cubic-bezier(.2,.9,.3,1.3) forwards }}
@keyframes pop {{ from {{ opacity: 0; transform: translateY(16px) }} to {{ opacity: 1; transform: none }} }}</style></defs>
{''.join(cards)}
''', w, h


PROJECTS = [
    ("onetake", "OneTake", "🎬", VIOLET, "#6366f1", "FLAGSHIP · iOS + ANDROID",
     ["Self-tape audition studio for actors.", "Voice-follow teleprompter, filming HUD,", "auto tape check, casting-ready exports."],
     ["SwiftUI", "Compose", "AVFoundation", "CameraX"]),
    ("hustlr", "Hustlr", "🏆", "#f59e0b", "#ef4444", "TOP 15 / 4,400+ TEAMS",
     ["InsurTech product built for Guidewire", "DEVTrails 2026, the national", "InsurTech hackathon."],
     ["Flutter", "Node.js", "Supabase", "Postgres"]),
    ("predelinquency", "Pre-Delinquency", "🏦", "#10b981", CYAN, "ML · FINTECH",
     ["Flags bank customers before they", "default, explains why with SHAP,", "and keeps a human in the loop."],
     ["XGBoost", "SHAP", "FastAPI", "React"]),
    ("skillreels", "SkillReels", "📲", PINK, VIOLET, "EDTECH · RECOMMENDER",
     ["Short-form learning feed with coding", "challenges built in, and an engine", "that breaks passive scrolling."],
     ["React", "TypeScript", "FastAPI"]),
]


def card(p):
    _, name, emoji, a, b, tag, desc, stack = p
    w, h = 490, 260
    chips, x = [], 30
    for s in stack:
        cw = 20 + len(s) * 7.6
        chips.append(f'<rect x="{x}" y="206" width="{cw:.0f}" height="28" rx="14" fill="{a}" fill-opacity=".12" stroke="{a}" stroke-opacity=".5"/>'
                     f'<text x="{x+cw/2:.0f}" y="224.5" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="600" fill="#f3f4f6">{escape(s)}</text>')
        x += cw + 8
    lines = "".join(f'<text x="30" y="{128+i*24}" font-size="15.5" fill="#cbd5e1">{escape(l)}</text>' for i, l in enumerate(desc))
    return f'''
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{a}"/><stop offset=".5" stop-color="{b}"/><stop offset="1" stop-color="{a}"/>
    <animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <radialGradient id="gl" cx="1" cy="0" r="1"><stop offset="0" stop-color="{a}" stop-opacity=".35"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
  <radialGradient id="gl2" cx="0" cy="1" r=".8"><stop offset="0" stop-color="{b}" stop-opacity=".18"/><stop offset="1" stop-color="{b}" stop-opacity="0"/></radialGradient>
  <filter id="tg" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
  <clipPath id="c"><rect x="2" y="2" width="{w-4}" height="{h-4}" rx="20"/></clipPath>
  <style>.pulse {{ animation: pu 3s ease-in-out infinite }} @keyframes pu {{ 50% {{ opacity: .45 }} }}</style>
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="21" fill="none" stroke="url(#bd)" stroke-width="2.5"/>
<g clip-path="url(#c)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect class="pulse" width="{w}" height="{h}" fill="url(#gl)"/>
  <rect width="{w}" height="{h}" fill="url(#gl2)"/>
</g>
<text x="30" y="46" font-family="{MONO}" font-size="12" font-weight="700" fill="{a}" letter-spacing="1.5">{escape(tag)}</text>
<text x="30" y="90" font-size="32" font-weight="900" fill="{a}" filter="url(#tg)" opacity=".8" letter-spacing="-.8">{escape(name)}</text>
<text x="30" y="90" font-size="32" font-weight="900" fill="#ffffff" letter-spacing="-.8">{escape(name)}</text>
<text x="{w-30}" y="92" text-anchor="end" font-size="34">{emoji}</text>
{lines}
{''.join(chips)}
''', w, h


write("hero", *hero())
write("stats", *stats())
for p in PROJECTS:
    write(p[0], *card(p))
print("ok")
