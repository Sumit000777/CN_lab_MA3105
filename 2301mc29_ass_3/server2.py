#!/usr/bin/env python3
"""
part2_raw_socket_server.py
Simple raw-socket HTTP server demonstrating Set-Cookie and Cookie handling.
Each new client receives a random session id via Set-Cookie.
"""

import socket
import uuid
import threading
from datetime import datetime, timedelta, UTC
from email.utils import formatdate

HOST = "0.0.0.0"
PORT = 8080

def build_response(body_text, set_cookie_value=None):
    body_bytes = body_text.encode("utf-8")
    headers = []
    headers.append("HTTP/1.1 200 OK")
    headers.append("Content-Type: text/html; charset=utf-8")
    headers.append(f"Content-Length: {len(body_bytes)}")
    # Add a simple Cache-Control to avoid browser caching for testing
    headers.append("Cache-Control: no-store")
    if set_cookie_value:
        # Set cookie expires in 7 days (HTTP-date)
        expires = (datetime.now(UTC) + timedelta(days=7))
        expires_str = formatdate(timeval=expires.timestamp(), usegmt=True)
        headers.append(f'Set-Cookie: session={set_cookie_value}; Expires={expires_str}; Path=/; HttpOnly')
    headers.append("")  # blank line to end headers
    headers.append("")  # placeholder for body
    header_bytes = ("\r\n".join(headers)).encode("utf-8")
    return header_bytes + body_bytes

def handle_client(conn, addr):
    try:
        data = conn.recv(8192).decode("utf-8", errors="ignore")
        if not data:
            conn.close()
            return
        # Split request lines
        lines = data.split("\r\n")
        request_line = lines[0]
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            parts = line.split(":", 1)
            if len(parts) == 2:
                headers[parts[0].strip()] = parts[1].strip()

        cookie_header = headers.get("Cookie")
        if cookie_header:
            # Try to parse session cookie
            session = None
            for part in cookie_header.split(";"):
                kv = part.strip().split("=", 1)
                if len(kv) == 2 and kv[0] == "session":
                    session = kv[1]
                    break
            if session:
                body = f"<html><body><h1>Welcome back!</h1><p>Your session id is: {session}</p></body></html>"
                response = build_response(body)
                conn.sendall(response)
                conn.close()
                return

        # If no session cookie, create a random one and send Set-Cookie
        new_session = "User" + uuid.uuid4().hex[:8]
        body = f"<html><body><h1>Welcome, new user!</h1><p>Your new session id: {new_session}</p></body></html>"
        response = build_response(body, set_cookie_value=new_session)
        conn.sendall(response)
    except Exception as e:
        print("Error handling client:", e)
    finally:
        conn.close()

def serve_forever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Part2 raw-socket HTTP server listening at http://{HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                # handle each client in a new thread
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("Shutting down server.")

if __name__ == "__main__":
    serve_forever()

