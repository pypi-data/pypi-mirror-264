"""
This is a simple Python script which subscribed to the INS messages in the LCMTypes
old standard and republishes them in the new standard.
"""
import lass_republisher_oi as oi
import senlcm
import navlcm
import lcm
import numpy as np
from scipy.spatial.transform import Rotation as R
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class INSRepublisher:
    def __init__(self) -> None:
        """
        Subscribes Kearfott messages and republish them in the new standard.
        """

        # Initialize LCM
        self.lc = lcm.LCM()

        # LCM channels subscription
        ins_channel = "INS_KEARFOTT_OI"
        dvl_channel = "DVL_KEARFOTT_OI"
        self.subscriptions = {}
        self.subscriptions[ins_channel] = self.lc.subscribe(ins_channel, self.handle_kearfott_message)
        self.subscriptions[dvl_channel] = self.lc.subscribe(dvl_channel, self.handle_dvl_message)

        # Header variables for LCM messages
        self.sequence = dict()
        self.sequence["imu"] = 0
        self.sequence["ins"] = 0
        self.sequence["depth"] = 0
        self.sequence["dvl_ins"] = 0
        self.sequence["dvl"] = 0
        self.frame_id = dict()
        self.frame_id["imu"] = "imu_link_frd"
        self.frame_id["ins"] = "ins_link_ned"
        self.frame_id["depth"] = "depth_link_frd"
        self.frame_id["dvl"] = "dvl_link_frd"

    ####################################################################################################################
    # LCM Handlers                                                                                                     #
    ####################################################################################################################
    def handle_kearfott_message(self, channel: str, data: lcm.Event) -> None:
        """
        Kearfott LCM messages handler to republish into the following channels:

        * IMU_KEARFOTT_COMPAS: senlcm.imu_t
        * DEPTH_KEARFOTT_COMPAS: senlcm.depth_t
        * STATE_KEARFOTT_COMPAS: navlcm.odometry_t
        * DVL_INS_KEARFOTT_COMPAS: senlcm.dvl_t

        Attributes
        ----------
        channel : str
            Subscription channel
        data : lcm.Event
            Message data in a senlcm::ahrs_t LCM structure.
        """
        # Get data
        data = oi.kearfott_t.decode(data)
        quat_vec = R.from_euler("ZYX", np.array([data.heading_rad, data.pitch_rad, data.roll_rad])).as_quat().flatten()

        # IMU message
        msg_imu = senlcm.imu_t()
        msg_imu.header.timestamp = int(data.time_unix_sec * 1e+06)
        msg_imu.header.sequence = self.sequence["imu"]
        msg_imu.header.frame_id = self.frame_id["imu"]
        msg_imu.orientation = quat_vec
        msg_imu.angRate = np.array([data.prate_rads, data.qrate_rads, data.rrate_rads])
        msg_imu.xyz_ddot = np.array([data.accelx_ms2, data.accely_ms2, data.accelz_ms2])

        self.lc.publish("IMU_KEARFOTT_COMPAS", msg_imu.encode())
        self.sequence["imu"] += 1

        # Depth Message
        msg_depth = senlcm.depth_t()
        msg_depth.header.timestamp = int(data.time_unix_sec * 1e+06)
        msg_depth.header.sequence = self.sequence["depth"]
        msg_depth.header.frame_id = self.frame_id["depth"]
        msg_depth.depth = data.depth_m

        self.lc.publish("DEPTH_KEARFOTT_COMPAS", msg_depth.encode())
        self.sequence["depth"] += 1

        # State Message
        msg_state = navlcm.odometry_t()
        msg_state.header.timestamp = int(data.time_unix_sec * 1e+06)
        msg_state.header.sequence = self.sequence["ins"]
        msg_state.header.frame_id = self.frame_id["ins"]
        msg_state.pose.pose.position.x = data.northing_m
        msg_state.pose.pose.position.y = data.easting_m
        msg_state.pose.pose.position.z = data.depth_m
        msg_state.pose.pose.orientation.x = quat_vec[0]
        msg_state.pose.pose.orientation.y = quat_vec[1]
        msg_state.pose.pose.orientation.z = quat_vec[2]
        msg_state.pose.pose.orientation.w = quat_vec[3]
        msg_state.pose.pose_covariance = (np.eye(6) * 1e-05).flatten()
        msg_state.twist.twist.linear.x = data.vbodyx_ms
        msg_state.twist.twist.linear.y = data.vbodyy_ms
        msg_state.twist.twist.linear.z = data.vbodyz_ms
        msg_state.twist.twist.angular.x = data.prate_rads
        msg_state.twist.twist.angular.y = data.qrate_rads
        msg_state.twist.twist.angular.z = data.rrate_rads
        msg_state.twist.twist_covariance = (np.eye(6) * 1e-05).flatten()

        self.lc.publish("STATE_KEARFOTT_COMPAS", msg_state.encode())
        self.sequence["ins"] += 1

        # DVL Message
        msg_dvl_ins = senlcm.dvl_t()
        msg_dvl_ins.header.timestamp = int(data.time_unix_sec * 1e+06)
        msg_dvl_ins.header.sequence = self.sequence["dvl_ins"]
        msg_dvl_ins.header.frame_id = self.frame_id["dvl"]
        msg_dvl_ins.btv = np.array([data.vbodyx_ms, data.vbodyy_ms, data.vbodyz_ms, 0.0])
        msg_dvl_ins.altitude = data.bheight_m

        self.lc.publish("DVL_INS_KEARFOTT_COMPAS", msg_dvl_ins.encode())
        self.sequence["dvl_ins"] += 1

    def handle_dvl_message(self, channel: str, data: lcm.Event) -> None:
        """
        DVL LCM messages handler

        Attributes
        ----------
        channel : str
            Subscription channel
        data : lcm.Event
            Message data in an LCM structure
        """
        # Get data
        data = oi.rdi_pd4_t.decode(data)

        # DVL Message
        msg_dvl = senlcm.dvl_t()
        msg_dvl.header.timestamp = int(data.time_unix_sec * 1e+06)
        msg_dvl.header.sequence = self.sequence["dvl"]
        msg_dvl.header.frame_id = self.frame_id["dvl"]
        msg_dvl.btv = np.array([data.xvelbtm_mms, data.yvelbtm_mms, data.zvelbtm_mms, data.evelbtm_mms]) * 1e-03
        msg_dvl.range = np.array([data.beam1_cm_uint, data.beam2_cm_uint, data.beam3_cm_uint, data.beam4_cm_uint]) * 1e-02
        # This channel does not report bottom height

        self.lc.publish("DVL_KEARFOTT_COMPAS", msg_dvl.encode())
        self.sequence["dvl"] += 1

    def run(self) -> None:
        """
        Threads handler for multiple handlers in parallel for the LCM broadcasting.
        """
        while True:
            self.lc.handle()


if __name__ == "__main__":
    ins_subpub = INSRepublisher()
    ins_subpub.run()
