import ipaddress
import sunspec2.modbus.client as client

# Creating the connection.
# A static ip address is set for the AXS unit at 192.168.0.64 using the config file on the SD card.
# Using port 5020 instead of 502 to avoid firewall issues.
d = client.SunSpecModbusClientDeviceTCP(ipaddr="192.168.0.64", ipport=5020)

# Scan for the available models. In my test case, there will only be the 64110 OutBack block since nothing else is connected to the AXS Port.
d.scan()

# One of the values I can extract is the reported tcp ip address value.
ip = d.model_64110[0].TCPIP_address.value
print("ip address read from the AXS port:", ipaddress.ip_address(ip))