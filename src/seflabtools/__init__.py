'''
SEFLab Tools is a software package that provides tools for running experiments
in the SEFLab as well as for analyzing the resulting data.

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
import os.path

from exceptions import ArgumentsError
import synch
import loadmon
import loadgen

availableTools = ["synch", "loadgen", "loadmon"]


def getToolOptions(tools):
    ntools = len(tools)
    printableTools = [tools[0], "|"]
    for i in range(1, ntools - 1):
        printableTools.append(tools[i])
        printableTools.append("|")
    printableTools.append(tools[ntools - 1])

    return printableTools


def getUsageInformation(cmdName, tools):
    usageInformation = ""
    usageInformation += "Usage: {0} [-h] [-t <{1}>] ...".format(cmdName, ''.join(getToolOptions(tools))) + "\n"
    usageInformation += "-h\t\tprints this usage information\n"
    usageInformation += "-t\t\tselects which tool to use\n"
    usageInformation += "\nFor tool specific help do:\n"
    usageInformation += "{0} -t <tool>".format(cmdName) + "\n"
    return usageInformation


def parseArguments(argv):
    cmdName = os.path.basename(argv[0])
    usageInformation = getUsageInformation(cmdName, availableTools)
    try:
        opts, _ = getopt.getopt(argv[1:], "ht:m:d:s:c:o:w:", ["tool="])
    except getopt.GetoptError as e:
        raise ArgumentsError(str(e), usageInformation)
    tool = None
    for opt, arg in opts:
        if opt == '-h':
            tool = "help"
        elif opt in ("-t", "--tool"):
            tool = arg
    if tool == None:
        raise ArgumentsError("No tool selected", usageInformation)
    if tool not in availableTools and tool is not "help":
        raise ArgumentsError("{0} tool is not available".format(tool), usageInformation)

    return tool


def main(argv):
    try:
        tool = parseArguments(argv)

        if tool == "synch":
            synch.main(argv[2:])
        elif tool == "loadgen":
            loadgen.main(argv[2:])
        elif tool == "loadmon":
            loadmon.main(argv[2:])
        elif tool == "help":
            print getUsageInformation(argv[0], availableTools)
    except ArgumentsError as e:
        print str(e)
