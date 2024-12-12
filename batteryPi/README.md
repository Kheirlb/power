# BatteryPi
BatteryPi is the Raspberry Pi installed in the Power Room to read in the actual battery voltage at a higher resolution than the MATE3S reports.

## Software
Reading in the data will be handled by the scripts in this folder. The service will then send the data via MQTT to the "PowerPi" installed at the house.

mosquitto broker is installed on the PowerPi, and the little config file has 2 lines to allow batterPi to connect.

```
sudo nano /etc/mosquitto/mosquitto.conf
```

```
listener 1883
allow_anonymous true
```

NodeRed is also now installed on PowerPi with a very basic flow to subscribe to the MQTT data and push to influxdb.

## Hardware
The hardware link is:
1. battery
2. voltage divider
3. ads1115
4. rasbperry pi via i2c
5. ethernet to powerPi

More documentation is required. I need to add some photos/graphics. At some point, we need to rename this stuff too since I'm already confused between PowerPi and BatteryPi.
