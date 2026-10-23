"""Generate light/dark SVG assets for the IneshAg profile README."""
# Usage: python3 scripts/generate_assets.py assets
import os, sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "light": dict(bg="#ffffff", card="#ffffff", border="#e5e7eb", text="#0b1020", sub="#4b5563",
                  muted="#6b7280", chip="#f3f4f6", chipText="#374151", grid="#eef0f3"),
    "dark":  dict(bg="#0d1117", card="#0d1117", border="#262c36", text="#f0f3f6", sub="#b1bac4",
                  muted="#8b949e", chip="#161b22", chipText="#c9d1d9", grid="#161b22"),
}

ACCENT_A, ACCENT_B = "#7c3aed", "#06b6d4"


def write(name, theme, body, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'font-family="{FONT}">{body}</svg>')
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w") as f:
        f.write(svg)


def header(theme):
    t = THEMES[theme]
    w, h = 1000, 300
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.6" fill="{t["border"]}"/>'
        for x in range(640, 990, 22) for y in range(26, 290, 22))
    return f'''
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ACCENT_A}"/><stop offset="1" stop-color="{ACCENT_B}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.82" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{ACCENT_A}" stop-opacity="{0.20 if theme == 'dark' else 0.12}"/>
    <stop offset="1" stop-color="{ACCENT_A}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t["bg"]}" stop-opacity="1"/><stop offset="0.35" stop-color="{t["bg"]}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="r"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  <style>
    .pulse {{ animation: p 2.4s ease-in-out infinite; transform-origin: 62px 236px; }}
    @keyframes p {{ 0%,100% {{ opacity: .35; transform: scale(1); }} 50% {{ opacity: 0; transform: scale(2.4); }} }}
  </style>
</defs>
<g clip-path="url(#r)">
  <rect width="{w}" height="{h}" fill="{t["bg"]}"/>
  {dots}
  <rect x="600" width="400" height="{h}" fill="url(#fade)"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect width="{w}" height="4" fill="url(#g)"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{t["border"]}"/>

<text x="56" y="78" font-family="{MONO}" font-size="15" fill="{t["muted"]}" letter-spacing="1">HI, I'M</text>
<text x="54" y="142" font-size="62" font-weight="800" fill="{t["text"]}" letter-spacing="-2">Inesh Agarwal</text>
<text x="56" y="186" font-size="22" fill="{t["sub"]}">I build <tspan fill="{t["text"]}" font-weight="600">mobile apps</tspan> and <tspan fill="{t["text"]}" font-weight="600">ML products</tspan>, and I ship them.</text>

<circle class="pulse" cx="62" cy="236" r="6" fill="#22c55e"/>
<circle cx="62" cy="236" r="5" fill="#22c55e"/>
<text x="78" y="241" font-size="15" fill="{t["sub"]}">Currently shipping <tspan fill="{t["text"]}" font-weight="600">OneTake</tspan> on iOS + Android</text>
<text x="56" y="272" font-family="{MONO}" font-size="13" fill="{t["muted"]}">CS @ SRMIST Chennai '28  ·  Open to internships</text>

<g transform="translate(760 70)">
  <rect width="180" height="160" rx="20" fill="{t["card"]}" stroke="{t["border"]}"/>
  <text x="90" y="62" text-anchor="middle" font-size="44" font-weight="800" fill="url(#g)">Top 15</text>
  <text x="90" y="92" text-anchor="middle" font-size="14" fill="{t["sub"]}">of 4,400+ teams</text>
  <line x1="40" y1="110" x2="140" y2="110" stroke="{t["border"]}"/>
  <text x="90" y="134" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["muted"]}">GUIDEWIRE DEVTRAILS '26</text>
</g>
''', w, h


PROJECTS = [
    ("onetake", "OneTake", "#8b5cf6", "FLAGSHIP · iOS + ANDROID",
     ["A self-tape audition studio for actors:", "teleprompter, filming HUD, casting exports."],
     ["SwiftUI", "Compose", "AVFoundation", "CameraX"]),
    ("hustlr", "Hustlr", "#f59e0b", "TOP 15 / 4,400+ · DEVTRAILS '26",
     ["InsurTech app built for Guidewire's", "national InsurTech hackathon."],
     ["Flutter", "Node.js", "Supabase", "Postgres"]),
    ("predelinquency", "Pre-Delinquency", "#10b981", "ML · FINTECH",
     ["Flags bank customers before they default,", "explains why, keeps a human in the loop."],
     ["XGBoost", "SHAP", "FastAPI", "React"]),
    ("skillreels", "SkillReels", "#ec4899", "EDTECH · RECOMMENDER",
     ["A short-form learning feed with coding", "challenges that break passive scrolling."],
     ["React", "TypeScript", "FastAPI"]),
]


def chip_w(label):
    return 18 + len(label) * 7.4


def card(theme, p):
    _, name, accent, tag, desc, stack = p
    t = THEMES[theme]
    w, h = 480, 210
    chips, x = [], 28
    for s in stack:
        cw = chip_w(s)
        chips.append(f'<rect x="{x}" y="160" width="{cw:.0f}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                     f'<text x="{x + cw/2:.0f}" y="177" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["chipText"]}">{escape(s)}</text>')
        x += cw + 8
    lines = "".join(f'<text x="28" y="{108 + i*22}" font-size="15" fill="{t["sub"]}">{escape(l)}</text>' for i, l in enumerate(desc))
    return f'''
<defs><clipPath id="c"><rect width="{w}" height="{h}" rx="16"/></clipPath>
<radialGradient id="glow" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{accent}" stop-opacity="{0.18 if theme == 'dark' else 0.10}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
<g clip-path="url(#c)">
  <rect width="{w}" height="{h}" fill="{t["card"]}"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect width="5" height="{h}" fill="{accent}"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{t["border"]}"/>
<text x="28" y="42" font-family="{MONO}" font-size="11" font-weight="600" fill="{accent}" letter-spacing="1.2">{escape(tag)}</text>
<text x="28" y="76" font-size="26" font-weight="800" fill="{t["text"]}" letter-spacing="-0.6">{escape(name)}</text>
<text x="{w-28}" y="76" text-anchor="end" font-size="20" fill="{t["muted"]}">↗</text>
{lines}
{''.join(chips)}
''', w, h


def stack(theme):
    t = THEMES[theme]
    w, h = 1000, 150
    rows = [("LANGUAGES", "Swift · Kotlin · Dart · Python · TypeScript · Java · C++"),
            ("FRAMEWORKS", "SwiftUI · Jetpack Compose · Flutter · React · FastAPI · Node.js"),
            ("DATA & ML", "PostgreSQL · Supabase · SQLite · PyTorch · XGBoost · SHAP")]
    body = "".join(
        f'<text x="40" y="{50 + i*36}" font-family="{MONO}" font-size="12" font-weight="600" fill="{t["muted"]}" letter-spacing="1.2">{escape(a)}</text>'
        f'<text x="190" y="{50 + i*36}" font-size="16" fill="{t["text"]}">{escape(b)}</text>'
        for i, (a, b) in enumerate(rows))
    return f'''
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>
{body}
''', w, h


for theme in THEMES:
    write("header", theme, *header(theme))
    for p in PROJECTS:
        write(p[0], theme, *card(theme, p))
    write("stack", theme, *stack(theme))
print("ok")
