import os
from time import sleep
import RPi.GPIO as GPIO
import sys
from pubnub.callbacks import SubscribeCallback
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNOperationType, PNStatusCategory


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
#pin set up for buzzer
GPIO.setup(13,GPIO.OUT)
#pin set up for servo
GPIO.setup(11,GPIO.OUT)
#pin set up for pir sensor
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.IN)

pnconfig = PNConfiguration() 
pnconfig.subscribe_key = 'sub-c-3d83ece2-8993-11e7-9a51-32b88659ac4c'
pnconfig.publish_key = 'pub-c-be3a81ea-fbf2-43cd-96a8-c919cc4a4dff' 
pubnub = PubNub(pnconfig)
channel = 'disco'

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
    
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def message(self, pubnub, message):
        main()


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('disco').execute()




def main():
    buzzer()
    dog_arrived = sensor()
    while(dog_arrived == 0):
          print('dog is not here')
          dog_arrived = sensor()
    servo()
        
#define a function for PIR Sensor
def sensor():
     i=GPIO.input(15)
     return i

#define a function for controlling servo
def servo():
    #pin set up for servo 
    GPIO.setup(11, GPIO.OUT)
    pwm = GPIO.PWM(11, 50)
    left_position = 0.40
    right_position = 2.5
    middle_position = (right_position - left_position) / 2 + left_position
    positionList = [left_position, right_position, left_position]
    ms_per_cycle = 1000 / 50
    for i in range(1):
	# This sequence contains positions from left to right
	# and then back again.  Move the motor to each position in order.
	for position in positionList:
		duty_cycle_percentage = position * 100 / ms_per_cycle
		print("Position: " + str(position))
		print("Duty Cycle: " + str(duty_cycle_percentage))
		print("")
		pwm.start(duty_cycle_percentage)
		sleep(.5)
    pwm.stop()

# define a function for buzzer
def buzzer ():

    #Dash Dash Dash
    GPIO.output(13,GPIO.LOW)
    sleep(.2)
    GPIO.output(13,GPIO.HIGH)
    sleep(.2)
    GPIO.output(13,GPIO.LOW)
    sleep(.2)
    GPIO.output(13,GPIO.HIGH)
    sleep(.2)
    GPIO.output(13,GPIO.LOW)
    sleep(.2)
    GPIO.output(13,GPIO.HIGH)
    sleep(.2)
    GPIO.output(13,GPIO.LOW)
    sleep(.2)

