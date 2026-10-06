from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none",
    "filter": True,
    "persistAuthorization": True,
    "tryItOutEnabled": True,
    "displayRequestDuration": True,
    "tagsSorter": "alpha",
    "operationsSorter": "alpha",
    "defaultModelsExpandDepth": 1,
    "deepLinking": True,
}

CUSTOM_STYLE = """
<style>
  :root {
    --bg-page: #fff5f9;
    --bg-card: #ffffff;
    --bg-soft: #fff0f6;
    --text-main: #3d3138;
    --text-muted: #8a747f;
    --border: #f2d7e3;
    --accent: #e0559a;
    --accent-dark: #c93d84;
    --get: #2f9e6f;
    --post: #e0559a;
    --put: #e79035;
    --delete: #dc4a5b;
  }

  html, body {
    background-color: var(--bg-page) !important;
    color: var(--text-main) !important;
  }

  body {
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Helvetica,
      Arial, sans-serif !important;
    -webkit-font-smoothing: antialiased;
  }

  .swagger-ui {
    background-color: var(--bg-page);
    color: var(--text-main);
  }

  .swagger-ui .topbar {
    display: none;
  }

  .swagger-ui .info {
    margin: 0 0 18px 0;
    padding: 22px 24px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
  }

  .swagger-ui .info .title {
    color: var(--text-main);
    font-weight: 600;
    font-size: 26px;
    letter-spacing: -0.4px;
  }

  .swagger-ui .info .title span,
  .swagger-ui .info h1.title small,
  .swagger-ui .info small.version-stamp,
  .swagger-ui .info pre.version {
    display: none !important;
  }

  .swagger-ui .info p,
  .swagger-ui .info li,
  .swagger-ui .info code,
  .swagger-ui .info a {
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.7;
  }

  .swagger-ui .info a {
    color: var(--accent);
  }

  .swagger-ui .scheme-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px 16px;
    box-shadow: none;
    top: 62px;
  }

  .swagger-ui .opblock-tag {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--text-main);
    font-size: 15px;
    font-weight: 600;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: background-color 0.15s ease;
  }

  .swagger-ui .opblock-tag:hover {
    background: var(--bg-soft);
  }

  .swagger-ui .opblock-tag small {
    color: var(--text-muted);
    font-size: 13px;
  }

  .swagger-ui .opblock {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 5px solid var(--border);
    border-radius: 12px;
    box-shadow: 0 1px 4px rgba(184, 92, 138, 0.06);
    margin-bottom: 14px;
    overflow: hidden;
  }

  .swagger-ui .opblock .opblock-summary {
    padding: 14px 18px;
  }

  .swagger-ui .opblock .opblock-summary-method {
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.6px;
    min-width: 72px;
    padding: 6px 12px;
    box-shadow: none;
  }

  .swagger-ui .opblock.opblock-get { border-left-color: var(--get); }
  .swagger-ui .opblock.opblock-post { border-left-color: var(--post); }
  .swagger-ui .opblock.opblock-put { border-left-color: var(--put); }
  .swagger-ui .opblock.opblock-delete { border-left-color: var(--delete); }

  .swagger-ui .opblock.opblock-get .opblock-summary { background: #f4fbf8; }
  .swagger-ui .opblock.opblock-post .opblock-summary { background: #fff3f9; }
  .swagger-ui .opblock.opblock-put .opblock-summary { background: #fffaf2; }
  .swagger-ui .opblock.opblock-delete .opblock-summary { background: #fff5f6; }

  .swagger-ui .opblock.opblock-get .opblock-summary-method { background: var(--get); color: #fff; }
  .swagger-ui .opblock.opblock-post .opblock-summary-method { background: var(--post); color: #fff; }
  .swagger-ui .opblock.opblock-put .opblock-summary-method { background: var(--put); color: #fff; }
  .swagger-ui .opblock.opblock-delete .opblock-summary-method { background: var(--delete); color: #fff; }

  .swagger-ui .opblock-summary-path,
  .swagger-ui .opblock-summary-path__deprecated,
  .swagger-ui .opblock-summary-description {
    color: var(--text-main);
    font-weight: 500;
  }

  .swagger-ui .opblock-description_wrapper p,
  .swagger-ui .opblock-external-docs-wrapper p {
    color: var(--text-muted);
  }

  .swagger-ui .opblock-body {
    background: var(--bg-card);
    border-top: 1px solid var(--border);
  }

  .swagger-ui .opblock-body pre.microlight,
  .swagger-ui textarea.curl {
    background: var(--bg-soft);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-main);
  }

  .swagger-ui table {
    border: none;
  }

  .swagger-ui table thead tr th {
    background: var(--bg-soft);
    color: var(--text-main);
    border-bottom: 1px solid var(--border);
    font-weight: 600;
    font-size: 12px;
  }

  .swagger-ui table tbody tr td {
    border-bottom: 1px solid var(--border);
    color: var(--text-main);
  }

  .swagger-ui .parameter__name,
  .swagger-ui .parameter__type,
  .swagger-ui .response-col_status,
  .swagger-ui .response-col_links,
  .swagger-ui .responses-inner h4,
  .swagger-ui .responses-inner h5 {
    color: var(--text-main);
  }

  .swagger-ui .parameters-col_description p {
    color: var(--text-muted);
  }

  .swagger-ui section.models {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    margin-top: 24px;
  }

  .swagger-ui section.models h4 {
    color: var(--text-main);
    border-bottom: 1px solid var(--border);
    padding: 16px 18px;
    font-weight: 600;
  }

  .swagger-ui section.models .model-container {
    background: var(--bg-card);
  }

  .swagger-ui .model-box,
  .swagger-ui .model {
    background: var(--bg-card) !important;
    border: 1px solid var(--border);
    border-radius: 10px;
  }

  .swagger-ui .model .prop-name,
  .swagger-ui .model .prop-type,
  .swagger-ui .model-title span {
    color: var(--text-main);
  }

  .swagger-ui .model-toggle {
    color: var(--accent);
  }

  .swagger-ui .btn {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-main);
    box-shadow: none;
    font-weight: 500;
    padding: 8px 16px;
    transition: all 0.15s ease;
  }

  .swagger-ui .btn:hover {
    background: var(--bg-soft);
    border-color: var(--accent);
    box-shadow: none;
  }

  .swagger-ui .btn.try-out__control {
    color: var(--accent-dark);
    border-color: var(--border);
  }

  .swagger-ui .btn.try-out__control.cancel {
    color: var(--delete);
    border-color: var(--delete);
    background: var(--bg-card);
  }

  .swagger-ui .btn.execute {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
  }

  .swagger-ui .btn.execute:hover {
    background: var(--accent-dark);
    border-color: var(--accent-dark);
    box-shadow: none;
  }

  .swagger-ui .btn.authorize {
    color: var(--accent-dark);
    border-color: var(--accent);
    background: var(--bg-card);
  }

  .swagger-ui .btn.authorize:hover {
    background: var(--bg-soft);
    box-shadow: none;
  }

  .swagger-ui .btn-group .btn {
    background: var(--bg-card);
    border-color: var(--border);
  }

  .swagger-ui .btn-group .btn:last-child {
    border-radius: 0 10px 10px 0;
  }

  .swagger-ui .control-btn {
    color: var(--accent);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
  }

  .swagger-ui input[type="text"],
  .swagger-ui input[type="password"],
  .swagger-ui input[type="number"],
  .swagger-ui input[type="search"],
  .swagger-ui textarea,
  .swagger-ui select {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-main);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }

  .swagger-ui input:focus,
  .swagger-ui textarea:focus,
  .swagger-ui select:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(224, 85, 154, 0.16);
    outline: none;
    color: var(--text-main);
  }

  .swagger-ui .microlight,
  .swagger-ui .highlight-code pre {
    background: var(--bg-soft);
    color: var(--text-main);
    border: 1px solid var(--border);
    border-radius: 10px;
  }

  .swagger-ui .tab li a {
    color: var(--text-muted);
    border-bottom: 2px solid transparent;
    font-weight: 500;
  }

  .swagger-ui .tab li.active a {
    color: var(--accent-dark);
    border-bottom-color: var(--accent);
  }

  .swagger-ui .response-col_description__inner div {
    color: var(--text-main);
  }

  .swagger-ui .opblock-control-header .opblock-control {
    color: var(--text-main);
  }

  .swagger-ui .download-contents {
    color: var(--accent);
  }

  .swagger-ui .filter .operation-filter-input {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-main);
  }
</style>
"""

