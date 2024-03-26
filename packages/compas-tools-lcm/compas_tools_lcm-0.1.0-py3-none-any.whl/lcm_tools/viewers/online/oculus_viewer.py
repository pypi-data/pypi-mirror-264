import numpy as np
import cv2
from wand.image import Image as wImage


import lcm
from senlcm.oculus_sonar_t import oculus_sonar_t

import argparse

class OculusViewer:
    def __init__(self, channel_sonar: str):
        self.m_lcm = lcm.LCM()
        self.lcm_channel_sonar = channel_sonar
        self.subscription_oculus = None
        
        # Original image
        self.oculus_message = oculus_sonar_t()
        self.orig_image = np.ndarray(0)
        self.bearings = np.ndarray(0)
        self.range = float(0)
        
        # Converted image
        self.WIDTH_METERS = 10
        self.HEIGHT_METERS = 8
        self.PIXELS = 512
        self.conv_image = np.ndarray(0)
        
        # Variables bluerov
        self.res = float()
        self.height = float()
        self.rows = float()
        self.width = float()
        self.cols = float()
        self.map_x = float()
        self.map_y = float()
        self.f_bearings = float()
        self.REVERSE_Z = 1
        self.flipped_img = None
        self.horizontalFOVDeg = 130
        
    def lcm_receive_oculus_image(self, _, data):
        # This method is probably taking too long, so it lags.
        msg = oculus_sonar_t.decode(data)
        image_shape = np.array([msg.nRanges, msg.nBeams ])
        img = np.frombuffer(msg.image, dtype=np.uint8).reshape(image_shape)
        self.orig_image = img
        self.range = msg.range
        self.bearings = msg.bearings
        self.oculus_message = msg
        
        # self.flipped_img = np.flip(self.orig_image, axis=0)
        # self.conv_image = wImage(blob=cv2.imencode('.jpg', self.flipped_img)[1].tobytes())
        self.conv_image = wImage(blob=cv2.imencode('.jpg', self.orig_image)[1].tobytes())
        self.conv_image.virtual_pixel = 'background'
        angle = abs(self.bearings[-1]/100) + abs(self.bearings[0]/100)
        angle = self.horizontalFOVDeg  #The angle coming from LCM seems to be wrong. Or at least the computation done here.
        arguments = (angle,0,msg.nRanges,0)
        polar2cart = True
        if polar2cart:
            self.conv_image.rotate(180)
            self.conv_image.distort('arc', arguments)
            # self.conv_image.rotate(180)
        self.conv_image = np.asarray(bytearray(self.conv_image.make_blob()), dtype=np.uint8)
        self.conv_image = cv2.imdecode(self.conv_image, cv2.IMREAD_UNCHANGED)
    

    def run(self):        
        while True:
            print(self.lcm_channel_sonar)
            self.subscription_oculus = self.m_lcm.subscribe(self.lcm_channel_sonar,self.lcm_receive_oculus_image)
            self.m_lcm.handle()
            self.m_lcm.unsubscribe(self.subscription_oculus)
            scale_percent = 100 # percent of original size
            width = int(self.conv_image.shape[1] * scale_percent / 100)
            height = int(self.conv_image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(self.conv_image, dim, interpolation = cv2.INTER_AREA)
            cv2.imshow("img", resized)
            # cv2.imshow("img", self.conv_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description="A viewer for the BP Oculus Sonar")
    parser.add_argument("-c","--channel_sonar", default= "ROV_SEN_SONAR_OCULUS", type=str)
    args = parser.parse_args()
    
    ic = OculusViewer(args.channel_sonar)
    ic.run()
    
