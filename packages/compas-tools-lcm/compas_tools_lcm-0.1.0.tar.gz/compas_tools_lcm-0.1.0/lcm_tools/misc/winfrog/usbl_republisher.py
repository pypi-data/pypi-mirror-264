"""
Simple script to stablish a tcp connection and publish the data through LCM
as a senlcm::gps_fix_t message.
"""
import argparse
import datetime
import socket
import warnings

import lcm
from senlcm import gps_fix_t
warnings.filterwarnings("ignore", category=DeprecationWarning)


def parse_msg(data: str, last_timestamp: str, sequence: int, channel: str) -> None:
    # Message example: $GPGGA,202743.41,3636.5955,N,12153.4558,W,0,00,0.0,-1003.5,M,0.0,M,0.0,0000
    #                     0      1         2      3     4      5 6 7   8       9  10 11 12 13  14
    # Fields of interest:
    # 1: UTC time status of position (hours/minutes/seconds/ decimal seconds)
    # 2: Latitude (DDmm.mm)
    # 3: Latitude direction (N = North, S = South)
    # 4: Longitude (DDDmm.mm)
    # 5: Longitude direction (E = East, W = West)
    # 9: Antenna altitude above/below mean sea level
    # 10: Units of antenna altitude (M = metres)

    fields = data.decode().strip().split(",")

    # Reject message if the timestamp have not changed
    if fields[1] == last_timestamp and last_timestamp != "":
        return last_timestamp, sequence

    # Parse data
    utc_timestamp = f"{fields[1][:2]}:{fields[1][2:4]}:{fields[1][4:6]}.{fields[1][7:]}"
    lat = float(fields[2])
    lon = float(fields[4])
    alt = float(fields[9])

    # Convert UTC timestamp to microseconds since the epoc
    unix_timestamp = int(datetime.datetime.strptime(utc_timestamp, "%H:%M:%S.%f").timestamp() * 1.0e+06)

    # Populate senlcm::gps_fix_t message
    msg = gps_fix_t()
    msg.header.sequence = sequence
    msg.header.frame_id = "map"
    msg.header.timestamp = unix_timestamp
    msg.latitude = lat
    msg.longitud = lon
    msg.altitude = alt

    # Publish message
    lc.publish(channel, msg.encode())
    return fields[1], sequence + 1


def main():
    # create the parser object
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument("--ip", type=str, help="IP addresse for TCP connect")
    parser.add_argument("--port", type=int, help="Port addresse for TCP connect")
    parser.add_argument("--channel", type=str, help="LCM Channel to publish TCP data")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds for TCP connection, default 60", default=60)
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        exit()

    global lc
    lc = lcm.LCM()

    # socket.AF_INET for IPv4 or socket.AF_INET6 for IPv6
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.settimeout(args.timeout)
    tcp_socket.connect((args.ip, args.port))
    print(f"TCP connection stablished to: {args.ip}:{str(args.port)}")
    print(f"Timeout set to {args.ip}:{str(args.port)}")
    print(f"LCM channel set to: {args.channel}")

    last_timestamp, sequence = "", 0
    while True:
        # Receive data setting buffer size (example data is 56 bytes)
        try:
            data = tcp_socket.recv(1024)
        except socket.timeout:
            data = None
            print(f"No messages received from {args.ip}:{str(args.port)} in {str(args.timeout)} seconds.")
        except KeyboardInterrupt:
            print("Keyboard interrupt received, closing connection")
            tcp_socket.close()
            break

        if data is not None:
            last_timestamp, sequence = parse_msg(data, last_timestamp, sequence, args.channel)


if __name__ == "__main__":
    main()
