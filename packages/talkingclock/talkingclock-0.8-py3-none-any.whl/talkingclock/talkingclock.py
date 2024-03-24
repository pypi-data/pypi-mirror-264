
import sys,os
from datetime import datetime
from playsound import playsound

def play_soundtime():
	PATH= os.path.join(os.path.dirname(__file__), 'mp3')
	d = datetime.now()
	begin="begintime.mp3"
	narika="narika.mp3"
	natee="natee.mp3"
	vinatee="vinatee.mp3"
	end="endtime.mp3"
	print(d)

	playsound(os.path.join(PATH,begin))
	playsound(os.path.join(PATH,str(d.hour)+".mp3"))
	playsound(os.path.join(PATH,narika))
	playsound(os.path.join(PATH,str(d.minute)+".mp3"))
	playsound(os.path.join(PATH,natee))

	playsound(os.path.join(PATH,str(d.second)+".mp3"))
	playsound(os.path.join(PATH,vinatee))
	playsound(os.path.join(PATH,end))

if __name__=="__main__":
	play_soundtime()
