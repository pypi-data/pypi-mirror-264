"""
Simple code to simulate a TCP connection a publish data parsed from a txt file.
"""
import argparse
import socket
import time
from os.path import isfile

HOST = '127.0.0.1'
PORT = 65432


def main():
    # create the parser object
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument("--file", type=str, help="File path.")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        exit()
    # Check if the file exists
    if not isfile(args.file):
        print(f"{args.file} is not a valid file in the system.")
        exit()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((HOST, PORT))
        print(f"TCP connection established to: {HOST}:{str(PORT)}")

        with open(args.file, "r") as file:
            line = file.readline().strip()
            while line:
                tcp_socket.send(line.encode())
                print(f"Sent message: {line}")
                line = file.readline().strip()
                time.sleep(2)
            tcp_socket.close()

    print("All messages sent")


if __name__ == "__main__":
    main()
