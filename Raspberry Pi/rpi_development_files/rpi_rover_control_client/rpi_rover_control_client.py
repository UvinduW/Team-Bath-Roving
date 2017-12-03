# rpi_rover_control_client.py
# Created: 2017.12.03
# Uvindu Wijesinghe
#
# Note: Code adapted from RCAutopilot
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

import socket
from time import sleep
import serial

# Initialise everything
# IP Address of server computer & port (change as needed)
host = "192.168.0.22"
port = 8000

print "Connecting to command server"
command_client = socket.socket()  # Create a socket object
command_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_client.connect((host, port))  # Bind to the port
print  "Should be connected to command server"
print ""

while True:
    recvCommand = command_client.recv(1024)
    print recvCommand

    # Add code to scale and send commands to motors below:
