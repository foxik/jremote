JREMOTE is a python program to send joystick/gamepad input over a network connection between two Linux machines.

It consists of two programs:

The client:

It reads inputs from a connected joystick/gamepad and send them over the network to the server.

Usage:

python client/main.py -a [ip address of server] -p [port of server] -d [path to physical joystick/gamepad device e.g: /dev/input/js0]

The server

It listens for an incomming connection and creates a virtual joystick with the same number of buttons and axes of the device attached to the client. 
Then it can receive inputs from the client and will act as a pysically connected joystick/gamepad.

python server/main.py -p [port to listen for connection]
