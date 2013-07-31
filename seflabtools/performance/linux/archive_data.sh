#!/bin/bash

# SEFLab Tools is a software package that provides tools for running experiments in the SEFLab
# as well as for analyzing the resulting data.
#
# Copyright (C) 2013  Software Improvement Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ARCHIVE_NAME=$1
SOURCE_DIR=$2

if [ -z ARCHIVE_NAME ] | [ -z $SOURCE_DIR ]; then
	echo "Parameter missing: $(basename $0) <archive name> <source dir>"	
	echo "  <archive name>: is the name of the archive file to be created"
	echo "    <source dir>: is the directory to be archived"
	exit
fi

tar -czf $ARCHIVE_NAME $SOURCE_DIR && rm -rf $SOURCE_DIR
