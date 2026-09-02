# Tarjeta digital · Iván Bastías Castex

Tarjeta de contacto permanente publicada en Vercel (cuenta aictmopenclaw):
**https://ivan-bastias.vercel.app/**

- `index.html` — la tarjeta (HTML/CSS puro, sin build, sin dependencias).
- `ivan-bastias.vcf` — contacto descargable (vCard 3.0).
- `assets/logos/` — logos oficiales en PNG con transparencia (fuente: carozzicorp.com y mastercat.cl).
- `scripts/make_qr.py` — genera los QR en `entregables/` (segno, local).
- `scripts/verify_qr.py` — decodifica los QR y confirma el contenido.
- `scripts/process_logos.py` — limpia los logos crudos de `assets/logos/raw/` (carpeta ignorada en git).

## Por qué este QR no vence
El QR impreso codifica directamente la URL de arriba. No hay acortador, plataforma ni suscripción entre medio.
Mientras exista el proyecto en Vercel (cuenta aictmopenclaw), la página responde.

## Agregar la foto de Iván
Guardar la foto como `assets/foto.jpg` (cuadrada, 600x600 px o más, menos de 300 KB) y desplegar.
No hay que tocar código: la página muestra la foto si el archivo existe y las iniciales "IB" si no.

## Idiomas
La página trae selector ES / EN / PT en la cabecera. Detecta el idioma del teléfono al abrir,
recuerda la elección, y acepta `?lang=en` o `?lang=pt` en la URL. Cada idioma descarga su propio vCard
(`ivan-bastias.vcf`, `ivan-bastias-en.vcf`, `ivan-bastias-pt.vcf`) con el cargo traducido.
Los textos están en el diccionario `I18N` dentro de `index.html`.

## Actualizar datos
Editar `index.html` y los tres `.vcf`, hacer commit y push a `main`, y desplegar con `npx -y vercel@latest --prod --yes` desde esta carpeta (sesión Vercel de aictm).
El QR impreso no cambia: sigue apuntando a la misma URL.

## Entorno local
```bash
python3 -m venv .venv && .venv/bin/pip install segno opencv-python-headless Pillow reportlab cairosvg numpy
.venv/bin/python scripts/make_qr.py && .venv/bin/python scripts/verify_qr.py
```
