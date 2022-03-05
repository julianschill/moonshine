# moonshine
Controlling LEDs from [Klipper](https://www.klipper3d.org) using [LED Control](https://github.com/jackw01/led-control) and a moonraker component. This repository contains the needed files and an installation script. 

## Hardware setup

This supports WS2812B or SK6812 LED strips connected to a raspberry pi.

Check the section in the [LED Control documentation](https://github.com/jackw01/led-control#hardware-setup) on how to connect the LEDs.

## Installation

This installation is adapted for MainsailOS, FluiddPi or a setup done by KIAUH.
To install, clone the repository and run the installation script:
```
git clone https://github.com/julianschill/moonshine.git
cd moonshine
./install.sh
```

You can specify your klipper configuration directory and the moonraker directory with
```
./install.sh [-c /path/to/configuration_directory] [-m /path/to/moonraker]
```
if it is not in ~/klipper_config and ~/moonraker, respectively

This installs LED Control, adds an init.d script to start it at boot, links the module to moonraker, configures moonraker and adds gcode macros in the file ledcontrol.cfg.

## Configuration

1. Edit the file
```
/etc/default/ledcontrol
```
and change the numbers of LEDs to the number of your setup. 

2. Restart ledcontrol with
```
sudo service ledcontrol restart
```
LED Control should now be accesible with your browser under
```http://<ip_of_the_pi>:8000```

4. Add the following to your printer.cfg and restart klipper:
```
[include ledcontrol.cfg]
```

## Calling the patterns and presets from Klipper

In the file ledcontrol.cfg exists a basic macro called SET_LED_CONTROL, which calls moonraker to set the patterns in LED Control. There are also the ids of the patterns and palettes in the comments.

### Starting a preset

1. Create a preset in the web interface and save it under some meaningful name. 

2. Call the macro to start this preset:

```
SET_LED_CONTROL PRESET="my_own_preset"
```

Change `my_own_preset` to the name you entered in the web interface

### Modify settings directls
You can also change parameters by calling the macro:
```
SET_LEDCONTROL GROUP="main" BRIGHTNESS=0.7 SATURATION=0.5 PATTERN=0 SCALE=0.2 SPEED=0.4 PALETTE=0 GLOBAL_BRIGHTNESS=1.0 GLOBAL_SATURATION=1.0
```

You can set one or multiple parameters at once.

#### Parameters:
  * **GROUP**: The name of the LED group to configure, as named in the web interface (or the id, as defined in `/etc/ledcontrol.json`). If not specified the "main" group is selected.
  * **BRIGHTNESS**: The brightness for the group
  * **SATURATION**: The saturation value for the group
  * **PATTERN**: The pattern id (see [ledcontrol.cfg] for a list of built in ids)
  * **SCALE**: The scale value for the pattern
  * **SPEED**: The speed value for the pattern
  * **PALETTE**: The id of the palette (see [ledcontrol.cfg] for a list of built in ids)
  * **GLOBAL_BRIGHTNESS**: The brightness for all LEDs
  * **GLOBAL_SATURATION**: The saturation for all LEDs

## Creating your own patterns and palettes (advanced)

You can create patterns and palettes over the UI of LED Control by opening ```http://<ip_of_the_pi>:8000``` in your browser. Once you are happy with your settings you can get the ids of the patterns by calling ```http://<ip_of_the_pi>:8000/getfunctions``` and ```http://<ip_of_the_pi>:8000/getpalettes```. This responds with a JSON object containing the data of the configured patterns and palettes. For better readability you can open the file in a JSON formatter tool such as https://jsonformatter.org/. We are looking for the ids of the patterns and palettes, which are the keys of the JSON objects. You can then use those ids additionaly to the provided ones in your klipper macros.

The saved configuration of LED Control, where the IDs can be found and edited can be found in 
```
/etc/ledcontrol.json
```


