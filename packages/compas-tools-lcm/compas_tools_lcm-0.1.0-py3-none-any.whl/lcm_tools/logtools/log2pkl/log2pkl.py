"""
This script provides the class for the LCMLog data structure with the corresponding
properties and methods for the parsing, and writing of new logs given a data in a
dictionary structure.

This script runs automatically to convert all the LCM logs into pickle files.
"""

from typing import Any, Dict, Iterable, Optional, Union
from pathlib import Path
from lcm import EventLog
from navlib.lcmlog import parse_and_save

# import lcmlog2smat.scan_for_lcmtypes
import os
import pickle
import argparse

import numpy as np


class nav_structtype ():
    pass


class LCMLog:
    """
    Generic Class for SE(3) matrices. Contain the path to the .00 lcmlog file
    """

    def __init__(self, lcmlog_path: Path) -> None:
        """
        Initialize LCMLog object.

        Parameters
        ----------
        lcmlog_path : Path
            Path to the lcmlog file
        """
        super().__init__()
        self._lcmlogPath = lcmlog_path
        self.data = dict()
        self.events_dir = list()
        self.times_dir = list()
        self.errors = 0

    ####################################################################################################################
    # Properties                                                                                                       #
    ####################################################################################################################

    @property
    def path(self) -> str:
        """lcmlog file path"""
        return str(self._lcmlogPath)

    ####################################################################################################################
    # Methods                                                                                                          #
    ####################################################################################################################

    # def parse_log(self) -> None:
    #     """
    #     Parse LCM log into dictionary. Each log channel is a key of the dictionary,
    #     the data for each channel is nested into the dictionary values.
    #     """
    #     verbose = False
    #     channelsToProcess = ".*"
    #     channelsToIgnore = ""

    #     type_db = lcmlog2smat.scan_for_lcmtypes.make_lcmtype_dictionary()

    #     channelsToProcess = re.compile(channelsToProcess)
    #     channelsToIgnore = re.compile(channelsToIgnore)

    #     log = EventLog(self.path, "r")

    #     ignored_channels = []
    #     msgCount = 0

    #     # Iterate LCM log file
    #     for e in log:
    #         packed_fingerprint = e.data[:8]
    #         lcmtype = type_db.get(packed_fingerprint, None)
    #         if not lcmtype:
    #             if verbose:
    #                 print(f"Ignoring channel {e.channel} - not a known LCM type")
    #             ignored_channels.append(e.channel)
    #             continue
    #         try:
    #             msg = lcmtype.decode(e.data)
    #         except Exception:
    #             print(f"Error: couldn't decode msg on channel {e.channel}")
    #             continue

    #         msgCount = msgCount + 1
    #         if (msgCount % 5000) == 0:
    #             print(f"read {msgCount} messages, {log.tell() / float(log.size()) * 100:.2f}% done")

    #         LCMLog.msg_to_dict(self.data, e.channel, msg, verbose, e.timestamp / 1e6, e.eventnum, lcmtype)

    def create_log(self) -> None:
        """
        Creates an events directory as a list, where each element is a sublist that
        contains: 1) The unix time lcm timestamp in milliseconds as integer, 2) the
        channel to broadcast the data, and 3) the message encoded.
        """
        # Create event in an iterative mode:
        for channel in [*self.data]:
            print("Writing %s events from channel %s" % (len(self.data[channel]["eventnum"]), channel))
            s = ".".join(str(self.data[channel]["lcmtype"][0]).split("'")[1].split(".")[:-1]) + "()"
            s.replace("lcmtypes", "compas_lcm")
            msg = eval(s)
            for event in range(len(self.data[channel]["eventnum"])):
                try:
                    msg2 = LCMLog.special_messages(LCMLog.read_slots(msg, self.data[channel], event), channel)
                    self.events_dir.append(
                        [int(self.data[channel]["lcm_timestamp"][event] * 1e6), channel, msg2.encode()]
                    )
                    self.times_dir.append(int(self.data[channel]["lcm_timestamp"][event] * 1e6))
                except Exception:
                    print(f"Error {self.errors}: Failed to encode event {event} on channel {channel}")
                    self.errors += 1

        # sort time directories and get indices
        self.times_dir = list(np.argsort(np.array(self.times_dir)))

    def write_log(self, output_file: str, overwrite: bool):
        """
        Create an EventLog with the filename, and writes the data from a dictionary
        as events.

        Parameters
        ----------
        output_file : str
            Path to write the corrected LCM log.
        overwrite: bool
            Flag that states if the file should be overwrite if the fname matches an
            existing file.
        """
        # Create lcmlog binary file
        log = EventLog(output_file, "w", overwrite=overwrite)

        # Read events directory and write events into the eventlog
        self.create_log()

        for event_index in self.times_dir:
            event = self.events_dir[event_index]
            log.write_event(event[0], event[1], event[2])

    def read_log(self, processed_channels) -> nav_structtype:
        """
        read_log gets a file name and returns the data as a nav_structtype
        object. If the fname does not correspond to a .pkl file the transforms a
        lcm_log to a pickle file.

        Parameters
        ----------
        fname: Path
            File path

        Returns
        -------
        LCMLog data as a nav_structtype object
        """
        fname = Path(self.path)
        parent, stem = Path(fname.parent), Path(fname.stem)
        # Check if file is not already parsed to a pickle file
        if not os.path.isfile(str(parent/stem) + ".pkl"):
            # If it is not a file, replace "." and "-" by "_"
            stem_alt = str(stem).replace(".", "_").replace("-", "_")
            try:
                if not os.path.isfile("/".join([str(parent), ".".join([stem_alt, "pkl"])])):
                    print("Pickle file not found, looking for lcmlog with same stem")
                    parse_and_save(str(fname), [('-k', ''), 
                                                ('-o', str(parent/stem) + '.pkl'),
                                                ('-c', processed_channels)])
                    print(f"LCMLogs {str(fname)} parsed to .pkl format")
                    fname_alt = str(parent/stem)
            except FileNotFoundError:
                print('{fname} not found neither as lcmlog nor as .pkl file.')
                return
        else:
            fname_alt = str(parent/stem)

        # Load Pickle file
        print(f"Loading pickle logfile:  {fname_alt}.pkl")
        pkl_file = open(fname_alt + '.pkl', 'rb')
        ddata = pickle.load(pkl_file)

        # Convert dictionary to a structure with numpy arrays
        data = LCMLog.dict_to_struct(ddata)
        print("LCMLog successfully transformed to nav_structtype object")
        return data

    @staticmethod
    def msg_to_dict(
        data: Dict,
        e_channel: str,
        msg: Any,
        verbose: Optional[bool] = False,
        lcm_timestamp: Optional[Union[float, int]] = -1,
        eventnum: Optional[int] = -1,
        lcmtype: Optional[str] = None,
    ) -> None:
        """
        Get and lcm message and add all the slots' values into the corresponding
        channel key.

        Parameters:
        -----------
        data: dict
            Dictionary to store the messages data
        e_channel: str
            Channel that the message belongs to
        msg: object from the lcm class event
            Message to store in data
        statusMsg: str
            Progress information to display in terminal
        verbose: Bool, optional -> default: False
            Flag that indicates whether to display information or not
        lcm_timestamp: int, optional -> default: -1
            Status for message lcm_timestamp
        eventnum: int, optional -> default: -1
            Status for message eventnum
        lcmtype: str, optional -> default: None
            Message lcmtype
        """
        # Initializing channel
        if e_channel not in data:
            data[e_channel] = dict()

            # Iterate each constant of the LCM message
            constants = LCMLog.msg_getconstants(msg)
            for i in range(len(constants)):
                myValue = None
                myValue = eval("msg." + constants[i])
                data[e_channel][constants[i][:31]] = myValue

        # Get lcm fields and constants
        fields = LCMLog.msg_getfields(msg)

        # Iterate each field of the LCM message
        for i in range(len(fields)):
            myValue = None
            myValue = eval(" msg." + fields[i])
            if isinstance(myValue, (int, float, tuple, list, str)):
                try:
                    data[e_channel][fields[i][:31]].append(myValue)
                except KeyError:
                    data[e_channel][fields[i][:31]] = [(myValue)]

            elif hasattr(myValue, "__slots__"):
                submsg = eval("msg." + fields[i])
                LCMLog.msg_to_dict(data[e_channel], fields[i][:31], submsg, verbose)

            else:
                if verbose:
                    LCMLog.logger.warning(f"Ignoring field {fields[i]} from channel {e_channel}.")
                continue

        # Add extra field with lcm_timestamp
        if lcm_timestamp > 0:
            try:
                data[e_channel]["lcm_timestamp"].append(lcm_timestamp)
            except KeyError:
                data[e_channel]["lcm_timestamp"] = [lcm_timestamp]

        # Add extra field with eventnum
        if eventnum > 0:
            try:
                data[e_channel]["eventnum"].append(eventnum)
            except KeyError:
                data[e_channel]["eventnum"] = [eventnum]

        # Add lcmtype:
        try:
            data[e_channel]["lcmtype"].append(lcmtype)
        except KeyError:
            data[e_channel]["lcmtype"] = [(lcmtype)]

    @staticmethod
    def msg_getfields(lcm_msg: Any) -> Iterable[str]:
        """
        Get all the slots in a lcm message

        Parameters:
        -----------
        lcm_msg: Any
            Decoded message

        Returns:
        --------
        slots: Iterable[str]
            Slots from the lcm message
        """
        return lcm_msg.__slots__

    @staticmethod
    def msg_getconstants(lcm_msg: Any) -> Iterable[str]:
        """
        Get the attributes that are common between all the messages

        Parameters:
        -----------
        lcm_msg: Any
            Decoded message

        Returns:
        --------
        constants: Iterable[str]
            Constant attributes from the lcm message
        """
        # Get full list of valid attributes
        fulllist = dir(lcm_msg)
        # Get constants
        constantslist = [
            x
            for x in fulllist
            if not (x[0] == "_")
            if not (x == "decode")
            if not (x == "encode")
            if x not in LCMLog.msg_getfields(lcm_msg)
        ]
        return constantslist


    @staticmethod
    def dict_to_struct(ddata: Dict) -> nav_structtype:
        """
        nav_dict_to_struct takes as input a simple or nested dictionary with
        data and returns an object of the class nav_structtype with the data.

        Parameters
        ----------
        ddata : Dict
            LCMLog data dictionary

        Returns
        -------
        LCMLog data as a nav_structtype object
        """
        # Create new object
        sdata = nav_structtype()

        # Iterate each element of the dictionary
        for k, v in ddata.items():

            # Fix dictionary key name (remove '.')
            k = k.replace('.', '_')
            k = k.replace('$', 'S')

            # Recursive function to deal with nested dictionaries
            if isinstance(v, dict):
                exec(compile('sdata.' + k + ' = LCMLog.dict_to_struct(v)', '<string>', 'exec'))
            else:
                exec(compile('sdata.' + k + ' = np.array(v)', '<string>', 'exec'))

        return sdata


def search_files(directory, file_list):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            search_files(path, file_list)
        else:
            if "lcmlog" in path and not any(ext in path for ext in [".txt", ".pkl", ".jlp"]):
                print(f"lcmlog found at: {path}")
                file_list.append(path)


def main():
    # create the parser object
    parser = argparse.ArgumentParser(description='LCM log to Pickle converter.', add_help=True)

    # add the arguments
    parser.add_argument('-p', '--path', help='Directory path.', required=True)
    parser.add_argument('-c', '--processed_channels', help='RegEx with processed channels', default=".*")

    # parse the arguments
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        exit()

    if not os.path.isdir(args.path):
        raise ValueError("The provided path is not a directory in the system.")
    directory = args.path
    processed_channels = args.processed_channels
    lcmlogs = []
    search_files(directory, lcmlogs)

    for log_path in lcmlogs:
        print(f"Processing: {log_path}\n")
        LCMLog(log_path).read_log(processed_channels)
        print("\n----------\n")
        print(f"Logs conversion to pkl completed for top folder: {directory}")


if __name__ == "__main__":
    main()
