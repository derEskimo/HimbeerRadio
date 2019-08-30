import subprocess
import time
import os

     
subprocess.check_output("sudo service mpd start", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)


def load_radio_playlist():
    subprocess.check_output("mpc clear", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)   
    subprocess.check_output("mpc load Radio_List", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

    subprocess.check_output("mpc random 0", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)   
    subprocess.check_output("mpc repeat 1", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def load_music_playlist():
    subprocess.check_output("mpc clear", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)   
    #subprocess.check_output("mpc update", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)   
    subprocess.check_output("mpc add /", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

    subprocess.check_output("mpc repeat 1", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)   
    subprocess.check_output("mpc random 1", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    subprocess.check_output("mpc crossfade 14", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
   

def play(position):
    subprocess.check_output("mpc play "+str(position), shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def next():
    subprocess.check_output("mpc next", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    
def prev():
    subprocess.check_output("mpc prev", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def stop():
    subprocess.check_output("mpc stop", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)



def sender_info():
    radioinfo =(subprocess.check_output("mpc current", shell=True, stderr=subprocess.STDOUT, universal_newlines=True))
    if radioinfo[0:5]=="http:":
        print("getting info")
        return("  ","  Searching for Info")
    radioinfo=radioinfo.partition(": ")
    if "\n" in radioinfo[0]:
        return((radioinfo[0][:-1])[:20],radioinfo[2][:-1])
    return(radioinfo[0][:20],radioinfo[2][:-1])

def music_info():
    radioinfo =(subprocess.check_output("mpc", shell=True, stderr=subprocess.STDOUT, universal_newlines=True))
    name=(radioinfo.split("\n")[0])
    zeile2=radioinfo.split("\n")[1]
    zeile2=zeile2.split("#")[1]
    
    number,egal,egal,times,percentage=zeile2.split(" ")
    numberofsong, gesamtzahl=number.split("/")
    number=numberofsong.zfill(4)+"/"+gesamtzahl.zfill(4)
    #timeleft_in_seconds=str(int((times.split("/")[0]).split(":")[0])*60+int((times.split("/")[0]).split(":")[1])-int((times.split("/")[1]).split(":")[0])*60+int((times.split("/")[1]).split(":")[1]))
    
    percentage=percentage[1:-2]
    
    return(name,number,percentage)



def mute():
    subprocess.check_output("mpc volume 0", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def get_vol():
    vol = subprocess.check_output("mpc volume", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    vol = vol[7:10]
    return int(vol)
    
def vol_up():
        subprocess.check_output("mpc volume +1", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def vol_down():
        subprocess.check_output("mpc volume -1", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

