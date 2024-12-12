BatteryPi is the Raspberry Pi installed in the Power Room
and its orginal usage at least is to read in the battery voltage.

Reading in the data will be handled by the scripts in this folder.

It will then send it via MQTT to the "PowerPi" installed at the house.

At some point, we need to rename this stuff haha. I'm already confused.
The PowerPi runs an MQTT broker, and NodeRed will move the MQTT data into influx.

mosquitto broker is installed, and the little config file has 2 lines to allow access.
NodeRed is also installed with a very basic flow to grab data and push to influxdb.

More documentation is required.
