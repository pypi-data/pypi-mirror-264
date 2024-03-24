
# -*- coding: utf-8 -*-
import sys,os,icalendar,re,csv
from datetime import datetime,timedelta
from playsound import playsound


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def csv_to_dict(csv_file):
    data_dict = {}
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                key, value = row[:2]  # Assuming two columns
                data_dict[key] = value
            else:
                print(f"Ignoring row: {row}")
    return data_dict

def is_next_day(date_obj):
    # Get today's date
    today = datetime.now().date()

    # Get the date of the next day
    next_day = today + timedelta(days=1)

    # Check if the date of the datetime object is the same as the date of the next day
    return date_obj.date() == next_day
def is_today(date_obj):
    # Get today's date
    today = datetime.now().date()

    # Check if the date of the datetime object is the same as the date of today
    return date_obj.date() == today

def get_holyday():
    cal_file = os.path.join(os.path.dirname(__file__), 'buddha.ics')
    e = open(cal_file, 'rb')
    ecal = icalendar.Calendar.from_ical(e.read())
    i=0
    holyday={}
    for component in ecal.walk():
        if component.name == "VEVENT":
            #i=i+1
            #print("-------------------------------------")
            #print("No:"+str(i))
            #print(component.get("name"))
            #print(component.get("description"))
            #print(component.get("organizer"))
            #print(component.get("location"))
            #print(component.decoded("dtstart"))
            #print(component.decoded("dtend"))
            hdate = component.decoded("dtstart")
            hdesc = re.sub(r'\(.*\)', '', component.get("description"))
            holyday[hdate] = hdesc
    e.close()
    #today = datetime.now().date() + timedelta(days=1)  
    #holyday[today]=re.sub(r'\(.*\)', '', " วันอาทิตย์ แรม 14 ค่ำ เดือนอ้าย(๑) ปีมะโรง")
    return holyday

def process_holyday(holyday):
    PATH= os.path.join(os.path.dirname(__file__), 'mp3')

    today = datetime.now().date()
    # Get the date of the next day
    next_day = today + timedelta(days=1)  
    next_2day = today + timedelta(days=2)  
    desc=""
    sound_list=[]

    if next_2day in holyday:
        desc = holyday.get(next_2day)
        sound_list+=["kmomkha.mp3"]
        sound_list+=["iksongwan.mp3"]
        sound_list+=["iswanpra.mp3"]
        play_sound(desc,sound_list)
    elif next_day in holyday:
        desc = holyday.get(next_day)
        sound_list+=["kmomkha.mp3"]
        sound_list+=["tomorrow.mp3"]
        sound_list+=["iswanpra.mp3"]
        play_sound(desc,sound_list)

    elif today in holyday:
        desc = holyday.get(today)
        sound_list+=["kmomkha.mp3"]
        sound_list+=["today.mp3"]
        sound_list+=["iswanpra.mp3"]
        play_sound(desc,sound_list)

        

def play_sound(desc,sound_list):
    token = desc.split(" ")
    #print("Token:"+str(token))
    soundmap = os.path.join(os.path.dirname(__file__), 'soundmap.txt')
    sound_dict = csv_to_dict(soundmap)
    #print(sound_dict)
    for t in token:
        if t is not None:
            if len(t) > 0:
                if t in sound_dict:
                    sound_file = sound_dict.get(t)+".mp3"
                    #print("file:"+sound_file)
                    sound_list+=[sound_file]
                elif is_integer(t):
                    sound_file = str(t)+".mp3"
                    sound_list+=[sound_file]

    for s in sound_list:
        mp3_path = os.path.join(os.path.join(os.path.dirname(__file__), 'mp3'),s)
        playsound(mp3_path)

def play_holysound():
    holyday = get_holyday()
    process_holyday(holyday)

if __name__=="__main__":
    play_holysound()

