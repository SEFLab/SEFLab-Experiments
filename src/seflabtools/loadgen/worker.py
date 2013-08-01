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

import time
import random
import multiprocessing
from tempfile import TemporaryFile


class Worker(object):

    def doWork(self):
        raise NotImplementedError("Method from abstract class not implemented")

    def startWorkers(self):
        ncpus = multiprocessing.cpu_count()
        processes = []
        for _ in range(1, random.randrange(1, ncpus + 1)):
            p = multiprocessing.Process(target=self.doWork)
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

    def start(self, duration):
        self.duration = duration
        if self.multiworker:
            self.startWorkers()
        else:
            self.doWork()

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError(
                "Constructor of abstract class should not be called")


class CPUWorker(Worker):
    '''
    classdocs
    '''

    def doWork(self):
        startTime = time.time()
        while time.time() - startTime < self.duration:
            pass

    def __init__(self, multiworker):
        '''
        Constructor
        '''
        self.multiworker = multiworker
        random.seed(time.time())


class HDDWorker(Worker):
    '''
    classdocs
    '''
    dataChunk = "some data to write to the file"

    def doWork(self):
        tmp = TemporaryFile()
        tmp.write(HDDWorker.dataChunk)
        startTime = time.time()
        while time.time() - startTime < self.duration:
            flag = random.randrange(1, 4)
            if flag == 1:
                tmp.seek(0, 2)
                tmp.write(HDDWorker.dataChunk)
                tmp.write(HDDWorker.dataChunk)
                tmp.write(HDDWorker.dataChunk)
                tmp.write(HDDWorker.dataChunk)
                tmp.flush()
            elif flag == 2:
                tmp.seek(0, 0)
                tmp.read(len(HDDWorker.dataChunk))
                tmp.read(len(HDDWorker.dataChunk))
                tmp.read(len(HDDWorker.dataChunk))
                tmp.read(len(HDDWorker.dataChunk))
            else:
                time.sleep(random.random())
        tmp.close()

    def __init__(self, multiworker):
        '''
        Constructor
        '''
        self.multiworker = multiworker
        random.seed(time.time())
