# -*- coding: utf-8 -*-
import I2C_LCD_driver
import time
import Alarm
mylcd = I2C_LCD_driver.lcd()

#Übersetze Zahlen in Schema f←r groſe Zahlen
#in positions werden Zahlen im Format 3x3 festgelegt
#dabei stehen im Tripel immer
#[zeile(0-3),spalte(0-3),Art(1=Strich oben,2=Strich unten,255=komplett füllen)
def numbers_big(number):
    if number==0:
        positions=[[1,0,255],[1,1,2],[1,2,255],
                   [2,0,255],[2,1,32],[2,2,255],
                   [3,0,255],[3,1,1],[3,2,255]]
        return(positions)
    if number==1:
        positions=[[1,0,32],[1,1,2],[1,2,255],
                  [2,0,32],[2,1,32],[2,2,255],
                  [3,0,32],[3,1,32],[3,2,255]]
        return(positions)
    if number==2:
        positions=[[1,0,2],[1,1,2],[1,2,255],
                   [2,0,255],[2,1,2],[2,2,2],
                   [3,0,255],[3,1,1],[3,2,1]]
        return(positions)
    if number==3:
        positions=[[1,0,2],[1,1,2],[1,2,255],
                   [2,0,2],[2,1,2],[2,2,255],
                   [3,0,1],[3,1,1],[3,2,255]]
        return(positions)
    if number==4:
        positions=[[1,0,255],[1,1,32],[1,2,32],
                   [2,0,255],[2,1,1],[2,2,255],
                   [3,0,32],[3,1,32],[3,2,255]]
        return(positions)
    if number==5:
         positions=[[1,0,255],[1,1,2],[1,2,2],
                   [2,0,255],[2,1,1],[2,2,1],
                   [3,0,1],[3,1,1],[3,2,255]]
         return(positions)
    if number==6:
         positions=[[1,0,255],[1,1,2],[1,2,2],
                   [2,0,255],[2,1,2],[2,2,255],
                   [3,0,255],[3,1,1],[3,2,255]]
         return(positions)
    if number==7:
         positions=[[1,0,2],[1,1,2],[1,2,255],
                   [2,0,32],[2,1,32],[2,2,255],
                   [3,0,32],[3,1,32],[3,2,255]]
         return(positions)
    if number==8:
         positions=[[1,0,255],[1,1,2],[1,2,255],
                   [2,0,255],[2,1,2],[2,2,255],
                   [3,0,255],[3,1,1],[3,2,255]]
         return(positions)
    if number==9:
         positions=[[1,0,255],[1,1,2],[1,2,255],
                   [2,0,255],[2,1,1],[2,2,255],
                   [3,0,1],[3,1,1],[3,2,255]]
         return(positions)
        
    
def write_big_number(number, pos):
    positions=numbers_big(number)
    for i in positions:
        spalte=i[1]
        zeile=i[0]
        zeichen=i[2]
        mylcd.lcd_display_string(chr(zeichen),0+zeile,pos+spalte)

def write_big_time():
        if Alarm.get_alarm_time()[1]>0:
            mylcd.lcd_display_string(chr(7)+Alarm.get_alarm_time()[0],4,1)
        
        h_zehner=int(time.strftime("%H")[0])
        h_einer=int(time.strftime("%H")[1])
        m_zehner=int(time.strftime("%M")[0])
        m_einer=int(time.strftime("%M")[1])


        write_big_number(h_zehner,1)
        write_big_number(h_einer,5)
        
        mylcd.lcd_display_string(chr(3),2,9)
        mylcd.lcd_display_string(chr(3),3,9)
        
        write_big_number(m_zehner,10)
        write_big_number(m_einer,14)

        mylcd.lcd_display_string(time.strftime("%d.%m.%Y"),4,9)

        
    
    
