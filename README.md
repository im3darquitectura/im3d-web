# IM3D Arquitectura — sitio estático

Réplica de www.im3darquitectura.com (Portfoliobox) como sitio estático para GitHub Pages.
60 páginas (ES + EN), 390 imágenes, mismas URL que el sitio actual (`/proyectos/`, `/casateyuna-es/`, `/home/`, …).

## 1. Subir a GitHub

1. Crear un repositorio **público** en GitHub (por ejemplo `im3d-web`).
2. Subir **todo** el contenido de esta carpeta a la raíz del repositorio
   (incluida la carpeta oculta `.github/`, que trae el flujo que descarga las imágenes).
3. En el repositorio: **Settings → Pages → Build and deployment → Source: "Deploy from a branch"**,
   rama `main`, carpeta `/ (root)`. Guardar.

## 2. Descargar las imágenes (antes de cancelar Portfoliobox)

Las fotos todavía están en el servidor de Portfoliobox. Para copiarlas al repositorio:

1. Pestaña **Actions** del repositorio → "Descargar imágenes desde Portfoliobox" → **Run workflow**.
2. Tarda unos minutos. Descarga las 390 imágenes de `imagenes.txt`, las reduce a máx. 2400 px
   (quedan ~150–250 MB en total) y las guarda en `img/` con un commit automático.
3. Si GitHub pide habilitar permisos: **Settings → Actions → General → Workflow permissions →
   "Read and write permissions"**.

Hay que hacerlo **mientras Portfoliobox siga activo**; después las imágenes ya viven en el repositorio.

## 3. Conectar el dominio www.im3darquitectura.com

El archivo `CNAME` ya está en la raíz. En el proveedor donde está registrado el dominio
(no en Portfoliobox) cambiar los registros DNS:

| Tipo  | Nombre | Valor |
|-------|--------|-------|
| CNAME | www    | `TU-USUARIO.github.io` |
| A     | @      | 185.199.108.153 |
| A     | @      | 185.199.109.153 |
| A     | @      | 185.199.110.153 |
| A     | @      | 185.199.111.153 |

(borrar los registros que apuntaban a Portfoliobox). Luego en **Settings → Pages → Custom domain**
escribir `www.im3darquitectura.com`, esperar a que valide y marcar **Enforce HTTPS**.
La propagación de DNS puede tardar entre minutos y 24 h.

## 4. Formulario de contacto

GitHub Pages no procesa formularios. El formulario usa **Web3Forms** (gratis):
envía los mensajes a `s.vallejo@im3darquitectura.com`. La **primera vez** que alguien envíe
el formulario, FormSubmit manda un correo de activación a esa dirección: hay que hacer clic
en "Activate" una sola vez.

## 5. Editar el sitio después

- Textos y proyectos: editar `data.json` (en la carpeta `fuente/`) y correr `python3 gen.py`,
  o editar directamente el `index.html` de cada carpeta.
- Para un proyecto nuevo: subir las fotos a `img/`, añadir la entrada en `data.json`
  (lista de proyectos + página con galería) y regenerar.
- Estilos: `css/estilo.css`. Menú móvil y visor de fotos: `js/sitio.js`.
