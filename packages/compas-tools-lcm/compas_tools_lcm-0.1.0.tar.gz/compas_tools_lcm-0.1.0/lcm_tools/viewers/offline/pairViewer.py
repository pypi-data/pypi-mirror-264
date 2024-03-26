#!/usr/bin/python

import argparse
import os
from os.path import isdir, join

import cv2
import lcm
import numpy as np
from senlcm import image_sync_t


class PairViewer:

    def __init__(self, lcm, channel_l, channel_r, path, scale):
        # LCM channels
        self.channel_l = channel_l
        self.channel_r = channel_r
        self.lcm = lcm

        # Directories to load bayer images from
        if not isdir(path):
            raise ValueError("The provided path is not a directory.")
        self.path = path
        self.path_l = ""
        self.path_r = ""

        # Timers to manage synchronization
        self.utime_l = 1_000_000
        self.utime_r = 0

        # Viewer scale factor
        self.scale = scale

    def handler_utime(self, channel, data):
        msg = image_sync_t.decode(data)
        if channel == self.channel_l:
            self.utime_l = msg.utime
            self.path_l = join(self.path, "MANTA_L", str(self.utime_l) + ".tif")
        elif channel == self.channel_r:
            self.utime_r = msg.utime
            self.path_r = join(self.path, "MANTA_R", str(self.utime_r) + ".tif")

    def run(self):
        # Subscribe to LCM channels
        self.lcm.subscribe(self.channel_l, self.handler_utime)
        self.lcm.subscribe(self.channel_r, self.handler_utime)

        while True:
            self.lcm.handle_timeout(100)
            # Check if the images are synchronized (within 100 ms)
            if np.abs(self.utime_l - self.utime_r) < 100_000:
                # Check if the images exist
                if os.path.isfile(self.path_l) & os.path.isfile(self.path_r):
                    img_l = cv2.imread(self.path_l, cv2.IMREAD_GRAYSCALE)
                    img_r = cv2.imread(self.path_r, cv2.IMREAD_GRAYSCALE)
                    # Convert to BGR
                    try:
                        img_l = cv2.cvtColor(img_l, cv2.COLOR_BAYER_BG2BGR)
                        img_r = cv2.cvtColor(img_r, cv2.COLOR_BAYER_BG2BGR)
                    except Exception:
                        continue

                    # Add timestamp to the images
                    color = (0, 255, 0)
                    cv2.putText(img_l, f"LEFT: {self.utime_l}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                    cv2.putText(img_r, f"RIGHT: {self.utime_r}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)

                    # Horizontally stack the images
                    stack = np.hstack((img_l, img_r))

                    # Resize the image
                    h = int(stack.shape[0]*self.scale)
                    w = int(stack.shape[1]*self.scale)
                    stack = cv2.resize(stack, (w, h))

                    # Show the images
                    cv2.imshow("Images", stack)

            key = cv2.waitKey(1)
            if key & 0xFF == ord("q"):
                break

    def run_test(self):
        self.lcm.subscribe(self.channel_l, self.handler_utime)
        self.lcm.subscribe(self.channel_r, self.handler_utime)
        while True:
            self.lcm.handle_timeout(100)
            # if np.abs(self.utime_l - self.utime_r) < 100_000
            if os.path.isfile(self.path_r):
                print(self.path_r)
                bayer_r = cv2.imread(self.path_r, cv2.IMREAD_GRAYSCALE)
                bayer_l = bayer_r*0
                stack = np.hstack((bayer_l, bayer_r))
                h = int(stack.shape[0]*self.scale)
                w = int(stack.shape[1]*self.scale)
                stack_res = cv2.resize(stack, (w, h))
                cv2.imshow("Images", stack_res)
            key = cv2.waitKey(1)
            if key & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A camera calibration viewer tool", add_help=True)
    parser.add_argument("-cL", "--channel_left", default="MANTA_L_SYNC", type=str)
    parser.add_argument("-cR", "--channel_right", default="MANTA_R_SYNC", type=str)
    parser.add_argument("-vs", "--viewer_scale", default="0.33", type=float)
    parser.add_argument("-p", "--bayer_path", default="", type=str)
    args = parser.parse_args()

    # Initialize LCM
    lc = lcm.LCM()

    # Initialize viewer
    viewer = PairViewer(lc, args.channel_left, args.channel_right, args.bayer_path, args.viewer_scale)
    viewer.run()
