"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import serial
from pythonosc import dispatcher
from pythonosc import osc_server, udp_client

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_rotate_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_button_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def send_back(inData):
      client_iphone.send_message("/1/rotary1", inData)
      client_local.send_message("/1/rotary1", inData)
      print("sent message {0}".format(inData))


def servo_call(unused_addr, args, volume):                         # read incomming data from touchOSC
  
    path = unused_addr.split("/")[2]
    print("[{0}] ~ {1} ~ {2}".format(args[0], path, volume))    
    if path == "rotary1":                                             # if control is push button on the phone
        inData = volume                                            # set value, 0 = 0 degrees, 1 = 180 degrees
        send_back(inData)                             # from the phone
    if path == "push1":                                             # if control is push button on the phone
        inData = 0.0                                              # set value, 0 = 0 degrees, 1 = 180 degrees
        send_back(inData)
    if path == "push2":
        inData = 0.25
        send_back(inData)
    if path == "push3":
        inData = 0.5
        send_back(inData)
    if path == "push4":
        inData = 0.75
        send_back(inData)
    if path == "push5":
        inData = 1.0
        send_back(inData)

    pos = int(180 * inData)                                     # map 0..1 -> 0..180 degrees
    servo_msg = chr(pos)                                        # convert integer -> ascii = chr(num)
    #print "%s => %.2f  %s" % (path, inData, str(pos))           # other way around:  ascii -> integer = ord(num)
    #myLabel = 'angle: ' + str(pos)                              # update the text label for the virtual environment
    data.write(servo_msg.encode())                                       #send the angle to the Arduino through serial port


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.1.237", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()
  serialPort = '/dev/cu.Bluetooth-Incoming-Port'
  data = serial.Serial(serialPort, 9600, timeout=1)               # data send to Arduino via serial port (UBS connetion)


  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/filter", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
  dispatcher.map("/1/rotary1",servo_call, "Rotary")
  dispatcher.map("/1/push1",servo_call, "PushButton 0")
  dispatcher.map("/1/push2",servo_call, "PushButton 45")
  dispatcher.map("/1/push3",servo_call, "PushButton 90")
  dispatcher.map("/1/push4",servo_call, "PushButton 135")
  dispatcher.map("/1/push5",servo_call, "PushButton 180")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  client_iphone = udp_client.SimpleUDPClient("192.168.1.25", 9000) #send back
  client_local = udp_client.SimpleUDPClient("192.168.1.237", 9000) #send back
  
  server.serve_forever()