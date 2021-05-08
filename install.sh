#!/bin/bash


echo "Installing pre-requisits"
sudo apt-get install scons swig

echo "Installing LED Control"
git clone --recurse-submodules https://github.com/jackw01/led-control.git
cd led-control
sudo python3 setup.py develop
cd ..

echo "Installing init scripts"
sudo cp ./ledcontrol.default /etc/default/ledcontrol
sudo cp ./ledcontrol.initd /etc/init.d/ledcontrol
sudo chmod +x /etc/init.d/ledcontrol

sudo update-rc.d ledcontrol defaults

echo "Starting LED Control"
sudo service ledcontrol start

echo "Copying moonraker component"
cp ledcontrol.py ~/moonraker/moonraker/components

echo "Copying klipper macros"
cp ledcontrol.cfg ~/klipper_config/

echo "Configuring moonraker"
echo "[ledcontrol]" >> ~/klipper_config/moonraker.conf
echo "address: http://localhost:8000" >>  ~/klipper_config/moonraker.conf

echo "Restarting Moonraker"
sudo service moonraker restart

echo "Installation finished. Configure your LEDs in /etc/defaults/ledcontrol"
echo "Add [include ledcontrol.cfg] to your printer.cfg and restart klipper"
