#!/bin/bash 
echo "Creating a virtual environment"

python3 -m venv env3
source env3/bin/activate
pip install -U pip

echo
echo "Installing requirements"
pip install -r requirements.txt

echo
echo "Installing MP4Box"
sudo apt install -y gpac

echo
echo "Copying the sample webex_config.py file if it does not exist"
if [ ! -f webex_config.py ]; then
    cp sam_webex_config.py webex_config.py 

fi
echo
echo "Please activate the virtual environment using the following command:"
echo "source env3/bin/activate"
