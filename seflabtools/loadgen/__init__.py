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



def printUsage(cmdName):
    print "Usage: {0} -w <cpu | hdd> -d <duration_in_seconds> [-s <serial_port>] [-o <file>]".format(cmdName)
    print "-w\t\tselects the hardware component worker to run"
    print "-d\t\tdefines for how long (in seconds) load should be generated"
    print "-s\t\tgenerates synchronization pulses sent through a serial port"
    print "-o\t\tdefines the file whereto print the timestamps to."
    
def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    hwString = None
    durationString = None
    serialPort = None
    outputFile = None
    try:
        opts, _ = getopt.getopt(argv[1:],"w:d:s:o:",["worker=","duration=","serial=", "output="])
    except getopt.GetoptError as e:
        print str(e)
        printUsage(cmdName)
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-w", "--worker"):
            hwString = arg
        elif opt in ("-d", "--duration"):
            durationString = arg
        elif opt in ("-s", "--serial"):
            serialPort = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
    if (hwString != 'cpu' and hwString != 'hdd') or durationString == None or durationString == '0':
        print "Hardware has to be one of (cpu | hdd) and a duration greater than 0"
        printUsage(cmdName)
        sys.exit(2)
    if outputFile != None:
        try:
            file(outputFile, 'a').close()
        except IOError as e:
            print "Can't write to output file for timestamps. Reason: ", str(e)
            sys.exit(3)
    duration = 0
    try:
        duration = float(durationString)
    except ValueError, e:
        print "Invalid duration:", str(e)
        printUsage(cmdName)
        sys.exit(3)
    
    worker = None
    if hwString == 'cpu':
        worker = CPUWorker(True)
    else:
        worker  = HDDWorker(False)
    
    return worker, duration, serialPort, outputFile

def main(argv):
    worker, duration, serialPort, outputFile = parseArguments(argv)
    
    ctr = Controller(duration, worker)
    if serialPort != None:
        serialDeviceWrapper = SerialDevice(serialPort)
        synch = Synchronizer(serialDeviceWrapper, outputFile)
        print "Generating load with synchronization pulses"
        synch.doRunFunction(ctr.start)
    else:
        print "Generating load"
        ctr.start()
    

if __name__ == "__main__":
    import os
    import sys
    import getopt
    
    from controller import Controller
    from worker import CPUWorker
    from worker import HDDWorker
    from synch.synchronizer import Synchronizer
    from synch.serialdevice import SerialDevice

    main(sys.argv)


        


