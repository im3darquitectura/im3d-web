#!/usr/bin/env python3
"""Genera el sitio estático de IM3D Arquitectura en ./site a partir de data.json."""
import json, os, re, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
CDN = "https://dkemhji6i1k0x.cloudfront.net/000_clients/913095/"
DOMAIN = "www.im3darquitectura.com"
BG = "#3c4a52"

data = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))

# --------------------------------------------------------------------------
# Lista de imágenes a descargar (url remota -> ruta local)
images = {}  # local relative path -> remote url
PREVIEW = os.environ.get("PREVIEW") == "1"   # usar las imágenes remotas (solo para previsualizar)
def img(name, folder="page"):
    local = f"img/{name}"
    images[local] = CDN + f"{folder}/{name}"
    return images[local] if PREVIEW else "/" + local

LOGO = img("913095UH02ypYh.png", "file")
FAVICON_ICO = img("32x32-91309542cNJvja.ico", "file")
FAVICON_PNG = img("196x196-91309542cNJvja.jpg", "file")

MENUS = {
    "es": {
        "items": [("INICIO", "/"), ("PROYECTOS", "/proyectos/"), ("ESTUDIO", "/estudio/"), ("CONTACTO", "/contacto/"), ("| EN", "/home/")],
        "footer": "© 2025 IM3D Arquitectura | TODOS LOS DERECHOS RESERVADOS",
        "lang": "es",
        "desc": "Estudio de Arquitectura e interiorismo especializado en visualización 3D",
    },
    "en": {
        "items": [("HOME", "/home/"), ("PROJECTS", "/projects/"), ("STUDIO", "/studio/"), ("CONTACT", "/contact/"), ("| ES", "/")],
        "footer": "© 2025 IM3D Arquitectura | ALL RIGHTS RESERVED.",
        "lang": "en",
        "desc": "Architecture and interior design studio specialized in 3D visualization",
    },
}
EN_PAGES = {"home", "projects", "studio", "contact"}
def lang_of(uri):
    return "en" if (uri in EN_PAGES or uri.endswith("-en")) else "es"

# --------------------------------------------------------------------------
def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

def paras_html(paras, highlight=True):
    out = []
    for p in paras:
        if p == "---":
            out.append("<hr>")
            continue
        if p == "":
            out.append("<p>&nbsp;</p>")
            continue
        size = None
        if "|" in p and re.match(r"^\d+px\|", p):
            size, p = p.split("|", 1)
        txt = md_inline(p.strip()).replace("  ", "&nbsp;&nbsp;&nbsp;")
        cls = ""
        if size == "28px":
            cls = ' class="titulo"'
        elif highlight and size in ("16px", "14px"):
            cls = f' class="meta meta-{size[:-2]}"'
        elif size:
            cls = f' style="font-size:{size}"'
        out.append(f"<p{cls}>{txt}</p>")
    return "\n".join(out)

def layout(uri, title, body, lang, extra_class=""):
    m = MENUS[lang]
    cur = "/" if uri == "inicio" else f"/{uri}/"
    nav = []
    for label, href in m["items"]:
        active = ' class="activo"' if href == cur else ""
        nav.append(f'<li><a href="{href}"{active}>{html.escape(label)}</a></li>')
    canonical = f"https://{DOMAIN}{cur}"
    return f"""<!DOCTYPE html>
<html lang="{m['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(m['desc'])}">
<meta name="theme-color" content="{BG}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="IM3D Arquitectura">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(m['desc'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON_ICO}">
<link rel="apple-touch-icon" href="{FAVICON_PNG}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=PT+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/estilo.css">
</head>
<body class="{extra_class}">
<header class="cabecera">
  <a class="logo" href="{'/home/' if lang=='en' else '/'}"><img src="{LOGO}" alt="IM3D Arquitectura"></a>
  <button class="menu-btn" aria-label="Menú" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="menu"><ul>{''.join(nav)}</ul></nav>
</header>
<main>
{body}
</main>
<section class="redes">
  <a href="https://www.instagram.com/im3darquitectura/" target="_blank" rel="noopener" aria-label="Instagram">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2M12 0C8.7 0 8.3 0 7.1.1 5.8.1 4.9.3 4.1.6c-.8.3-1.5.7-2.1 1.4C1.3 2.6.9 3.3.6 4.1.3 4.9.1 5.8.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.1 1.3.3 2.2.6 3 .3.8.7 1.5 1.4 2.1.6.6 1.3 1 2.1 1.4.8.3 1.7.5 3 .6C8.3 24 8.7 24 12 24s3.7 0 4.9-.1c1.3-.1 2.2-.3 3-.6.8-.3 1.5-.7 2.1-1.4.6-.6 1-1.3 1.4-2.1.3-.8.5-1.7.6-3 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.1-1.3-.3-2.2-.6-3-.3-.8-.7-1.5-1.4-2.1C21.4 1.3 20.7.9 19.9.6 19.1.3 18.2.1 16.9.1 15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>
  </a>
</section>
<footer class="pie">{html.escape(m['footer'])}</footer>
<div class="lightbox" id="lightbox" hidden>
  <button class="lb-cerrar" aria-label="Cerrar">&times;</button>
  <button class="lb-prev" aria-label="Anterior">&#8249;</button>
  <img alt="">
  <button class="lb-next" aria-label="Siguiente">&#8250;</button>
</div>
<script src="/js/sitio.js" defer></script>
</body>
</html>
"""

