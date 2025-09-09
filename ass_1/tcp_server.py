#!/usr/bin/env python3
"""
tcp_server.py
Simple TCP server for CN Lab assignment.
Listens on a port > 5000, accepts client JSON messages of form:
  {"name": "Client of X", "number": 42}
Responds with JSON:
  {"name": "Server of Y", "number": 58}
If a client's "number" is outside 1..100, the server closes all sockets and exits.
"""
import socket
import json
import threading
import random
import sys

HOST = "0.0.0.0"
PORT = 60000            # choose > 5000
SERVER_NAME = "Server of Sumit Sheoran"  # change if you want

# Event to signal server shutdown
shutdown_event = threading.Event()

def handle_client(conn, addr, server_socket):
    try:
        with conn:
            data = b""
            # read until newline (we send JSON + '\n')
            while not data.endswith(b"\n"):
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk
            if not data:
                return
            try:
                msg = json.loads(data.decode().strip())
            except Exception as e:
                print(f"[{addr}] Invalid JSON: {e}")
                return

            client_name = msg.get("name", "<unknown>")
            client_num = msg.get("number")
            print(f"\nReceived from client {addr}:")
            print("  Client's name:", client_name)
            print("  Server's name:", SERVER_NAME)

            # Validate client's number
            if not isinstance(client_num, int) or not (1 <= client_num <= 100):
                print("  Client's integer:", client_num, "(OUT OF RANGE)")
                print("-> Received out-of-range number. Server shutting down.")
                # send no reply; set shutdown flag and close server socket
                shutdown_event.set()
                try:
                    server_socket.close()  # this will unblock accept()
                except:
                    pass
                return

            # pick a server integer between 1 and 100
            server_num = random.randint(1, 100)
            print("  Client's integer:", client_num)
            print("  Server's integer:", server_num)
            print("  Sum:", client_num + server_num)

            reply = {"name": SERVER_NAME, "number": server_num}
            reply_json = json.dumps(reply) + "\n"
            conn.sendall(reply_json.encode())
    except Exception as e:
        print(f"Error handling client {addr}: {e}")

def main():
    print(f"Starting server on {HOST}:{PORT} ... (Ctrl-C to stop manually)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow quick restart
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        # Accept loop
        try:
            while not shutdown_event.is_set():
                try:
                    conn, addr = s.accept()
                except OSError:
                    # socket closed (likely due to shutdown_event); break
                    break
                print(f"\nConnection from {addr}")
                # handle connection in a separate thread (so server can accept others)
                t = threading.Thread(target=handle_client, args=(conn, addr, s), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nServer interrupted by user.")
    print("Server exiting.")

if __name__ == "__main__":
    main()
