if writing custom node, I need to write custom javascript
this maybe implies I should not use python or pysunspec2
i think I did so much work to get pysunspec2 working, it would be a waste to not use
additinally, I could potentially get the json endpoint to work...
maybe I just need to go test the json stuff in person first
that is probably the right step

if we need to keep with modbus, then we should use pysunspec2
the easiest way to get this date into nodered I think is a publish as mqtt
a custom configuration node could be added?
i wonder if there is an easier way to install apps to the raspberry pi
mqtt can also be published to adafruit easily

oh, one other problem is that we were not batching writes to the database
a custom tristar flow could get values every 5 seconds
show them on the dashboard of course immediately
but then batch write to database

a backup raspberry pi would be cool
mini RAID config

for this mqtt bridge, there are some configuration options
1. device config
2. scan and return points to record
3. configure/save points to record

I'd like to be able to support option 2 for my dad.
