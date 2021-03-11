#! /usr/bin/sh

if [ -f $1 ]
then
    echo 1 > checkPath
else
    if [ -d $1 ]
    then
        echo 1 > checkPath
    else
        echo 0 > checkPath
    fi
fi