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

OUTPUTDIR=$1
USER=$2
INCLUDE=$3
EXCLUDE=$4
ZIP=$5

if [ -z OUTPUTDIR ] | [ -z $USER ] | [ -z $INCLUDE ]; then
	echo "Parameter missing: $(basename $0) <output directory> <user or pid> <include> [<exclude>] [<zip>]"	
	echo "  <output directory>: is the direcvtory where proc files will be copied to"
	echo "       <user or pid>: if a user name us passed here then all processes of that user"
	echo "                      will be scaned against the inclusin and exclusion criteria"
	echo "           <include>: regex that defines the strings to be matched against the output"
	echo "                      of pstree to include a given process in the data collection"
	echo "           <exclude>: regex that defines the strings to be matched against the output"
	echo "                      of pstree to exclude a given process in the data collection"
	echo "               <zip>: If any value is passed here then the data will be zipped every 10 minutes"
	exit
fi

stop=0
trap "stop=1" SIGQUIT

collect_data() {
    tmpdir=$1
	date=$2

	while read -r line; do
		if [ ! -z $EXCLUDE ]; then
			pid=$(echo $line | grep -v -E $EXCLUDE)
		else
			pid=$line
		fi

		pid=$(echo $pid | sed -e "s/^[a-zA-Z0-9_-]*,//" -e "s/ .*//")

		if [ ! -z $pid ]; then
			cp /proc/"$pid"/stat $tmpdir/"$date"_"$pid"_"$USER"_"$INCLUDE"_stat
		fi
	done < <(pstree -alp $USER | grep -v -E "{[a-zA-Z]+}" | sed "s/^[^a-zA-Z]*//" | grep -E $INCLUDE)
}

move_files() {
	$src=$1
	$dst=$2
	
	cd ${src}
	for f in $(ls); do
		mv $f ../${dst}
	done
	cd -
}

sleeptime=0.7
tmpdir=$OUTPUTDIR/tmp
mkdir $tmpdir
while [ $stop -eq 0 ]; do
    fulldate=$(date "+%Y%m%d_%0H%M%S")
	collect_data $tmpdir $fulldate
	cp /proc/stat $tmpdir/"$date"_stat

	if [ ! -z $ZIP ] & [[ $fulldate =~ [0-9]{8}_[0-9]{4}[0-9]0 ]]; then
        archivedir=$OUTPUTDIR/$fulldate                  
        mkdir $archivedir
		move_files $tmpdir $archivedir
        nohup ./archive_script "${archivedir}_stat.tar.gz" "$archivedir"
		continue
	fi
	sleep $sleeptime
done

fulldate=$(date "+%Y%m%d_%0H%M%S")
archivedir=$OUTPUTDIR/$fulldate
mkdir $archivedir
mv $tmpdir/* $archivedir
./archive_data.sh "${archivedir}_stat.tar.gz" "$archivedir"
rm -rf $tmpdir
