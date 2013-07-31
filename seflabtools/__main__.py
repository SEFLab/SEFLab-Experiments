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

import sys
import getopt
import os.path

import synch
import loadmon
import loadgen


availableTools = ["synch", "loadgen", "loadmon"]

def printToolOptions(tools):
    ntools = len(tools)
    printableTools = [tools[0], "|"]
    for i in range(1, ntools - 1):
        printableTools.append(tools[i])
        printableTools.append("|")
    printableTools.append(tools[ntools - 1])
    
    return printableTools

def printUsage(cmdName, tools):
    print "Usage: {0} [-h] [-t <{1}>] ...".format(cmdName, ''.join(printToolOptions(tools)))
    print "-h\t\tprints this usage information"
    print "-t\t\tselects which tool to use"
    print "\nFor tool specific help do:"
    print "{0} -t <tool>".format(cmdName)
    

def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    try:
        opts, _ = getopt.getopt(argv[1:], "ht:m:d:s:c:o:w:", ["tool="])
    except getopt.GetoptError as e:
        print str(e)
        printUsage(cmdName, availableTools)
        sys.exit(1)
    tool = None
    for opt, arg in opts:
        if opt == '-h':
            printUsage(cmdName, availableTools)
            sys.exit()
        elif opt in ("-t", "--tool"):
            tool = arg
    if tool == None:
        print "No tool selected"
        printUsage(cmdName, availableTools)
        sys.exit(2)
    if tool not in availableTools:
        print "Selected tool is not available:", tool
        printUsage(cmdName, availableTools)
        sys.exit(2)
    
    return tool


if __name__ == '__main__':
    tool = parseArguments(sys.argv)
    
    if tool == "synch":
        synch.main(sys.argv[2:])
    elif tool == "loadgen":
        loadgen.main(sys.argv[2:])
    elif tool == "loadmon":
        loadmon.main(sys.argv[2:])
    