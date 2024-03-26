"""
Splice images into an LCM log from a directory, using the file name as a timestamp.
"""

import argparse
from pathlib import Path

try:
    from senlcm import image_t
    IMAGE_MODULE = "SENLCM"
except ImportError:
    from bot_core import image_t
    IMAGE_MODULE = "BOTCORE"

import cv2
import numpy as np
from lcmlog import LogReader, LogWriter, Event, Header


def get_image_as_message(image_path: Path, timestamp: int, sequence: int) -> image_t:
    """
    Load and encode an image as a `senlcm.image_t` message object.

    Args:
        image_path: Path to image file
        timestamp: Timestamp to use for the image
        sequence: Sequence number

    Returns:
        Image as an `image_t` message object
    """
    image = cv2.imread(str(image_path))

    # Convert to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.uint8)

    # TODO: How to encode here? 12-bit bayer (BGGR12) is originally sent in the senlcm::image_t message, but we don't have that...
    image_bytes = image.tobytes()  # just the RGB as uint8 for now

    # Pack data into message
    image_message = image_t()
    if IMAGE_MODULE == "SENLCM":
        image_message.header.timestamp = timestamp
        image_message.header.sequence = sequence
        image_message.header.frame_id = "camera_left" if "L" in str(image_path) else "camera_right"
    else:
        image_message.utime = timestamp
    image_message.width = image.shape[1]
    image_message.height = image.shape[0]
    image_message.row_stride = image_message.width * 3
    image_message.pixelformat = image_t.PIXEL_FORMAT_RGB
    image_message.size = len(image_bytes)
    image_message.data = image_bytes
    image_message.nmetadata = 0
    image_message.metadata = []

    return image_message


def splice(input: Path, channel: str, directory: Path, output: Path):
    """
    Splice images into an LCM log from a directory, using the file name as a timestamp.

    Args:
        input: Log file to splice into
        channel: Channel name to use for images
        directory: Directory of images to splice
        output: Log file to write
    """
    reader = LogReader(input)
    writer = LogWriter(output)

    image_paths = sorted(directory.glob("*"))
    image_timestamps = [int(image_path.stem) for image_path in image_paths]

    # Reindex events
    last_event_number = 0

    def write(event: Event):
        nonlocal last_event_number
        event.header.event_number = last_event_number + 1
        writer.write(event)
        last_event_number = event.header.event_number

    current_image_idx = 0
    for event in reader:
        # Check for images to write before this event
        while current_image_idx < len(image_paths):
            image_path = image_paths[current_image_idx]
            image_timestamp = image_timestamps[current_image_idx]

            if image_timestamp < event.header.timestamp:
                # Write image event
                image_message = get_image_as_message(image_path, image_timestamp, current_image_idx)
                event_bytes = image_message.encode()

                image_header = Header(-1, image_timestamp, len(channel), len(event_bytes))
                image_event = Event(image_header, channel, event_bytes)
                write(image_event)

                print(f"Spliced {image_path} at {image_timestamp} (event {image_header.event_number})")
                current_image_idx += 1
            else:
                break

        # Write event
        write(event)

    print(f"Spliced {current_image_idx} images into {input}, wrote to {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Log file to splice into")
    parser.add_argument("channel", type=str, help="Channel name to use for images")
    parser.add_argument("directory", type=Path, help="Directory of images to splice")
    parser.add_argument("output", type=Path, help="Log file to write")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite output file if it exists")

    args = parser.parse_args()

    if not args.overwrite and args.output.exists():
        parser.error(f"Output file {args.output} already exists")

    if not args.directory.is_dir():
        parser.error(f"Image directory {args.directory} does not exist")

    if not args.input.exists():
        parser.error(f"Input file {args.input} does not exist")

    splice(args.input, args.channel, args.directory, args.output)


if __name__ == "__main__":
    main()
