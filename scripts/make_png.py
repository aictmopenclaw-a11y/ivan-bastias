"""PNG diseñado con foto + QR: vertical (impresión / WhatsApp) y cuadrado (redes). QR compacto, texto grande."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import segno

ROOT = Path(__file__).resolve().parent.parent
A, OUT = ROOT / "assets", ROOT / "entregables"
URL = "https://ivan-bastias.vercel.app/"
CREMA, PAPEL, ROJO, TINTA, GRIS = (246,241,232), (255,253,249), (179,18,27), (29,24,22), (92,83,78)
NOMBRE, CARGO, EMPRESA = "Iván Bastías Castex", "Comprador de Envases", "Empresas Carozzi S.A."
FONO, MAIL, WEB = "+56 9 6647 3044", "ibastias@carozzi.cl", "ivan-bastias.vercel.app"

def F(size, serif=True):
    return ImageFont.truetype(str(ROOT / ".venv" / ("fraunces.ttf" if serif else "instrumentsans.ttf")), size)

def tint_white(png):
    im = Image.open(png).convert("RGBA"); w = Image.new("RGBA", im.size, (255,255,255,255)); w.putalpha(im.split()[3]); return w

def fit(im, w=None, h=None):
    r = min((w / im.width) if w else 9e9, (h / im.height) if h else 9e9)
    return im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)

def qr_image(size, logo_frac=0.22):
    qr = segno.make(URL, error="h", boost_error=False)
    n = qr.symbol_size(border=0)[0]; scale = max(1, size // n)
    buf = ROOT / ".venv/_qr.png"; qr.save(buf, scale=scale, border=0, dark="#1d1816", light="#ffffff")
    im = Image.open(buf).convert("RGBA")
    lg = fit(Image.open(A / "logos/carozzi-icono.png").convert("RGBA"), w=int(im.width * logo_frac))
    pad = int(im.width * 0.018); box = Image.new("RGBA", (lg.width + 2*pad, lg.height + 2*pad), (255,255,255,255))
    box.alpha_composite(lg, (pad, pad)); im.alpha_composite(box, ((im.width - box.width)//2, (im.height - box.height)//2))
    return im

def circle_photo(diam, ring):
    """Foto circular con anillo blanco y sombra suave (supersampleado para bordes limpios)."""
    ss = 4; D = (diam + 2*ring) * ss
    out = Image.new("RGBA", (D, D), (0,0,0,0)); d = ImageDraw.Draw(out)
    d.ellipse((0, 0, D-1, D-1), fill=(255,255,255,255))
    ph = Image.open(A / "foto.jpg").convert("RGBA").resize((diam*ss, diam*ss), Image.LANCZOS)
    m = Image.new("L", (diam*ss, diam*ss), 0); ImageDraw.Draw(m).ellipse((0, 0, diam*ss-1, diam*ss-1), fill=255)
    out.paste(ph, (ring*ss, ring*ss), m)
    return out.resize((D//ss, D//ss), Image.LANCZOS)

def paste_shadowed(canvas, im, xy, blur, alpha=90, dy=10):
    sh = Image.new("RGBA", canvas.size, (0,0,0,0))
    a = im.split()[3].point(lambda v: v * alpha // 255)
    sh.paste((60,10,12,255), (xy[0], xy[1] + dy), a); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh); canvas.alpha_composite(im, xy)

def shadow_card(canvas, box, radius, blur=40, alpha=70, offset=(0, 18)):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", canvas.size, (0,0,0,0)); d = ImageDraw.Draw(sh)
    d.rounded_rectangle((x0+offset[0], y0+offset[1], x1+offset[0], y1+offset[1]), radius, fill=(126,11,18,alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); canvas.alpha_composite(sh)
    ImageDraw.Draw(canvas).rounded_rectangle(box, radius, fill=PAPEL + (255,))

def header(canvas, h):
    W = canvas.width; grad = Image.new("RGBA", (W, h)); px = grad.load()
    for y in range(h):
        for x in range(W):
            t = (x / W) * 0.55 + (y / h) * 0.45
            px[x, y] = (int(214 + (126-214)*t), int(31 + (11-31)*t), int(42 + (18-42)*t), 255)
    canvas.alpha_composite(grad, (0, 0))
    glow = Image.new("RGBA", (W, h), (0,0,0,0)); ImageDraw.Draw(glow).ellipse((-W*0.2, -h*0.9, W*0.6, h*0.9), fill=(255,255,255,50))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(h*0.25)))

def th(d, text, font):  # alto real del texto
    bb = d.textbbox((0,0), text, font=font); return bb[3]-bb[1]

def centered(d, y, text, font, fill, W):
    bb = d.textbbox((0,0), text, font=font); d.text(((W - (bb[2]-bb[0]))/2 - bb[0], y - bb[1]), text, font=font, fill=fill); return bb[3]-bb[1]

def leftcol(d, x, y, text, font, fill):
    bb = d.textbbox((0,0), text, font=font); d.text((x - bb[0], y - bb[1]), text, font=font, fill=fill); return bb[3]-bb[1]

def wa_icon(h):
    return fit(Image.open(A / "logos/whatsapp.png").convert("RGBA"), h=h)

def dashed(d, x0, x1, y, S):
    for x in range(x0, x1, int(14*S)): d.line((x, y, x + int(6*S), y), fill=(29,24,22,40), width=max(1, int(2*S)))

def base(W, H, logo_h=48, logo_y=64):
    S = W / 1200
    c = Image.new("RGBA", (W, H), CREMA + (255,))
    hh = int(0.27 * H); header(c, hh)
    lg = fit(tint_white(A / "logos/carozzi.png"), h=int(logo_h*S)); c.alpha_composite(lg, (int(70*S), int(logo_y*S)))
    d = ImageDraw.Draw(c); fl = F(int(22*S), serif=False); txt = "COMPARTIR HACE BIEN"
    bb = d.textbbox((0,0), txt, font=fl); d.text((W - int(70*S) - (bb[2]-bb[0]), int(logo_y*S) + (lg.height - (bb[3]-bb[1]))//2 - bb[1]), txt, font=fl, fill=(255,255,255,220))
    return c, S, hh

def footer(c, bottom, S):
    W = c.width; d = ImageDraw.Draw(c); py = bottom + int(44*S)
    py += centered(d, py, "Escanea para guardar mi contacto", F(int(32*S)), ROJO, W) + int(34*S)
    logos = [fit(Image.open(A / f"logos/{n}.png").convert("RGBA"), w=int(150*S), h=int(56*S)) for n in ["ambrosoli","costa","bresler","san-francisco","master-cat","master-dog"]]
    gap = int(34*S); tw = sum(l.width for l in logos) + gap*(len(logos)-1); x = (W - tw)//2
    for l in logos:
        c.alpha_composite(l, (x, py + (int(56*S) - l.height)//2)); x += l.width + gap

def vertical(name):
    W, H = 1200, 1800; c, S, hh = base(W, H, logo_h=84, logo_y=112); d = ImageDraw.Draw(c)
    m = 80; diam, ring = 280, 10; top = hh - 60
    fn, fc, fe, ft, fu = F(74), F(36, False), F(30, False), F(32, False), F(27, False)
    qs = 470
    # altura de la tarjeta calculada desde el contenido
    inner = diam//2 + 40 + th(d, NOMBRE, fn) + 22 + th(d, CARGO, fc) + 12 + th(d, EMPRESA, fe) + 46 + qs + 44 + th(d, FONO, ft) + 14 + th(d, WEB, fu) + 64
    bottom = top + inner
    shadow_card(c, (m, top, W - m, bottom), 36)
    ph = circle_photo(diam, ring); paste_shadowed(c, ph, ((W - ph.width)//2, top - ph.height//2), blur=22)
    y = top + diam//2 + 40
    y += centered(d, y, NOMBRE, fn, TINTA, W) + 22
    y += centered(d, y, CARGO, fc, ROJO, W) + 12
    y += centered(d, y, EMPRESA, fe, GRIS, W) + 46
    qr = fit(qr_image(qs), w=qs); c.alpha_composite(qr, ((W - qr.width)//2, y)); y += qr.height + 44
    d = ImageDraw.Draw(c)
    line = FONO + "   ·   " + MAIL; bb = d.textbbox((0,0), line, font=ft); lh = bb[3]-bb[1]
    ic = wa_icon(int(lh * 1.25)); gap = 14; tw = ic.width + gap + (bb[2]-bb[0]); x0 = (W - tw)//2
    c.alpha_composite(ic, (x0, y + (lh - ic.height)//2)); d = ImageDraw.Draw(c)
    d.text((x0 + ic.width + gap - bb[0], y - bb[1]), line, font=ft, fill=TINTA); y += lh + 14
    centered(d, y, WEB, fu, GRIS, W)
    footer(c, bottom, S)
    c.convert("RGB").save(OUT / name, optimize=True); print("OK", name, (W, H), "tarjeta hasta", bottom)

def cuadrada(name):
    W, H = 1500, 1500; c, S, hh = base(W, H); d = ImageDraw.Draw(c)
    m = 100; pad = 80; top = hh - 70; bottom = H - int(236*S); 
    shadow_card(c, (m, top, W - m, bottom), 44)
    # columna derecha: QR compacto
    qs = 460; qr = fit(qr_image(qs), w=qs); qx = W - m - pad - qr.width; qy = top + (bottom - top - qr.height)//2
    c.alpha_composite(qr, (qx, qy)); d = ImageDraw.Draw(c)
    # columna izquierda: foto + textos grandes
    x = m + pad; diam, ring = 230, 9
    fn, fc, fe, ft, fu = F(72), F(36, False), F(30, False), F(31, False), F(27, False)
    n1, n2 = "Iván Bastías", "Castex"
    block = diam + 2*ring + 34 + th(d, n1, fn) + 6 + th(d, n2, fn) + 22 + th(d, CARGO, fc) + 12 + th(d, EMPRESA, fe) + 34 + 34 + th(d, FONO, ft) + 12 + th(d, MAIL, ft) + 14 + th(d, WEB, fu)
    y = top + (bottom - top - block)//2
    ph = circle_photo(diam, ring); paste_shadowed(c, ph, (x - ring, y), blur=18); y += ph.height + 34
    d = ImageDraw.Draw(c)
    y += leftcol(d, x, y, n1, fn, TINTA) + 6
    y += leftcol(d, x, y, n2, fn, TINTA) + 22
    y += leftcol(d, x, y, CARGO, fc, ROJO) + 12
    y += leftcol(d, x, y, EMPRESA, fe, GRIS) + 34
    dashed(d, x, qx - 60, y, S); y += 34
    bb = d.textbbox((0,0), FONO, font=ft); lh = bb[3]-bb[1]; ic = wa_icon(int(lh * 1.25))
    c.alpha_composite(ic, (x, y + (lh - ic.height)//2)); d = ImageDraw.Draw(c)
    y += leftcol(d, x + ic.width + 12, y, FONO, ft, TINTA) + 12
    y += leftcol(d, x, y, MAIL, ft, TINTA) + 14
    leftcol(d, x, y, WEB, fu, GRIS)
    footer(c, bottom, S)
    c.convert("RGB").save(OUT / name, optimize=True); print("OK", name, (W, H))

vertical("1-tarjeta-vertical.png")
cuadrada("2-tarjeta-cuadrada.png")
