import socket
import uinput 
import ujson as json
import time
import sys
import getopt


short_options = "p:"
long_options = ["port="]
argument_list = sys.argv[1:]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

port = 6666       # Port to listen on (non-privileged ports are > 1023)

for current_argument, current_value in arguments:
    if current_argument in ("-p", "--port"):
        port = int(current_value)

def createDevice(deviceData):
    buttons = deviceData["button_mapHex"]
    axes = deviceData["axis_mapHex"]
    
    arrayUinputButtons = []
    arrayUinputAxes = []
    for button in buttons:
        arrayUinputButtons.append((0x01,button))
        
    for axis in axes:
        arrayUinputAxes.append((0x03,axis) + (-32767, 32767, 0, 0))
    
    events = []
    events = events + arrayUinputButtons
    events = events + arrayUinputAxes
    return uinput.Device(tuple(events))
      

HOST = ''  # Standard loopback interface address (localhost)


device = None
lastDeviceName = ""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, port))
    s.listen()
    while True:
        print("Listening for connection...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            buff = ""
            while True:
                data = conn.recv(70)
                if not data:
                    break
                buff = buff + data.decode()
            
                packets = buff.split("|")
                for packet in packets:
                    #process packet
                    if packet != "":
                        if packet != packets[-1]:
                            parsedData = json.loads(packet)
                            if "deviceName" in parsedData:
                                if parsedData["deviceName"] != lastDeviceName:
                                    print("Device: " + parsedData["deviceName"] + " connected")
                                    device = createDevice(parsedData)
                                    time.sleep(2)
                                    lastDeviceName = parsedData["deviceName"]
                            if "typ" in parsedData:
                                if parsedData["typ"] == "button":
                                    #print("button")
                                    #print(parsedData["index"])
                                    button = (0x01,parsedData["cod"])
                                    device.emit(button,parsedData["value"])
                                else:
                                    axes = (0x03,parsedData["cod"])
                                    device.emit(axes,parsedData["value"])
                        
                        
                buff = packets[-1]
            
