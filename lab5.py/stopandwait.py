import random
import time

def stop_and_wait(frames, loss_prob=0.2, timeout=2):
    frame_id = 0
    while frame_id < len(frames):
        print(f"Sending Frame {frame_id}")
        # Simulate frame loss
        if random.random() < loss_prob:
            print(f"Frame {frame_id} lost, retransmitting ...")
            time.sleep(timeout)
            continue
        print(f"ACK {frame_id} received")
        frame_id += 1

frames = [f"Frame {i}" for i in range(5)]
stop_and_wait(frames)
