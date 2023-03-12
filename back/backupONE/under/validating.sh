<<<<<<< HEAD
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

=======
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

>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
echo "The result is: $result" > result.txt