'''
SEFLab Tools is a software package that provides tools for running experiments in the SEFLab
as well as for analyzing the resulting data.

Copyright (C) 2013  Software Improvement Group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import getopt
import os
import sys
import serial
import time

from seflabtools.exceptions import ArgumentsError
from synchronizer import Synchronizer
from serialdevice import SerialDevice

RUN_MODE = "run"
IDLE_MODE = "idle"


def getUsageInformation(cmdName):
    usageInformation = ""
    usageInformation += "Usage: {0} -m <mode> -s <serial_port> [-c <command>] [-d <idle duration>] [-o <file>\n".format(cmdName)
    usageInformation += "-m\t\tsets the tool workign mode to run a command or idle for a period of time.\n"
    usageInformation += "  \t\tOptions are {0} or {1}.\n".format(RUN_MODE, IDLE_MODE)
    usageInformation += "  \t\tif duration is specified with mode run, then the tool will abort execution\n"
    usageInformation += "  \t\tafter the defined number of seconds.\n"
    usageInformation += "-s\t\tselects through which serial port to send the synchronization pulse.\n"
    usageInformation += "-c\t\tdefines the command to execute.\n"
    usageInformation += "-d\t\tdefines the number of seconds the tool should idle for.\n"
    usageInformation += "-o\t\tdefines the file whereto usageInformation += the timestamps to."
    return usageInformation


def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    usageInformation = getUsageInformation(cmdName)
    try:
        opts, _ = getopt.getopt(argv[1:], "s:c:m:d:o:", ["serial=", "command=", "mode=", "duration=", "output="])
    except getopt.GetoptError as e:
        raise ArgumentsError(str(e), usageInformation)
    mode = None
    serialPort = None
    command = None
    durationString = None
    outputFile = None
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-s", "--serial"):
            serialPort = arg
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-d", "--duration"):
            durationString = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
    if serialPort == None:
        raise ArgumentsError("No serial port selected.", usageInformation)
    if mode == RUN_MODE and command == None:
        raise ArgumentsError("Tool set to run command but no command was defined.", usageInformation)
    if mode == IDLE_MODE and (durationString == None or durationString == "0"):
        raise ArgumentsError("Tool set to idle but no valid duration was defined.", usageInformation)
    if outputFile != None:
        try:
            file(outputFile, 'a').close()
        except IOError as e:
            raise ArgumentsError("Can't write to output file for timestamps.\n" + str(e), usageInformation)

    duration = None
    if durationString != None:
        try:
            duration = float(durationString)
        except ValueError, e:
            raise ArgumentsError("Invalid duration: " + str(e), usageInformation)

    return (mode, serialPort, command, duration, outputFile)


def main(argv):
    (mode, serialPort, command, duration, outputFile) = parseArguments(argv)

    serialDeviceWrapper = SerialDevice(serialPort)
    serialDeviceWrapper.init()
    synch = Synchronizer(serialDeviceWrapper, outputFile)

    if mode == RUN_MODE:
        if duration == None:
            synch.doRun(command)
        else:
            synch.doThreadedRun(command, duration)
    else:
        synch.doIdle(duration)
