import matplotlib.pyplot as plt
import random

def tcp_congestion_control(rounds=30, loss_prob=0.1):
    cwnd = 1
    ssthresh = 16
    cwnd_history = []
    for i in range(rounds):
        if random.random() < loss_prob:
            print(f"Packet loss at round {i}, cwnd drops to 1")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1
        else:
            if cwnd < ssthresh:
                cwnd *= 2  # Slow start
            else:
                cwnd += 1  # Congestion avoidance
        cwnd_history.append(cwnd)
    plt.plot(cwnd_history)
    plt.xlabel('Round')
    plt.ylabel('cwnd')
    plt.title('TCP Congestion Control')
    plt.show()

tcp_congestion_control()
