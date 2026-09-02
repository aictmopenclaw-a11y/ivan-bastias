"""Genera los QR de Iván Bastías (estáticos, sin servicios externos).
QR A: URL de la tarjeta digital (error H, logo Carozzi al centro opcional).
QR B: vCard reducido, funciona sin internet (error M).
Uso: .venv/bin/python scripts/make_qr.py
"""
from pathlib import Path
import segno
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entregables"
OUT.mkdir(exist_ok=True)

URL = "https://ivan-bastias.vercel.app/"

VCARD_MIN = (
    "BEGIN:VCARD\r\nVERSION:3.0\r\n"
    "N:Bastías Castex;Iván;;;\r\nFN:Iván Bastías Castex\r\n"
    "ORG:Empresas Carozzi S.A.\r\nTITLE:Compra de Envases\r\n"
    "TEL;TYPE=CELL:+56966473044\r\nEMAIL:ibastias@carozzi.cl\r\n"
    "URL:https://www.carozzi.cl\r\n"
    "ADR;TYPE=WORK:;;Camino Internacional 2825;Reñaca Alto, Viña del Mar;;2540059;Chile\r\n"
    "END:VCARD\r\n"
)

DARK = "#1a1a1a"

def export(qr, stem, scale_px=2000, dark=DARK, logo=None):
    # PNG a ~2000 px de ancho con quiet zone de 4 módulos
    modules = qr.symbol_size(border=4)[0]
    scale = max(1, scale_px // modules)
    png = OUT / f"{stem}.png"
    qr.save(png, scale=scale, border=4, dark=dark, light="#ffffff")
    qr.save(OUT / f"{stem}.svg", border=4, dark=dark, light="#ffffff", scale=10)
    qr.save(OUT / f"{stem}.pdf", border=4, dark=dark, light="#ffffff", scale=10)
    if logo and Path(logo).exists():
        im = Image.open(png).convert("RGBA")
        lg = Image.open(logo).convert("RGBA")
        w = im.width
        # logo ocupa ~22% del ancho: seguro con corrección H (30%)
        target = int(w * 0.22)
        ratio = target / max(lg.size)
        lg = lg.resize((max(1, int(lg.width * ratio)), max(1, int(lg.height * ratio))), Image.LANCZOS)
        pad = int(w * 0.015)
        box = Image.new("RGBA", (lg.width + 2 * pad, lg.height + 2 * pad), (255, 255, 255, 255))
        box.alpha_composite(lg, (pad, pad))
        im.alpha_composite(box, ((w - box.width) // 2, (im.height - box.height) // 2))
        im.save(OUT / f"{stem}-con-logo.png")
    print(f"{stem}: version {qr.version}, error {qr.error}, {modules}x{modules} módulos, scale {scale}")

qr_a = segno.make(URL, error="h", boost_error=False)
export(qr_a, "qr-pagina", logo=ROOT / "assets/logos/carozzi-icono.png")

qr_b = segno.make(VCARD_MIN, error="m", boost_error=False)
export(qr_b, "qr-vcard")
