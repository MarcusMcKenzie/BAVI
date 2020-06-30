# must validate on hardware
import RPi.GPIO as GPIO 
import time

def some_event(channel): #can have the script enter the draw_weight_event
	#do something here

def button_release(channel): #do something else
	printf("button was released!\n")
	#do something else

def button_push(channel): #button push event
	print("Button was pushed!\n")
	GPIO.output(22,GPIO.input(11)) #button will trigger LED
	time.sleep(0.05) 
	#have it enter draw_weight_script? 

GPIO.setwarnings(False) #temporary warrning 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(22,GPIO.IN) #set up LED to switch, must pull down to ground

GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Button on Pin11(GPIO17)
GPIO.add_event_detect(11, GPIO.RISING, callback = button_push) #Triggered on rising edge to enter button_push
GPIO.add_event_detect(11, GPIO.FALLING, callback = button_release) #on falling edge, enter button_release, given no ground bounce

GPIO.cleanup() #clean up

#old code
# from gpiozero import Button
# from time import sleep

# button = Button()

# while True:
#     if button.is_pressed:
#         print("Pressed")
#     else:
#         print("Released")
#     sleep(1)
