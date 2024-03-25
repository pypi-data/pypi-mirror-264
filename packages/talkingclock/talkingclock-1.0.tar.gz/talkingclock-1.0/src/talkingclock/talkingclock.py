
import sys,os,subprocess
from datetime import datetime
from playsound import playsound

is_play_command = False

def play_sound(path):
	global is_play_command  

	if is_play_command:
		# The "play" command is available
		# So, we execute the "play" command
		subprocess.run(["play", path])
	else:
		# If the "play" command is not available or encounters an error
		# We use the playsound library to play the sound
		playsound(path)
def check_playcommand():
	try:
		# Check if the "play" command is available
		subprocess.run(["play", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# If the above line runs without errors, it means "play" command is available
		# So, we execute the "play" command
		return True
	except Exception as e:
		# If the "play" command is not available or encounters an error
		# We use the playsound library to play the sound
		return False

def play_soundtime():
	# check if play command is available
	global is_play_command  
	is_play_command = check_playcommand()

	PATH= os.path.join(os.path.dirname(__file__), 'mp3')
	d = datetime.now()
	begin="begintime.mp3"
	narika="narika.mp3"
	natee="natee.mp3"
	vinatee="vinatee.mp3"
	end="endtime.mp3"
	print(d)

	play_sound(os.path.join(PATH,begin))
	play_sound(os.path.join(PATH,str(d.hour)+".mp3"))
	play_sound(os.path.join(PATH,narika))
	play_sound(os.path.join(PATH,str(d.minute)+".mp3"))
	play_sound(os.path.join(PATH,natee))

	play_sound(os.path.join(PATH,str(d.second)+".mp3"))
	play_sound(os.path.join(PATH,vinatee))
	play_sound(os.path.join(PATH,end))

if __name__=="__main__":
	play_soundtime()
