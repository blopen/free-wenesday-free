<<<<<<< HEAD
#!/bin/bash

# Backup the sources list files
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/docker.list.bak

# Remove the duplicate entry from sources.list and sources.list.d/docker.list
sudo sed -i '/stable\/cnf\/Commands-all/d' /etc/apt/sources.list
sudo sed -i '/stable\/cnf\/Commands-all/d' /etc/apt/sources.list.d/docker.list

# Update the package information
sudo apt update

=======
#!/bin/bash

# Backup the sources list files
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /etc/apt/sources.list.d/docker.list /etc/apt/sources.list.d/docker.list.bak

# Remove the duplicate entry from sources.list and sources.list.d/docker.list
sudo sed -i '/stable\/cnf\/Commands-all/d' /etc/apt/sources.list
sudo sed -i '/stable\/cnf\/Commands-all/d' /etc/apt/sources.list.d/docker.list

# Update the package information
sudo apt update

>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
