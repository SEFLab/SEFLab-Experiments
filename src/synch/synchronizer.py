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

import os
import psutil
import time
import multiprocessing
from datetime import datetime


class Synchronizer(object):
    '''
    classdocs
    '''
    pulseDuration = 1
    
    def doSetup(self):
        self.serialDeviceWrapper.setRTS(False)
        print "RTS set to low... waiting 5 seconds"
        time.sleep(5)

    def sendPulse(self, seconds):
        self.serialDeviceWrapper.setRTS(True)
        time.sleep(seconds)
        self.serialDeviceWrapper.setRTS(False)
        
    def runCommand(self, command):
        os.system(command)
    
    def doRunFunction(self, function):
        self.doSetup()
        print "Starting"
        self.sendPulse(Synchronizer.pulseDuration)
        startTime = datetime.now()
        function()
        endTime = datetime.now()
        self.sendPulse(Synchronizer.pulseDuration)
        print "Function terminated."
        self.printTimestamps(startTime, endTime, "run function")

    def doRun(self, commandToRunApplication):
        self.doSetup()
        print "Starting"
        self.sendPulse(Synchronizer.pulseDuration)
        startTime = datetime.now()
        self.runCommand(commandToRunApplication)
        endTime = datetime.now()
        self.sendPulse(Synchronizer.pulseDuration)
        print "Application terminated."
        self.printTimestamps(startTime, endTime, "run command")

    def terminateProcessAndAllSubProcesses(self, process):
        proc = psutil.Process(process.pid)
        children = proc.get_children(recursive=True)
        for child in children:
            child.terminate()
        proc.terminate()
        
    def doThreadedRun(self, commandToRunApplication, duration):
        p = multiprocessing.Process(target = self.runCommand, args = [commandToRunApplication])
        self.doSetup()
        print "Starting"
        self.sendPulse(Synchronizer.pulseDuration)
        startTime = datetime.now()
        p.start()
        time.sleep(duration)
        self.terminateProcessAndAllSubProcesses(p)
        endTime = datetime.now()
        self.sendPulse(Synchronizer.pulseDuration)
        print "Application terminated at timeout."
        self.printTimestamps(startTime, endTime, "run command for duration")
        
    def doIdle(self, duration):
        self.doSetup()
        print "Starting"
        self.sendPulse(Synchronizer.pulseDuration)
        startTime = datetime.now()
        time.sleep(duration)
        endTime = datetime.now()
        self.sendPulse(Synchronizer.pulseDuration)
        print "Idle period terminated"
        self.printTimestamps(startTime, endTime, "idle")

    def printTimestamps(self, startTime, endTime, activity):
        print "Start pulse sent at '", startTime, "'; End Pulse sent at '", endTime, "'"
        if self.outputFile != None:
            f = open(self.outputFile, 'a')
            f.write(unicode(startTime))
            f.write(", ")
            f.write(unicode(endTime))
            f.write(", ")
            f.write(activity)
            f.write("\n")
            f.close()  
        
        
    def __init__(self, outputFile, serialDeviceWrapper):
        '''
        Constructor
        '''
        self.serialDeviceWrapper = serialDeviceWrapper
        self.outputFile = outputFile
