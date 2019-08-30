# -*- coding: utf-8 -*-
#Web-Radio Player basierend auf mpd/mpc mit 20x4 LCD Display
#Autor Hannes Zakes
#----------------------------------------------------------------------
#Taster1: Vorwärts: GND und GPIO4
#Taster2: Rückwärts/Down: GND und GPIO17
#
#Drehimpulsgeber(DIG)
#DIG-Taster(2Pins): Auswahl: GND und GPIO 27
#DIG-Dreh(3Pins): GPIO5 und GPIO6 und GND(Mitte)
#
#20x4 LCD-Display mit I2C
#GND->GND
#VCC->5V
#SDA->I2C1 SDA (GPIO2)
#SCL->I2C1 SCL (GPIO3)
#
#TouchSensor: Auswahl/StopAlarm: Green:3,3V; Blue:GPIO24; Yellow:Sensor; RED/White:12V
#
#Relais: Schaltet Verstärker Ein/Aus: Purple:5V; Black:GND; Blue:GPIO21
#
#Digitalpoti: Regelt Displayhelligkeit: 
#-----------------------------------------------------------------------
import I2C_LCD_driver
import time
import Radio
import mpc_library
import Clock
import sd_card
import AudioIn
import Alarm
import threading
from rotary_class import RotaryEncoder
import RPi.GPIO as GPIO
#-----------------------------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21,GPIO.OUT)

mpc = mpc_library

menu = True
menu_time=time.time()
functions=["Clock ", "Radio ", "SD-Karte", "AudioIn ", "Wecker"]
class_names=[1, Radio, sd_card, AudioIn, Alarm]
mode=1
sens_limit_clockwise = 2
sens_limit_anticlockwise = 2

pill2kill = threading.Event()
t1 = threading.Thread(target=Radio.run, args=(pill2kill, "task"))


mylcd = I2C_LCD_driver.lcd()
fontdata1 = [
        #chr(0) ü
        [ 0b01010,
          0b00000,
          0b10001,
          0b10001,
          0b10001,
          0b10011,
          0b01101,
          0b00000 ],
        #chr(1) untere Hälfte
        [ 0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b11111,
          0b11111 ],
        #chr(2) obere hälfte
        [ 0b11111,
          0b11111,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000 ],
        #chr(3) Punkt
        [ 0b11100,
          0b11100,
          0b11100,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000],
        #chr(4) Strich oben/unten
        [ 0b11111,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b11111 ],
        #chr(5) Klammer zu
        [ 0b11111,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b11111 ],
        #chr(6) Klammer auf
        [ 0b11111,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b11111 ],
        #chr(7) AlarmGlocke
        [ 0b00000,
          0b00100,
          0b01110,
          0b01110,
          0b01110,
          0b11111,
          0b00100,
          0b00000 ]
        #chr(255) voll ausgefüllt
        #chr(32) leer
]
mylcd.lcd_load_custom_chars(fontdata1)




def drehimpulsgeber(event):
    global menu
    global class_names
    global menu_time
    global sens_limit_clockwise, sens_limit_anticlockwise
    
    dim_lcd(0)
    menu_time=time.time()
    
    if event == RotaryEncoder.BUTTONPRESSED or event==24:
            if menu:
                leave_menue(class_names[mode])
                print("Verlasse Menue zu: "+functions[mode])
                menu=False
            else:
                enter_menue()
                print("Betrete Menue")
                menu=True
    elif menu:
        if event == RotaryEncoder.CLOCKWISE:
            sens_limit_clockwise=sens_limit_clockwise+1
            if sens_limit_clockwise > 2:
                print("Nächster Menüpunkt")
                sens_limit_clockwise = 0
                menue_next()
                
        elif event == RotaryEncoder.ANTICLOCKWISE:
            sens_limit_anticlockwise=sens_limit_anticlockwise+1
            if sens_limit_anticlockwise >2:
                sens_limit_anticlockwise =0
                print("Vorheriger Menüpunkt")
                menue_prev()
            

    else:
        if mode == 4:
            if event == RotaryEncoder.CLOCKWISE:
                Alarm.up()
                print("TimeUp")
            elif event == RotaryEncoder.ANTICLOCKWISE:
                Alarm.down()
                print("TimeDown")
        else:
            if event == RotaryEncoder.CLOCKWISE:
                mpc_library.vol_up()
                print("Lauter")
            elif event == RotaryEncoder.ANTICLOCKWISE:
                mpc_library.vol_down()
                print("Leiser")
    
    
    
