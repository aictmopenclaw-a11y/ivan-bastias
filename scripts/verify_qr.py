"""Decodifica los QR generados y verifica que el contenido sea exactamente el esperado."""
import sys
from pathlib import Path
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_qr import URL, VCARD_MIN, OUT

det = cv2.QRCodeDetector()
ok = True
for stem, expected in [("qr-pagina", URL), ("qr-pagina-con-logo", URL), ("qr-vcard", VCARD_MIN)]:
    p = OUT / f"{stem}.png"
    if not p.exists():
        print(f"SKIP {stem} (no existe)"); continue
    img = cv2.imread(str(p))
    # reducir para que el detector no se ahogue con 2000 px
    h, w = img.shape[:2]
    if w > 800:
        img = cv2.resize(img, (800, int(h * 800 / w)), interpolation=cv2.INTER_AREA)
    data, pts, _ = det.detectAndDecode(img)
    match = data.replace("\n", "\r\n") == expected or data == expected
    ok &= match
    print(f"{'OK ' if match else 'FAIL'} {stem}: {data[:60]!r}...")
print("TODOS OK" if ok else "HAY FALLAS")
sys.exit(0 if ok else 1)
