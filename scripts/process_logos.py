"""Convierte los logos crudos (fondo blanco / círculo) en PNG con transparencia real.
Método: recorte al contenido y 'unmix from white' (alpha = 255 - blancura), sin recortes duros."""
from pathlib import Path
import numpy as np
from PIL import Image
import cairosvg

RAW = Path(__file__).resolve().parent.parent / "assets/logos/raw"
OUT = RAW.parent

def unmix(im, max_side=900, pad=0.04):
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, alpha0 = a[..., :3], a[..., 3] / 255.0
    white = rgb.min(axis=2)                      # blancura = canal mínimo
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    lum = rgb.mean(axis=2)
    alpha = (255.0 - white) / 255.0
    # sombras grises claras (baja saturación, luminosas) -> fuera
    alpha[(sat < 28) & (lum > 175)] = 0.0
    alpha *= alpha0
    # des-premultiplicar contra blanco
    with np.errstate(divide="ignore", invalid="ignore"):
        col = (rgb - 255.0 * (1.0 - alpha[..., None])) / np.maximum(alpha[..., None], 1e-4)
    col = np.clip(col, 0, 255)
    col[alpha < 0.02] = 0
    out = np.dstack([col, alpha * 255.0]).astype(np.uint8)
    # recorte al contenido con alpha > 5%
    ys, xs = np.where(out[..., 3] > 12)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    ph, pw = int((y1 - y0) * pad), int((x1 - x0) * pad)
    y0, y1 = max(0, y0 - ph), min(out.shape[0], y1 + ph + 1)
    x0, x1 = max(0, x0 - pw), min(out.shape[1], x1 + pw + 1)
    res = Image.fromarray(out[y0:y1, x0:x1])
    if max(res.size) > max_side:
        r = max_side / max(res.size)
        res = res.resize((round(res.width * r), round(res.height * r)), Image.LANCZOS)
    return res

def crop_center(im, frac):
    """Recorta el cuadrado central (círculo del slider) para descartar la sombra exterior."""
    w, h = im.size; s = int(min(w, h) * frac)
    return im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))

jobs = {
    "carozzi.png":       ("cz-logo_carozzi_.png", None),
    "carozzi-icono.png": ("cz-icono.png", None),
    "ambrosoli.png":     ("cz-ambrosoli_logo_slider_marcas.png", 0.62),
    "costa.png":         ("cz-costa_logo_slider_marcas.png", 0.62),
    "bresler.png":       ("cz-bresler_logo_slider_marcas.png", 0.62),
    "master-dog.png":    ("cz-masterdog_logo_slider_marcas.png", 0.62),
    "san-francisco.png": ("cz-logo_carozzi_marcas_loncomilla.png", None),
}
for name, (src, frac) in jobs.items():
    p = RAW / src
    if not p.exists() or p.stat().st_size < 500:
        print("FALTA", name, "<-", src); continue
    im = Image.open(p)
    if frac: im = crop_center(im, frac)
    res = unmix(im)
    res.save(OUT / name); print("OK", name, res.size)

# Master Cat: vector oficial -> PNG nítido
cairosvg.svg2png(url=str(RAW / "mc-logomastercat.svg"), write_to=str(OUT / "master-cat.png"), output_width=800)
print("OK master-cat.png (svg)")

# hoja de contacto sobre fondo verde para revisar transparencia
files = sorted(OUT.glob("*.png"))
cell = (320, 200); cols = 3; rows = (len(files) + cols - 1) // cols
from PIL import ImageDraw
sheet = Image.new("RGB", (cols * cell[0], rows * (cell[1] + 24)), (110, 160, 120)); d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGBA"); im.thumbnail((cell[0] - 20, cell[1] - 20))
    x = (i % cols) * cell[0]; y = (i // cols) * (cell[1] + 24)
    sheet.paste(im, (x + 10, y + 10), im); d.text((x + 10, y + cell[1]), f.name, fill=(0, 0, 0))
sheet.save("/private/tmp/claude-501/-Users-cristobaltejero-Projects/caae831d-121d-4210-84ca-be50ff2c1876/scratchpad/logos-final.png")
