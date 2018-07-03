# pc_gamepad_transmission.py
# Created: 2017.12.03
# Uvindu Wijesinghe, Varun Chhabra, and Oliver Wilkins
#
# Note: Some code adapted from Project Intelligent Car & RCAutopilot
#
# Description:
# A program to receive gamepad input and send it over a UDP socket
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
import sys


axis_steer = 0
axis_throttle = 2
axis_sampler = 3 #find axis

forwards_moved = 0
reverse_moved = 0
reverse_engaged = 0
throttle = "090"

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
 

ip_address = "192.168.0.102" # Address of RPi 
port = 8001 #port value must be the same on both scripts

size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.init()
pygame.joystick.init()
j_count = pygame.joystick.get_count()

gamepad = pygame.joystick.Joystick(0)
gamepad.init()

while True:
    pygame.event.pump()
    
    steer_angle = str(int(round(gamepad.get_axis(axis_steer)*90 + 90, 0))).zfill(3)
    sampler_value = str(int(round(gamepad.get_axis(axis_sampler)*90 + 90, 0))).zfill(3) 
    """
    if gamepad.get_axis(axis_throttle) < 0:
        forwards_moved = 1

    if gamepad.get_axis(axis_throttle) > 0:
        reverse_moved = 1

    if forwards_moved == 1:
        throttle = str(90 - int(round(gamepad.get_axis(axis_throttle)*45 + 45, 0))).zfill(3)

    if reverse_moved == 1 and gamepad.get_axis(axis_throttle) != -1:
        throttle = str(90 + int(round(gamepad.get_axis(axis_throttle)*45 + 45, 0))).zfill(3)
    """
    throttle = str(90+int(round(gamepad.get_axis(axis_throttle)*90,0))).zfill(3)
    transmission_string = throttle + steer_angle + sampler_value

    print(transmission_string)
    
    
    s.sendto(transmission_string.encode(), (ip_address, port))
    sleep(0.1)
    
