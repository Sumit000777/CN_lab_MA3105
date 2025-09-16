#!/usr/bin/env python3
"""
part1_server.py
Simple HTTP server demonstrating ETag (MD5) and Last-Modified header handling.
Serves index.html in the current directory.
"""

import http.server
import socketserver
import hashlib
import os
import time
from email.utils import formatdate, parsedate_to_datetime

PORT = 8000
INDEX_FILE = "index.html"

def compute_etag(path):
    with open(path, "rb") as f:
        data = f.read()
    md5 = hashlib.md5(data).hexdigest()
    return '"' + md5 + '"'  # strong ETag notation with quotes

def http_date_from_mtime(mtime):
    # formatdate expects seconds since epoch; use usegmt True to produce 'GMT'
    return formatdate(timeval=mtime, usegmt=True)

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve only index.html (or let SimpleHTTPRequestHandler serve others)
        if self.path == "/" or self.path == "/index.html":
            path = os.path.join(os.getcwd(), INDEX_FILE)
            if not os.path.exists(path):
                self.send_error(404, "File not found")
                return

            # Compute validators
            etag = compute_etag(path)
            mtime = os.path.getmtime(path)
            last_modified = http_date_from_mtime(mtime)

            # Read client's headers
            client_etag = self.headers.get("If-None-Match")
            client_if_modified_since = self.headers.get("If-Modified-Since")

            send_full = True

            # Check ETag (strong validator) first
            if client_etag and client_etag.strip() == etag:
                send_full = False
            else:
                # Fallback to Last-Modified check (weak)
                if client_if_modified_since:
                    try:
                        client_dt = parsedate_to_datetime(client_if_modified_since)
                        server_dt = time.gmtime(mtime)
                        # convert client_dt to timestamp for easier compare
                        client_ts = client_dt.timestamp()
                        if client_ts >= mtime:
                            send_full = False
                    except Exception:
                        # if parsing fails, treat as modified
                        send_full = True

            if not send_full:
                # Respond 304 Not Modified with validators
                self.send_response(304)
                self.send_header("ETag", etag)
                self.send_header("Last-Modified", last_modified)
                self.end_headers()
                return

            # Else send 200 OK with content + headers
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified)
            self.end_headers()
            self.wfile.write(content)
            return
        else:
            # Fall back to default file serving behavior for other paths
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CachingHandler) as httpd:
        print(f"Part1 HTTP server serving {INDEX_FILE} at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()

