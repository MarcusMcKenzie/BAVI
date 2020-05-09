"""
Lidar.py is responsible for reading data from the lidar.
It relies upon linux system calls. The first call sets the lidar to
return int mm readings. It should only be necessary once per boot, but more
calls won't be harmful. The second call starts a serial listen w/ the lidar.
"""

"""
TODO: implement these calls
1)
echo -en '\x00\x11\x01\x45' > /dev/ttyACM0; # set up int mode
2) *maybe don't need sudo?
sudo screen /dev/ttyACM0 -U --parity=no --word=8 --stop=1 115200; # initialize serial connection
"""