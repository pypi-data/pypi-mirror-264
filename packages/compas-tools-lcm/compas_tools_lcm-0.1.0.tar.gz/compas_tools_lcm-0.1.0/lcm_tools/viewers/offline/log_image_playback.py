"""
Script to play lcm log of an AVT camera, waiting for an
image sync message, and then publishing the correct image to LCM.
"""
import argparse
import time

import cv2
import lcm
from senlcm.image_sync_t import image_sync_t
from senlcm.image_t import image_t

LCM_URL = "udpm://239.255.76.67:7667?ttl=0"


class AVTLogplayer:
    """Class to read and play an AVT LCM log.
    """
    def __init__(self, args):
        self.args = args
        self.lcm_obj = lcm.LCM(LCM_URL)
        self.lcm_log = lcm.EventLog(args.path_logfile)

    def cv_image_to_bot_image(self, cv_img, utime):
        """Converts an OpenCV image to a bot_core image_t type

        Args:
            cv_img (nparray): input cv_image
            utime (int): input timestamp

        Returns:
            bot_img: a bot_core image_t LCM type
        """
        bot_img = image_t()
        bot_img.utime = utime
        bot_img.width = cv_img.shape[1]
        bot_img.height = cv_img.shape[0]
        bot_img.size = 0
        bot_img.nmetadata = 0

        # Always publish as RGB
        bot_img.pixelformat = bot_img.PIXEL_FORMAT_RGB
        bot_img.row_stride = cv_img.shape[2] * bot_img.width
        bot_img.size = bot_img.width * bot_img.height * cv_img.shape[2]
        bot_img.data = cv_img.astype("uint8").tobytes()
        return bot_img

    def run(self):
        """Goes event by event in the LCM log, publishing
        the bot_img when an image_sync msg is available
        """
        last_timestamp = 0
        # To skip the first msg
        start_waiting = False
        for event in self.lcm_log:
            if event.channel == self.args.channel_sync:
                # New sync message
                msg = image_sync_t.decode(event.data)
                utime = msg.utime
                # Get image with timestamp
                img = cv2.imread(self.args.path_images + str(utime)+self.args.image_extension)
                bot_img = self.cv_image_to_bot_image(img, utime)
                # Publish Image
                self.lcm_obj.publish(self.args.channel_images, bot_img.encode())
                self.lcm_obj.publish(event.channel, event.data)
                if start_waiting:
                    # Waits the necessary time between events
                    time.sleep((event.timestamp - last_timestamp)/1000000)
                start_waiting = True
                last_timestamp = event.timestamp
                
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A logplayer to publish images from image sync")
    parser.add_argument("-c", "--channel_sync", default="PROSILICA_R_SYNC", type=str)
    parser.add_argument("-i", "--channel_images", default="PROSILICA_R", type=str)
    parser.add_argument("-p", "--path_images", default="./bin/imagesR/", type=str)
    parser.add_argument("-l", "--path_logfile", type=str, required=True)
    parser.add_argument("-e", "--image_extension", default=".tiff", type=str)
    cli_args = parser.parse_args()

    logplayer = AVTLogplayer(cli_args)
    logplayer.run()
