#!/usr/bin/env bash

## add-apt-repository -y ppa:freecad-maintainers/freecad-legacy
add-apt-repository -y ppa:freecad-maintainers/freecad-stable
apt-get update
# apt-get install -y freecad
apt-get install -y libfreecad-python3-0.18
apt-get install -y libfreecad-python2-0.18
# apt-get install -y python-enum34
DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip
# pip install autologging
# pip3 install autologging
pip install pytest
pip3 install pytest
mkdir -p /home/vagrant/.local/lib/python2.7/site-packages
echo "/usr/lib/freecad-python2/lib" > /home/vagrant/.local/lib/python2.7/site-packages/freecad.pth
mkdir -p /home/vagrant/.local/lib/python3.6/site-packages
echo "/usr/lib/freecad-python3/lib" > /home/vagrant/.local/lib/python3.6/site-packages/freecad.pth
pip install -e /vagrant/
pip3 install -e /vagrant/
## pip install dill==0.2.7.1
