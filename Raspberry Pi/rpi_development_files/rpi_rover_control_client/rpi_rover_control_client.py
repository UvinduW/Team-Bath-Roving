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
import RPI.GPIO as GPIO
#Number the RPI IO pins using BOARD
GPIO.setmode(GPIO.BOARD) 
#Set the first pin as an output
GPIO.setup(1,GPIO.OUT)
#Create a PWM instance
p = GPIO.PWM(1,50)

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
    throttle = int(data[0:3])
    steer_angle = int(data[3:6])
    sampler_position = int(data[-3:])
    #scale throttle, steer angle, and sampler position to range [-1,1]
    scaled_sampler_position = (90 - sampler_position)/90 #1 is max clockise, -1 max anticlockwise
    scaled_throttle =  (90 - throttle)/90
    scaled_steer_angle = (steer_angle - 90)/90

	
    left_power = scaled_throttle + scaled_steer_angle
    right_power = scaled_throttle - scaled_steer_angle
	
#Scale left_power and right_power so both stay in range [-1,1]	

    if (left_power >= 1) or (right_power <= -1)
        left_power  *= 1/2
        right_power *= 1/2
	
    TB1.SetMotors(left_power)
    TB2.SetMotors(right_power)

        
    #Sampler Control Code
    #Servo is neutral at 1.5ms, >1.5 Counter-Clockwise, <1.5 Clockwise
   pulse_width = 1.5 - scaled_sampler_position
   duty_cycle = pulse_width * 5 # this is the simplification of D = PW/T * 100 with f=1/T = 50Hz
   sampler.ChangeDutyCycle(duty_cycle)


GPIO.cleanup() #Check if neccessary
