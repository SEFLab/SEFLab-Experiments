SEFLab-Experiments
==================

SEFLab Experiments is a software package that provides tools for running
experiments in the SEFLab.

For more information about the SEFLab see http://seflab.com

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


Package Structure
=================

The tools for running experiments have to be as lightweight as possible in order
to reduce interference with the system under test as much as possible.
This package contains tools written in Python 2.7, Bash and C.

The main functionalities provided are:
- measurement synchronization pulses:
	* When running an experiment it is most often the case that some application
	  will be run on a SEFLab machine while data about computational resources
	  and power consumption is being collected. In order to know when did the
	  actual application start and terminated, the SEFLab measurement setup
	  provides a way to send a synchronization pulse right before the
	  application starts and another one right after. These pulses will be 
	  recorded together with the power measurements and can later be analyzed to
	  precisely identify the period in which the application used in the test
	  was running. This tool is implemented in Python 2.7.
- load generation
	* This functionality can be used to artificially generate load in a machine.
	  As of now, it can generate load with random intensity and at random
	  intervals. That is what is typically called variable load. This tool will
	  soon be extended to also generate a constant load that maxes out the
	  capacity of the machine. This tool can currently generate CPU and hard
	  drive load. This tool is implemented in Python 2.7 and in the future it
	  will have a C extension that is capable of generating load on the memory
	  banks as well.
- machine load monitoring
	* This functionality monitors the CPU and hard drive load and prints it to
	  the console as comma separated values. This tool is implemented in
	  Python 2.7.
- process CPU monitoring (currently only for linux)
	* This functionality monitors CPU usage by processes. This tool is written 
	  in Bash.


Usage Examples
==============

In the examples bellow com3 is the serial port to where the synchronization hardware is connected
to. Replace that for the port on the system you're using.

Scenario: Idle for 10 seconds and record the timestamps on a file called pulseTimes.txt.
          Every time you write the timestamps to the same file they get appended.

          bin/seflabtools.[bat|sh] -t synch -m idle -d 10 -s com3 -o pulseTimes.txt

Scenario: Run a command for 10 seconds (forcing it to quit) and record the timestamps on a file
          called pulseTimes.txt. It is better to always create a script file with the command 
          you wanna run because this prevents problems with parsing of command line options

          bin/seflabtools.[bat|sh] -t synch -m run -d 10 -s com3 -o pulseTimes.txt -c command.script

Scenario: Run a command until it quits. Same thing as before only you don't specify a duration (-d).
          If you don't specify an output file for the timestamps they are not printed to a file but
          still appear on the screen.

          seflabtools.[bat|sh] -t synch -m run -s com3 -c command.bat

