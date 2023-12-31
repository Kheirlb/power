# power
Smart off-grid power control.

# System Overview
Disclaimer: This repo has a lot of specific content for our custom home project, and would need to be adapted heavily for others to use. Maybe someday I will make it auto-configure, but until that day, good luck making it work for you.

Relevant hardware:
- 6 tristar solar charge controllers
- 1 mate3s connected to 3 outback radian inverters
- 1 16-port unmanaged switch
- 1 raspberry pi 4 with a touchscreen, power supply, and large sd card
- 1 router / access point
- cat5 ethernet

In our setup, the mate3s and the solar charge controllers are connected to an unmanaged 16-port network switch. That switch then runs an ethernet line to the house. The other end of the ethernet line is connected to a router in the house. The raspberry pi is expected to be wired into the ethernet switch, and the raspberry pi connected to a mobile hotspot via WiFi for internet connectivty.

TODO: insert diagram

This repo is all about setting up a raspberry pi for monitoring and automation.

# Setup
The raspberry pi setup is a little cumbersome right now. I could potentially put some of this in an installation script, but I am not sure how to do some of the steps automagically. So we are going to do it almost all manually. Step-by-step. Sorry in advance.

## 64-bit raspbian
Install 64-bit raspbian onto a 128GiB sd card. We are using a large sd card here so we can have a bunch of storage space for data. The "64-bit" is required for influxdb software.
- Set the user to be "pi". Choose a password.
- Set the hostname to "power".
- Enable ssh access.
- Ideally have it connect to a wifi network with internet access.

## Networking
We need to get the raspberry pi on the network with all the power room hardware.

### Router Setup
The python scripts we will install later all expect each device to have a very specific ip address:

