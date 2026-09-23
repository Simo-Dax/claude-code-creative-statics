#!/usr/bin/env python3
"""Route A - riempie un template HTML per ogni ad di ads.json. Un loop, non N generazioni.

    python3 build.py <batch_dir>

<batch_dir>/ads.json:
{
  "template": ".claude/skills/statics-css/templates/headline_subheading.html",
  "fonts": {"Headline": "context/brand/assets/fonts/Headline-Bold.otf",
            "Body": "context/brand/assets/fonts/Body-Medium.otf"},
  "ads": [
    {"id": "c1_a", "headline": ["Prima riga", "*seconda* riga", "terza"], "body": "Una frase breve.",
     "ground": "#1A1A2E", "ink": "#F5F2EA", "accent": "#C8F25C", "chip": "#B8B6F8",
     "logo": "context/brand/assets/logos/logo_01.svg", "headline_size": 110}
  ]
}

*parola* nell'headline = colore accento. Font, logo e immagini vengono inlineati come data URI,
cosi' l'HTML si rasterizza identico ovunque. Percorsi relativi alla root del repo (cwd).
"""
import base64, html, json, mimetypes, pathlib, re, sys

MIME = {".otf": "font/otf", ".ttf": "font/ttf", ".woff2": "font/woff2", ".woff": "font/woff", ".svg": "image/svg+xml"}


def data_uri(path):
    p = pathlib.Path(path)
    mime = MIME.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def font_faces(fonts):
    out = []
    for family, path in fonts.items():
        if pathlib.Path(path).exists():
            out.append(f'@font-face {{ font-family: "{family}"; src: url("{data_uri(path)}"); }}')
        else:
            print(f"  ATTENZIONE font mancante: {path} - uso il fallback di sistema (non on-brand)")
    return "\n  ".join(out)


def headline_html(lines):
    esc = [html.escape(l) for l in lines]
    return "<br>".join(re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', l) for l in esc)


def main():
    batch = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    spec = json.loads((batch / "ads.json").read_text())
    tpl = pathlib.Path(spec["template"]).read_text()
    faces = font_faces(spec.get("fonts", {}))
    for ad in spec["ads"]:
        size = ad.get("headline_size", 105)
        logo = ad.get("logo")
        if logo and pathlib.Path(logo).exists():
            logo_html = f'<img src="{data_uri(logo)}" alt="">'
        else:
            logo_html = f'<span class="wordmark">{html.escape(ad.get("wordmark", "logo"))}</span>'
        # body parte sotto l'headline: pitch = size (interlinea 100%) + gap 40px (§4)
        body_top = 60 + size * len(ad["headline"]) + 40
        page = (tpl.replace("{{FONT_FACES}}", faces)
                   .replace("{{GROUND}}", ad["ground"]).replace("{{INK}}", ad["ink"])
                   .replace("{{ACCENT}}", ad["accent"]).replace("{{CHIP}}", ad.get("chip", ad["accent"]))
                   .replace("{{HEADLINE_SIZE}}", str(size)).replace("{{BODY_TOP}}", str(body_top))
                   .replace("{{HEADLINE_HTML}}", headline_html(ad["headline"]))
                   .replace("{{BODY}}", html.escape(ad.get("body", "")))
                   .replace("{{LOGO}}", logo_html))
        (batch / f"{ad['id']}.html").write_text(page)
        print(f"built {ad['id']}.html")


if __name__ == "__main__":
    main()
