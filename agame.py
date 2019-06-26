#a game by Antoine D.
import time as t
#people
class comet:
	def __init__(self):
		self.name = input("Name?")
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

class introduction:
	player = comet()
	print("Hey, what's up?")
	t.sleep(3)
	print("Oh yeah, you can't speak to me.")
	t.sleep(1)
	print("Not yet at least. You might pick it up along the way.")
	t.sleep(2)
	print("Look %s, you can't stay out there forever." % player.name)
	t.sleep(1)
	print("And once you come back, you can never leave again.")
	t.sleep(1)
	print("Have fun")

#checks time since game started
def checktime():
	tyme=t.time()-zero_time
	return tyme

#game clock
zero_time=t.time()

#intro
'''
intro_timer=0
if intro_timer<1000000:
	intro_timer+=1
'''
