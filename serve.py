"""Serve the mirrored ClinicSoftware site from the local port root."""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit
import posixpath
import os


ROOT = Path(__file__).resolve().parent
SITE = ROOT / "www.lassomd.com"
ASSET_ROOTS = {
    "ajax.googleapis.com",
    "cdn.prod.website-files.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
}


class ClinicSoftwareHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Revalidate pages after deployments and rollbacks.
        self.send_header("Cache-Control", "no-cache, max-age=0, must-revalidate")
        super().end_headers()

    def translate_path(self, path: str) -> str:
        request_path = unquote(urlsplit(path).path)
        parts = [part for part in posixpath.normpath(request_path).split("/") if part not in {"", ".", ".."}]
        base = ROOT if parts and parts[0] in ASSET_ROOTS else SITE
        target = base.joinpath(*parts)
        if target.is_dir():
            target /= "index.html"
        return str(target)


if __name__ == "__main__":
    host = os.getenv("CLINICSOFTWARE_HOST", "127.0.0.1")
    port = int(os.getenv("CLINICSOFTWARE_PORT", "8081"))
    server = ThreadingHTTPServer((host, port), ClinicSoftwareHandler)
    print(f"ClinicSoftware site: http://{host}:{port}")
    server.serve_forever()
