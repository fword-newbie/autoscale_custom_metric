#!/bin/sh
s1=$1
s2=$2
s3=$3
s4=$4
sudo kubectl apply -f $s1
sudo kubectl wait deployment/$s2 --for=condition=available --timeout=100s
sudo kubectl apply -f $s3
sleep 3
sudo kubectl delete -f $s4