- 192.168.1.100 mate3s
- 192.168.1.101 sc1 (sc1 == solar charge controller #1)
- 192.168.1.102 sc2
- 192.168.1.103 sc3
- 192.168.1.104 sc4
- 192.168.1.105 sc5
- 192.168.1.106 sc6

Note, it is also expected that the raspberry pi is:
- 192.168.1.109 over Ethernet
- 192.168.1.108 over WiFi (not used anymore)

The first step would be to connect up all your hardware as described in the overview section. Connect a laptop to your router, and navigate to its admin page, typically at http://192.168.1.1. The default credentials are usually username:admin/password:admin. Add a "DHCP reservation" for all of the required devices at the ip addresses listed above. This reservation will map a devices MAC address to a specific ip address that won't change. Assuming all your devices are powered and talking, you should be able to add reservations for the mate3s, and the solar charge controllers, and the raspberry pi for ethernet.

### Raspberry Pi Network Setup
You can skip this step if then router has an internet connection.

The one important networking thing we need to setup on the raspberry pi relates to WiFi, Ethernet, and the _internet_. We struggle to have internet where we live. Since our router doesn't have WAN port connected to internet, in order for the raspberry pi to get internet (in order for it to keep track of time and install software and stuff), it needs to be over WiFi on a mobile hotspot. This makes things a little complicated because as soon as we plug in the raspberry pi over ethernet into the router, all internet traffic starts to try to go through ethernet (the "faster" wired connection), even if the raspberry pi is connected to that mobile hotspot. The way to avoid this issue is to set a static ip address for the ethernet connection _without_ a gateway. On the raspberry pi, click the ethernet connection icon, go to more/advanced settings, edit "Ethernet connection 1", and change the ipv4 address from automatic to manual. Then add a manual entry at `192.168.1.109`, a netmask of `24`, and leave the gateway EMPTY. This should ensure internet traffic goes through the mobile hotspot in the future.

### Modbus TCP Port
The mate3s and solar charge controllers can communicate over Modbus TCP. By default, Modbus TCP devices use port `502`. On linux however, ports `<1024` are reserved for the operating system. Because of this linux limitation, I was unable to get the python scripts running on the raspberry pi communicating over the modbus port `502`. Forunately, it is relatively easy to change the port. I decided to change it to `1025`, 1 over the limit.

For the mate3s, I following the documentation and used the built-in interface to change the number. It required around 3-4 minutes of spinning my finger around the silly little dial. This can also probably be updated by exporting a config xml file to the sd card, changing the value on a personal laptop, and then importing the updated file. The 3-4 minutes of spinning ended up not being too bad.

For the tristar solar charge controllers, there is not a built-in interface. But, since we have the charge controllers on the network, I was able to connect over Ethernet easy enough with a personal laptop using the tristart MSView software. In order to update the settings over Ethernet, dip switch 8 needs to be switched up while the charge cotrollers are powered off. I used MSView to change the port number from `502` to `1025` for every controller, and then rebooted the controllers one more time to apply the change. It took a moment because you need to click through a bunch of screens, but it was easy enough.

## Install Software
Time to install all the software onto the raspberry pi. Hopefully you have it connected to a fast internet connection. I recommend doing this over SSH if you can. If not, plug a USB keyboard/mouse and do it with the raspberry pi directly with the pi connected to an external monitor over HDMI.

### InfluxDB
InfluxDB is a popular open-source (I think) "time-series database" where we will record all our data.

Once the raspberry pi is up and running, install influxdb following the instructions here. TODO: Copy the instructions here. Go to the webpage and create a login with username "admin" and your desired password. Save the token that is generated to a file (important for grafana and python later).

### Grafana
Grafana is a popular open-source "Graphical Dashboard" tool that easily connects to InfluxDB.

Install grafana to the raspberry pi following the instructions here. TODO: Copy the instructions here. Go to the webpage and create a login with username "admin" and your desired password. Connect grafana to influx as a data source. You will need to copy that token here.

Create a new dashboard and import the .json file from this script. This will automatically configure your dashboard. You won't have any data tough until we do the following steps.

### Clone power
Clone our git repo "power" into a GitHub folder in ~/. This repo (where you are reading this README) has our custom python scripts.
```
mkdir GitHub
cd GitHub/
git clone https://github.com/Kheirlb/power.git
cd power/
```

### Install Python Packages
We need to install influxdb-client, pymodbus, and pysunspec2.

The latest version of raspbian really tries to avoid letting you change system python packges.
Ideally we would be doing this all in docker, but because of bad internet at the ranch, it was
too much to download the initial docker deps. We could also do things in a virtual environment,
but I am less familiar with how to do that outside of development. Moral of the story,
we are just going to intentially `--break-system-packages` and hope for the best.
```
python3 -m pip install -r requirements.txt --break-system-packages
```

Because we needed to hack pysunspec2 to get it to work, we need to install this hacked python package separately. For whatever reason, the submodule I put in this fork will not work on the raspberry pi. So we need to hack around my hack for now.
```
git clone https://github.com/Kheirlb/pysunspec2-fork.git
cd pysunspec2-fork/sunspec2
rm -r models
git clone https://github.com/Kheirlb/models-fork.git models
cd ../..
python3 -m pip install -e pysunspec2-fork/ --break-system-packages
```

TODO: Fix the submodule thing.
TODO: get sunspec to update main repo so we don't need to have the above part at all.

### Configure Power Service
We will be using a linux systemd file to auto-start our python script on boot and on-failure.

We need use that influx token we saved awhile back in the python script. The script `service.py` pulls that token from an environmental variable `INFLUXDB_TOKEN`. We can pass that environment variable using the `power.service` file. Add a new line `Environment="INFLUXDB_TOKEN=<TOKEN HERE>"` under `User=pi`, and change `<TOKEN_HERE>` to be your token.

### Start the Power Service
Copy the service file to systemd's desired location. You will need root access. Then start the service.
```
sudo cp power.service /etc/systemd/service/
sudo systemctl daemon-reload
sudo systemctl start power.service
```

Check the status to confirm it is running.
```
systemctl status power.service
```

Or use the following to follow the logs.
```
journalctl -efu power.service
```

Note, the script won't work unless the raspberry pi is connected to a network that can talk to all the required devices.

TODO: Maybe I can add a little config hack to stub with fake data easily.

# Dashboard Time
You can now go look at your dashboard and see your amazing data.

Grafana runs on port 3000 by default. We just need the ip address.

On the raspberry pi, connecting is easy. Open the web browser and type http://localhost:3000 to get to grafana. Use F11 to make it full screen.

If you want to see the dashboard on your personal laptop, you need to be on the same network as the raspberry pi. If the pi is connected to the same mobile hotspot as your laptop, you can use mDNS and the hostname easily by just typing http://power.local:3000.

If your personal laptop is connected to our old school router, mDNS does not work, so you will need to type the ipv4 address of the raspberry pi. Over ethernet that would be http://192.168.1.109:3000.

Navigate to your new dashboard and viola.

Note, if you did not import the .json file in the initial grafana setup, you will need to manually configure your dashboard now. This is quite a cumbersome process... so good luck.

Otherwise, we are all setup for now!
