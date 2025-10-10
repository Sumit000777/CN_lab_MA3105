import random
import time

def go_back_n(total_frames=10, window_size=4, loss_prob=0.2):
    base = 0
    next_seq = 0
    frames = [f"Frame {i}" for i in range(total_frames)]
    while base < total_frames:
        # Send window
        end = min(base + window_size, total_frames)
        print(f"Sending frames {base} to {end-1}")
        lost = -1
        for i in range(base, end):
            if random.random() < loss_prob:
                print(f"Frame {i} lost, retransmitting frames {i} to {end-1}")
                lost = i
                break
        if lost != -1:
            base = lost
        else:
            print(f"ACK {end-1} received")
            base = end

go_back_n()
