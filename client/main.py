from joystick import Joystick
import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 6666        # The port used by the server

js1 = Joystick("/dev/input/js2")
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(str.encode(jsonDeviceData + "|"))
    
    print(jsonDeviceData)
    
    
    while True:
        comand = js1.readDevice()
        if comand is not None:
            print(str.encode(json.dumps(comand) + "|"))
            s.sendall(str.encode(json.dumps(comand) + "|")) 
        #axis = js1.readAxis()
        #if axis is not None:
        #    print(json.dumps(axis) + "|")
        #    s.sendall(str.encode(json.dumps(axis) + "|"))
        