def leave_menue(v):
    global pill2kill
    global t1
    
    
    t1 = threading.Thread(target=v.run, args=(pill2kill, "task"))
    pill2kill.clear()
    t1.start()
    print("START")

def enter_menue():
    global pill2kill
    global t1
    
    pill2kill.set()
    t1.join()
    print("STOP")
    update_lcd(1)




def menue_next():
    global mode
    
    if mode==0:
        print("Stoppe Uhr")
        mode=1
        update_lcd(1)
        return

    if mode in [1,2,3]:
        mode=mode+1
        update_lcd(0)
        return

    if mode ==4:
        mylcd.lcd_clear()
        print("Starte Uhr")
        amplifier_off() #Relais schaltet verstärker aus
        Clock.write_big_time()
        mode=0
        return
    

def menue_prev():
    global mode

    if mode==0:
        print("Stoppe Uhr")
        mode=4
        update_lcd(1)
        return

    if mode==1:
        mylcd.lcd_clear()
        print("Starte Uhr")
        amplifier_off() #Relais schaltet verstärker aus
        Clock.write_big_time()
        mode=0
        return

    if mode in [2,3,4]:
        mode=mode-1
        update_lcd(0)
        return







        
def update_lcd(ueberschrift):
    if ueberschrift:
            mylcd.lcd_clear()
            amplifier_on() #Relais schaltet Verstärker ein
            mylcd.lcd_load_custom_chars(fontdata1)
            mylcd.lcd_display_string("Hauptmen",1,5)
            mylcd.lcd_display_string(chr(0),1,13)
    mylcd.lcd_display_string(chr(60)+((18-len(functions[mode]))/2)*" "+functions[mode]+((18-len(functions[mode]))/2)*" "+chr(62), 3)



def dim_lcd(gedimmt):
    stundedestages=int(time.strftime("%H"))
    if gedimmt:
        if 7<stundedestages<21:
            if 8<stundedestages<20:
                mylcd.lcd_dim(511)
            else:
                mylcd.lcd_dim(275)
        else:
            mylcd.lcd_dim(150)
    else:
        if 7<stundedestages<21:
            if 8<stundedestages<20:
                mylcd.lcd_dim(511)
            else:
                mylcd.lcd_dim(300)
        else:
            mylcd.lcd_dim(200)
 

def amplifier_on():
    GPIO.output(21, GPIO.HIGH)

def amplifier_off():
    GPIO.output(21, GPIO.LOW)


#Touch Schalter
GPIO.add_event_detect(24,GPIO.FALLING, callback=drehimpulsgeber, bouncetime=1500)

knob=RotaryEncoder(6,5,27,drehimpulsgeber)
update_lcd(1)
dim_lcd(0)



while True:
    time.sleep(25)

    
    if mode==0:
        mode=5
        print("update Clock")
        Clock.write_big_time()
        time.sleep(0.3)
        mode=0
        
    if Alarm.get_alarm_time()[0]==time.strftime("%H:%M"):
        enter_menue()
        modusnr=Alarm.get_alarm_time()[1]
        mpc.mute()
        if modusnr==1:
            leave_menue(Radio)
            menu=False
        if modusnr==2:
            leave_menue(sd_card)
            menu=False
        mode=1
        dim_lcd(0)
        for k in range(0,30):
            mpc.vol_up()
            time.sleep(2)
        time.sleep(30)
        
    if mode>0 and menu and time.time()-menu_time>20:
        mylcd.lcd_clear()
        print("Starte Uhr")
        amplifier_off()#Relais schaltet verstärker aus
        Clock.write_big_time()
        mode=0

    dim_lcd(1)

