"""Main power room service."""
import time
import datetime
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import config
import mate3s_sunspec
# import solar_charge_controllers

# Setup database client.
# Token is set in ~/.bashrc file on raspberry pi. 
token = os.environ.get("INFLUXDB_TOKEN")
org = "Parks Ranch"
url = f"http://{config.hostname}:8086"
bucket="power"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Setup inverter connection.
inverters = mate3s_sunspec.connect()

# Setup solar charge controller connection.
# controllers = solar_charge_controllers.connect()

while True:
    print(datetime.datetime.now())

    try:
        points = []
        # Get data from inverters.
        points.extend(mate3s_sunspec.get_points(inverters))

        # Get data from solar charge controllers.
        # points.extend(solar_charge_controllers.get_points(*controllers))

        # Write data to database.
        write_api.write(bucket=bucket, org=org, record=points)

    except Exception as e:
        print(e)
        # TODO(kparks) Restart all connections?

    # Do a sleep loop.
    time.sleep(config.delay_s)
