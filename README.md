# Tarjeta digital · Iván Bastías Castex

Tarjeta de contacto permanente publicada en GitHub Pages:
**https://aictmopenclaw-a11y.github.io/ivan-bastias/**

- `index.html` — la tarjeta (HTML/CSS puro, sin build, sin dependencias).
- `ivan-bastias.vcf` — contacto descargable (vCard 3.0).
- `assets/logos/` — logos oficiales en PNG con transparencia (fuente: carozzicorp.com y mastercat.cl).
- `scripts/make_qr.py` — genera los QR en `entregables/` (segno, local).
- `scripts/verify_qr.py` — decodifica los QR y confirma el contenido.
- `scripts/process_logos.py` — limpia los logos crudos de `assets/logos/raw/` (carpeta ignorada en git).

## Por qué este QR no vence
El QR impreso codifica directamente la URL de arriba. No hay acortador, plataforma ni suscripción entre medio.
Mientras exista este repositorio en GitHub, la página responde.

## Actualizar datos
Editar `index.html` y `ivan-bastias.vcf`, hacer commit y push a `main`. GitHub Pages publica solo.
El QR impreso no cambia: sigue apuntando a la misma URL.

## Entorno local
```bash
python3 -m venv .venv && .venv/bin/pip install segno opencv-python-headless Pillow reportlab cairosvg numpy
.venv/bin/python scripts/make_qr.py && .venv/bin/python scripts/verify_qr.py
```
