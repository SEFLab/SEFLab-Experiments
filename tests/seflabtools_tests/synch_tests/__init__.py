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
from seflabtools.synch.serialdevice import AbstractSerialDevice


class MockSerialDevice(AbstractSerialDevice):

    def init(self):
        self.statusRTS = None
        self.statusRTSHistory = []

    def setRTS(self, level):
        self.statusRTSHistory.append(self.statusRTS)
        self.statusRTS = level

    def getRTS(self):
        return self.statusRTS

    def getRTSHistory(self):
        return self.statusRTSHistory

    def clearRTSHistory(self):
        self.statusRTSHistory = []
