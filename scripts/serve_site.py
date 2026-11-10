#!/usr/bin/env python3
"""Preview the site, rebuilding its resource index when local source files change."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import threading
from urllib.parse import urlsplit

import build_site

_lock = threading.Lock()
_last_snapshot = None


def snapshot():
    paths = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=build_site.ROOT,
    ).decode().split('\0')
    watched = {build_site.ROOT / p for p in paths if p and Path(p).parts[0] in build_site.SEMESTERS}
    watched.update(build_site.ROOT / p for p in ['site/app.js', 'site/styles.css', 'site/index.html'])
    return tuple(sorted((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in watched if p.is_file()))


def refresh():
    global _last_snapshot
    with _lock:
        current = snapshot()
        if current != _last_snapshot:
            build_site.build()
            _last_snapshot = snapshot()


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path in ['/', '/index.html', '/data.js']:
            refresh()
        super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=4173)
    args = parser.parse_args()
    refresh()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(PreviewHandler, directory=str(build_site.ROOT / 'site')))
    print(f'Preview: http://localhost:{args.port} (refresh the page after editing course files)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
