#!/usr/bin/env bash

## add-apt-repository -y ppa:freecad-maintainers/freecad-legacy
## add-apt-repository -y ppa:freecad-maintainers/freecad-stable
apt-get update
apt-get install -y freecad
DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
pip install pytest
mkdir -p /home/vagrant/.local/lib/python2.7/site-packages
echo "/usr/lib/freecad/lib" > /home/vagrant/.local/lib/python2.7/site-packages/freecad.pth
pip install -e /vagrant/
