# rpi_rover_control_client.py
# Created: 2017.12.03
# Uvindu Wijesinghe
#
# Note: Code adapted from Project Intelligent Car
#
# Description:
# Receives input from a server computer. The input will be
# provided by a gamepad for rover manoeuvring
#
# Usage:
# When server script is ready for a client, run this script. The
# commands received will be printed on the terminal
# PyGame may not work properly on Windows.
# Script was tested on Ubuntu 16.04 LTS
# Some code adapted from https://www.piborg.org/blog/thunderborg-getting-started
import serial
import socket
import servo # importing servo library for scoop
import ThunderBorg

#Need to set the board address of each Thunderborg separately to addresses e.g. 10 11

# Board #1, address 10, two left motors, Motor1: Front, Motor2: Rear
TB1 = ThunderBorg.ThunderBorg()
TB1.i2cAddress = 10
TB1.Init()
TB1.ResetEpo()
# Board #2, address 11, two right motors, Motor1: Front, Motor2: Rear
TB2 = ThunderBorg.ThunderBorg()
TB2.i2cAddress = 11
TB2.Init()
TB2.ResetEpo()



# Set IP and port.
ip_address = "192.168.0.22"
local_address = "0.0.0.0"
port = 8000

# Create a socket object for control signal transmission.
socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the IP and port to the socket object.
socket_control.bind((local_address, port))

while True:
    # Receive control strings over the socket from the PC.
    data, addr = socket_control.recvfrom(1024)
    
    # Print the messages
    print "Message: ", data
	
	# Use the data to control motors

    #Extract throttle and steer_angle from data
    throttle = int(data[:3])
    steer_angle = int(data[-3:])
    #scale throttle and steer angle to range [-1,1], then multiply both by factor 1/2 to change each range to [-0.5,0.5], respectively.
    scaled_throttle =  (1/2)*(90 - throttle)/90
    scaled_steer_angle = (1/2)*(steer_angle - 90)/90


    left_power = scaled_throttle + scaled_steer_angle
    right_power = scaled_throttle - scaled_steer_angle


    TB1.SetMotors(left_power)
    TB2.SetMotors(right_power)

        



