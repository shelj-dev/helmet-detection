import RPi.GPIO as GPIO
import threading
import time


ON_DELAY = 5
OFF_DELAY = 15 # minimum 6
BUZZER_DELAY = 8

class RelayService:
    def __init__(self, pin=17, buzzer=27):
        self.pin = pin
        self.buzzer = buzzer
        self.on_counter = 0
        self.off_counter = 0
        self.status = "OFF"

        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.buzzer, GPIO.OUT)
        GPIO.setup(self.pin, GPIO.OUT)

        GPIO.output(self.pin, GPIO.LOW)

        print("Relay initialized")
        
    def turn_on(self):
        if self.on_counter >= ON_DELAY:
            self.status = "ON"
            
            GPIO.output(self.pin, GPIO.HIGH)
            
            print("Turned ON")
        
        else:
            print("ON Counter", self.on_counter)
            self.on_counter += 1
            self.off_counter = 0
            self.buzzer_off()


    def turn_off(self):
        if self.off_counter >= OFF_DELAY:
            self.status = "OFF"
            
            GPIO.output(self.pin, GPIO.LOW)
            
            print("Turned OFF")
            self.buzzer_off()
            
        else:
            self.buzzer_off()

            if self.off_counter > OFF_DELAY - 6:
                self.buzzer_on()
                
            print("OFF Counter", self.off_counter)
            self.off_counter += 1
            self.on_counter = 0
            
            
    def buzzer_on(self):
        if self.status == "ON":
            GPIO.output(self.buzzer, GPIO.HIGH)
            print("Buzzer ON")
        

    def buzzer_off(self):
        # if self.status != "OFF":
            # GPIO.output(self.buzzer, GPIO.LOW)
            # print("Buzzer OFF")
        GPIO.output(self.buzzer, GPIO.LOW)
        print("Buzzer OFF")
        

    def cleanup(self):
        GPIO.cleanup()
        