
# import RPi.GPIO as GPIO
# from time import sleep



# class RelayService:
#     def __init__(self, pin=17):
#         self.pin = pin
#         self.state = False

#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.pin, GPIO.OUT)

#         self.turn_off()

#     def turn_off(self):
#         GPIO.output(self.pin, GPIO.LOW)
#         self.state = False
#         print("Relay OFF")
        
#     def turn_on(self):
#         GPIO.output(self.pin, GPIO.HIGH)
#         self.state = True
#         print("Relay ON")

#     def set_manual(self, state: bool):
#         if state:
#             self.turn_on()
#         else:
#             self.turn_off()

#     def cleanup(self):
#         GPIO.cleanup()
        
        
# relay = RelayService()


# while True:
#     relay.turn_on()
#     sleep(1)
#     relay.turn_off()
#     sleep(1)


# import RPi.GPIO as GPIO
# from time import sleep

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)

# GPIO.output(17, GPIO.HIGH)
# print("Set HIGH")
# sleep(5)

# GPIO.output(17, GPIO.LOW)
# print("Set LOW")
# sleep(5)

# GPIO.cleanup()


import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

RELAY = 17

GPIO.setup(RELAY, GPIO.OUT, initial=GPIO.HIGH)

loop = 0

while True:
    
    if loop == 2:
        print("Break")
        break
    
    print("ON")
    GPIO.output(RELAY, GPIO.LOW)   # active LOW
    sleep(1)

    print("OFF")
    GPIO.output(RELAY, GPIO.HIGH)
    sleep(1)
    
    # loop += 1

GPIO.cleanup()