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

import socket
import pygame
from time import sleep

# Name the gamepad axes.
axis_steer = 0
axis_forwards = 4
axis_reverse = 5

# Initialise flags and throttle value.
forwards_moved = 0
reverse_moved = 0
reverse_engaged = 0
throttle = "090"

# Set IP and port.
ip_address = "192.168.0.32" # Address of RPi
port = 8000

# Create a socket object (UDP) for message transmission.
socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setup the pygame library
pygame.init()
pygame.joystick.init()
j_count = pygame.joystick.get_count()

# Set the gamepad to be the first one found
gamepad = pygame.joystick.Joystick(1)
gamepad.init()

#Configure the second joystick to control the sampler
sampler = pygame.joystick.Joystick(2)
sampler.init()

while True:
    # Refresh the values from gamepad
    pygame.event.pump()
    
	# The gamepad analog axes and triggers provide a value between -1 and positive 1 depending on how
	#  far they've been pushed or pressed. 0 is the center point for the thumbsticks or
	#  half pressed for the shoulder triggers
	
	# The Scaling used should be changed as required by the motor controller chosen
	
    # Get the steering angle from axis0. Round, scale, and shift it, make it a three-char string.
	# Scaled such that 0: full left; 90: centered; 180: full right
    steer_angle = str(int(round(gamepad.get_axis(axis_steer)*90 + 90, 0))).zfill(3)
    
	# The Xbox triggers can be used for the throttle. With PyGame and the Xbox controller
	#  the trigger reads -1 when fully pressed or 1 when not pressed at all. Due to how 
	#  the library has been implemented, if you haven't pressed the trigger yet, its
	#  default value is 0 - which is the value you would get if it is half pressed.
	#  Some latching logic is used to only take the value of the trigger, once its been
	#  pressed at least once.
	
    # Latch the forwards_moved flag if the forward gamepad axis ever moves from zero.
    if gamepad.get_axis(axis_forwards) != 0:
        forwards_moved = 1

    # Latch the reverse_moved flag if the reverse gamepad axis ever moves from zero.
    if gamepad.get_axis(axis_reverse) != 0:
        reverse_moved = 1

    # Start calculating throttle values once the throttle has been moved once.
	# Scaled such that 0: full speed forwards; 90: no throttle; 180: full speed reverse
    if forwards_moved == 1:
        # Read the forward axis and calculate a throttle value, rounded, scaled, shifted, stringed, extended.
        throttle = str(90 - int(round(gamepad.get_axis(axis_forwards)*45 + 45, 0))).zfill(3)

    # If the reverse trigger is pressed at all, override throttle value with this value.
    if reverse_moved == 1 and gamepad.get_axis(axis_reverse) != -1:
        # Read the reverse axis and calculate a throttle value, rounded, scaled, shifted, stringed, extended.
        throttle = str(90 + int(round(gamepad.get_axis(axis_reverse)*45 + 45, 0))).zfill(3)

    # Create a string to transmit over the socket by concatenating the two values.
    transmission_string = throttle + steer_angle

    # Print and send the string.
    print transmission_string
    socket_control.sendto(transmission_string, (ip_address, port))
    sleep(0.1)
