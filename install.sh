#!/bin/bash

# Add deadsnakes PPA for Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update

# Install Python 3.10 and related packages
sudo apt-get install python3.10 -y
sudo apt install python3.10-venv -y
sudo apt-get install python3.10-dev -y
sudo apt-get install git -y

# Create a virtual environment using Python 3.10
python3.10 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install packaging separately as requested
pip install packaging

# Upgrade pip again as requested
pip install --upgrade pip

# Install the rest of the dependencies from requirements.txt
pip install -r requirements.txt

# reinstall SimpleITK !
python3 -m pip install SimpleITK==2.1.1.2

