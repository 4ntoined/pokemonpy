#what if i made a class that had some functions to look at a pokemon battle in progress
#and make some determinations thereabout
import numpy as np
from moves import mov

class cpu:
    def __init__(self,battlefield):
        self.party = battlefield.cpus
        self.activemon = battlefield.cpu_mon
        self.enemymon = battlefield.usr_mon
        self.bfield = battlefield
        return

    def echo(self):
        print('echo')
        return

    def test1(self,memon=''):
        if not memon:
            memon=self.activemon
        print(memon.name)
        return
    
    def go(self,pokeme='',pokeyou=''):
        global mov
        if not pokeme:  pokeme = self.activemon
        if not pokeyou: pokeyou = self.enemymon
        #
        choice1 = self.fightswitch()    #will be 'fight' or 'switch'
        if choice1 == 'switch':
            #switch pokemon, for now randomly, but maybe not forever
            print('switching')
            pass
        elif choice1 == 'fight':
            movecat = mov[pokeme.knownMoves]['special?']
            status = np.squeeze(np.argwhere(movecat == 2))                              #indeces from knownMoves of status moves
            damages = np.squeeze(np.argwhere(np.logical_or(movecat==0,movecat==1)))     #indeces from knownMoves of damaging moves
            #do we use a damage move or status move
            #status move logic doesnt exist yet so we'll set some ~20% chance to use a status
            # vv need to replace with proper status move logic vv #
            roll_for_status = rng.random() 
            if ( len(damages) == 0 ) or ( len(status) >= 1 and roll_for_status < 0.20):   #if you have at least one status move and the roll is right
                #use a status move at random
                choice3 = rng.choice(status)
                print(mov[pokeme.knownMoves[choice3]]['name'] )
            else:   #you have 1+ damage move, and ( no status moves or roll didnt hit)
                #use a damage move USING logic
                ratings = [ self.damageMoveRating(pokeme.knownMoves[i],pokeme=pokeme,pokeyou=pokeyou)**3. for i in damages ]
                ratinga = np.array(ratings,dtype=float)
                rat_sum = sum(ratinga)
                ratp = ratinga / rat_sum
                choice2 = rng.choice(damages,p=ratp)
                print(mov[pokeme.knownMoves[choice2]]['name'] )
        return

    def fightswitch(self,pokeme='',pokeyou=''):
        """
        let's start here
        the cpu has to decide whether it will fight or choose a new pokemon
        logic: default to fighting, switch if (low health), (type-disadvantage), (defense / attack < certain threshold) eh
        mechanism: pressure to switch builds due to certain influences > built switch pressure is divided by total possible pressure
            > switch pres. ratio is further weighted for fine tuning > if it is less than 0.05, it is set to 0.05
            > this value becomes the probabilty that the cpu will switch
        """
        if not pokeme:  pokeme = self.activemon
        if not pokeyou: pokeyou = self.enemymon
        #ans = 'fight'
        #switchpressure = 0.
        #target_type = self.enemymon.tipe
        ## consider type disadvantage ## the lower the typead() value, the less likely to switch ##
        #type pressure = (0, 1), for typeAd = (1 or less, 9)
        typep_max = 1.
        typep = max( (self.typeAdvantage(defender=pokeme,attacker=pokeyou)-1.) / 8., 0.)
        ## check self health ##
        healthp_max = 1.
        if pokeme.currenthpp <= 20:     healthp = 1.
        elif pokeme.currenthpp < 50:    healthp = 0.6
        else:                           healthp = 0.
        ## defense  ##
        ##          ##
        ## collecting it all ##
        all_pressures = [typep, healthp]
        all_max = [typep_max, healthp_max]
        ##                   ##
        #pressuremax = sum(all_max)
        ## taking sums ##
        switchpressure = sum(all_pressures) / sum(all_max)  #range (0,1)
        thresh = max(switchpressure * 0.8, 0.05) #at least 5% chance to switch
        ## choosing ##
        ans = rng.choice(['fight','switch'], p=[ 1.-thresh, thresh ])
        return ans
    def stat_vs_damage_Rating(self):
        #the cpu has decided to use a move instead of switching out
        #we will check for special cases where a status move could be handy
        #if none exist we will prioritize damaging

        #if low-health, look for a healing move
        #if you can set up a beneficial weather or terrain, do that

        ## if have water-damaging moves, and rain dance, use rain dance
        ## if fire-damage moves and sunny day, use sunny day
        
        ## if rock type and has sandstorm, use sandstorm
        ## if ice type and have hail/snowscape, use snowscape
        
        ## if damaging grass, psychic, or electric move and have the terrain, use the terrain
        ## if oppo is dragon type, use misty terrain

        ## if you have aqua ring (and not already in it), use it

        ## if you have a stat-boosting move, use it with a set probability,
        #higher prob if you dont already have a boost

        ## if multiple things apply here, pick one mostly at random

        return
    def statMoveRating(self): #prob gonna scrap
        #prioritize healing move, if low health
        # 
        ans = 1.
        return ans
    def chooseStatMove(self,poke,targetmon): #sounds like same as above, prob scrap
        #will choose among the status moves of poke and decide what to use
        return
    def damageMoveRating(self,movei,pokeme='',pokeyou='',maxx=16,debug=False):
        #overall, considering all the things
        #things to consider: effective power, secondary effects, phy/spec
        #priority to brick break when a screen is up
        #priority to high crit moves when a screen is up or target has boosted defense
        #priority to noMiss moves when oppo evasion is high or self accuracy is low
        #
        global mov
        #if not targetmon: targetmon = self.enemymon
        movedat = mov[ movei ]
        move_phys = movedat['special?'] == 0
        move_notes = movedat['notes'].copy()
        splitnotes = move_notes.split(' ')
        ##      consider physical vs special        ##
        #physical moves are favored when attacker has greater physical than special stat, vise versa
        #physical moves are favored when target has greater special than physical, vise versa
        phys_attacker = pokeme.bat > pokeme.bsa
        phys_defense = pokeyou.bde > pokeyou.bsd
        physpec = 1.
        if move_phys:
            if phys_attacker:       physpec += 0.2
            if not phys_defense:    physpec += 0.2
        else:
            if not phys_attacker:   physpec += 0.2
            if phys_defense:        physpec += 0.2
        ##                                          ##
        ##      consider secondary effects      ##
        weatherball_flag = self.bfield.field.weather != 'clear'
        seconds = ('burn' in splitnotes) or ('frze' in splitnotes) or ('pois' in splitnotes) \
                or ('badPois' in splitnotes) or ('para' in splitnotes) or ('sleep' in splitnotes)
        thirds = ('highCrit' in splitnotes) or ('frostbreath' in splitnotes) or ('conf' in splitnotes) \
                or ('flinch' in splitnotes) or (weatherball_flag and ('weatherball' in splitnotes))
        if seconds or thirds:   fourth = 1.3
        else:                   fourth = 1.
        ##                                      ##
        ##      calc move power and stab and stat boosts nerfs
        power = self.powerRating(movei,pokeme=pokeme,pokeyou=pokeyou)
        ##      put it all together     ##
        parts = [physpec, fourth]
        ans = power
        for i in parts: ans *= i
        ##                              ##
        if debug:   return (ans, parts)
        else:       return ans
    def powerRating(self,movei,pokeme='',pokeyou='',maxx=16):
        #this function will look at a move of poke, apply
        #base power, type, category with opponent mon self.enemymon
        global mov,statStages
        if not pokeme:  pokeme = self.activemon
        if not pokeyou: pokeyou = self.enemymon
        #if not targetmon: targetmon = self.enemymon
        #check the weather
        weathe = self.bfield.field.weather
        terrai = self.bfield.field.terrain
        #unload move
        movedat = mov[ movei ]
        move_phys = movedat['special?'] == 0
        move_notes = movedat['notes'].copy()
        splitnotes = move_notes.split(' ')
        #   check for 2turn or must rest, we'll nerf the base power #
        if ('2turn' in splitnotes) or ('mustRest' in splitnotes):
            if ('solar' in splitnotes) and (weathe=='sunny'):       turnnerf = 1.
            else:                                                   turnnerf = 0.75
        else:                                                       turnnerf = 1.
        #                                                           #
        #   check for stab  #
        if movedat['type'] in pokeme.tipe:      stab = 1.5
        else:                                   stab = 1.
        #                   #
        #   consider offensive/defensive stat stages, burns, screens    #
        screen = 1.
        burn = 1.
        if not move_phys:
            boost = statStages[pokeme.sastage] / statStages[pokeyou.sdstage]
            if self.bfield.field.lightscACounter > 0:   screen = 0.5
        else:
            boost = statStages[pokeme.atstage] / statStages[pokeyou.destage]
            if pokeme.burned:                             burn = 0.5
            if self.bfield.field.reflectACounter > 0:   screen = 0.5
        #                                               #
        #   consider weather synergy    #
        #weatherboost = 1.
        weatheron = (( weathe == 'sunny') and ( movedat['type']==1 )) or \
                (( weathe == 'rain') and ( movedat['type'] == 2 )) or \
                (( terrai == 'grassy') and ( movedat['type']==3 )) or \
                (( terrai == 'electric') and ( movedat['type'] == 4 )) or \
                (( terrai == 'psychic') and ( movedat['type'] == 10 ))
        if weatheron:   weatherboost = 1.3
        else:           weatherboost = 1.
        #                               #
        #
        ans = movedat['pwr'] * typeeff(movedat['type'],pokeyou.tipe) * stab * \
                turnnerf * boost * weatherboost * burn * screen
        return ans
    
    def typeAdvantage(self,defender='',attacker=''):
        """
        defender: mon() object worried about being hit
        attacker: mon() object doing the hitting
        determine if one pokemon has a type advantage over the other
        considers only pokemon-typing, not move-typing!
        """
        if not defender:    defender = self.activemon
        if not attacker:    attacker = self.enemymon
        defending = defender.tipe
        attacking = attacker.tipe
        if len(attacking)==2:
            do1 = typeeff(attacking[0],defending)
            do2 = typeeff(attacking[1],defending)
            dote = do1 * do2
            if dote > 8.:       dote = 9.
            elif dote < 0.125:  dote = 0.111
        else:   dote = typeeff(attacking[0],defending)
        #dote will vary from 0.111 to 9 when attacker has 2 types
        # 0.25 to 4 when attacker has only 1 type
        return dote

def typeeff(attackType,defendType):
    #attackType: integer (0, 18)
    #defendType: list of 1 or 2 integers ie [1, 2]
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
rng = np.random.default_rng()
codex = codexer()
statStages=[2/8,2/7,2/6,2/5,2/4,2/3,2/2,3/2,4/2,5/2,6/2,7/2,8/2] #0 to 6 to 12
if __name__ == '__main__':
    pass
else:
    pass

