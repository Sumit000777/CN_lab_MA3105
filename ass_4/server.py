import cv2
import socket
import math
import time

# Server settings
IP = "127.0.0.1"     # Change to client IP if over network
PORT = 5000
ADDR = (IP, PORT)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open video
cap = cv2.VideoCapture("/home/iitp/Downloads/6521834-uhd_3840_2160_30fps.mp4")   
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = 1 / fps if fps > 0 else 0.04

CHUNK_SIZE = 60000  # UDP packet size limit

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for efficiency
    frame = cv2.resize(frame, (640, 480))

    # Encode frame as JPEG
    _, encoded = cv2.imencode('.jpg', frame)
    data = encoded.tobytes()

    # Split frame into chunks
    total_chunks = math.ceil(len(data) / CHUNK_SIZE)

    for i in range(total_chunks):
        chunk = data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
        marker = 1 if i == total_chunks - 1 else 0  # last packet marker
        packet = bytes([marker]) + chunk
        sock.sendto(packet, ADDR)

    time.sleep(frame_interval)

cap.release()
sock.close()

