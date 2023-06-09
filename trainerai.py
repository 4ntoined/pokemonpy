#what if i made a class that had some functions to look at a pokemon battle in progress
#and make some determinations thereabout
import numpy as np
from moves import mov

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
    def damageMoveRating(self,poke,movei,targetmon='',maxx=16):
        #overall, considering all the things
        #things to consider: power, secondary effects, phy/spec
        #priority to brick break when a screen is up
        #priority to high crit moves when a screen is up or target has boosted defense
        #
        global mov
        if not targetmon: targetmon = self.enemymon
        movedat=mov[movei]
        #nmoves = len(poke.knownMoves)
        #if nmoves > maxx: nmoves = maxx
        #for i in range(len(nmoves)):
        #move category poke stats synergy
        phys_attacker = poke.bat > poke.bsa
        if phys_attacker and movedat['special?']==0:        physpec = 1.3
        elif not phys_attacker and movedat['special?']==1:  physpec = 1.3
        else: physpec = 1.
        ## calc move power and stab and stat boosts nerfs
        power = powerRating(self,poke,movei,targetmon=targetmon)
        ans = power * physpec

        return
    def powerRating(self,poke,movei,targetmon='',maxx=16):
        #this function will look at the moves of poke, apply their
        #base powers, types, categories with opponent mon self.enemymon
        global mov,statStages
        if not targetmon: targetmon = self.enemymon
        #unload move
        movedat = mov[movei]
        #check for 2turn or must rest, well halve the power
        if '2turn' in movedat['notes'] or 'mustRest' in movedat['notes']:   turnnerf = 0.75
        else:                                                               turnnerf = 1.
        #check for stab
        if movedat['type'] in poke.tipe:    stab = 1.5
        else:                               stab = 1.
        #consider stat stages
        if movedat['special?']==1:  boost = statStages[poke.sastage]
        else:                       boost = statStages[poke.atstage]
        #
        ans = movedat['pwr'] * typeeff(movedat['type'],targetmon.tipe) * stab * turnnerf * boost
        return ans

def typeeff(attackType,defendType):
    global codex
    match1 = codex[attackType,defendType[0]]
    if len(defendType)>1:   match2 = codex[attackType,defendType[1]]
    else:                   match2 = 1.
    return match1*match2
def codexer():
    #normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
    #ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,dark 15,
    #steel 16,fairy 17,typeless (no relationships) 18
    codex=np.ones((19,19),dtype=float)
    codex[0,12],codex[0,13],codex[0,16]=\
            0.5,0,0.5 #normal
    codex[1,1],codex[1,2],codex[1,3],codex[1,5],codex[1,11],\
            codex[1,12],codex[1,14],codex[1,16]=\
            0.5,0.5,2.0,2.0,2.0,0.5,0.5,2.0 #fire
    codex[2,1],codex[2,2],codex[2,3],codex[2,8],codex[2,12],codex[2,14]=\
            2.0,0.5,0.5,2.0,2.0,0.5 #water
    codex[3,1],codex[3,2],codex[3,3],codex[3,7],codex[3,8],\
            codex[3,9],codex[3,11],codex[3,12],codex[3,14],codex[3,16]=\
            0.5,2.0,0.5,0.5,2.0,0.5,0.5,2.0,0.5,0.5 #grass
    codex[4,2],codex[4,3],codex[4,4],codex[4,8],codex[4,9],codex[4,14]=\
            2.0,0.5,0.5,0.0,2.0,0.5 #electric
    codex[5,1],codex[5,2],codex[5,3],codex[5,5],codex[5,8],\
            codex[5,9],codex[5,14],codex[5,16]=\
            0.5,0.5,2.0,0.5,2.0,2.0,2.0,0.5 #ice
    codex[6,1],codex[6,5],codex[6,7],codex[6,9],codex[6,10],codex[6,11],\
            codex[6,12],codex[6,13],codex[6,15],codex[6,16],codex[6,17]=\
            2.0,2.0,0.5,0.5,0.5,0.5,2.0,0.0,2.0,2.0,0.5 #fighting
    codex[7,3],codex[7,7],codex[7,8],codex[7,12],\
            codex[7,13],codex[7,16],codex[7,17]=\
            2.0,0.5,0.5,0.5,0.5,0.0,2.0 #poison
    codex[8,1],codex[8,3],codex[8,4],codex[8,7],codex[8,9],\
            codex[8,11],codex[8,12],codex[8,16]=\
            2.0,0.5,2.0,2.0,0.0,0.5,2.0,2.0 #ground
    codex[9,3],codex[9,4],codex[9,6],codex[9,11],codex[9,12],codex[9,16]=\
            2.0,0.5,2.0,2.0,0.5,0.5 #flying
    codex[10,6],codex[10,7],codex[10,10],codex[10,15],codex[10,16]=\
            2.0,2.0,0.5,0.0,0.5 #psychic
    codex[11,1],codex[11,3],codex[11,6],codex[11,7],codex[11,9],codex[11,10],\
            codex[11,13],codex[11,15],codex[11,16],codex[11,17]=\
            0.5,2.0,0.5,0.5,0.5,2.0,0.5,2.0,0.5,0.5  #bug
    codex[12,1],codex[12,5],codex[12,6],codex[12,8],\
            codex[12,9],codex[12,11],codex[12,16]=\
            2.0,2.0,0.5,0.5,2.0,2.0,0.5 #rock
    codex[13,0],codex[13,10],codex[13,13],codex[13,15]=\
            0.0,2.0,2.0,0.5 #ghost
    codex[14,14],codex[14,16],codex[14,17]=\
            2.0,0.5,0.0 #dragon
    codex[15,6],codex[15,10],codex[15,13],codex[15,15],codex[15,17]=\
            0.5,2.0,2.0,0.5,0.5 #dark
    codex[16,1],codex[16,2],codex[16,4],codex[16,5],\
            codex[16,12],codex[16,16],codex[16,17]=\
            0.5,0.5,0.5,2.0,2.0,0.5,2.0 #steel
    codex[17,1],codex[17,6],codex[17,7],codex[17,14],codex[17,15],codex[17,16]=\
                0.5,2.0,0.5,2.0,2.0,0.5 #fairy
    return codex
codex = codexer()
statStages=[2/8,2/7,2/6,2/5,2/4,2/3,2/2,3/2,4/2,5/2,6/2,7/2,8/2] #0 to 6 to 12
if __name__ == '__main__':
    pass
else:
    pass

