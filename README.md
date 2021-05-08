# moonshine
Controlling LEDs from [Klipper](https://www.klipper3d.org) using [LED Control](https://github.com/jackw01/led-control) and a moonraker component. This repository contains the files and an installation script.

## Installation

To install clone the repository and run the installation script:
```
git clone https://github.com/julianschill/moonshine.git
cd moonshine
./install.sh
```

This installs LED Control, adds an init.d script to start it at boot, configures moonraker and adds some sample gcode macros.

## Configuration

1. Edit the file
```
/etc/default/ledcontrol
```
and change the numbers of LEDs to the number of your setup. Then restart ledcontrol with
```
sudo service ledcontrol restart
```
2. Add the following to your printer.cfg and restart klipper:
```
[include ledcontrol.cfg]
```

