# -*- coding: utf-8 -*-
import I2C_LCD_driver
import mpc_library
import RPi.GPIO as GPIO
import time

mylcd=I2C_LCD_driver.lcd()

def run(stop_event, arg):
    mylcd.lcd_clear()

    print("Audio-In")
    #Setze Lautstärke auf 60%  ???
    #Schalte Relais an
    
    while not stop_event.wait(0):
        
        mylcd.lcd_display_string("Audio-In     "+time.strftime("%H:%M"), 1, 1)
        time.sleep(1)
        #eventuell Balkenanimation von Verstärker-LEDS als Input
        
    #Schalte Relais aus
