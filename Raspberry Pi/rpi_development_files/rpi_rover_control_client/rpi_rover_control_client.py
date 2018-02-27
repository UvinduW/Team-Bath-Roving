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

import serial
import socket

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
