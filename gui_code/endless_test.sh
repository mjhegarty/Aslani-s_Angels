#!/bin/bash
rm demofile.txt
while :
    do
    for i in {1..10}
    do
    echo $i >> demofile.txt
    sleep .1
    done
    done

