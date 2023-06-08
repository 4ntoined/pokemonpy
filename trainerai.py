#what if i made a class that had some functions to look at a pokemon battle in progress
#and make some determinations thereabout

class cpu:
    def __init__(self,battlefield):
        self.party = battlefield.cpus
        self.activemon = battlefield.cpu_mon
        self.enemymon = battlefield.usr_mon
        self.field = battlefield
        return

    def echo(self):
        print('echo')
        return

    def test1(self):
        print(self.activemon.name)
        return
    def checkMoveEffectiveness(movei, typing):

        return

    def fightswitch(self):
        #let's start here
        #the cpu has to deicde whether it will fight or choose a new pokemon
        #influences: do we have super-effective moves? stab moves?, are we faster?, are we defensive
        #are we the right kind of defensive, based on target's stats
        #logic: try to fight, if we have supereffective moves or otherwise highly rated moves, fight
        #       if we have no highly rated moves, switch
        target_type = self.enemymon.tipe
        
        return
    def moveRating():
        return
    def statMoveRating(self):
        return
    def damageMoveRating(self,poke,targetmon='',maxx=16):
        #overall, considering all the things
        #things to consider: power, secondary effects, phy/spec
        #priority to brick break when a screen is up
        #priority to high crit moves when a screen is up or target has boosted defense
        #
        if not targetmon: targetmon = self.enemymon
        nmoves = len(poke.knownMoves)
        if nmoves > maxx: nmoves = maxx
        for i in range(len(nmoves)):
            ans = power * 
        return
    def powerRating(self,poke,targetmon='',maxx=16):
        #this function will look at the moves of poke, apply their
        #base powers, types, categories with opponent mon self.enemymon
        #if not targetmon: targetmon = self.enemymon
        #determine/set number of moves to consider
        nmoves = len(poke.knownMoves)
        if nmoves > maxx: nmoves = maxx
        #for each move, give a rating
        for i in range(len(nmoves)):
            
            ans = movepower * typeeff * stab

        
        return
