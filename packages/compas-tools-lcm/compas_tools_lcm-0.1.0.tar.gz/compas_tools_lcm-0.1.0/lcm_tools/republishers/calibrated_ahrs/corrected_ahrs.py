"""
This script subscribes to an AHRS message and republishes it in a new channel
with the magnetic field, angular rate and attitude corrected given a gyroscope
and magnetometer calibration.
"""

import argparse
import math
import warnings
import time
from os.path import isfile
from pathlib import Path
from typing import Any, Iterable, Union
import lcm
import json
import numpy as np
from scipy.spatial.transform import Rotation as R
from senlcm import ahrs_t
warnings.filterwarnings("ignore", category=DeprecationWarning)


def hpr2rot(hpr: Union[np.ndarray, Iterable[float]]) -> np.ndarray:
    """
    Heading, Pitch and Roll (HPR) angles to SO(3) rotation matrix.
    Note: Euler angles convention used is ZYX

    Parameters
    ----------
    hpr : Union[np.ndarray, Iterable[float]]
        hpr angles in radians as a numpy array or as a list.

    Returns
    -------
    The rotation matrix using hor with the convention ZYX
    """
    hpr = np.array(hpr).flatten() if isinstance(hpr, list) else hpr.flatten()
    if hpr.shape[0] != 3:
        raise ValueError("Usage: RotMat=hpr2rot([angH angP angR])")

    angH = hpr[0]
    angP = hpr[1]
    angR = hpr[2]

    c1 = math.cos(angH)
    s1 = math.sin(angH)
    c2 = math.cos(angP)
    s2 = math.sin(angP)
    c3 = math.cos(angR)
    s3 = math.sin(angR)

    RotMat = np.array(
        [
            [c1 * c2, c1 * s2 * s3 - c3 * s1, s1 * s3 + c1 * c3 * s2],
            [c2 * s1, c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3],
            [-s2, c2 * s3, c2 * c3],
        ]
    )

    return RotMat


def handle_ahrs_message(channel: str, data: Any) -> None:
    ahrs_msg = ahrs_t.decode(data)

    # Original Data
    hpr = R.from_quat(ahrs_msg.orientation).as_euler("ZYX").flatten()
    angrate = np.array(ahrs_msg.angRate).flatten()
    magfield = np.array(ahrs_msg.magfield).flatten()

    # CorSOFT_IRON
    c_magfield = np.dot(SOFT_IRON, magfield) + HARD_IRON.flatten()
    c_angrate = angrate + GYRO_BIAS.flatten()
    hpr_0h = np.concatenate([[0.0], hpr[1:]])
    flat_mag_field = np.dot(hpr2rot(hpr_0h), c_magfield)
    h = np.arctan2(-flat_mag_field[1], flat_mag_field[0]) - np.deg2rad(DECLINATION)
    c_hpr = np.concatenate([[h], hpr[1:]])

    # Corrected message
    cahrs_msg = ahrs_t()
    cahrs_msg.header.timestamp = ahrs_msg.header.timestamp
    cahrs_msg.header.sequence = ahrs_msg.header.sequence
    cahrs_msg.header.frame_id = ahrs_msg.header.frame_id
    cahrs_msg.orientation = R.from_euler("ZYX", c_hpr).as_quat().flatten()
    cahrs_msg.angRate = c_angrate
    cahrs_msg.xyz_ddot = ahrs_msg.xyz_ddot
    cahrs_msg.magfield = c_magfield

    lc.publish(CHANNEL_OUT, cahrs_msg.encode())


def main():
    # create the parser object
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument("-i", "--channel_in", type=str, help="Input channel to subscribe")
    parser.add_argument("-o", "--channel_out", type=str, help="Output channel to publish")
    parser.add_argument("-p", "--config_path", type=Path, help="Path to configuration file")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        exit()

    print("AHRS Calibrated Measurements Republisher")
    global CHANNEL_IN
    CHANNEL_IN = args.channel_in
    print(f"Subscribing to: {CHANNEL_IN}")
    global CHANNEL_OUT
    CHANNEL_OUT = args.channel_out
    print(f"Publishing to: {CHANNEL_OUT}")

    # Initialize LCM
    global lc
    lc = lcm.LCM()

    # Parse configuration file
    if not isfile(args.config_path):
        raise ValueError(f"{args.config_path} is not an available file in the system.")
    # Read the configuration file for the platform in use
    with open(args.config_path, "r") as read_file:
        config = json.load(read_file)

    global SOFT_IRON
    SOFT_IRON = np.array(config["soft-iron"])
    if SOFT_IRON.shape != (3, 3):
        raise ValueError("Soft Iron matrix must be a (3, 3) array.")
    print(f"Soft Iron: {SOFT_IRON.tolist()}")
    global HARD_IRON
    HARD_IRON = np.array(config["hard-iron"])
    if HARD_IRON.shape[0] != 3:
        raise ValueError("Hard Iron matrix must be a (3,) or (3, 1) or array.")
    print(f"Hard Iron: {HARD_IRON.flatten()}")
    global GYRO_BIAS
    GYRO_BIAS = np.array(config["gyro-bias"])
    if GYRO_BIAS.shape[0] != 3:
        raise ValueError("Gyroscope Bias matrix must be a (3,) or (3, 1) or array.")
    print(f"Gyroscope Bias: {GYRO_BIAS.flatten()}")
    global DECLINATION
    DECLINATION = float(config["declination"])
    print(f"Magnetic declination: {DECLINATION} deg")

    # Subscribe to channel
    lc.subscribe(args.channel_in, handle_ahrs_message)

    while True:
        try:
            lc.handle()
            time.sleep(0.01)
        except KeyboardInterrupt:
            print("Keyboard interrupt received, closing connection")
            exit()


if __name__ == "__main__":
    main()
