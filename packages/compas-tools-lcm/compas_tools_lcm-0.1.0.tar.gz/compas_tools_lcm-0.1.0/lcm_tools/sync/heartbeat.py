"""
Clock publishing through LCM as a message with a utime. The default frequency of
the clocks is 1, 5  and 20 Hz.
"""

import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import lcm
import senlcm


class Clock:
    def __init__(self, frequency: int) -> None:
        self.channel = f"HEARTBEAT_{frequency}_HZ"
        self.publish_time = time.time()
        self.timestep = 1.0 / frequency
        self.sequence = 0
        self.frame_id = "none"
        print(f"[INFO] Heartbeat initialized at {frequency} Hz published through {self.channel}")

    def check(self):
        if time.time() - self.publish_time >= self.timestep:
            self.publish_time = time.time()
            return True
        else:
            return False

    def publish(self):
        msg = senlcm.image_sync_t()
        msg.header.timestamp = int(self.publish_time * 1e+06)
        msg.header.sequence = int(self.sequence)
        msg.header.frame_id = self.frame_id
        msg.utime = int(self.publish_time * 1e+06)
        return msg


if __name__ == "__main__":
    # Connect to LCM
    lc = lcm.LCM()

    # Create Clocks
    clock_1_hz = Clock(1)
    clock_5_hz = Clock(5)
    clock_20_hz = Clock(20)

    while True:
        if clock_1_hz.check():
            lc.publish(clock_1_hz.channel, clock_1_hz.publish().encode())
            clock_1_hz.sequence += 1

        if clock_5_hz.check():
            lc.publish(clock_5_hz.channel, clock_5_hz.publish().encode())
            clock_5_hz.sequence += 1

        if clock_20_hz.check():
            lc.publish(clock_20_hz.channel, clock_20_hz.publish().encode())
            clock_20_hz.sequence += 1

        time.sleep(0.001)
