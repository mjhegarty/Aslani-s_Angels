#!/bin/bash
echo "Hello world from Bash"

until  sudo rfcomm connect hci0 xxxxxx
do
    echo "Trying again"
    sleep 2
done

