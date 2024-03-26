"""
Script to subscribe to an lcm channel, waiting for an
image sync message, and then publishing the correct image to LCM.
"""
import argparse

import cv2
import lcm
from senlcm.image_sync_t import image_sync_t
from senlcm.image_t import image_t

LCM_URL = "udpm://239.255.76.67:7667?ttl=0"

class AVTSubplayer:
    """Class to subscribe to an lcm channel and publish corresponding images.
    """
    def __init__(self, args):
        self.args = args
        self.lcm_obj = lcm.LCM(LCM_URL)
        print('Subscribing to', self.args.channel_sync)
        self.lcm_obj.subscribe(self.args.channel_sync, self.on_sync)
    
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
    
    def on_sync(self, channel, data):
        if channel != self.args.channel_sync:  # skip other channels
            return
        
        # New sync message
        msg = image_sync_t.decode(data)
        
        # Get image with timestamp
        utime = msg.utime
        img = cv2.imread(self.args.path_images + str(utime)+self.args.image_extension)
        if img is None:
            print('Could not get image', str(utime)+self.args.image_extension)
            return
        
        bot_img = self.cv_image_to_bot_image(img, utime)

        # Publish Image
        self.lcm_obj.publish(self.args.channel_images, bot_img.encode())
    
    def run(self):
        while True:
            try:
                self.lcm_obj.handle()
            except:
                break
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A utility to publish images from a subscribed image sync")
    parser.add_argument("-c","--channel_sync", default="PROSILICA_R_SYNC", type=str)
    parser.add_argument("-i","--channel_images", default="PROSILICA_R", type=str)
    parser.add_argument("-p","--path_images", default="./bin/imagesR/", type=str)
    parser.add_argument("-e","--image_extension", default=".tiff", type=str)
    cli_args = parser.parse_args()
    
    logplayer = AVTSubplayer(cli_args)
    logplayer.run()
