"""Genera og.png (1200x630), favicon.svg y apple-touch-icon.png."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import urllib.request, io

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "assets"

def font(size, serif=True, weight="Medium"):
    # Fraunces / Instrument Sans desde Google Fonts (solo para renderizar la imagen OG)
    fam = "fraunces" if serif else "instrumentsans"
    url = {
        "fraunces": "https://github.com/undercasetype/Fraunces/raw/master/fonts/static/ttf/Fraunces_144pt-Medium.ttf",
        "instrumentsans": "https://github.com/Instrument/instrument-sans/raw/main/fonts/ttf/InstrumentSans-Medium.ttf",
    }[fam]
    cache = ROOT / ".venv" / f"{fam}.ttf"
    if not cache.exists():
        try:
            urllib.request.urlretrieve(url, cache)
        except Exception as e:
            print("fuente no descargada, uso fallback:", e)
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf" if serif else "/System/Library/Fonts/Supplemental/Arial.ttf", size)
    return ImageFont.truetype(str(cache), size)

W, H = 1200, 630
im = Image.new("RGB", (W, H), "#f6f1e8")
d = ImageDraw.Draw(im)
# franja roja diagonal con degradado
for y in range(H):
    t = y / H
    r = int(214 + (126 - 214) * t); g = int(31 + (11 - 31) * t); b = int(42 + (18 - 42) * t)
    d.line([(0, y), (W * 0.42 - y * 0.12, y)], fill=(r, g, b))
# logo carozzi blanco en la franja
lg = Image.open(A / "logos/carozzi.png").convert("RGBA")
white = Image.new("RGBA", lg.size, (255, 255, 255, 255)); white.putalpha(lg.split()[3])
white.thumbnail((260, 80)); im.paste(white, (70, 70), white)
# foto circular (o iniciales si no existe)
foto = A / "foto.jpg"
if foto.exists():
    ph = Image.open(foto).convert("RGB").resize((360, 360), Image.LANCZOS)
    mask = Image.new("L", (1440, 1440), 0); ImageDraw.Draw(mask).ellipse((0, 0, 1439, 1439), fill=255); mask = mask.resize((360, 360), Image.LANCZOS)
    ring = Image.new("RGB", (376, 376), (255, 255, 255)); rmask = Image.new("L", (1504, 1504), 0); ImageDraw.Draw(rmask).ellipse((0, 0, 1503, 1503), fill=255); rmask = rmask.resize((376, 376), Image.LANCZOS)
    im.paste(ring, (62, 200), rmask); im.paste(ph, (70, 208), mask)
else:
    fi = font(190); d.text((70, 300), "IB", font=fi, fill=(255, 255, 255))
# texto
fn = font(64); fs = font(30, serif=False); fk = font(22, serif=False)
d.text((560, 170), "Iván Bastías", font=fn, fill="#1d1816")
d.text((560, 245), "Castex", font=fn, fill="#1d1816")
d.text((560, 345), "Compra de Envases", font=fs, fill="#b3121b")
d.text((560, 390), "Empresas Carozzi S.A.", font=fs, fill="#5c534e")
d.text((560, 480), "+56 9 6647 3044  ·  ibastias@carozzi.cl", font=fk, fill="#5c534e")
d.text((560, 520), "Toca para guardar el contacto", font=fk, fill="#5c534e")
im.save(A / "og.png", optimize=True)

# favicon: círculo rojo con IB
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#b3121b"/><text x="32" y="42" text-anchor="middle" font-family="Georgia,serif" font-size="30" font-weight="600" fill="#fff">IB</text></svg>'''
(A / "favicon.svg").write_text(svg)
ic = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); dd = ImageDraw.Draw(ic)
dd.rounded_rectangle((0, 0, 179, 179), radius=40, fill="#b3121b")
f = font(84); bb = dd.textbbox((0, 0), "IB", font=f)
dd.text(((180 - (bb[2] - bb[0])) / 2 - bb[0], (180 - (bb[3] - bb[1])) / 2 - bb[1]), "IB", font=f, fill="white")
ic.save(A / "apple-touch-icon.png")
print("og.png, favicon.svg, apple-touch-icon.png listos")
