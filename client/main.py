from joystick import Joystick
import socket
import json
import getopt
import sys

short_options = "a:p:d:"
long_options = ["ip=","port=","device="]
argument_list = sys.argv[1:]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)
    
host = '127.0.0.1' 
port = 6666   
device = "/dev/input/js0"

for current_argument, current_value in arguments:
    if current_argument in ("-a", "--ip"):
        host =  current_value
    elif current_argument in ("-p", "--port"):
        port = int(current_value)
    elif current_argument in ("-d", "--device"):
        device = current_value

js1 = Joystick(device)
js1.openDevice();
deviceName = js1.getDeviceName()
num_axes = js1.getNumberAxes()
num_buttons = js1.getNumberButtons()
axis_map = js1.getAxisMap()
button_map = js1.getButtonMap()
axis_mapHex = js1.getAxisMapHex()
button_mapHex = js1.getButtonMapHex()



deviceData = {
 "deviceName": deviceName,
 "num_axes": num_axes,
 "num_buttons" : num_buttons,
 "axis_mapHex" : axis_mapHex,
 "button_mapHex" : button_mapHex
}

jsonDeviceData = json.dumps(deviceData)

        
# Main event loop
lastValue = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(str.encode(jsonDeviceData + "|"))
    
    print(jsonDeviceData)
    
    
    while True:
        comand = js1.readDevice()
        if comand is not None:
            #print(str.encode(json.dumps(comand) + "|"))
            
            if "typ" in comand:
                if comand["typ"] == "axis":     
                    intervalA = [-32767.0, 32767.0];
                    intervalB = [-255, 255];
                    val = int((comand["value"]  - intervalA[0]) * (intervalB[1] - intervalB[0]) / (intervalA[1] - intervalA[0]) + intervalB[0])
                    if(lastValue != val):
                        #print(str.encode(json.dumps(comand)))
                        s.sendall(str.encode(json.dumps(comand) + "|")) 
                        lastValue = val;
                else:
                    s.sendall(str.encode(json.dumps(comand) + "|")) 

        
