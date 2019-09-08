#!/usr/bin/python

import pigpio
import time
import urllib2

pi = pigpio.pi()
pi.set_mode(27, pigpio.OUTPUT)

commands = ["still", "still"]


movement = 5

ip = "192.168.43.247"
port = "5000"



while True:
    commands = urllib2.urlopen("http://" + ip + ":" + port).read().split()
    print commands
    
    if commands[0] == "RIGHT" and pi.get_servo_pulsewidth(27) < 2400:
        pi.set_mode(27, pigpio.OUTPUT)
        pi.set_servo_pulsewidth(27, pi.get_servo_pulsewidth(27) + movement)
    elif commands[0] == "LEFT" and pi.get_servo_pulsewidth(27) > 600:
        pi.set_mode(27, pigpio.OUTPUT)
        pi.set_servo_pulsewidth(27, pi.get_servo_pulsewidth(27) - movement)

    time.sleep(0.015)

    """
    pi.set_mode(17, pigpio.OUTPUT)
    if commands[1] == "UP":
        pi.set_servo_pulsewidth(17, pi.get_servo_pulsewidth(17) + movement)
    elif commands[1] == "DOWN":
        pi.set_servo_pulsewidth(17, pi.get_servo_pulsewidth(17) - movement)

    time.sleep(0.035)
    """
pi.stop()
