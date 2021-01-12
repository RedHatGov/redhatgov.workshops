#!/bin/bash

export nodes=$1
export students=$2
export domain=$3
export workshop=$4

export count=1 student=0 node=1

while [ $count -lt `echo $nodes*$students+1 | bc` ]; do
  export mod=`echo $count%$nodes|bc`
#  echo count# $count mod is $mod student is $student node is $node
  echo $workshop.node$node.$student.$domain
  count=`echo $count+1 |bc`
  if [ $mod -eq 0 ]; then
    student=`echo $student+1|bc`
    node=1
  else
    node=`echo $node+1|bc`
  fi
done
