#!/bin/bash

apt-get update && apt-get upgrade
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install libgl1 -y

pip3 install ultralytics
pip3 install ultralytics --upgrade
pip3 install opencv-python
pip3 install torchvision
pip3 install numpy
