#!/bin/sh
s1=$1
response=$(curl $s1)
values=$(echo "$response" | jq -r '.data.result[0].values[] | .[1]')

filename="a.txt"
echo "$values" > "$filename"
cp a.txt /shared-data/a.txt