def render_sections(uri, page):
    parts = []
    for s in page["S"]:
        t = s["t"]
        if t == "cover":
            parts.append(f'<section class="portada" style="background-image:url({img(s["img"])})"></section>')
        elif t == "collection":
            tiles = []
            for suri, title, thumb in s["c"]:
                tiles.append(
                    f'<a class="tarjeta" href="/{suri}/" style="background-image:url({img(thumb)})">'
                    f'<span class="tarjeta-titulo">{html.escape(title)}</span></a>'
                )
            parts.append('<section class="coleccion">' + "\n".join(tiles) + "</section>")
        elif t == "gallery":
            txt = paras_html(s["p"])
            imgs = []
            for i, g in enumerate(s["g"]):
                name, w, h = g[0], g[1], g[2]
                imgs.append(
                    f'<a class="foto" href="{img(name)}" data-i="{i}">'
                    f'<img src="{img(name)}" width="{w}" height="{h}" loading="{"eager" if i < 2 else "lazy"}" alt="{html.escape(page["T"])}"></a>'
                )
            parts.append(f'<section class="proyecto"><div class="ficha">{txt}</div><div class="galeria">' + "\n".join(imgs) + "</div></section>")
        elif t == "form":
            txt = paras_html(s["p"], highlight=False)
            fields = []
            for ftype, label in s["form"]:
                name = re.sub(r"[^a-z]", "", label.lower()) or "campo"
                if ftype == "textarea":
                    fields.append(f'<label>{html.escape(label)}<textarea name="{name}" rows="6" required></textarea></label>')
                else:
                    fields.append(f'<label>{html.escape(label)}<input type="{ftype}" name="{name}" required></label>')
            lang = lang_of(uri)
            next_url = f"https://{DOMAIN}/{uri}/?enviado=1"
            parts.append(f"""<section class="contacto">
<div class="contacto-texto">{txt}</div>
<form class="formulario" action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="31324569-55df-45b6-b777-4a7f4f8c6228">
  <input type="hidden" name="subject" value="Mensaje desde {DOMAIN}">
  <input type="hidden" name="from_name" value="IM3D Arquitectura - Sitio web">
  <input type="hidden" name="redirect" value="{next_url}">
  <input type="checkbox" name="botcheck" class="oculto" tabindex="-1" autocomplete="off">
  {''.join(fields)}
  <button type="submit">{s.get('btn','Enviar')}</button>
  <p class="form-ok" hidden>{'Thank you, your message was sent.' if lang=='en' else 'Gracias, tu mensaje fue enviado.'}</p>
</form>
</section>""")
    return "\n".join(parts)

# --------------------------------------------------------------------------
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

sitemap = []
for uri, page in data.items():
    lang = lang_of(uri)
    body = render_sections(uri, page)
    cls = "inicio" if page["S"][0]["t"] == "cover" else ""
    title = "IM3D Arquitectura" if uri in ("inicio", "home") else f"{page['T']} - IM3D Arquitectura"
    doc = layout(uri, title, body, lang, cls)
    folder = os.path.join(OUT, uri)
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(doc)
    if uri == "inicio":
        open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(doc)
    sitemap.append(f"https://{DOMAIN}/" if uri == "inicio" else f"https://{DOMAIN}/{uri}/")

# estáticos
for d in ("css", "js"):
    shutil.copytree(os.path.join(ROOT, "static", d), os.path.join(OUT, d))
open(os.path.join(OUT, "CNAME"), "w").write(DOMAIN + "\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in sitemap) + "</urlset>\n")
# 404
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
    layout("404", "IM3D Arquitectura", '<section class="proyecto"><div class="ficha"><p class="titulo">4 0 4</p><p class="meta meta-16">Página no encontrada / Page not found</p></div></section>', "es"))

# lista de imágenes
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
with open(os.path.join(OUT, "imagenes.txt"), "w") as f:
    for local, url in sorted(images.items()):
        f.write(f"{local}\t{url}\n")

print(f"{len(data)} páginas, {len(images)} imágenes")
