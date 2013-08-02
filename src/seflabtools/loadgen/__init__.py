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
from controller import Controller
from seflabtools.exceptions import ArgumentsError
from seflabtools.synch import serialdevice
from seflabtools.synch.synchronizer import Synchronizer
from worker import CPUWorker, HDDWorker
import getopt
import os
import seflabtools.synch.serialdevice
import sys



def getUsageInformation(cmdName):
    usageInformation = ""
    usageInformation += "Usage: {0} -w <cpu | hdd> -d <duration_in_seconds> [-s <serial_port>] [-o <file>]\n".format(cmdName)
    usageInformation += "-w\t\tselects the hardware component worker to run\n"
    usageInformation += "-d\t\tdefines for how long (in seconds) load should be generated\n"
    usageInformation += "-s\t\tgenerates synchronization pulses sent through a serial port\n"
    usageInformation += "-o\t\tdefines the file whereto print the timestamps to.\n"
    return usageInformation


def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    usageInformation = getUsageInformation(cmdName)

    workerString = None
    durationString = None
    serialPort = None
    outputFile = None
    try:
        opts, _ = getopt.getopt(argv[1:], "w:d:s:o:", ["worker=", "duration=", "serial=", "output="])
    except getopt.GetoptError as e:
        raise ArgumentsError(str(e), usageInformation)
    for opt, arg in opts:
        if opt in ("-w", "--worker"):
            workerString = arg
        elif opt in ("-d", "--duration"):
            durationString = arg
        elif opt in ("-s", "--serial"):
            serialPort = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
    if (workerString != 'cpu' and workerString != 'hdd') or durationString == None or durationString == '0':
        raise ArgumentsError("Hardware has to be one of (cpu | hdd) and a duration greater than 0", usageInformation)
    if outputFile != None:
        try:
            file(outputFile, 'a').close()
        except IOError as e:
            raise ArgumentsError("Can't write to output file for timestamps.\n" + str(e), usageInformation)
    duration = 0
    try:
        duration = float(durationString)
    except ValueError, e:
        raise ArgumentsError("Invalid duration: " + str(e), usageInformation)

    worker = None
    if workerString == 'cpu':
        worker = CPUWorker(True)
    else:
        worker = HDDWorker(False)

    return (worker, duration, serialPort, outputFile)


def main(argv):
    (worker, duration, serialPort, outputFile) = parseArguments(argv)

    ctr = Controller(duration, worker)
    if serialPort != None:
        synch = Synchronizer(serialdevice.getSerialDeviceWrapper(serialPort), outputFile)
        print "Generating load with synchronization pulses"
        synch.doRunFunction(ctr.start)
    else:
        print "Generating load"
        ctr.start()
