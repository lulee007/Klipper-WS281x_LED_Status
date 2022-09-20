# Great project and thanks 11chrisadams11

# Klipper-WS281x_LED_Status
This script will take the printer status from Klipper/Moonraker and apply different effects to a WS281x LED strip.

The code has been migrated from the OctoPrint-WS281x_LED_Status (https://github.com/cp2004/OctoPrint-WS281x_LED_Status) plugin to work with Klipper.

----

## Directions for use

1. Install prerequsits
   1. ```sudo apt update && sudo apt install -y git```
   2. ```sudo pip3 install requests PyYAML RPi.GPIO rpi_ws281x adafruit-circuitpython-neopixel```
2. Clone code to Raspberry Pi running Klipper and Moonraker
   1. ```cd /home/pi```
   2. ```git clone https://github.com/11chrisadams11/Klipper-WS281x_LED_Status.git```
   3. ```cd Klipper-WS281x_LED_Status.git```
3. Make script executable
   1. ```chmod 744 ./klipper_ledstrip.py```
4. Change strip values in settings.conf (LED pin, brightness, timeout)
5. Optionally, change effects and colors for standby, paused, and error states in settings.conf
6. If you want to run it manually, start script before starting print (otherwise use the service below)
   1. ```./klipper_ledstrip.py```

### change 1: core_freq
need add below line in /boot/config.txt with raspberry pi 3b+
`core_freq=250`

### change 2: enable SPI interface for pi
```sh
sudo raspi-config
# Interfaceing Options->P4 SPI->Yes(enable this spi interface)
reboot
```
check spi
```sh
lsmod |grep spi_bcm
# spi_bcm2835 7596 0
```

### change 3: add power section in moonraker.conf
if `shutdown_when_complete` set with `True` then
need `[power printer]` section or will error with get power state
power doc -> https://moonraker.readthedocs.io/en/latest/configuration/#power

```conf
[power printer]
type: homeassistant
address: 192.168.0.1
port: 8123
device: switch.wifi_socket_2
token: ha_token_xxxxxx
domain: switch
```

## Directions to run as a systemd service

1. Copy contents of ledstrip.service to /etc/systemd/system/ledstrip.service
2. Modify User, Group, WorkingDirectory, and ExecStart to match your setup
3. Run ```systemctl daemon-reload``` to enable the service
4. Run ```systemctl enable ledstrip``` to have the service start on boot
5. Run ```systemctl start ledstrip``` to start the service

## Directions to change settings (when using service)

1. Modify settings in settings.conf
2. Run ```systemctl restart ledstrip``` to restart the ledstrip service

### Single run for static colors
#### Will only work by itself, not if running as a service

```
./klipper_ledstrip.py <red> <green> <blue> <brightness:optiona>

Example:
  ./klipper_ledstrip.py 255 255 255 255 ## Full brightness white
  ./klipper_ledstrip.py 255 0 0 ## Red with default brightness specified in the script
```

#### To call from gcode shell commands (thanks to [JV_JV](https://www.reddit.com/user/JV_JV/) for the setup directions)
Add custom entries to printer.cfg 

```
[gcode_shell_command led_off]
command: /home/pi/Klipper-WS281x_LED_Status/klipper_ledstrip.py 0 0 0
timeout: 2.
verbose: True

[gcode_shell_command led_white]
command: /home/pi/Klipper-WS281x_LED_Status/klipper_ledstrip.py 255 255 255
timeout: 2.
verbose: True

[gcode_shell_command led_purple]
command: /home/pi/Klipper-WS281x_LED_Status/klipper_ledstrip.py 255 0 255
timeout: 2.
verbose: True

[gcode_macro LED_OFF]
gcode:
    RUN_SHELL_COMMAND CMD=led_off

[gcode_macro LED_WHITE]
gcode:
    RUN_SHELL_COMMAND CMD=led_white

[gcode_macro LED_PURPLE]
gcode:
    RUN_SHELL_COMMAND CMD=led_purple
```

----

rpi_ws281x library instructions for needed changes depending on GPIO pin used: https://github.com/jgarff/rpi_ws281x
