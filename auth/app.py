"""Backend de acceso a /docs/ para la landing de LibraClub -- config sobre
libra_web_kit.docs_auth (extraído 2026-07-26, ver
wiki/analyses/auditoria-duplicacion-familia-libra.md).

`verify_path` es `/auth/verify` y no `/api/auth/verify`: LibraClub monta su
auth con `libraauth.session_auth`, como Gestiolibra/MedLibra/VentaLibra.
Contalibra y Restolibra usan la otra convención.
"""
from libra_web_kit.docs_auth import DocsLoginTheme, build_docs_login_app

app = build_docs_login_app(
    product_name="LibraClub",
    apex_domain_default="libraclub.com.ar",
    secret_key_env="DOCS_SESSION_SECRET",
    secret_key_default="libraclub-docs-secret-change-me",
    verify_path="/auth/verify",
    slug_placeholder="tu-complejo",
    # El verde del icono del producto, medido del kit de marca -- ver el
    # concepto `identidad-visual-suite-libra` del wiki.
    theme=DocsLoginTheme(accent="#017b4b", accent_hover="#015c38"),
)
