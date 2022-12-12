#!/bin/bash

while true
	do
	dana=`cat dane`
	wzorzec='^[0-9]+$'
	if [[ "$dana" =~ $wzorzec ]] ; then
		echo $(( 2 * $dana - 1)) > wyniki
		echo '' > dane
	fi
done 
