#!/usr/bin/python

import argparse

import cv2
import lcm
import numpy as np
from senlcm import image_t


class LCMPairViewer:
    def __init__(self, lcm_, channel_l, channel_r, scale):
        # Initialize channels and LCM
        self.channel_l = channel_l
        self.channel_r = channel_r
        self.lcm = lcm_

        # Timers to compute frame rate
        self.last_time_l = 0
        self.last_time_r = 0
        self.frame_rate_l = 0
        self.frame_rate_r = 0

        # Viewer scale factor
        self.scale = scale

        # Image counter
        self.counter_l = 0
        self.counter_r = 0

    def handler_lcmimage(self, channel, data):
        msg = image_t.decode(data)

        # Image dimensions
        height = msg.height
        width = msg.width

        # Convert to numpy array
        buffer = np.frombuffer(bytes(msg.data), dtype=np.uint8)
        utime = msg.header.timestamp

        # Compute frequency
        if channel == self.channel_l:
            if self.last_time_l != 0:
                self.frame_rate_l = 1/((utime * 1e-06) - self.last_time_l)
            self.last_time_l = (utime * 1e-06)
            self.counter_l += 1
        if channel == self.channel_r:
            if self.last_time_r != 0:
                self.frame_rate_r = 1/((utime * 1e-06) - self.last_time_r)
            self.last_time_r = (utime * 1e-06)
            self.counter_r += 1

        print(f"Received {self.counter_l} images left and {self.counter_r} images right ({self.frame_rate_r:.4f} Hz)",
              end="\r", flush=True)

        # Convert to OpenCV format
        # Gray scale image
        if msg.pixelformat == msg.PIXEL_FORMAT_GRAY:
            buffer = buffer.reshape((height, width, 1)).astype("uint8")

        # RGB image
        elif msg.pixelformat == msg.PIXEL_FORMAT_RGB:
            buffer = buffer.reshape((height, width, 3)).astype("uint8")
            # OpenCV works with images in BGR
            buffer = buffer[:, :, ::-1]

        # BGR image
        elif msg.pixelformat == msg.PIXEL_FORMAT_BGR:
            buffer = buffer.reshape((height, width, 3)).astype("uint8")

        # Bayer8 image
        elif msg.pixelformat == msg.PIXEL_FORMAT_BAYER_RGGB or \
             msg.pixelformat == msg.PIXEL_FORMAT_BAYER_GRBG or \
             msg.pixelformat == msg.PIXEL_FORMAT_BAYER_GBRG or \
             msg.pixelformat == msg.PIXEL_FORMAT_BAYER_BGGR:
            buffer = buffer.reshape((height, width, 1)).astype("uint8")
            buffer = cv2.cvtColor(buffer, cv2.COLOR_BayerRG2BGR)

        # Bayer16 image
        elif msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_RGGB or\
             msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_GRBG or\
             msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_GBRG or\
             msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_BGGR:
            buffer = np.frombuffer(msg.data, np.uint16)
            buffer = buffer.reshape((height, width, 1)).astype("uint16")*16
            buffer = cv2.cvtColor(buffer, cv2.COLOR_BAYER_RG2BGR)

        # MJPEG image
        elif msg.pixelformat == msg.PIXEL_FORMAT_MJPEG:
            buffer = cv2.imdecode(buffer, -1).reshape((height, width, 3)).astype("uint8")

        elif msg.pixelformat == msg.PIXEL_FORMAT_YUV411P or\
             msg.pixelformat == msg.PIXEL_FORMAT_YUV420:
            # buffer = np.fromstring(msg.data, np.uint16)
            # buffer = cv2.imdecode(buffer,-1)
            # buffer = buffer.reshape((int(0.75*height), width, 1)).astype("uint8")
            # buffer = cv2.cvtColor(buffer, cv2.COLOR_YUV2BGR_NV21)
            raise Exception("YUV pixel format not supported")
        else:
            raise Exception("Pixel format not supported")

        # Resize
        img = cv2.resize(np.array(buffer, dtype=np.uint8), (0, 0), fx=self.scale, fy=self.scale)

        # Write timestamp in the left-upper corner
        cv2.putText(img, f"utime: {utime}", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 155, 0))

        # Show images
        if channel == self.channel_l:
            cv2.imshow('imageL', img)
        else:
            cv2.imshow('imageR', img)
        cv2.waitKey(10)

    def run(self):
        # Start LCM subscription
        self.lcm.subscribe(self.channel_l, self.handler_lcmimage)
        self.lcm.subscribe(self.channel_r, self.handler_lcmimage)

        while True:
            self.lcm.handle_timeout(100)
            key = cv2.waitKey(1)
            if key & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A stereo camera viewer over LCM", add_help=True)
    parser.add_argument("-cL", "--channel_left", default="MANTA_L_SYNC", type=str)
    parser.add_argument("-cR", "--channel_right", default="MANTA_R_SYNC", type=str)
    parser.add_argument("-vs", "--viewer_scale", default="0.33", type=float)
    args = parser.parse_args()

    # Initialize LCM
    lc = lcm.LCM()

    # Initialize viewer
    viewer = LCMPairViewer(lc, args.channel_left, args.channel_right, args.viewer_scale)
    viewer.run()

    # Quit message
    print(" " * 100)
    print("Quitting...")
