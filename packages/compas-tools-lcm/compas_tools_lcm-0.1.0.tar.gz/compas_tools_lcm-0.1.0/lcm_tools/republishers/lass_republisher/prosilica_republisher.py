"""
This is a simple Python script which subscribed to the PROSILICA messages in the LCMTypes
old standard and republishes them in the new standard.
"""
import lass_republisher_bot_core as bot_core
import senlcm
import lcm
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class CameraRepublisher:
    def __init__(self) -> None:
        """
        Subscribes Kearfott messages and republish them in the new standard.
        """

        # Initialize LCM
        self.lc = lcm.LCM()

        # LCM channels subscription
        caml_channel = "PROSILICA_L"
        camlsync_channel = "PROSILICA_L_SYNC"
        camr_channel = "PROSILICA_R"
        camrsync_channel = "PROSILICA_R_SYNC"
        gps_channel = "MBARI_GPSTIME.SYNC"
        self.subscriptions = {}
        self.subscriptions[caml_channel] = self.lc.subscribe(caml_channel, self.handle_cam_message)
        self.subscriptions[camr_channel] = self.lc.subscribe(camr_channel, self.handle_cam_message)
        self.subscriptions[camr_channel] = self.lc.subscribe(camlsync_channel, self.handle_sync_message)
        self.subscriptions[camr_channel] = self.lc.subscribe(camrsync_channel, self.handle_sync_message)
        self.subscriptions[camr_channel] = self.lc.subscribe(gps_channel, self.handle_sync_message)

        # Header variables for LCM messages
        self.sequence = dict()
        self.sequence["caml"] = 0
        self.sequence["camr"] = 0
        self.sequence["caml_sync"] = 0
        self.sequence["camr_sync"] = 0
        self.sequence["gps_sync"] = 0

        self.frame_id = dict()
        self.frame_id["caml"] = "stereo_camera_left_frd"
        self.frame_id["camr"] = "stereo_camera_right_frd"
        self.frame_id["caml_sync"] = "stereo_camera_left_frd"
        self.frame_id["camr_sync"] = "stereo_camera_right_frd"
        self.frame_id["gps"] = "gps"

    ####################################################################################################################
    # LCM Handlers                                                                                                     #
    ####################################################################################################################
    def handle_cam_message(self, channel: str, data: lcm.Event) -> None:
        """
        PROSILICA_X LCM messages handler to republish into PROSILICA_X_COMPAS

        Attributes
        ----------
        channel : str
            Subscription channel
        data : lcm.Event
            Message data in a senlcm::ahrs_t LCM structure.
        """
        # Get data
        msg = bot_core.image_t.decode(data)

        # IMU message
        msg_cam = senlcm.image_t()
        msg_cam.header.timestamp = msg.utime
        msg_cam.header.sequence = self.sequence["caml"] if channel == "PROSILICA_L" else self.sequence["camr"]
        msg_cam.header.frame_id = self.frame_id["caml"] if channel == "PROSILICA_L" else self.frame_id["camr"]
        msg_cam.width = msg.width
        msg_cam.height = msg.height
        msg_cam.row_stride = msg.row_stride
        print(msg.width, msg.height, msg.row_stride, msg.pixelformat)
        msg_cam.pixelformat = msg.pixelformat
        msg_cam.size = msg.size
        msg_cam.data = msg.data
        msg_cam.nmetadata = 0
        msg_cam.metadata = []

        self.lc.publish(f"{channel}_COMPAS", msg_cam.encode())
        if channel == "PROSILICA_L":
            self.sequence["caml"] += 1
        else:
            self.sequence["camr"] += 1

    def handle_sync_message(self, channel: str, data: lcm.Event) -> None:
        """
        SYNC LCM messages handler

        Attributes
        ----------
        channel : str
            Subscription channel
        data : lcm.Event
            Message data in an LCM structure
        """
        # Get data
        msg = bot_core.image_sync_t.decode(data)
        if channel == "MBARI_GPS.SYNC":
            device = "gps_sync"
        else:
            device = "caml_sync" if channel == "PROSILICA_L" else "camr_sync"

        # DVL Message
        msg_gps = senlcm.image_sync_t()
        msg_gps.header.timestamp = msg.utime
        msg_gps.header.sequence = self.sequence[device]
        msg_gps.header.frame_id = self.frame_id[device]
        msg_gps.utime = msg.utime

        self.lc.publish(f"{channel}_COMPAS", msg_gps.encode())
        self.sequence[device] += 1

    def run(self) -> None:
        """
        Threads handler for multiple handlers in parallel for the LCM broadcasting.
        """
        while True:
            self.lc.handle()


if __name__ == "__main__":
    cam_subpub = CameraRepublisher()
    cam_subpub.run()
