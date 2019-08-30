# -*- coding: utf-8 -*-
import I2C_LCD_driver
import mpc_library
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)                            #set up BCM GPIO numbering
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #NEXT-BUTTON an 3,3V und GPIO4
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #PREV-BUTTON an 3,3V und GPIO17
#--------------------------------------------------------------------------------
mylcd=I2C_LCD_driver.lcd()
mpc=mpc_library

i=0

def next_song(channel):
    global i

    print("Button next Pressed")
    mpc.next()
    i=0

def prev_song(channel):
    global i

    print("Button prev Pressed")
    mpc.prev()
    i=0

def update_lcd():
    global mylcd
    global i
    info=mpc.music_info()
    mylcd.lcd_display_string("SD-Karte     "+time.strftime("%H:%M"), 1, 1)

    mylcd.lcd_display_string(info[1],2,0)

    percentage=int(round(int(info[2])/5)*5)/5
    if percentage>=1:
        mylcd.lcd_display_string(chr(255),3,-1+percentage)
    if percentage==0:
        mylcd.lcd_display_string(chr(6)+18*chr(4)+chr(5),3)
        
        
    #LCD Laufschrift für title
    title=(info[0])
    if i<=20+len(title):
            text=20*" "+title+20*" "
            text=text[0+i:20+i]
            mylcd.lcd_display_string(text,4)
            i=i+1
    else:
            i=0
    
def run(stop_event, arg):
    mylcd.lcd_clear()
    GPIO.add_event_detect(4,GPIO.RISING, callback=prev_song, bouncetime=500)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=next_song, bouncetime=500)

    mpc.load_music_playlist()
    mpc.play(1)
    next_song(0)
            
    while not stop_event.wait(0):
        update_lcd()
        print("SD-Karte läuft")

    mpc.stop()
    
    GPIO.remove_event_detect(4)
    GPIO.remove_event_detect(17)
