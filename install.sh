#!/bin/bash

CONFIG_DIR=~/klipper_config
MOONRAKER_DIR=~/moonraker
while getopts c:m flag
do
    case "${flag}" in
        c) CONFIG_DIR=${OPTARG};;
        m) MOONRAKER_DIR=${OPTARG};;
    esac
done

if [ ! -d "$CONFIG_DIR" ]; then
  echo "Cannot find klipper configuration directory ${CONFIG_DIR}. Please specify with -c <directory>"
  exit 1
fi

if [ ! -d "$MOONRAKER_DIR" ]; then
  echo "Cannot find klipper configuration directory ${CONFIG_DIR}. Please specify with -m <directory>"
  exit 1
fi

echo "Installing pre-requisits"
sudo apt-get install -y scons swig libev-dev python3-dev python3-setuptools 

echo "Installing LED Control"
git clone --recurse-submodules https://github.com/jackw01/led-control.git
cd led-control
git checkout tags/v2.0.0
sudo python3 setup.py develop
cd ..

echo "Installing init scripts"
sudo cp ./ledcontrol.default /etc/default/ledcontrol
sudo cp ./ledcontrol.initd /etc/init.d/ledcontrol
sudo chmod +x /etc/init.d/ledcontrol

sudo update-rc.d ledcontrol defaults

echo "Starting LED Control"
sudo service ledcontrol start

echo "Installing moonraker component"
ln -sr ./ledcontrol.py $MOONRAKER_DIR/moonraker/components

echo "Installing klipper macros"
ln -sr ./ledcontrol.cfg $CONFIG_DIR/ledcontrol.cfg

echo "Configuring moonraker"

grep -qxF '[ledcontrol]' $CONFIG_DIR/moonraker.conf || echo -e '\n[ledcontrol]\naddress: http://localhost:8000' >> $CONFIG_DIR/moonraker.conf

echo "Restarting Moonraker"
sudo service moonraker restart

echo "Installation finished."
echo ""
echo "Add [include ledcontrol.cfg] to your printer.cfg and restart klipper"
