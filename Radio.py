# -*- coding: utf-8 -*-
import I2C_LCD_driver
import time
import os
import RPi.GPIO as GPIO
import mpc_library

GPIO.setmode(GPIO.BCM)                              #set up BCM GPIO numbering
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #NEXT-BUTTON an Gnd und GPIO4
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #PREV-BUTTON an Gnd und GPIO17
########################################################################################

i=0                     #Counter fuer Laufschrift
mylcd = I2C_LCD_driver.lcd()
mpc = mpc_library
rememberSender=1

def next_station(channel):
    global i
    global rememberSender
    print("Button next Pressed")
    mpc.next()
    i=0
    if rememberSender<16:  #16=Anzahl Radiosender in Playlist...
        rememberSender=rememberSender+1
    else: rememberSender=1
    
    
def prev_station(channel):
    global i
    global rememberSender
    print("Button prev Pressed")
    mpc.prev()
    i=0
    if rememberSender>1:
        rememberSender=rememberSender-1
    else: rememberSender=16

def update_lcd():
        global mylcd
        global i
        mylcd.lcd_display_string("Now Playing:", 2, 4)
    
        mylcd.lcd_display_string("WebRadio     "+time.strftime("%H:%M"), 1, 1)
            
        #radioinfo abfragen
        radioinfo = mpc.sender_info()

        print(radioinfo[0])
        print(radioinfo[1])
        print(" ")

        
        mylcd.lcd_display_string((((20-len(radioinfo[0]))/2)*" "+radioinfo[0]+20*" ")[:20], 3)

        #LCD Laufschrift für title
        title=(radioinfo[1])
        if i<=20+len(title):
            text=20*" "+title+20*" "
            text=text[0+i:20+i]
            mylcd.lcd_display_string(text,4)
            i=i+1
        else:
            i=0





def run(stop_event, arg):
    mylcd.lcd_clear()
    
    GPIO.add_event_detect(4,GPIO.RISING, callback=prev_station, bouncetime=500)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=next_station, bouncetime=500)

    mpc.load_radio_playlist()
    mpc.play(rememberSender)

    while not stop_event.wait(0):
        update_lcd()
        print("Radio läuft")

    mpc.stop()
    print("RememberSender: "+str(rememberSender))
    GPIO.remove_event_detect(4)
    GPIO.remove_event_detect(17)



