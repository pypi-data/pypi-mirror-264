"""
Script to log images from an LCM channel into files.
"""
import argparse
import struct
import os

import cv2
import lcm
from senlcm.image_t import image_t
import numpy as np

from PIL import Image

LCM_URL = "udpm://239.255.76.67:7667?ttl=0"


class ImageLogger:
    """Class to receive images and save them to files.
    """
    def __init__(self, args):
        self.args = args
        self.lcm_obj = lcm.LCM(LCM_URL)

    def senlcm_image_to_file(self, channel, data):
        """Converts a senlcm image into an OpenCV image and then saves it to file

        Args:
            channel (str): name of the channel the images are being published to
            data (byte array): byte array of the image data
        """
        senlcm_img = image_t.decode(data)
        height = senlcm_img.height
        width = senlcm_img.width
        cv_img = np.fromstring(senlcm_img.data, np.uint8)
        if senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_GRAY:
            cv_img = cv_img.reshape((height, width, 1)).astype("uint8")
        elif senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_RGB:
            cv_img = cv_img.reshape((height, width, 3)).astype("uint8")
            # OpenCV works with images in BGR
            cv_img = cv_img[:, :, ::-1]
        elif senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BGR:
            cv_img = cv_img.reshape((height, width, 3)).astype("uint8")
        elif senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BAYER_RGGB or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BAYER_GRBG or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BAYER_GBRG or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BAYER_BGGR:
            cv_img = cv_img.reshape((height, width, 1)).astype("uint8")
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BayerRG2RGB)
        elif senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BE_BAYER16_RGGB or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BE_BAYER16_GRBG or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BE_BAYER16_GBRG or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_BE_BAYER16_BGGR:
            cv_img = np.fromstring(senlcm_img.data, np.uint16)
            cv_img = cv_img.reshape((height, width, 1)).astype("uint16")*16
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BAYER_RG2RGB)
        elif senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_MJPEG:
            cv_img = cv2.imdecode(cv_img, -1).reshape((height, width, 3)).astype("uint8")
        elif senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_YUV411P or\
                senlcm_img.pixelformat == senlcm_img.PIXEL_FORMAT_YUV420:
            # cv_img = np.fromstring(msg.data, np.uint16)
            # # cv_img = cv2.imdecode(cv_img,-1)
            # cv_img = cv_img.reshape((int(0.75*height), width, 1)).astype("uint8")
            # cv_img = cv2.cvtColor(cv_img, cv2.COLOR_YUV2BGR_NV21)
            raise Exception("YUV pixel format not supported")
        else:
            raise Exception("Pixel format not supported")
        # new_width = int(width * self.args.scale)
        # new_height = int(height * self.args.scale)
        # cv_image = cv2.resize(cv_img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        # Metadata:
        metadata = {}
        for meta in senlcm_img.metadata:
            metadata[meta.key] = struct.unpack('d', meta.value[:meta.n])[0]
        # Save to file
        # cv2.imshow("img", cv_img)
        # cv2.waitKey(1)
        self.cv_to_file(cv_img, senlcm_img.header.timestamp, metadata, width, height)

    def cv_to_file(self, cv_image, utime, metadata, width, height):
        filename = self.args.path_images + str(utime) + self.args.image_extension
        cv2.imwrite(filename, cv_image)

        # If image in tiff format, write metadata
        if self.args.image_extension == ".tiff" or self.args.image_extension == ".tif":
            img_tiff = Image.open(filename)
            img_tiff.tag[256] = width
            img_tiff.tag[257] = height
            img_tiff.tag[315] = ("GAIN:" + str(metadata["Gain"])
                                 + ",EXPOSURE:" + str(metadata["ExposureTimeAbs"])
                                 )
            img_tiff.save(filename, tiffinfo=img_tiff.tag)

    def run(self):
        """Subscribes to images from lcm and starts saving images
        """
        self.lcm_obj.subscribe(self.args.channel_images, self.senlcm_image_to_file)
        while True:
            self.lcm_obj.handle_timeout(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A logger to save images from LCM")
    parser.add_argument("-i", "--channel_images", default="PROSILICA_R", type=str,
                        help="LCM channel from which to read images (default: %(default)s)")
    parser.add_argument("-p", "--path_images", default="./imagesR/", type=str,
                        help="Path to save the images to (default: %(default)s)")
    parser.add_argument("-e", "--image_extension", default=".tiff", type=str,
                        help="Extension of the images to save (default: %(default)s)")
    cli_args = parser.parse_args()

    if cli_args.path_images[-1] != "/":
        cli_args.path_images += "/"
    if cli_args.image_extension[0] != ".":
        cli_args.image_extension = "." + cli_args.image_extension

    extensions_not_supported = [".jpg"]
    if cli_args.image_extension in extensions_not_supported:
        print("Extension '{}' not supported".format(cli_args.image_extension))
        exit(1)

    os.makedirs(cli_args.path_images, exist_ok=True)

    logplayer = ImageLogger(cli_args)
    logplayer.run()
