# LibraClub — Sitio Web / Landing

Landing de marketing de [LibraClub](https://libraclub.com.ar), el vertical de
**complejos deportivos** de la familia Libra. Mismo patrón que las otras siete
landings: HTML estático servido por nginx en un contenedor Docker, con `/docs/`
gateado por un login real contra la instancia del cliente.

## Qué se edita dónde

🔴 **Dos de los tres pedazos de este sitio NO se editan acá.**

| Qué | Dónde vive | Cómo se actualiza |
|---|---|---|
| `public/index.html` | **Este repo** | A mano |
| `public/css/style.css` | `libra-web-kit` → `templates/style.css.template` + `site_css_tokens.SITES["libraclub"]` | `scripts/generate_css.py` |
| `public/docs/*.html` | `libra-web-kit` → `docs_content/libraclub/*.html` + `docs_pages` + `docs_sidebars` | `scripts/generate_docs.py` |

Los generados llevan un encabezado que lo dice. Editarlos acá funciona hasta la
próxima corrida del generador, que los pisa sin avisar.

```bash
cd ~/proyectos/libra-web-kit
.venv/bin/python scripts/generate_css.py
.venv/bin/python scripts/generate_docs.py
```

## Qué promete esta landing, y qué no

LibraClub está en **F1**. La landing describe sólo lo construido —agenda,
canchas, tarifas, reservas, canchas fijas, bloqueos, clientes, sucursales— y
tiene una sección **"En camino"** explícita para el portal público, la caja y
factura, el buffet y el panel del dueño, que **no existen todavía**.

🔴 **Y por eso los planes son uno solo.** `plans.py` de LibraClub declara tres
—básico, estándar, premium— pero los tres habilitan exactamente lo mismo,
porque no hay ningún módulo gateable. Dibujar tres columnas idénticas en la
landing prometería una diferencia que no existe. Cuando el portal o el buffet
se construyan y se decida qué se cobra aparte, esta sección vuelve a ser de
tres.

## Estructura

```
public/
  index.html          — Landing completa
  css/style.css       — GENERADO por libra-web-kit
  docs/               — 11 páginas, GENERADAS por libra-web-kit (gateadas por login)
auth/                 — Backend FastAPI del login de /docs/
  app.py              — 20 líneas de config sobre libra_web_kit.docs_auth
  Dockerfile          — python:3.12-slim
  requirements.txt
Dockerfile            — FROM ghcr.io/marianocappucci/libra-nginx-web (imagen compartida)
docker-compose.yml    — web (8101:80) + auth (interno), red stack_stack-net
.github/workflows/
  deploy.yml          — llama al reusable workflow de libra-web-kit
  alerta-ci.yml       — avisa por Telegram si el deploy sale en rojo
```

## Desarrollo local

```bash
docker compose build
docker compose up -d
```

Sirve en `http://localhost:8101`. Requiere la red externa `stack_stack-net`; en
el VPS ya existe, en local se crea con `docker network create stack_stack-net`.

## El login de /docs/

El backend `auth/` no tiene tabla de usuarios propia: valida en tiempo real
contra `https://{subdominio}.libraclub.com.ar/auth/verify`, el endpoint
server-to-server de la app, con el secreto compartido `DOCS_AUTH_SECRET`. El
login pide el **subdominio** por texto.

Rate limiting incluido en el kit: 5 intentos fallidos por IP cada 15 minutos.

## Variables de entorno (VPS)

| Variable | Para qué |
|---|---|
| `DOCS_AUTH_SECRET` | El mismo valor que en el `.env` de cada instancia de LibraClub. Si difieren, el login de `/docs/` no valida nunca |
| `DOCS_SESSION_SECRET` | Firma la cookie de sesión de `/docs/` |
| `APEX_DOMAIN` | `libraclub.com.ar` |

## Relacionado

- Producto: [libraclub](https://github.com/marianocappucci/libraclub)
- Kit compartido: [libra-web-kit](https://github.com/marianocappucci/libra-web-kit)
- Mismo patrón: `contalibra_web`, `restolibra_web`, `gestiolibra_web`,
  `medlibra_web`, `ventalibra_web`, `libradesk_web`, `libracargo_web`