BANNER = """
<style>
  .dev-banner {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
  }

  .dev-banner-inner {
    max-width: 1460px;
    margin: 0 auto;
    padding: 13px 24px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .dev-banner-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--accent);
    flex-shrink: 0;
  }

  .dev-banner-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-main);
    letter-spacing: -0.2px;
  }

  .dev-banner-pill {
    font-size: 11px;
    font-weight: 600;
    color: #fff;
    background: var(--accent);
    padding: 3px 11px;
    border-radius: 999px;
    letter-spacing: 0.3px;
  }

  @media (max-width: 640px) {
    .dev-banner-inner {
      flex-wrap: wrap;
    }
  }
</style>
<div class="dev-banner">
  <div class="dev-banner-inner">
    <span class="dev-banner-dot"></span>
    <span class="dev-banner-title">API Data Mahasiswa</span>
    <span class="dev-banner-pill">Dokumentasi</span>
  </div>
</div>
"""


def setup_swagger_ui(app: FastAPI) -> None:
    async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
        response = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="API Data Mahasiswa - Swagger UI",
            oauth2_redirect_url=None,
            swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
        )
        html = response.body.decode("utf-8")
        html = html.replace("</head>", CUSTOM_STYLE + "\n</head>")
        html = html.replace("<body>", "<body>" + BANNER)
        return HTMLResponse(html)

    app.add_route("/docs", custom_swagger_ui_html, include_in_schema=False)
