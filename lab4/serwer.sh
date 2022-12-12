#!/bin/bash

trap "" SIGHUP SIGTERM
trap "exit 0" SIGUSR1

lacze="$HOME/lab04/serwerfifo"

if [  $# -eq 0 ];
then
	if [ -p $lacze ];
	then
		rm $lacze
	fi
	mkfifo $lacze
	while :;
	do
		echo "czekam na klienta"
		read dane < $lacze
		if [ -n "$dane" ];
		then
			lacze_klienta=$(echo $dane | awk '{print $1}')
			liczba=$(echo $dane | awk '{print $2}')
			./serwer.sh $liczba $lacze_klienta &
			trap "" SIGCHLD
			wait
		fi
	done
elif [ $# -eq 2 ];
then
	echo $((2*$1 - 1)) > $2
fi

exit 0
