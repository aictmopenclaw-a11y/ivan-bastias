"""Tarjeta/sticker imprimible 90x55 mm a 300 dpi con el QR de la página (PDF vectorial)."""
from pathlib import Path
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entregables"
W, H = 90 * mm, 55 * mm
ROJO, TINTA, GRIS = HexColor("#b3121b"), HexColor("#1d1816"), HexColor("#5c534e")

try:
    pdfmetrics.registerFont(TTFont("Fraunces", str(ROOT / ".venv/fraunces.ttf")))
    pdfmetrics.registerFont(TTFont("Sans", str(ROOT / ".venv/instrumentsans.ttf")))
    F_SERIF, F_SANS = "Fraunces", "Sans"
except Exception as e:
    print("fuentes fallback:", e); F_SERIF, F_SANS = "Times-Roman", "Helvetica"

c = canvas.Canvas(str(OUT / "5-tarjeta-imprenta-90x55mm.pdf"), pagesize=(W, H))
c.setTitle("Iván Bastías Castex · QR"); c.setAuthor("Kyest Marketing")
# fondo crema + franja roja izquierda
c.setFillColor(HexColor("#f6f1e8")); c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(ROJO); c.rect(0, 0, 4 * mm, H, stroke=0, fill=1)
# QR (SVG vectorial) a 32 mm
qr = svg2rlg(str(ROOT / "assets/qr/qr-pagina.svg"))
s = (32 * mm) / qr.width; qr.width *= s; qr.height *= s; qr.scale(s, s)
c.setFillColor(white); c.roundRect(9 * mm, (H - 36 * mm) / 2, 36 * mm, 36 * mm, 2 * mm, stroke=0, fill=1)
renderPDF.draw(qr, c, 11 * mm, (H - 32 * mm) / 2)
# textos
x = 50 * mm
c.setFillColor(TINTA); c.setFont(F_SERIF, 12.5); c.drawString(x, 38 * mm, "Iván Bastías"); c.drawString(x, 32.5 * mm, "Castex")
c.setFillColor(ROJO); c.setFont(F_SANS, 7.5); c.drawString(x, 26.5 * mm, "Comprador de Envases")
c.setFillColor(GRIS); c.setFont(F_SANS, 7); c.drawString(x, 22.5 * mm, "Empresas Carozzi S.A.")
c.setFont(F_SANS, 6.5); c.drawString(x, 15 * mm, "+56 9 6647 3044"); c.drawString(x, 11.5 * mm, "ibastias@carozzi.cl")
c.setFillColor(ROJO); c.setFont(F_SANS, 5.5); c.drawString(x, 6 * mm, "Escanea para guardar mi contacto")
c.showPage(); c.save()
print("tarjeta-qr-imprimir.pdf listo")
