# pc_gamepad_transmission.py
# Created: 2017.12.03
# Uvindu Wijesinghe and Oliver Wilkins
#
# Note: Code adapted from Project Intelligent Car & RCAutopilot
#
# Description:
# A program to receive gamepad input and send it over a TCP socket
# to a Raspberry Pi
#
# Usage:
# Ensure gamepad is connected to computer and configured.
# Run script. When prompted, run the Raspberry Pi client script.
# When you provide input on the gamepad, a scaled input value will
# be sent to the Raspberry Pi.

import pygame
from time import sleep
import socket

# Setup socket

# Client can connect through any network interface to port 8000
host = "0.0.0.0"
port = 8000

# Set up command server and wait for a connect
print 'Waiting for Raspberry Pi Command Client'
command_server_soc = socket.socket()  # Create a socket object
command_server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
command_server_soc.bind((host, port))  # Bind to the port

command_server_soc.listen(0)  # Wait for client connection
# Wait for client to connect
command_client, addr = command_server_soc.accept()
print "Raspberry Pi Connected! IP Address: "


# Initialise PyGame for controller input
pygame.init()
pygame.joystick.init()
j_count = pygame.joystick.get_count()

# Set the gamepad to be the first joystick found
gamepad = pygame.joystick.Joystick(0)
gamepad.init()

# Loop to retrieve gamepad state and send it to Rpi
while True:
    # Update gamepad state
    pygame.event.pump()

    # Get value from one of the gamepad axes
    zero_axis_pos = gamepad.get_axis(0)

    # Extract direction the stick was pushed
    if zero_axis_pos >= 0:
        # right-side
        direction = 0
    else:
        # left-side
        direction = 1

        # Convert value to a positive
        zero_axis_pos *= -1

    # Scale value to 100 and make sure it is a whole number
    scaled_input = int(100 * zero_axis_pos)

    # create 4 character string with first character indicating direction
    transmission_string = str(direction) + str(scaled_input).zfill(3)

    # Transmit the data to the Rpi
    command_client.send(transmission_string)

    # Print the values
    print "Raw Value: " + str(zero_axis_pos) + "  Transmitted Value: " + transmission_string
    sleep(0.1)
