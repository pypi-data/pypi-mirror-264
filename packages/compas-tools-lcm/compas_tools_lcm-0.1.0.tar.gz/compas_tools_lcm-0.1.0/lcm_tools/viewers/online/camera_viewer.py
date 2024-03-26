import argparse
from senlcm import image_t
import lcm
import cv2
import numpy as np


class CameraViewer:
    def __init__(self, lcm_channel, scale):
        self.lcm = lcm.LCM()
        self.lcm_channel = lcm_channel
        self.image = None
        self.scale = scale

    def lcm_handler(self, _, data):
        msg = image_t.decode(data)
        height = msg.height
        width = msg.width
        buffer = np.frombuffer(msg.data, np.uint8)
        if msg.pixelformat == msg.PIXEL_FORMAT_GRAY:
            buffer = buffer.reshape((height, width, 1)).astype("uint8")
        elif msg.pixelformat == msg.PIXEL_FORMAT_RGB:
            buffer = buffer.reshape((height, width, 3)).astype("uint8")
            # OpenCV works with images in BGR
            buffer = buffer[:, :, ::-1]
        elif msg.pixelformat == msg.PIXEL_FORMAT_BGR:
            buffer = buffer.reshape((height, width, 3)).astype("uint8")
        elif msg.pixelformat == msg.PIXEL_FORMAT_BAYER_RGGB or\
                msg.pixelformat == msg.PIXEL_FORMAT_BAYER_GRBG or\
                msg.pixelformat == msg.PIXEL_FORMAT_BAYER_GBRG or\
                msg.pixelformat == msg.PIXEL_FORMAT_BAYER_BGGR:
            buffer = buffer.reshape((height, width, 1)).astype("uint8")
            buffer = cv2.cvtColor(buffer, cv2.COLOR_BayerRG2RGB)
        elif msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_RGGB or\
                msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_GRBG or\
                msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_GBRG or\
                msg.pixelformat == msg.PIXEL_FORMAT_BE_BAYER16_BGGR:
            buffer = np.frombuffer(msg.data, np.uint16)
            buffer = buffer.reshape((height, width, 1)).astype("uint16")*16
            buffer = cv2.cvtColor(buffer, cv2.COLOR_BAYER_RG2RGB)
        elif msg.pixelformat == msg.PIXEL_FORMAT_MJPEG:
            buffer = cv2.imdecode(buffer, -1).reshape((height, width, 3)).astype("uint8")
        elif msg.pixelformat == msg.PIXEL_FORMAT_YUV411P or\
                msg.pixelformat == msg.PIXEL_FORMAT_YUV420:
            # buffer = np.fromstring(msg.data, np.uint16)
            # # buffer = cv2.imdecode(buffer,-1)
            # buffer = buffer.reshape((int(0.75*height), width, 1)).astype("uint8")
            # buffer = cv2.cvtColor(buffer, cv2.COLOR_YUV2BGR_NV21)
            raise Exception("YUV pixel format not supported")
        else:
            raise Exception("Pixel format not supported")
        new_width = int(width * self.scale)
        new_height = int(height * self.scale)
        self.image = cv2.resize(buffer, (new_width, new_height), interpolation=cv2.INTER_AREA)

    def start_image_acquisition(self):
        self.lcm.subscribe(self.lcm_channel, self.lcm_handler)

    def run(self):
        try:
            while True:
                self.lcm.handle()
                if self.image is not None:
                    cv2.imshow("img", self.image)
                    cv2.waitKey(1)
        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A viewer for camera feeds")
    parser.add_argument("-c","--channel_image", default="WEBCAM_IMAGE", type=str)
    parser.add_argument("-s","--scale", default="0.6", type=float)
    args = parser.parse_args()

    cam_viewer = CameraViewer(args.channel_image, args.scale)
    cam_viewer.start_image_acquisition()
    cam_viewer.run()
