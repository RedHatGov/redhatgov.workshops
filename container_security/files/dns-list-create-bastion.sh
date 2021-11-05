#!/bin/bash

export students=$1
export domain=$2
export workshop=$3

export count=0 student=0

while [ $count -lt $students ]; do
#  echo $workshop.node$node.$student.$domain
  echo bastion.$count.$workshop.$domain
  count=`echo $count+1 |bc`
done
