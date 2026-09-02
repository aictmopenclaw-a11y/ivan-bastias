"""PNG diseñado con el QR integrado: vertical (impresión) y cuadrado (WhatsApp)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import segno

ROOT = Path(__file__).resolve().parent.parent
A, OUT = ROOT / "assets", ROOT / "entregables"
URL = "https://ivan-bastias.vercel.app/"
CREMA, PAPEL, ROJO, ROJO_OSC, TINTA, GRIS = (246,241,232), (255,253,249), (179,18,27), (126,11,18), (29,24,22), (92,83,78)

def F(size, serif=True):
    return ImageFont.truetype(str(ROOT / ".venv" / ("fraunces.ttf" if serif else "instrumentsans.ttf")), size)

def tint_white(png):
    im = Image.open(png).convert("RGBA"); w = Image.new("RGBA", im.size, (255,255,255,255)); w.putalpha(im.split()[3]); return w

def fit(im, w=None, h=None):
    r = min((w / im.width) if w else 9e9, (h / im.height) if h else 9e9)
    return im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)

def qr_image(size):
    qr = segno.make(URL, error="h", boost_error=False)
    n = qr.symbol_size(border=0)[0]; scale = max(1, size // n)
    buf = ROOT / ".venv/_qr.png"; qr.save(buf, scale=scale, border=0, dark="#1d1816", light="#ffffff")
    im = Image.open(buf).convert("RGBA")
    lg = fit(Image.open(A / "logos/carozzi-icono.png").convert("RGBA"), w=int(im.width * 0.22))
    pad = int(im.width * 0.018); box = Image.new("RGBA", (lg.width + 2*pad, lg.height + 2*pad), (255,255,255,255))
    box.alpha_composite(lg, (pad, pad)); im.alpha_composite(box, ((im.width - box.width)//2, (im.height - box.height)//2))
    return im

def shadow_card(canvas, box, radius, blur=40, alpha=70, offset=(0, 18)):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", canvas.size, (0,0,0,0)); d = ImageDraw.Draw(sh)
    d.rounded_rectangle((x0+offset[0], y0+offset[1], x1+offset[0], y1+offset[1]), radius, fill=(126,11,18,alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); canvas.alpha_composite(sh)
    d = ImageDraw.Draw(canvas); d.rounded_rectangle(box, radius, fill=PAPEL + (255,))

def header(canvas, h):
    W = canvas.width; grad = Image.new("RGBA", (W, h))
    px = grad.load()
    for y in range(h):
        for x in range(0, W):
            t = (x / W) * 0.55 + (y / h) * 0.45
            px[x, y] = (int(214 + (126-214)*t), int(31 + (11-31)*t), int(42 + (18-42)*t), 255)
    canvas.alpha_composite(grad, (0, 0))
    glow = Image.new("RGBA", (W, h), (0,0,0,0)); gd = ImageDraw.Draw(glow)
    gd.ellipse((-W*0.2, -h*0.9, W*0.6, h*0.9), fill=(255,255,255,50)); glow = glow.filter(ImageFilter.GaussianBlur(h*0.25))
    canvas.alpha_composite(glow)

def centered(d, y, text, font, fill, W):
    bb = d.textbbox((0,0), text, font=font); d.text(((W - (bb[2]-bb[0]))/2 - bb[0], y), text, font=font, fill=fill)
    return bb[3]-bb[1]

def leftcol(d, x, y, text, font, fill):
    bb = d.textbbox((0,0), text, font=font); d.text((x - bb[0], y - bb[1]), text, font=font, fill=fill); return bb[3]-bb[1]

def render(W, H, name, layout="vertical"):
    S = W / 1200
    c = Image.new("RGBA", (W, H), CREMA + (255,))
    hh = int(0.30 * H); header(c, hh)
    lg = fit(tint_white(A / "logos/carozzi.png"), h=int(48*S)); c.alpha_composite(lg, (int(70*S), int(64*S)))
    d = ImageDraw.Draw(c)
    fl = F(int(22*S), serif=False); txt = "COMPARTIR HACE BIEN"
    bb = d.textbbox((0,0), txt, font=fl); d.text((W - int(70*S) - (bb[2]-bb[0]), int(76*S)), txt, font=fl, fill=(255,255,255,220))
    m = int(80*S); top = int(hh - 0.42*hh); pie = int(236*S)
    if layout == "vertical":
        pad_top, pad_bot, gap_qr, textos = int(70*S), int(56*S), int(44*S), int(300*S)
        qs = int(min(W - 2*m - 2*int(120*S), H - top - pad_top - gap_qr - textos - pad_bot - pie))
        qr = fit(qr_image(qs), w=qs)
        bottom = top + pad_top + qr.height + gap_qr + textos + pad_bot
        shadow_card(c, (m, top, W - m, bottom), int(36*S), blur=int(40*S))
        qx, qy = (W - qr.width)//2, top + pad_top; c.alpha_composite(qr, (qx, qy))
        d = ImageDraw.Draw(c); y = qy + qr.height + gap_qr
        y += centered(d, y, "Iván Bastías Castex", F(int(58*S)), TINTA, W) + int(22*S)
        y += centered(d, y, "Compra de Envases", F(int(28*S), False), ROJO, W) + int(12*S)
        y += centered(d, y, "Empresas Carozzi S.A.", F(int(26*S), False), GRIS, W) + int(30*S)
        for x in range(m + int(70*S), W - m - int(70*S), int(14*S)): d.line((x, y, x + int(6*S), y), fill=(29,24,22,40), width=max(1, int(2*S)))
        y += int(28*S)
        y += centered(d, y, "+56 9 6647 3044   ·   ibastias@carozzi.cl", F(int(26*S), False), TINTA, W) + int(14*S)
        centered(d, y, "ivan-bastias.vercel.app", F(int(24*S), False), GRIS, W)
    else:
        bottom = H - pie; pad = int(64*S)
        shadow_card(c, (m, top, W - m, bottom), int(36*S), blur=int(40*S))
        qs = int(min(bottom - top - 2*pad, W * 0.40)); qr = fit(qr_image(qs), w=qs)
        qx, qy = m + pad, top + (bottom - top - qr.height)//2; c.alpha_composite(qr, (qx, qy))
        d = ImageDraw.Draw(c); x = qx + qr.width + int(60*S)
        # medir bloque de texto para centrarlo verticalmente
        fn, fc, fe, ft, fu = F(int(50*S)), F(int(24*S), False), F(int(22*S), False), F(int(22*S), False), F(int(20*S), False)
        lines = [("Iván Bastías", fn, TINTA, int(4*S)), ("Castex", fn, TINTA, int(18*S)), ("Compra de Envases", fc, ROJO, int(10*S)),
                 ("Empresas Carozzi S.A.", fe, GRIS, int(26*S)), ("---", None, None, int(24*S)),
                 ("+56 9 6647 3044", ft, TINTA, int(10*S)), ("ibastias@carozzi.cl", ft, TINTA, int(12*S)), ("ivan-bastias.vercel.app", fu, GRIS, 0)]
        total = sum(((d.textbbox((0,0), t, font=f)[3]-d.textbbox((0,0), t, font=f)[1]) if f else 0) + g for t, f, _, g in lines)
        y = top + (bottom - top - total)//2
        for t, f, col, g in lines:
            if f is None:
                for xx in range(x, W - m - int(60*S), int(14*S)): d.line((xx, y, xx + int(6*S), y), fill=(29,24,22,40), width=max(1, int(2*S)))
            else:
                y += leftcol(d, x, y, t, f, col)
            y += g
    py = bottom + int(44*S)
    py += centered(d, py, "Escanea para guardar mi contacto", F(int(30*S)), ROJO, W) + int(36*S)
    logos = [fit(Image.open(A / f"logos/{n}.png").convert("RGBA"), w=int(150*S), h=int(56*S)) for n in ["ambrosoli","costa","bresler","san-francisco","master-cat","master-dog"]]
    gap = int(34*S); tw = sum(l.width for l in logos) + gap*(len(logos)-1); x = (W - tw)//2
    for l in logos:
        c.alpha_composite(l, (x, py + (int(56*S) - l.height)//2)); x += l.width + gap
    c.convert("RGB").save(OUT / name, optimize=True); print("OK", name, (W, H))

render(1200, 1800, "tarjeta-qr-vertical.png")
render(1500, 1500, "tarjeta-qr-cuadrada.png", layout="horizontal")
