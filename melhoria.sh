#!/bin/bash

if [ $# -ne 2 ]; then
    echo "ERROR: Illegal number of args"
    exit 1
fi

FILE1=$1
FILE2=$2
echo "-------- Melhoria Relativa --------"
paste $FILE1 $FILE2 | gawk '{print $1, (100*$5/$2) - 100}'

echo -e "\n"

echo "-------- Melhoria Absoluta --------"
paste $FILE1 $FILE2 | gawk '{print $1, $5-$2}'
echo "---------------- = ----------------"

exit 0

