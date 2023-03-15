#!/bin/bash

# This script will check all files in the current directory and format them to be optimized

for file in *
do

# Check if the file is a text file

    if [[ $file == *.txt ]]
    then
        # Format the file
        sed -i 's/\s\+/ /g' $file
    fi
done
# print result in file whit bash
echo "The result is: $result" > result.txt