#!/usr/bin/env python3
"""Generate or serve the read-only WireNet Inspector."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from okf_projection import build_graph, collect_okf_projection


DEFAULT_PORT = 4318


def load_template() -> str:
    plugin_root = Path(__file__).resolve().parents[1]
    return (plugin_root / "viewer/manager-viewer.html").read_text(encoding="utf-8")


def generate_html(manager_dir: Path, *, bundle_name: str | None = None) -> tuple[str, dict[str, int]]:
    manager_dir = manager_dir.expanduser().resolve()
    if not manager_dir.is_dir():
        raise FileNotFoundError(f"Manager directory not found: {manager_dir}")
    graph = build_graph(collect_okf_projection(manager_dir))
    graph_json = json.dumps(graph, ensure_ascii=False).replace("</", "<\\/")
    name_json = json.dumps(bundle_name or manager_dir.name, ensure_ascii=False).replace("</", "<\\/")
    html = load_template().replace("__BUNDLE_NAME__", name_json).replace("__BUNDLE_DATA__", graph_json)
    return html, {
        "concepts": len(graph["nodes"]),
        "edges": len(graph["edges"]),
        "bytes": len(html.encode("utf-8")),
    }


def default_output_path() -> Path:
    output_dir = Path(tempfile.gettempdir()) / "wirenet-manager"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "manager-viewer.html"


def serve_html(html: str, port: int) -> None:
    html_bytes = html.encode("utf-8")

    class ViewerHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            host = self.headers.get("Host", "").split(":", 1)[0].strip("[]")
            if host not in {"127.0.0.1", "localhost", "::1"}:
                self.send_error(403)
                return
            if self.path not in {"/", "/index.html"}:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(html_bytes)

        def log_message(self, format_string: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), ViewerHandler)
    print("WireNet Inspector", flush=True)
    print(f"URL: http://127.0.0.1:{server.server_port}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render Manager concepts in the read-only Google-derived WireNet Inspector."
    )
    parser.add_argument(
        "--manager-dir",
        type=Path,
        default=Path(os.environ.get("WIRENET_MANAGER_DIR", "~/Manager")),
        help="Manager content root (default: WIRENET_MANAGER_DIR or ~/Manager)",
    )
    parser.add_argument("--out", type=Path, help="Write the generated HTML to this path")
    parser.add_argument("--name", help="Bundle title (default: Manager directory name)")
    parser.add_argument("--serve", action="store_true", help="Serve the page on 127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Local port (default: {DEFAULT_PORT})")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not 1 <= args.port <= 65535:
        raise SystemExit("--port must be between 1 and 65535")
    html, counts = generate_html(args.manager_dir, bundle_name=args.name)
    print(f"Inspector concepts: {counts['concepts']}", flush=True)
    print(f"Graph edges: {counts['edges']}", flush=True)
    if args.serve:
        serve_html(html, args.port)
        return 0
    output_path = (args.out or default_output_path()).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Inspector: {output_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
