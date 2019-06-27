#a game by Antoine D.

#modules
import time as t

#variables aplenty
game_mode=0 #0-normal game #1 introduction and tutorial? idk
game_running=True
#some classes
#text colors
class tc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#people
class comet:
	def __init__(self):
		self.name = input("Name?\n")
		self.hunger = 0
		print("You're alive now. Sorry about that.")

	def eat(food):
		print("You ate the", food)
		hunger = 0
		print("You're full now!")
#food
class ice:
	def __init__(self, tipe):
		if tipe == 'banana':
			self.calories=10
		if tipe == 'steak':
			self.calories=40
		print("There's a", tipe)
#this plays when you start the game
class introduction():
	def __init__(self, fanny):
		print("Hey, what's up?")
		t.sleep(3)
		print("Oh yeah, you can't speak to me.")
		t.sleep(1)
		print("Not yet at least. You might pick it up along the way.")
		t.sleep(2)
		print("Look %s, you can't stay out there forever." % fanny.name)
		t.sleep(1)
		print("And once you come back, you can never leave again.")
		t.sleep(1)
		print("Have fun")
#this plays after the introduction lmao
class tutorial:
	print(tc.OKGREEN + "Hi! I'm the GUI." + tc.ENDC)
	t.sleep(2)
	print(tc.OKGREEN + "Here's how this works.." + tc.ENDC)
	t.sleep(2)
	print(tc.OKGREEN + "I feed you information from the World.." + tc.ENDC)
	t.sleep(1)
	print(tc.OKGREEN + "And I'll give you some options for a response." + tc.ENDC)
	t.sleep(2)
	print(tc.OKGREEN + "OK?" + tc.ENDC)
	t.sleep(2)
	

#checks time since game started
def checktime():
	tyme=t.time()-zero_time
	return tyme
#game clock
zero_time=t.time()

#intro
player = comet()
introduction(player)
tutorial()
innie=input("Is this okay? [yes] or [no]\n")
if innie=='yes' or innie=='y':
	print(tc.OKGREEN + "Oh great" + tc.ENDC)
	game_mode=0
	game_running=True

if innie=='no' or innie=='n':
	print(tc.OKGREEN + "Aw damn. Okay bye" + tc.ENDC)
		

while game_running:
	if game_mode==0:
		tea=input("try [eat]\n")
		if tea=="eat":
			player.eat()
			print(tc.OKGREEN + "Look! You ate!" + tc.ENDC)

#
'''
intro_timer=0
if intro_timer<1000000:
	intro_timer+=1
'''
