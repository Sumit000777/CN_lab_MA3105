#!/usr/bin/env python3
"""
tcp_client.py
Connects to the server, sends a JSON message with name and integer,
waits for server reply, then displays both names, integers and their sum.
"""
import socket
import json
import sys

SERVER_HOST = "127.0.0.1"   # change to server IP if remote
SERVER_PORT = 60000

def get_valid_int():
    # Accept integer between 1 and 100 from keyboard
    while True:
        try:
            s = input("Enter an integer between 1 and 100: ").strip()
            num = int(s)
            if 1 <= num <= 100:
                return num
            else:
                print("Number must be between 1 and 100. If you intentionally send an out-of-range number the server will terminate.")
        except ValueError:
            print("Please enter a valid integer.")

def main():
    client_name = f"Client of Sumit Sheoran"  # change if you want
    client_num = get_valid_int()

    payload = {"name": client_name, "number": client_num}
    payload_json = json.dumps(payload) + "\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
        except Exception as e:
            print(f"Could not connect to server at {SERVER_HOST}:{SERVER_PORT}: {e}")
            sys.exit(1)
        s.sendall(payload_json.encode())

        # Read reply (until newline)
        data = b""
        while not data.endswith(b"\n"):
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        if not data:
            print("No reply from server.")
            return
        try:
            reply = json.loads(data.decode().strip())
        except Exception as e:
            print("Invalid reply from server:", e)
            return

        server_name = reply.get("name", "<unknown>")
        server_num = reply.get("number")
        print("\n--- Exchange result ---")
        print("Client's name:", client_name)
        print("Server's name:", server_name)
        print("Client's integer:", client_num)
        print("Server's integer:", server_num)
        if isinstance(server_num, int):
            print("Sum:", client_num + server_num)
        else:
            print("Sum: cannot compute (server did not send an integer)")

if __name__ == "__main__":
    main()
