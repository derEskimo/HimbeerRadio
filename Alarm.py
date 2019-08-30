# -*- coding: utf-8 -*-
import I2C_LCD_driver
import mpc_library
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mylcd=I2C_LCD_driver.lcd()
alarmtimeh=07
alarmtimem=00
modus=["Aus  ","Radio","SD   "]
modusnr=0
pos=1


def up():
    global pos
    global alarmtimeh
    global alarmtimem
    global modusnr

    if pos==1:
        if alarmtimeh<23:
            alarmtimeh=alarmtimeh+1
        else:
            alarmtimeh=0
            
    if pos==2:
        if alarmtimem<59:
            alarmtimem=alarmtimem+1
        else:
            alarmtimem=0

    if pos==3:
        if modusnr<2:
            modusnr=modusnr+1
        else:
            modusnr=0
    time.sleep(0.2)
    
def down():
    global pos
    global alarmtimeh
    global alarmtimem
    global modusnr

    if pos==1:
        if alarmtimeh>0:
            alarmtimeh=alarmtimeh-1
        else:
            alarmtimeh=23
            
    if pos==2:
        if alarmtimem>0:
            alarmtimem=alarmtimem-1
        else:
            alarmtimem=59
            
    if pos==3:
        if modusnr>0:
            modusnr=modusnr-1
        else:
            modusnr=2
    time.sleep(0.2)


def set_prev(channel):
    global pos

    if pos>1:
        pos=pos-1
    else:
        pos=3
    print(pos)

def set_next(channel):
    global pos

    if pos<3:
        pos=pos+1
    else:
        pos=1
    print(pos)



    
def set_cursor(pos):
    if pos==1:
        mylcd.lcd_display_string(chr(2),4,1)
        mylcd.lcd_display_string(chr(2),4,2)
        time.sleep(0.3)
        mylcd.lcd_display_string(chr(32),4,1)
        mylcd.lcd_display_string(chr(32),4,2)
    if pos==2:
        mylcd.lcd_display_string(chr(2),4,4)
        mylcd.lcd_display_string(chr(2),4,5)
        time.sleep(0.3)
        mylcd.lcd_display_string(chr(32),4,4)
        mylcd.lcd_display_string(chr(32),4,5)
    if pos==3:
        mylcd.lcd_display_string(chr(60),3,12)
        mylcd.lcd_display_string(chr(62),3,18)
        time.sleep(0.3)
        mylcd.lcd_display_string(chr(32),3,12)
        mylcd.lcd_display_string(chr(32),3,18)
    

def get_alarm_time():
    return(str(alarmtimeh).zfill(2)+":"+str(alarmtimem).zfill(2),modusnr)

    
    
    
def run(stop_event, arg):
    global pos
    
    mylcd.lcd_clear()
    GPIO.add_event_detect(4,GPIO.FALLING, callback=set_prev, bouncetime=500)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=set_next, bouncetime=500)


    mylcd.lcd_display_string("Wecker einstellen:",1,1)
    
    
    while not stop_event.wait(0):
        set_cursor(pos)
        mylcd.lcd_display_string(str(alarmtimeh).zfill(2)+":"+str(alarmtimem).zfill(2) + "       "+modus[modusnr], 3, 1)
        time.sleep(0.3)

    pos=1  
    GPIO.remove_event_detect(4)
    GPIO.remove_event_detect(17)
