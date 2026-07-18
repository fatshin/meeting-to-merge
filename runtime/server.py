from __future__ import annotations

import argparse
import html
import json
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import product


ROOT = Path(__file__).resolve().parent
STYLE = (ROOT / "static" / "style.css").read_text()


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def result_markup(result: dict[str, Any]) -> str:
    metrics = "".join(
        f'<div class="metric"><strong>{esc(value)}</strong><span>{esc(key.replace("_", " "))}</span></div>'
        for key, value in result.get("metrics", {}).items()
    )
    findings = "".join(
        f"""<details class="finding">
          <summary><span>{esc(item.get("id", item.get("exercise", item.get("status", "Result"))))}</span><b>{esc(item.get("status", item.get("decision", item.get("severity", ""))))}</b></summary>
          <pre>{esc(json.dumps(item, indent=2, ensure_ascii=False))}</pre>
        </details>"""
        for item in result.get("items", [])
    )
    evidence = "".join(
        f'<li><span>{esc(item["label"])}</span><b>{esc(item["value"])}</b></li>'
        for item in result.get("evidence", [])
    )
    artifact = esc(json.dumps(result.get("artifact", {}), indent=2, ensure_ascii=False))
    return f"""<section class="result" aria-live="polite">
      <div class="status">{esc(result.get("status", "COMPLETE"))}</div>
      <h2>{esc(result.get("headline", "Analysis complete"))}</h2>
      <div class="metrics">{metrics}</div>
      <div class="result-grid">
        <div><h3>Findings</h3>{findings or '<p class="empty">No findings.</p>'}</div>
        <aside><h3>Evidence</h3><ul>{evidence}</ul></aside>
      </div>
      <details class="artifact"><summary>Machine-readable artifact</summary><pre>{artifact}</pre></details>
    </section>"""


def page(result: dict[str, Any] | None = None, values: dict[str, str] | None = None, error: str | None = None) -> str:
    definition = product.PRODUCT
    current = values or {field.name: field.value for field in definition.fields}
    fields = "".join(
        f"""<label>
          <span>{esc(field.label)}</span>
          <textarea name="{esc(field.name)}" rows="{field.rows}" spellcheck="false">{esc(current.get(field.name, field.value))}</textarea>
        </label>"""
        for field in definition.fields
    )
    if error:
        output = f'<section class="result error"><div class="status">INPUT ERROR</div><h2>{esc(error)}</h2></section>'
    elif result:
        output = result_markup(result)
    else:
        output = '<section class="idle"><div></div><p>Run the fixed offline case to generate a source-linked decision.</p></section>'
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{esc(definition.tagline)}">
  <title>{esc(definition.name)}</title>
  <style>:root{{--accent:{definition.accent}}}{STYLE}</style>
</head>
<body>
  <header><a href="/">PROOF {definition.number:02}</a><span>OPENAI BUILD WEEK · OFFLINE JUDGE PATH</span></header>
  <main>
    <section class="intro">
      <p>PRODUCT {definition.number:02}</p>
      <h1>{esc(definition.name)}</h1>
      <blockquote>{esc(definition.tagline)}</blockquote>
    </section>
    <div class="workspace">
      <form method="post">
        <div class="pane-title"><b>Input</b><small>Editable fixture</small></div>
        {fields}
        <button type="submit">Run analysis <span>→</span></button>
      </form>
      <div class="output">
        <div class="pane-title"><b>Decision</b><small>Validated evidence</small></div>
        {output}
      </div>
    </div>
  </main>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "BuildWeekProduct/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def send_page(self, markup: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = markup.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if urllib.parse.urlparse(self.path).path != "/":
            self.send_page(page(error="Not found"), HTTPStatus.NOT_FOUND)
            return
        self.send_page(page())

    def do_POST(self) -> None:
        if urllib.parse.urlparse(self.path).path != "/":
            self.send_page(page(error="Not found"), HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length", "0"))
        if length > 1_000_000:
            self.send_page(page(error="Input exceeds the 1 MB demo limit."), HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            return
        values = {
            key: items[-1]
            for key, items in urllib.parse.parse_qs(self.rfile.read(length).decode(), keep_blank_values=True).items()
        }
        try:
            self.send_page(page(result=product.analyze(values), values=values))
        except (KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
            self.send_page(page(values=values, error=str(exc)), HTTPStatus.BAD_REQUEST)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"{product.PRODUCT.name}: http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

