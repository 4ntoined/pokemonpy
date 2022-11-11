#Antoine
#the basic classes and functions of the pokemon code
#treat these lines of code with care
#thank you
import time as t
import copy
import numpy as np
from dexpoke import dex
from moves import mov,natures,struggle,futuresigh,getMoveInfo
#classes: mon, battle, field | functions: damage, checkBlackout, loadMon, makeMon, checktype effectiveness, HP, stats, 
rng = np.random.default_rng()
#aa:monclass
class mon:
    def __init__(self,level,named,nature=(0,0),hpbase=70,atbase=70,debase=70,sabase=70,sdbase=70,spbase=70,tipe=np.array([0])): #add natures
        #print("its a pokemon!")
        self.level=level
        self.nature = nature
        self.nature_str = natures[nature[0],nature[1]]
        self.null_nature = False
        if self.nature[0] == self.nature[1]:
            self.null_nature = True
            self.nature_multipliers = np.ones(5)
        else:
            self.nature_multipliers = np.ones(5)
            self.nature_multipliers[self.nature[0]] = 1.1
            self.nature_multipliers[self.nature[1]] = 0.9
        self.hpiv=rng.integers(0,32)
        self.ativ=rng.integers(0,32)
        self.deiv=rng.integers(0,32)
        self.saiv=rng.integers(0,32)
        self.sdiv=rng.integers(0,32)
        self.spiv=rng.integers(0,32)
        self.hpev=0
        self.atev=0
        self.deev=0
        self.saev=0
        self.sdev=0
        self.spev=0
        ##base stats===##
        self.hpb=hpbase
        self.atb=atbase
        self.deb=debase
        self.sab=sabase
        self.sdb=sdbase
        self.spb=spbase
        self.maxhp=HP(self.level,self.hpb,self.hpiv,self.hpev)
        self.currenthp=self.maxhp
        self.currenthpp=100.
        ##final stats, with evs, ivs, and one day natures==============##
        self.attack=stats(self.level,self.atb,self.ativ,self.atev,self.nature_multipliers[0])
        self.defense=stats(self.level,self.deb,self.deiv,self.deev,self.nature_multipliers[1])
        self.spatk=stats(self.level,self.sab,self.saiv,self.saev,self.nature_multipliers[2])
        self.spdef=stats(self.level,self.sdb,self.sdiv,self.sdev,self.nature_multipliers[3])
        self.speed=stats(self.level,self.spb,self.spiv,self.spev,self.nature_multipliers[4])
        ##=============================================================##
        self.name=named
        self.tipe=tipe
        if len(tipe)>1:
            self.dualType=True
        else:
            self.dualType=False
        self.fainted=False
        self.knownMoves=[19]
        self.PP=[35]
        if 9 in self.tipe: #flying types aren't grounded
            self.grounded=False
        else:
            self.grounded=True
        #battle stat stages
        self.atstage=6 #0 (at -6) to 6 (at 0) to 12 (at +6?)
        self.destage=6
        self.sastage=6
        self.sdstage=6
        self.spstage=6
        self.evstage=6
        self.acstage=6
        ##stats for battle, including temporary stat buffs and nerfs##
        self.bat=self.attack
        self.bde=self.defense
        self.bsa=self.spatk
        self.bsd=self.spdef
        self.bsp=self.speed
        ##==========================================================##
        self.battlespot = None #will be set to "red" or "blue" when sent out
        self.field = None #will be set equal to the battle() instance into which a pokemon is sent out?
        #battle statuses
        self.sleep=False        
        self.frozen=False
        self.burned=False
        self.paralyzed=False
        self.poisoned=False
        self.badlypoisoned=False
        self.confused=False
        self.sleepCounter=0
        self.poisonCounter=0
        self.confusionCounter=0
        #
        self.counter_damage = (0.0, "none") #damage points taken, "phys" or "spec"
        self.flinched=False #might not necessarily need this? idk
        self.resting=False #for moves where pokemon need to recharge
        self.charged=False #when true, pokemon has a 2turn move ready to use
        self.firstturnout=False
        self.curled=False
        self.aquaring=False
        self.flying=False       #used fly or bounce dont know about sky drop rn
        self.diving=False       #used dive
        self.digging=False      #used dig
        self.shadowing=False    #used shadow force, or phantom force
        self.rolling_out=0
    #save pokemon
    def save(self,filename='pypokemon.sav'):
        f=open(filename,'a')
        name=self.name
        lvl=self.level
        #pokemon base stats
        hp=self.hpb
        at=self.atb
        de=self.deb
        sa=self.sab
        sd=self.sdb
        sp=self.spb
        base=[hp,at,de,sa,sd,sp]
        #pokemon ivs
        hpi=self.hpiv
        ati=self.ativ
        dei=self.deiv
        sai=self.saiv
        sdi=self.sdiv
        spi=self.spiv
        iv=[hpi,ati,dei,sai,sdi,spi]
        #pokemon evs
        hpe=self.hpev
        ate=self.atev
        dee=self.deev
        sae=self.saev
        sde=self.sdev
        spe=self.spev
        ev=[hpe,ate,dee,sae,sde,spe]
        #pokemon types
        tip=self.tipe
        #nature
        nacher = self.nature
        #known moves
        mvs=self.knownMoves
        #construct line to save all pokemon data
        line=name
        line+=f",{lvl},"
        for i in base: #add all the base stats
            line+=f" {i}"
        line+=","
        for i in iv: #add all the ivs
            line+=f" {i}"
        line+=","
        for i in ev: #add all the evs
            line+=f" {i}"
        line+=","
        for i in tip:
            line+=f" {i}"
        line+=","
        for i in nacher:
            line+=f" {i}"
        line+=","
        for i in mvs:
            line+=f" {i}"
        f.write(line+"\n")
        f.close()
    #place moveset with random moves
    def randomizeMoveset(self,numb=6):
        global mov,mo
        ranMoves = rng.choice(mo,size=numb,replace=False)
        self.knownMoves = list(ranMoves)
        self.PP=[mov[i]["pp"] for i in ranMoves]
        return
    #recalculate stats
    def reStat(self):
        self.maxhp=HP(self.level,self.hpb,self.hpiv,self.hpev)
        self.attack=stats(self.level,self.atb,self.ativ,self.atev,self.nature_multipliers[0])
        self.defense=stats(self.level,self.deb,self.deiv,self.deev,self.nature_multipliers[1])
        self.spatk=stats(self.level,self.sab,self.saiv,self.saev,self.nature_multipliers[2])
        self.spdef=stats(self.level,self.sdb,self.sdiv,self.sdev,self.nature_multipliers[3])
        self.speed=stats(self.level,self.spb,self.spiv,self.spev,self.nature_multipliers[4])
        self.currenthp=self.maxhp
        self.currenthpp=100.
    
    #sending a pokemon out
    def chosen(self, trainer, fields):
        self.field=fields
        self.firstturnout=True
        if trainer == "user":
            self.battlespot = "red"
        elif trainer == "cpu":
            self.battlespot = "blue"
    
    ####things to reset upon being withdrawn
    def withdraw(self):
        #reset stat stages
        self.atstage=6
        self.destage=6
        self.sastage=6
        self.sdstage=6
        self.spstage=6
        self.acstage=6
        self.evstage=6
        self.bat=self.attack
        self.bde=self.defense
        self.bsa=self.spatk
        self.bsd=self.spdef
        self.bsp=self.speed
        #re-unground flying types
        if 9 in self.tipe: 
            self.grounded=False
        else:
            self.grounded=True
        #undo confusion
        self.confused=False
        self.confusionCounter=0
        #reset bad poison counter
        if self.poisonCounter>0:
            self.poisonCounter=1
        self.resting=False
        self.flinched=False
        self.charged=False
        self.firstturnout=False
        self.curled=False
        self.rolling_out=0
        self.aquaring=False
        self.counter_damage = (0.0, "none")
        self.flying=False
        self.diving=False
        self.digging=False
        self.shadowing=False
    #fainting
    def faint(self):
        self.currenthp=0.
        self.currenthpp=0.
        self.fainted=True
        self.withdraw()
        self.poisonCounter=0
        self.sleep=False
        self.frozen=False
        self.paralyzed=False
        self.burned=False
        self.poisoned=False
        self.badlypoisoned=False
        print(f"\n{self.name} faints!")
        shortpause()
    
    #back to full health!
    def restore(self):
        self.currenthp=self.maxhp
        self.currenthpp=100.
        self.PP=[getMoveInfo(i)['pp'] for i in self.knownMoves]
        self.fainted=False
        self.poisoned=False
        self.paralyzed=False
        self.burned=False
        self.badlypoisoned=False
        self.poisonCounter=0
        self.sleep=False
        self.sleepCounter=0
        self.frozen=False
        
    ####things to call/recall when a pokemon is battling
    def inBattle(self):
        global statStages
        #stat changes
        self.bat=self.attack*statStages[self.atstage]
        self.bde=self.defense*statStages[self.destage]
        self.bsa=self.spatk*statStages[self.sastage]
        self.bsd=self.spdef*statStages[self.sdstage]
        self.bsp=self.speed*statStages[self.spstage]
        #other things that may affect stats
        if self.paralyzed:
            self.bsp*=0.5
            print(f"{self.name} is slowed by paralysis..")
        #weather
        if 12 in self.tipe:
            if self.field.weather=='sandstorm':
                #rock type sp.def boost in a sandstorm!
                self.bsd*=1.5
                print(f"{self.name} is boosted by the sandstorm!")
        #ground or unground pokemon?
        #further in the list
    
    def stageChange(self,stat,level):
        #stat='at','de','sa','sd','sp'
        #level= 1,2,3 or -1,-2,-3
        #i think that this would be a good place to use match/case, but that's low priority and would break pre 3.10 pythons
        global stageStrings
        if stat=='at':
            maxd=(self.atstage==12 and level>0)
            mind=(self.atstage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Atk. stat can't go any higher!")
            elif mind:
                print(f"{self.name}'s Atk. stat can't go any lower!")
            else:
                self.atstage+=level
                if self.atstage>12: #catch overruns
                    level=12+level-self.atstage #reset "level" to account for hitting ceiling
                    self.atstage=12
                if self.atstage<0:
                    level=level-self.atstage
                    self.atstage=0
                print(f"{self.name}'s Atk. stat {stageStrings[level+3]}!")
        if stat=='de':
            maxd=(self.destage==12 and level>0)
            mind=(self.destage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Def. stat can't go any higher!")
            elif mind:
                print(f"{self.name}'s Def. stat can't go any lower!")
            else:
                self.destage+=level
                if self.destage>12: #catch overruns
                    level=12+level-self.destage #reset "level" to account for hitting ceiling
                    self.destage=12
                if self.destage<0:
                    level=level-self.destage
                    self.destage=0
                print(f"{self.name}'s Def. stat {stageStrings[level+3]}!")
        if stat=='sa':
            maxd=(self.sastage==12 and level>0)
            mind=(self.sastage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Sp.A stat can't go any higher!")
            elif mind:
                print(f"{self.name}'s Sp.A stat can't go any lower!")
            else:
                self.sastage+=level
                if self.sastage>12: #catch overruns
                    level=12+level-self.sastage #reset "level" to account for hitting ceiling
                    self.sastage=12
                if self.sastage<0:
                    level=level-self.sastage
                    self.sastage=0
                print(f"{self.name}'s Sp.A stat {stageStrings[level+3]}!")
        if stat=='sd':
            maxd=(self.sdstage==12 and level>0)
            mind=(self.sdstage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Sp.D stat can't go any higher!")
            elif mind:
                print(f"{self.name}'s Sp.D stat can't go any lower!")
            else:
                self.sdstage+=level
                if self.sdstage>12: #catch overruns
                    level=12+level-self.sdstage #reset "level" to account for hitting ceiling
                    self.sdstage=12
                if self.sdstage<0:
                    level=level-self.sdstage
                    self.sdstage=0
                print(f"{self.name}'s Sp.D stat {stageStrings[level+3]}!")
        if stat=='sp':
            maxd=(self.spstage==12 and level>0)
            mind=(self.spstage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Spe. stat can't go any higher!")
            elif mind:
                print(f"{self.name}'s Spe. stat can't go any lower!")
            else:
                self.spstage+=level
                if self.spstage>12: #catch overruns
                    level=12+level-self.spstage #reset "level" to account for hitting ceiling
                    self.spstage=12
                if self.spstage<0:
                    level=level-self.spstage
                    self.spstage=0
                print(f"{self.name}'s Spe. stat {stageStrings[level+3]}!")
        #accuracy
        if stat=='ac':
            maxd=(self.acstage==12 and level>0)
            mind=(self.spstage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Accuracy can't go any higher!")
            elif mind:
                print(f"{self.name}'s Accuracy can't go any lower!")
            else:
                self.acstage+=level
                if self.acstage>12: #catch overruns
                    level=12+level-self.acstage #reset "level" to account for hitting ceiling
                    self.acstage=12
                if self.acstage<0:
                    level=level-self.acstage
                    self.spstage=0
                print(f"{self.name}'s Accuracy {stageStrings[level+3]}!")
        #evasion
        if stat=='ev':
            maxd=(self.evstage==12 and level>0)
            mind=(self.evstage==0 and level<0)
            if maxd:
                print(f"{self.name}'s Evasion can't go any higher!")
            elif mind:
                print(f"{self.name}'s Evasion can't go any lower!")
            else:
                self.evstage+=level
                if self.evstage>12: #catch overruns
                    level=12+level-self.evstage #reset "level" to account for hitting ceiling
                    self.evstage=12
                if self.evstage<0:
                    level=level-self.evstage
                    self.evstage=0
                print(f"{self.name}'s Evasion {stageStrings[level+3]}!")
        #end of stat changes
    
    def afflictStatuses(self,notes):
        #global weather
        #global terrain
        afflicted=self.sleep or self.frozen or self.paralyzed or self.burned or self.poisoned or self.badlypoisoned
        mistyCheck=(self.field.terrain=="misty") and self.grounded #is the pokemon grounded on misty terrain?
        #paralyze
        if "para" in notes:
            if 4 in self.tipe: #electric types immune to paralysis
                print(f"\n{self.name} is immune to paralysis!")
            elif mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif afflicted:
                print(f"\n{self.name} already has a status condition...")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="para"))]) #the odds in percent of causing paralysis
                if rng.random()<=odds/100.:
                    self.paralyzed=True
                    print(f"\n{self.name} is paralyzed by the hit!")
                    micropause()
        #burn
        if "burn" in notes:
            if 1 in self.tipe: #fire types immune to burns
                print(f"\n{self.name} is immune to burns!")
            elif mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif afflicted:
                print(f"\n{self.name} already has a status condition...")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="burn"))]) #the odds in percent of causing paralysis
                if rng.random()<=odds/100.:
                    self.burned=True
                    print(f"\n{self.name} is burned by the hit!")
                    micropause()
        #poison
        if "pois" in notes:
            if (7 in self.tipe) or (16 in self.tipe): #poison and steel types immune
                print(f"\n{self.name} is immune to being poisoned!")
            elif mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif afflicted:
                print(f"\n{self.name} already has a status condition...")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="pois"))]) #the odds in percent of causing paralysis
                if rng.random()<=odds/100.:
                    self.poisoned=True
                    print(f"\n{self.name} is poisoned by the hit!")
                    micropause()
        #who's gonna do badly poisoned lol
        #me ugh
        if "badPois" in notes:
            if (7 in self.tipe) or (16 in self.tipe): #poison and steel types immune
                print(f"\n{self.name} is immune to being poisoned!")
            elif mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif afflicted:
                print(f"\n{self.name} already has a status condition...")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="badPois"))]) #the odds in percent of causing paralysis
                if rng.random()<=odds/100.:
                    self.badlypoisoned=True
                    self.poisonCounter=1
                    print(f"\n{self.name} is badly poisoned by the hit!")
                    micropause()
        #sleep
        if "sleep" in notes:
            electricCheck=(self.field.terrain=="electric") and self.grounded #electric terrain prevents sleep
            if electricCheck:
                print(f"\nThe electricity keeps {self.name} awake!")
            elif mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif afflicted:
                print(f"\n{self.name} already has a status condition...")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="sleep"))])
                if rng.random()<=odds/100.:
                    self.sleep=True
                    self.sleepCounter=rng.integers(1,4)
                    print(f"\n{self.name} falls asleep!")
                    micropause()
        #freeze
        if "frze" in notes:
            if self.field.weather=='sunny': #harsh sunlight prevents freezing
                print("\nThe harsh sunlight prevents freezing!")
            elif 5 in self.tipe: #ice types immune to freeze
                print(f"\n{self.name} is immune to being frozen!")
            elif mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif afflicted:
                print(f"\n{self.name} already has a status condition...")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="frze"))])
                if rng.random()<=odds/100.:
                    self.frozen=True
                    print(f"\n{self.name} is frozen in place!")
                    micropause()
        #confusion
        if "conf" in notes:
            if mistyCheck:
                print("\nThe mist prevents status conditions!")
            elif self.confused:
                print(f"\n{self.name} is already confused!")
            else:
                odds=int(notes[1+int(np.argwhere(np.array(notes)=="conf"))])
                if rng.random()<=odds/100.:
                    self.confused=True
                    self.confusionCounter=rng.integers(2,6)
                    print(f"\n{self.name} is confused now!")
                    micropause()
                #more status move effects
        return
    
    #pokemon move
    #aa:movefunction
    def move(self, opponent, moveIndex):
        global acevStages
        moveI=getMoveInfo(moveIndex)
        notas=moveI['notes'].split()
        #frozen, can't move #thinking out loud: maybe we should track
        if self.frozen:  #when a pokemons move fails/doesn't execute for whatever reason
            if "thaws" in notas:
                self.frozen=False
                print(f"\n{self.name} thaws itself out!")
            elif rng.random()<0.2: #user thaws and can move
                self.frozen=False
                print(f"\n{self.name} thaws out!")
            else:
                print(f"\n{self.name} is frozen and can't move!")
                self.rolling_out = 0
                self.charged=False
                self.flying=False
                self.digging=False
                self.diving=False
                self.shadowing=False
                return #end move() user still frozen
        #asleep, can't move
        if self.sleep:
            self.sleepCounter-=1
            if self.sleepCounter==0:
                self.sleep=False
                print(f"\n{self.name} wakes up!")
            else:
                print(f"\n{self.name} is fast asleep!")
                self.rolling_out = 0
                self.charged=False
                self.flying=False
                self.digging=False
                self.diving=False
                self.shadowing=False
                return
        #paralysis prevents move execution
        if self.paralyzed:
            if rng.random()<0.25:
                print(f"\n{self.name} is fully paralyzed!")
                self.rolling_out = 0
                self.charged=False
                self.flying=False
                self.digging=False
                self.diving=False
                self.shadowing=False
                return
        #confusion prevents rest of move execution
        if self.confused:
            #lower confusion counter for chance to snap out of confusion
            self.confusionCounter-=1
            #if counter is at 0, undo confusion
            if self.confusionCounter==0:
                self.confused=False
                print(f"{self.name} snaps out of confusion!")
            #if still confused, chance to hurt self, end move()
            else:
                print(f"\n{self.name} is confused!")
                if rng.random()<1/3:
                    self.confusionDamage()
                    self.rolling_out = 0
                    self.charged=False
                    self.flying=False
                    self.digging=False
                    self.diving=False
                    self.shadowing=False
                    return
        #check if move needs to be charged
        if "2turn" in notas:
            if self.charged: #pokemon has charged the move already
                self.charged=False #pokemon will release the move
                self.flying=False #these can go now
                self.digging=False
                self.diving=False
                self.shadowing=False
            else: #all of these will lead to a return, ending move() before anything else happens
                if "solar" in notas:
                    print(f"\n{self.name} is taking in sunlight!")
                    shortpause()
                    self.charged=True
                    if self.field.weather=="sunny": #if sun is out, continue to use the move
                        self.charged=False
                    else: #otherwise end the move
                        return
                elif "skullbash" in notas:
                    print(f"\n{self.name} tucks its head in...")
                    shortpause()
                    self.charged=True
                    self.stageChange("de",1)
                    return
                elif "geomance" in notas:
                    print(f"\n{self.name} is absorbing energy!")
                    shortpause()
                    self.charged=True
                    return
                elif 'flying' in notas:
                    print(f"\n{self.name} flies up high!")
                    self.charged = True
                    self.flying=True
                    shortpause()
                    return
                elif 'diving' in notas:
                    print(f"\n{self.name} dives underwater!")
                    self.charged = True
                    self.diving=True
                    shortpause()
                    return
                elif 'digging' in notas:
                    print(f"\n{self.name} digs underground!")
                    self.charged = True
                    self.digging=True
                    shortpause()
                    return
                elif 'shadowforce' in notas:
                    print(f"\n{self.name} vanishes into the shadows!")
                    self.charged = True
                    self.shadowing=True
                    shortpause()
                    return
                #other labels for other moves and charging contexts
        print(f"\n{self.name} uses {moveI['name']}!")
        if moveIndex!=struggle:
            self.PP[int(np.argwhere(np.array(self.knownMoves)==moveIndex))]-=1 #deduct PP for move usage
        shortpause()
        ###accuracy check##aa:accuracy#
        ## target is in semi-invulnerable turn
        #sky uppercut, twister
        ## flying hit by thousand arrows, smack down, thunder, hurricane, gust
        if opponent.flying and not (('thunder' in notas) or ('arrows' in notas) or ('gust' in notas)):
            hitCheck=False
        ## diving hit by surf and whirlpool
        elif opponent.diving and not ('surf' in notas):
            hitCheck=False
        ## digging hit by earthquake, fissure, and magnitude
        elif opponent.digging and not ('nerfGrassy' in notas):
            hitCheck=False
        ## those ghosts can't be stopped
        elif opponent.shadowing:
            hitCheck=False
        ## target is not in semi-invulnerable turn
        elif "noMiss" in notas:
            hitCheck=True
        ## moves bypass accuracy under certain conditions
        elif ('blizzard' in notas) and (self.field.weather=='hail'):
            hitCheck=True
        elif ('thunder' in notas) and (self.field.weather=='rain'):
            hitCheck=True
        else:
            #check evasion and accuracy stats
            effAccu=self.acstage-opponent.evstage+6 #get difference in evasion/accuracy stats, offset by proper center, index 6
            if effAccu>12:
                effAccu=12
            elif effAccu<0:
                effAccu=0
            effAccu=acevStages[effAccu]
            ##rain-moves in sun get accuracies tweaked
            if ('thunder' in notas) and (self.field.weather=='sunny'):
                hitCheck = rng.random() <= effAccu * ( 50. / 100. )
            else:
                hitCheck = rng.random() <= effAccu * ( moveI['accu'] / 100. )
            pass
        if hitCheck==False: #move misses
            print(f"\n{self.name}'s attack misses!")
            self.rolling_out = 0
            shortpause()
            # move failed 
            return
        else: #move will connect
            ##===========================status moves==========================##
            if moveI['special?']==2:
                ## stat changes ##
                if "stat" in notas:
                    statInfo=notas[1+int(np.argwhere(np.array(notas)=='stat'))]
                    targ,stat,phase=statInfo.split(",")[0:3]
                    stat=stat.split(":")
                    phase=phase.split(":")
                    if targ=='self':
                        if ("growth" in notas) and self.field.weather=='sunny':
                            phase=np.array([2,2],dtype=int)
                        for i in range(len(stat)):
                            self.stageChange(stat[i],int(phase[i]))
                        self.inBattle()
                    if targ=='targ':
                        for i in range(len(stat)):
                            opponent.stageChange(stat[i],int(phase[i]))
                        opponent.inBattle()
                ### end of stat changes ###
                #### defense curl, rollout boost ####
                if 'curled' in notas:
                    self.curled=True
                    print(f"{self.name} curled up!")
                ## weathers ##
                if "sun" in notas:
                    if self.field.weather=='sunny':
                        print("The move fails! It's already sunny!")
                    else:
                        self.field.weather='sunny'
                        self.field.weatherCounter=5
                        print("The sunlight turns harsh!")
                if "rain" in notas:
                    if self.field.weather=='rain':
                        print("The move fails! It's already raining!")
                    else:
                        self.field.weather='rain'
                        self.field.weatherCounter=5
                        print("It starts raining!")
                if 'sand' in notas:
                    if self.field.weather=='sandstorm':
                        print("The move fails! There's already a sandstorm!")
                    else:
                        self.field.weather='sandstorm'
                        self.field.weatherCounter=5
                        print("A sandstorm kicks up!")                
                if 'hail' in notas:
                    if self.field.weather=='hail':
                        print("The move fails! It's already hailing")
                    else:
                        self.field.weather='hail'
                        self.field.weatherCounter=5
                        print("It starts hailing!")
                ### end of the weathers ###
                ## terrains ##
                if "electric" in notas:
                    if self.field.terrain=="electric":
                        print("The move fails! The battlefield is already electrified!")
                    else:
                        self.field.terrain="electric"
                        self.field.terrainCounter=5
                        print("Electricity surges throughout the battlefield!")
                if "grassy" in notas:
                    if self.field.terrain=="grassy":
                        print("The move fails! The battlefield is already grassy!")
                    else:
                        self.field.terrain="grassy"
                        self.field.terrainCounter=5
                        print("Grass grows all over the place!")
                if "misty" in notas:
                    if self.field.terrain=="misty":
                        print("The move fails! The battlefield is already covered in mist!")
                    else:
                        self.field.terrain="misty"
                        self.field.terrainCounter=5
                        print("A mist descends on the battlefield!")
                if "psychic" in notas:
                    if self.field.terrain=="psychic":
                        print("The move fails! The battlefield is already weird!")
                    else:
                        self.field.terrain="psychic"
                        self.field.terrainCounter=5
                        print("The battlefield gets weird!")
                ## statuses bro ##
                statuses=[]
                if "para" in notas: #yeah these if statements are literally all the same besides the strings, i can for loop this
                    statuses.append("para")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="para"))]))
                if "burn" in notas:
                    statuses.append("burn")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="burn"))]))
                if "pois" in notas:
                    statuses.append("pois")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="pois"))]))
                if "badPois" in notas:
                    statuses.append("badPois")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="badPois"))]))
                if "frze" in notas:
                    statuses.append("frze")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="frze"))]))
                if "sleep" in notas:
                    statuses.append("sleep")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="sleep"))]))
                if "conf" in notas:
                    statuses.append("conf")
                    statuses.append(int(notas[1+int(np.argwhere(np.array(notas)=="conf"))]))
                if len(statuses)>0:
                    opponent.afflictStatuses(statuses)
                ## entry hazards oh boy oh geeze ##
                hazs = ("rocks", "spikes", "toxspk", "sticky")
                haz_dialog = ["Pointed rocks are scattered on the opposing side!", "Pointy spikes are scattered on the opposing side!",\
                        "Poison spikes are scattered on the opposing side!", "The opposing side is covered in a sticky web!"]
                for i in range(len(hazs)):
                    if hazs[i] in notas: #i know theres a better way to do this but if i sit here and fixate on that before i start a rough draft i'm never gonna get anywhere
                        if self.battlespot=="red": #user's pokemon
                            xx = self.field.hazarding(hazs[i], "blue")
                        elif self.battlespot=="blue": #cpu
                            xx = self.field.hazarding(hazs[i], "red")
                        if xx == "x": #makes sure hazard was executed successfully before printing the dialog
                            print(haz_dialog[i])
                ### end of entry hazards ###
                ## healing ## heal pulse? healing the target instead of the user, in the future
                if 'heals' in notas:
                    if 'recover' in notas:
                        healamount = self.maxhp/2.
                    if 'synthesis' in notas:
                        if (self.field.weather == 'rain') or (self.field.weather == 'sandstorm') or (self.field.weather == 'hail'):
                            healamount = self.maxhp/4.
                        elif self.field.weather == 'sunny':
                            healamount = 2.*self.maxhp/3.
                        else:
                            healamount = self.maxhp/2.
                    self.healing(healamount)
                ### end of healing ###
                if ('veil' in notas) and (self.field.weather != 'hail'):
                    print("The move fails! There isn't enough hail...")
                    micropause()
                    return
                ## screens ##
                screenz = ("reflect","lightscreen","veil")
                for i in range(len(screenz)):
                    if screenz[i] in notas:
                        if self.battlespot=='red':
                            self.field.upScreens(screenz[i], 'red')
                        elif self.battlespot=='blue':
                            self.field.upScreens(screenz[i], 'blue')
                        pass
                    #end if, if not, move on
                ### end of screens ###
                ## aqua ring ##
                if 'aquaring' in notas:
                    if self.aquaring:
                        print(f"The move fails! {self.name} already has an Aqua Ring...")
                    else:
                        self.aquaring=True
                        print(f"{self.name} is covered by a veil of water!")
                ### end of a ring ###
                #what's next
                return
            ##==========================    end of status moves    =======================================##
            #fake out fails if its the not pokemons first turn out
            if ('fakeout' in notas) and (not self.firstturnout):
                print('The move fails!')
                return
            # catching use and set up of future sight
            if ('futuresight' in notas):
                # set up a future sight attack to be executed in 2 turns
                # so my idea is that the counters will start at 3, be reduced by 1
                #at the end of every turn. They should be at 0 at the right time, we'll
                #do the check after the deduction 
                if self.battlespot=='red':
                    if self.field.futuresA > 0.: #user fails, fs already up
                        print("The move fails!")
                        shortpause()
                        return "failed"
                    else:
                        self.field.futuresA = 3
                        print(f"{self.name} foresaw an attack!")
                        shortpause()
                        return
                elif self.battlespot=='blue':
                    if self.field.futuresB > 0.: #cpu fails, fs already up
                        print("The move fails!")
                        shortpause()
                        return "failed"
                    else:
                        self.field.futuresB = 3
                        print(f"{self.name} foresaw an attack!")
                        shortpause()
                        return
            ans,eff,comment=damage(self,opponent,moveI['pwr'],moveI['type'],moveI['special?'],notas)
            if len(comment)>0: 
                if comment[0] == "failed": #bad mirror coat or counter
                    print("The move fails!")
                    shortpause()
                    return
            opponent.hit(self,ans,eff,notas,moveIndex,comment)
            #stat changes
            if "stat" in notas:
                statInfo=notas[1+int(np.argwhere(np.array(notas)=='stat'))]
                prob=int(statInfo.split(",")[3])/100.
                if rng.random()<=prob:
                    targ,stat,phase=statInfo.split(",")[0:3]
                    stat=stat.split(":")
                    phase=phase.split(":")
                    if targ=='self':
                        for i in range(len(stat)):
                            self.stageChange(stat[i],int(phase[i]))
                        self.inBattle() #recalc battle stats
                    if targ=='targ':
                        for i in range(len(stat)):
                            opponent.stageChange(stat[i],int(phase[i]))
                        opponent.inBattle() #recalc battle stats
                #end of stat changes
            #anything else to do after a successful hit?
        #anything else to do after either moving or missing?
        #end of move
    #zz:movefunction
    #aa:hitfunction
    def hit(self,attacker,damagepoints,effectiveness,notes,move_index,comments):
        global mov
        moveTipe = mov[move_index]['type']
        if effectiveness==0. and not ('arrows' in notes):
            print(f"{self.name} is immune!")
        else:
            if ('arrows' in notes) and (not self.grounded or self.flying): #will need to further generalize for smack down?
                print(f"The arrows can reach {self.name}!")
                self.grounded=True
                self.flying=False
                self.charged=False #canceling fly and bounce
                self.field.grounding(self)
                effectiveness=1.0
            print(f"\n{self.name} is hit!")
            micropause()
            #with a successful hit from rollout, the attacker rolling out counter increases
            if ('rollout' in notes):
                attacker.rolling_out+=1
                if attacker.rolling_out==5:
                    attacker.rolling_out=0 #pokemon is all rolled out,
                pass
            #with a successful hit from fusion move, set flag
            if ('fusion-b' in notes):
                self.field.fusionb=True
            if ('fusion-f' in notes):
                self.field.fusionf=True
            #with successful hit from brick break, break active screens
            screens_up = np.count_nonzero(( self.field.checkScreen(self.battlespot,'reflect'), \
                    self.field.checkScreen(self.battlespot,'lightscreen'), self.field.checkScreen(self.battlespot,'veil') ))
            if (screens_up >= 1.) and ('breakScreens' in notes):
                if (self.battlespot=='red'):
                    self.field.reflectACounter=0
                    self.field.lightscACounter=0
                    self.field.veilACounter=0
                    micropause()
                    print("It broke the screen(s)!")
                elif (self.battlespot=='blue'):
                    self.field.reflectBCounter=0
                    self.field.lightscBCounter=0
                    self.field.veilBCounter=0
                    micropause()
                    print("It broke the screen(s)!")
            #calculate potential recoil damage before currenthp is changed
            if damagepoints>self.currenthp:
                recoilDmg=self.currenthp
            else:
                recoilDmg=damagepoints
            #lose HP
            self.currenthp-=damagepoints
            self.currenthpp=100*self.currenthp/self.maxhp
            #show all the damage boosts
            for i in comments:
                micropause() #for drama
                print(f"{i}")
            micropause()
            #show effectiveness
            if effectiveness>2.:
                print("It's MEGA-effective!!")
            if effectiveness<=2. and effectiveness>1.:
                print("It's super-effective!")
            if effectiveness<0.5 and effectiveness>0.:
                print("It's barely effective...")
            if effectiveness>=0.5 and effectiveness<1.:
                print("It's not very effective.")
            micropause()
            #result of hit
            print(f"{self.name} lost {format(100*damagepoints/self.maxhp,'.2f')}% HP!")
            shortpause()
            #check for faint
            if self.currenthp<=0.:
                self.faint()
            else:
                print(f"{self.name} has {format(self.currenthpp,'.2f')}% HP left!")
                shortpause()
                ### setting counter/mirror coat damage data info
                if mov[move_index]['special?'] == 1:
                    self.counter_damage = (damagepoints, "spec")
                else:
                    self.counter_damage = (damagepoints, "phys")
                #status conditions
                #statuses bro
                statuses=[]  #hey, hear me out, what if we made a numpy array out of these strings, "para" "burn" etc., and used numpy tricks to do all
                if "para" in notes:    #these lines, but like in one shot
                    statuses.append("para")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="para"))]))
                if "burn" in notes:
                    statuses.append("burn")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="burn"))]))
                if "pois" in notes:
                    statuses.append("pois")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="pois"))]))
                if "badPois" in notes:
                    statuses.append("badPois")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="badPois"))]))
                if "frze" in notes:
                    statuses.append("frze")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="frze"))]))
                if "sleep" in notes:
                    statuses.append("sleep")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="sleep"))]))
                if "conf" in notes:
                    statuses.append("conf")
                    statuses.append(int(notes[1+int(np.argwhere(np.array(notes)=="conf"))]))
                if len(statuses)>0:
                    self.afflictStatuses(statuses)
                #end of status conditions
                #flinching, should only happen if pokemon didnt faint
                if "flinch" in notes:
                    flinChance=int(notes[1+int(np.argwhere(np.array(notes)=="flinch"))])
                    if rng.random()<=flinChance/100.:
                        self.flinch()
                    #end of flinching
                #thaw for fire moves
                if self.frozen and moveTipe==1:
                    self.frozen=False
                    print(f"The Fire-type move thaws {self.name} out!")
                #anything else to do after not fainting?
            #check for recoil, apply recoil if present
            if "recoil" in notes:
                amnt=notes[1+int(np.argwhere(np.array(notes)=="recoil"))]
                if amnt=="1/3":
                    attacker.recoil(recoilDmg,1./3.)
                elif amnt=="1/4":
                    attacker.recoil(recoilDmg,1./4.)
                elif amnt=="1/4maxhp":
                    attacker.recoil(attacker.maxhp,1./4.)
                #more possible recoil amounts?
            #recoil belongs in hit, because it doesn't happen if the target is immune to the hit()
            #setting need to rest
            if "mustRest" in notes:
                attacker.resting=True
        #end of hit()
    #zz:hitfunction
    #healing via moves
    def healing(self, amount):
        self.currenthp += amount
        print(f"{self.name} heals {format(100.*amount/self.maxhp,'.2f')}% HP!")
        if self.currenthp > self.maxhp:
            self.currenthp = self.maxhp
        self.currenthpp = 100. * self.currenthp/self.maxhp
    def aquaheal(self):
        amnt = np.floor(self.maxhp/16.)
        print(f"{self.name} is healed by its Aqua Ring!")
        self.healing(amnt)
    #flinching
    def flinch(self):
        self.flinched=True
    #recoil, gonna experiment with spacing here I guess whatever
    def recoil(self, damagedone, recoilAmount):
        self.currenthp -= damagedone * recoilAmount
        self.currenthpp = 100. * self.currenthp / self.maxhp
        print( f"{self.name} takes recoil damage!" )
        micropause()
        if self.currenthp <= 0.:
            self.faint()
        #i don't hate it
    #futureSightAttack
    def futureSight(self,target):
        global futuresight_i
        global mov
        notes = mov[futuresight_i]["notes"]
        print(notes)
        ans,eff,comment = damage(self,target,120,10,1,notes)
        print(f"{target.name} took the Future Sight attack!")
        shortpause()
        target.hit(self,ans,eff,notes,futuresight_i,comment)
        return
        #um
    #confusion
    def confusionDamage(self):
        dmg = (((( 2. * self.level ) / 5. + 2.) * 40. * self.bat / self.bde) / 50. + 2. ) * (rng.integers(85,101)*0.01)
        self.currenthp -= dmg
        self.currenthpp = 100. * self.currenthp / self.maxhp
        print( f"{self.name} hurt itself in its confusion!" )
        micropause()
        if self.currenthp <= 0.:
            self.faint()
    #poison
    def poisonDamage(self):
        self.currenthp-=self.maxhp/8.
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took poison damage!")
        micropause()
        if self.currenthp<=0.:
            self.faint()
    #badly poisoned
    def badPoison(self):
        self.currenthp-=self.poisonCounter*self.maxhp/16.
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took bad poison damage!")
        micropause()
        if self.currenthp<=0.0:
            self.faint()
    #burn
    def burnDamage(self):
        #would be the same as poisonDamage tbh
        self.currenthp-=self.maxhp/8.
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took burn damage!")
        micropause()
        if self.currenthp<=0.:
            self.faint()
    #sandstorm
    def sandDamage(self):
        immune=(12 in self.tipe) or (8 in self.tipe) or (16 in self.tipe) #check for rock, ground, and steel types
        if immune:
            print(f"{self.name} is unaffected by the sandstorm!")
            micropause()
        else:
            self.currenthp-=self.maxhp/16.
            self.currenthpp=100*self.currenthp/self.maxhp
            print(f"{self.name} took some damage from the sandstorm!")
            micropause()
            if self.currenthp<=0.:
                self.faint()
    #hail
    def hailDamage(self):
        if 5 in self.tipe:
            print(f"{self.name} is unaffected by the hail!")
            micropause()
        else:
            self.currenthp-=self.maxhp/16.
            self.currenthpp=100*self.currenthp/self.maxhp
            print(f"{self.name} took some damage from the hail!")
            micropause()
            if self.currenthp<=0.:
                self.faint()
    #healing from grassy terrain
    def grassyHeal(self):
        if self.currenthp==self.maxhp:
            return #do nothing, say nothing
        else:
            mount = self.maxhp/16.
            self.currenthp+=mount
            print(f"{self.name} is healed {format(100.*mount/self.maxhp,'.2f')}% by the grassy terrain!")
            micropause()
            if self.currenthp>self.maxhp: #lets not heal above the max lol
                self.currenthp=self.maxhp
                self.currenthpp=100.
            else:
                self.currenthpp=100.*self.currenthp/self.maxhp
    #entry hazard damages
    #guess we should check for faint after entry hazard damage
    #stealthrock
    def rocksDamage(self):
        self.currenthp-=self.maxhp/8.*checkTypeEffectiveness(12, self.tipe)
        print(f"Pointed stones dig into {self.name}!")
        micropause()
        if self.currenthp<=0.:
            self.faint()
        else:
            self.currenthpp=100.*self.currenthp/self.maxhp
    def spikesDamage(self,level):
        ##3 levels oop
        if level == 1:
            self.currenthp -= self.maxhp / 8.
        elif level == 2:
            self.currenthp -= self.maxhp / 6.
        elif level == 3:
            self.currenthp -= self.maxhp / 4.
        print(f"{self.name} is hurt by the spikes!")
        micropause()
        if self.currenthp<=0.:
            self.faint()
        else:
            self.currenthpp=100.*self.currenthp/self.maxhp
        
    def toxicAffliction(self,level): #1 layer of toxic spikes or two?
        #need to check for pre-existing status conditions
        if self.sleep or self.frozen or self.paralyzed or self.burned or self.poisoned or self.badlypoisoned:
            #pokemon already has status condition, no poisoning
            return
        if level == 1:
            self.poisoned=True
            print(f"{self.name} is poisoned by the spikes!")
            micropause()
            return
        elif level == 2:
            self.badlypoisoned=True
            self.poisonCounter=1
            print(f"\n{self.name} is badly poisoned by the spikes!")
            micropause()
            return
        
    def stickyNerf(self):
        self.stageChange('sp', -1)
        print(f"{self.name} is slowed down by the web!")
        return
    
    def checkup(self):
        global typeStrings
        print(f"Name: {self.name} // Lv. {self.level}")
        if len(self.tipe)==1:
            print(f"{typeStrings[self.tipe[0]]}")
        if len(self.tipe)>1:
            print(f"{typeStrings[self.tipe[0]]} / {typeStrings[self.tipe[1]]}")
        print(f"Current HP: {self.currenthp}, {self.currenthp/self.maxhp*100}%")
        
    def summary(self):
        global typeStrings, nature_stat_str
        print(f"\n############ {self.name} ############")
        if self.dualType:
            print(f"\nLevel {self.level} \t{typeStrings[self.tipe[0]]} // {typeStrings[self.tipe[1]]}")
        else:
            print(f"\nLevel {self.level} \t{typeStrings[self.tipe[0]]}")
        if self.null_nature == False:
            print(f"Nature : {self.nature_str} | Up - {nature_stat_str[self.nature[0]]}, Down - {nature_stat_str[self.nature[1]]}")
        else:
            print(f"Nature : {self.nature_str} | Up - None, Down - None")
        print(f"HP  : \t{format(self.currenthp,'.2f')}/{format(self.maxhp,'.2f')} \t{format(self.currenthpp,'.2f')}%")
        print(f"Atk : \t{format(self.attack,'.2f')}")
        print(f"Def : \t{format(self.defense,'.2f')}")
        print(f"Sp.A: \t{format(self.spatk,'.2f')}")
        print(f"Sp.D: \t{format(self.spdef,'.2f')}")
        print(f"Spe : \t{format(self.speed,'.2f')}")
        self.showMoves()
        print("##############################################")
        
    def battleSummary(self):
        global typeStrings,nature_stat_str
        print(f"\n############ {self.name} ############")
        if self.dualType:
            print(f"\nLevel {self.level} \t{typeStrings[self.tipe[0]]} // {typeStrings[self.tipe[1]]}")
        else:
            print(f"\nLevel {self.level} \t{typeStrings[self.tipe[0]]}")
        if self.null_nature == False:
            print(f"Nature : {self.nature_str} | Up - {nature_stat_str[self.nature[0]]}, Down - {nature_stat_str[self.nature[1]]}")
        else:
            print(f"Nature : {self.nature_str} | Up - None, Down - None")
        print(f"HP  : \t{format(self.currenthp,'.2f')}/{format(self.maxhp,'.2f')} \t{format(self.currenthpp,'.2f')}%")
        print(f"Atk : \t{format(self.bat,'.2f')}")
        print(f"Def : \t{format(self.bde,'.2f')}")
        print(f"Sp.A: \t{format(self.bsa,'.2f')}")
        print(f"Sp.D: \t{format(self.bsd,'.2f')}")
        print(f"Spe : \t{format(self.bsp,'.2f')}")
        print("\n** These stats reflect in-battle boosts and nerfs **")
        self.showMoves()
        print("##############################################")
    
    def showMoves(self):
        global typeStrings,mov
        print(f"############ {self.name}'s Moves #############")
        for i in range(len(self.knownMoves)):
            print(f"[{i+1}] {mov[self.knownMoves[i]]['name']}\t{typeStrings[int(mov[self.knownMoves[i]]['type'])]}\t{self.PP[i]}/{mov[self.knownMoves[i]]['pp']} PP")
        return
    #show evs and ivs
    def appraise(self):
        ez=[self.hpev,self.atev,self.deev,self.saev,self.sdev,self.spev]
        iz=[self.hpiv,self.ativ,self.deiv,self.saiv,self.sdiv,self.spiv]
        st=["HP  :","Atk :","Def :","Sp.A:","Sp.D:","Spe :"]
        print(f"\n############ {self.name} ############")
        print("\n     \tIV\tEV")
        for i in range(len(st)):
            print(f"{st[i]}\t{iz[i]}\t{ez[i]}")
        print("------------------------")
    #anymore pokemon attributes?
#zz:monclass
#aa:battleclass
class battle:
    def __init__(self, usr_party, cpu_party, fields, usr_name='You', cpu_name='OPPONENT'):
        ###can i get a uhhhhhhh
        self.usr_name = usr_name
        self.cpu_name = cpu_name
        self.usrs = usr_party
        self.cpus = cpu_party
        self.usr_mon = usr_party[0]
        self.cpu_mon = cpu_party[0]
        self.field = fields
        self.user_won = False

    #check status of battle
    #this needs to go IN battle()
    def checkBattle(self):
        global typeStrings
        print(f"\n****** {self.cpu_mon.name} ({self.cpu_name}) ******")
        if self.cpu_mon.dualType:
                print(f"{typeStrings[self.cpu_mon.tipe[0]]} // {typeStrings[self.cpu_mon.tipe[1]]}")
        else:
            print(f"{typeStrings[self.cpu_mon.tipe[0]]}")
        #should be all status conditions
        if self.cpu_mon.poisoned:
            print("__ POISONED __")
        elif self.cpu_mon.badlypoisoned:
            print("__ BADLY POISONED __")
        elif self.cpu_mon.burned:
            print("__ BURNED __")
        elif self.cpu_mon.paralyzed:
            print("__ PARALYZED __")
        elif self.cpu_mon.frozen:
            print("__ FROZEN __")
        elif self.cpu_mon.sleep:
            print("__ ASLEEP __")
        if self.cpu_mon.confused:
            print("** confused **")
        #show hp
        if self.cpu_mon.currenthpp>=91:
            print(f"HP |############| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<91 and self.cpu_mon.currenthpp>=82:
            print(f"HP |###########.| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=82 and self.cpu_mon.currenthpp>75:
            print(f"HP |##########..| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=75 and self.cpu_mon.currenthpp>66:
            print(f"HP |#########...| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=66 and self.cpu_mon.currenthpp>58:
            print(f"HP |########....| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=58 and self.cpu_mon.currenthpp>50:
            print(f"HP |#######.....| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=50 and self.cpu_mon.currenthpp>41:
            print(f"HP |######......| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=41 and self.cpu_mon.currenthpp>33:
            print(f"HP |#####.......| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=33 and self.cpu_mon.currenthpp>25:
            print(f"HP |####........| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=25 and self.cpu_mon.currenthpp>16:
            print(f"HP |###.........| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=16 and self.cpu_mon.currenthpp>8:
            print(f"HP |##..........| {format(self.cpu_mon.currenthpp,'.2f')}%")
        if self.cpu_mon.currenthpp<=8 and self.cpu_mon.currenthpp>0:
            print(f"HP |#...........| {format(self.cpu_mon.currenthpp,'.2f')}%")
        #stat boosts
        blueStats=[self.cpu_mon.atstage-6,self.cpu_mon.destage-6,self.cpu_mon.sastage-6, \
                   self.cpu_mon.sdstage-6,self.cpu_mon.spstage-6,self.cpu_mon.acstage-6, \
                       self.cpu_mon.evstage-6]
        statstrs=["Atk :","Def :","Sp.A:","Sp.D:","Spd :","Accu:","Evas:"]
        print("\nStat Boosts and Nerfs\n****************************")
        for i in range(len(blueStats)):
            if blueStats[i]==0:
                print(statstrs[i]+" none")
            elif blueStats[i]>0:
                print(statstrs[i]+f" +{blueStats[i]}")
            elif blueStats[i]<0:
                print(statstrs[i]+f" {blueStats[i]}")
        ## is there a screen up
        walls = (self.field.reflectBCounter, self.field.lightscBCounter, self.field.veilBCounter)
        #print(walls)
        prii = (f"\n=== Reflect Up : {self.field.reflectBCounter} ===", f"\n=== Light Screen Up : {self.field.lightscBCounter} ===",f"\n=== Aurora Veil Up : {self.field.veilBCounter} ===")
        for i in list(enumerate(walls)):
            if i[1]>0:
                print(prii[i[0]])
            pass
        print("------------------------------------")
        print(f"************ {self.usr_mon.name} (You) ************")
        if self.usr_mon.dualType:
                print(f"{typeStrings[self.usr_mon.tipe[0]]} // {typeStrings[self.usr_mon.tipe[1]]}")
        else:
            print(f"{typeStrings[self.usr_mon.tipe[0]]}")
        #should be all status conditions
        if self.usr_mon.poisoned:
            print("__POISONED__")
        elif self.usr_mon.badlypoisoned:
            print("__BADLY_POISONED__")
        elif self.usr_mon.burned:
            print("__BURNED__")
        elif self.usr_mon.paralyzed:
            print("__PARALYZED__")
        elif self.usr_mon.frozen:
            print("__FROZEN__")
        elif self.usr_mon.sleep:
            print("__ASLEEP__")
        if self.usr_mon.confused:
            print("**confused**")
        #show hp
        if self.usr_mon.currenthpp>=91:
            print(f"HP |############| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<91 and self.usr_mon.currenthpp>=82:
            print(f"HP |###########.| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=82 and self.usr_mon.currenthpp>75:
            print(f"HP |##########..| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=75 and self.usr_mon.currenthpp>66:
            print(f"HP |#########...| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=66 and self.usr_mon.currenthpp>58:
            print(f"HP |########....| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=58 and self.usr_mon.currenthpp>50:
            print(f"HP |#######.....| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=50 and self.usr_mon.currenthpp>41:
            print(f"HP |######......| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=41 and self.usr_mon.currenthpp>33:
            print(f"HP |#####.......| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=33 and self.usr_mon.currenthpp>25:
            print(f"HP |####........| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=25 and self.usr_mon.currenthpp>16:
            print(f"HP |###.........| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=16 and self.usr_mon.currenthpp>8:
            print(f"HP |##..........| {format(self.usr_mon.currenthpp,'.2f')}%")
        if self.usr_mon.currenthpp<=8 and self.usr_mon.currenthpp>0:
            print(f"HP |#...........| {format(self.usr_mon.currenthpp,'.2f')}%")
        #stat boosts
        redStats=[self.usr_mon.atstage-6,self.usr_mon.destage-6,self.usr_mon.sastage-6,self.usr_mon.sdstage-6,self.usr_mon.spstage-6,self.usr_mon.acstage-6,self.usr_mon.evstage-6]
        print("\nStat Boosts and Nerfs\n****************************")
        for i in range(len(redStats)):
            if redStats[i]==0:
                print(statstrs[i]+" none")
            elif redStats[i]>0:
                print(statstrs[i]+f" +{redStats[i]}")
            elif redStats[i]<0:
                print(statstrs[i]+f" {redStats[i]}")
        ## is there a screen up
        halls = (self.field.reflectACounter, self.field.lightscACounter, self.field.veilACounter)
        drii = (f"\n=== Reflect Up : {self.field.reflectACounter} ===", f"\n=== Light Screen Up : {self.field.lightscACounter} ===",f"\n=== Aurora Veil Up : {self.field.veilACounter} ===")
        for i in list(enumerate(halls)):
            if i[1]>0:
                print(drii[i[0]])
            pass
        print("------------------------------------")
        print("-------Battle Settings-------")
        if self.field.weather=="clear":
            weat="CLEAR"
        elif self.field.weather=="sunny":
            weat="SUNNY"
        elif self.field.weather=="rain":
            weat="RAINING"
        elif self.field.weather=="sandstorm":
            weat="SANDSTORM"
        elif self.field.weather=="hail":
            weat="HAILING"
        print(f"Weather : {weat}")
        if self.field.terrain=="none":
            terr="NONE"
        elif self.field.terrain=="grassy":
            terr="GRASSY"
        elif self.field.terrain=="electric":
            terr="ELECTRIC"
        elif self.field.terrain=="psychic":
            terr="PSYCHIC"
        elif self.field.terrain=="misty":
            terr="MISTY"
        print(f"Terrain : {terr}")
        print("\n___ End of battle status ___")


    def startbattle(self):
        ####Battle starts####
        print(f"\n{self.cpu_name} has challenged you to a Pokemon Battle!")
        dramaticpause()
        #userMon=self.usrs[0]
        #self.cpu_mon=self.cpus[0]
        userInd=0
        trainerInd=0
        print(f"\n{self.usr_mon.name}! I choose you!")
        shortpause()
        print(f"\n{self.cpu_name}: {self.cpu_mon.name}! Go!")
        shortpause()
        turn=1
        #### turn begins ####
        while 1: #only breaks when BattleOver is True
            #battle conditions?
            battleOver=False
            #emerald = field()
            self.usr_mon.chosen("user",self.field)
            self.cpu_mon.chosen("cpu",self.field)
            ####fight/run/pokemon/bag####
            while 1: #turn loop, advances to pokemon move exchange if user selects a move or shifts, otherwise we should loop back here
                switching=False
                fighting=False
                charging=False
                print(f"\n================ Turn {turn} ================\n")
                
                self.usr_mon.inBattle()
                self.cpu_mon.inBattle()
                #----UI----#
                print(f"\n{self.cpu_name}:\n{self.cpu_mon.name} // Level {self.cpu_mon.level}")
                print(f"HP: {format(self.cpu_mon.currenthpp,'.2f')}%")
                print("\n............Your team:")
                print(f"............{self.usr_mon.name} // Level {self.usr_mon.level}")
                print(f"............HP: {format(self.usr_mon.currenthp,'.2f')}/{format(self.usr_mon.maxhp,'.2f')} ({format(self.usr_mon.currenthpp,'.2f')}%)")
                ## if the usrs pokemon has their resting flag from a mustRest move, usr cant move (unless their move missed...
                if self.usr_mon.resting:    #or the target is immune.... more work)
                    resting=True
                    charging=False
                    print(f"\n{self.usr_mon.name} is recharging and can't move...")
                    shortpause()
                ## if the usrs pokemon is already committed to a move, and it was just charging it...
                elif self.usr_mon.charged:
                    charging=True
                    resting=False
                ## if the usr is locked into rollout
                elif self.usr_mon.rolling_out>0:
                    charging=False
                    resting=False
                    fighting=True
                    pass
                ## the usr will select a move, or send out another pokemon
                else:
                    resting=False
                    charging=False
                    userMove=input(f"What should {self.usr_mon.name} do?\n[F]ight\n[P]okemon\n[S]tatus\n[R]un\n: ")
                    #### run away to end battle ####
                    if userMove=='r' or userMove == 'R':
                        print(f"{self.usr_name} and {self.usr_mon.name} get away safely!")
                        battleOver=True
                        break #break the otherwise indefinite turn-loop, ending the battle
                    #### check status of battle? ####
                    if userMove=="s" or userMove=="S":
                        self.checkBattle()
                        input("enter anything to go back...")
                    #### go party pokemon ####
                    if userMove=='p' or userMove == 'P':
                        while 1: #a little input loop, for your party, 
                            print("\n////////////////////////////////\n//////// Party Pokemon /////////\n////////////////////////////////")
                            ## show the player's pokemon
                            for i in range(len(self.usrs)):
                                print(f"[{i+1}] {self.usrs[i].name} \tLv. {self.usrs[i].level} \tHP: {format(self.usrs[i].currenthpp,'.2f')}%")
                            partyChoice=input("Select a Pokemon...\n[#] or [b] to go back: ")
                            if partyChoice=='b' or partyChoice=="B":
                                break #goes back to user turn loop from pokemon selection
                            try:
                                select=self.usrs[int(partyChoice)-1]
                                nuserInd=int(partyChoice)-1
                                select.battleSummary()
                            except ValueError: #will print warning, and restart the party loop without seeing a pokemon
                                print("\nEnter the [#] corresponding to a Pokemon!\nor [b]ack")
                            except IndexError:
                                print("\nEnter the [#] corresponding to a Pokemon!\nor [b]ack")
                            else:
                                ### looking at a pokemon in the party ###
                                while 1: 
                                    pChoice=input(f"What to do with {select.name}?\n[s]hift into battle, see [m]oves, or [b]ack: ")
                                    ## go back
                                    if pChoice=="b" or pChoice=="B":
                                        break #breaks the singular pokemon loop and back to the party
                                    ## show move details
                                    if pChoice=="m" or pChoice=="M":
                                        while 1: #move input loop for displaying move info
                                            print("")
                                            select.showMoves()
                                            movChoice=input("Which move(s) to look at?\n[#] or [b]ack: ")
                                            if movChoice=="b" or movChoice=="B":
                                                #leave move info selection, back to what to do w pokemon
                                                break
                                            #try to get numbers from user input
                                            try:
                                                movez=movChoice.split() #pokemon movelist index (string)
                                                movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                                movez=[select.knownMoves[i] for i in movez] #pokemon move movedex index
                                            except ValueError:
                                                print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                                            except IndexError:
                                                print("\n** Use the indices to select moves to take a closer look at. **")
                                            else:
                                                for i in range(len(movez)):
                                                    print("")
                                                    moveInfo(movez[i])
                                                    micropause()
                                                #we got all the move info out?, go back to pokemon?
                                                #pause the code for reading purposes
                                                input("\nEnter anything to go back to Pokemon summary...")
                                                break #bacl to pokemon summary
                                            #move info contents
                                        #
                                    #switch pokemon
                                    if pChoice=="s" or pChoice=="S":
                                        #keep fainted pokemon off the field
                                        if select.fainted:
                                            print("\n** Cannot switch in fainted Pokemon! **")
                                            break #back to party
                                        if nuserInd==userInd:
                                            print(f"\n** {select.name} is already in battle! **")
                                            break #bacl to party
                                        switching=True
                                        break
                                    #anything other than approved things repeat the loop
                                if switching:
                                    break #breaks the party loop and throws you back into the turn loop, user will switch pokemon
                            #end of pokemon selection loop
                        #end of party pokemon block
                        #just dawned on me that user pokemon switching does not need to take place entirely in this if statement
                    #fight
                    if userMove=='f':                    
                        #fighting options
                        while 1: #move input loop
                            for i in range(len(self.usr_mon.knownMoves)):
                                print(f"[{i+1}] \t{getMoveInfo(self.usr_mon.knownMoves[i])['name']} \t{self.usr_mon.PP[i]} PP")
                            if np.count_nonzero(self.usr_mon.PP)==0:
                                print(f"{self.usr_mon.name} can only Struggle!")
                                fighting=True
                                moveDex=struggle_i
                                break
                            userFight=input(f"What move should {self.usr_mon.name} use?\n(Lead with 'i' to see move info)\n[#] or [b]: ")
                            #go back
                            infom = userFight.split()
                            if userFight=='b':
                                break
                            elif len(infom)>1:
                                if userFight.split()[0]=="i" or userFight.split()[0]=="I":
                                    try:
                                        movez=userFight.split()[1:] #pokemon movelist index (string)
                                        movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                        movez=[self.usr_mon.knownMoves[i] for i in movez] #pokemon move movedex index
                                    except ValueError:
                                        print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                                    except IndexError:
                                        print("\n** Use the indices to select moves to take a closer look at. **")
                                    else:
                                        for i in range(len(movez)):
                                            print("")
                                            moveInfo(movez[i])
                                            micropause() #drama
                                        #we got all the move info out?, go back to pokemon?
                                        input("\nenter anything to continue...")
                                else: #other secret options
                                    pass
                            else:
                                #try to use user input to call a move
                                try:
                                    fightChoice=int(userFight)-1 #make sure given input refers to a move
                                    if self.usr_mon.PP[fightChoice]==0:
                                        print(f"{self.usr_mon.name} does not have enough energy to use this move!")
                                        continue
                                    moveDex=self.usr_mon.knownMoves[fightChoice]
                                    fighting=True
                                    break
                                except:
                                    print("\n**Enter one of the numbers above.**")
                                    micropause()
                    
                ####after either swithing or attacking
                if fighting or switching or resting or charging:
                    #user shifting?
                    if switching:
                        #put current pokemon back?
                        self.usr_mon.withdraw()
                        self.usrs[userInd]=self.usr_mon
                        print(f"\n{self.usr_mon.name} come back!")
                        shortpause()
                        #set new selection as user pokemon
                        self.usr_mon=select
                        userInd=nuserInd
                        print(f"{self.usr_mon.name}, it's your turn!")
                        shortpause()
                        #assign the pokemon to users side of the field
                        self.usr_mon.chosen("user",self.field)
                        # calculate the pokemon's stat's, considering the weather and status conditions
                        self.usr_mon.inBattle()
                        # apply the field to the pokemon (entry hazards)
                        self.field.landing(self.usr_mon)
                    #does the trainer mon need to rest?
                    if self.cpu_mon.resting:
                        #trainerRest=True
                        print(f"\n{self.cpu_mon.name} must recharge and cannot attack!")
                    else:
                        #trainerRest=False
                        pass
                    if self.cpu_mon.charged:
                        #trainerCharge=True
                        pass
                    else:
                        #trainerCharge=False
                        pass
                    trainerShift=False
                    #10% chance for opponent to randomly switch pokemon
                    #check how many nonfainted pokemon trainer has
                    nfp,nfpList=checkBlackout(self.cpus)
                    if nfp>1 and rng.random()<0.1 and (not self.cpu_mon.resting) and (not self.cpu_mon.charged): #if trainer has more than 1 non fainted pokemon, 10% of the time, but not if their pokemon has to recharge
                        del nfpList[int(np.argwhere(np.array(nfpList)==trainerInd))] #removing the current pokemon from the list of nonfainted pokemon in the party
                        self.cpu_mon.withdraw()
                        self.cpus[trainerInd]=self.cpu_mon #put pokemon away
                        print(f"\n{self.cpu_name}'s {self.cpu_mon.name} is withdrawn!")
                        #take new pokemon out, random
                        nTrainerInd=rng.choice(nfpList)
                        trainerInd=nTrainerInd
                        self.cpu_mon=self.cpus[trainerInd]
                        shortpause()
                        print(f"{self.cpu_name}: {self.cpu_mon.name}! Finish them off!")
                        shortpause()
                        self.cpu_mon.chosen("cpu",self.field)
                        self.cpu_mon.inBattle()
                        self.field.landing(self.cpu_mon)
                        trainerShift=True
                        #end of trainer switching
                    ########################################################
                    # if both pokemon are attacking, compare move priority #
                    # then compare pokemon speeds ##########################
                    ########################################################
                    uFaint=False
                    tFaint=False
                    flinching=False
                    ######## opponent selecting a move #######
                    if self.cpu_mon.charged:
                        pass #trainMoveInd should already be set from last round
                    elif self.cpu_mon.rolling_out>0:
                        pass #uhh same
                    else:
                        trainStruggle=False
                        cpu_ppcheck = np.argwhere(np.array(self.cpu_mon.PP) > 0)
                        if np.size(cpu_ppcheck) > 0:
                            trainMoveInd=int(rng.choice(cpu_ppcheck))
                            tmovedex = self.cpu_mon.knownMoves[trainMoveInd]
                        else: #struggle will trigger 
                            trainStruggle=True
                        pass
                    #### speed and priority check ####
                    prior_check = (getMoveInfo(moveDex)['priority'], getMoveInfo(tmovedex)['priority'])
                    if prior_check[0] == prior_check[1]:
                        #set boolean to true if user has higher effective speed stat
                        userFast=self.usr_mon.bsp>=self.cpu_mon.bsp
                    elif prior_check[0] > prior_check[1]:
                        userFast=True
                    else:
                        userFast=False
                    ##USER FASTER##
                    if userFast:
                        #USER ATTACK
                        #make sure user/trainer didn't switch in this turn
                        if fighting or charging: #is never set to true if resting is true this turn, not set to true if the user decided to switch mons
                            self.usr_mon.move(self.cpu_mon, moveDex)
                            # check for faints after 1st move used
                            if self.cpu_mon.fainted:
                                tFaint=True
                            if self.usr_mon.fainted:
                                uFaint=True
                            if self.cpu_mon.flinched and (not tFaint):
                                flinching=True
                                self.cpu_mon.rolling_out=0
                                print(f"\n{self.cpu_name}'s {self.cpu_mon.name} flinches and can't attack!")
                                shortpause()
                        ##OPPO ATTACK
                        if (not trainerShift) and (not flinching) and (not tFaint):
                            if uFaint:
                                print(f"\nThere is no target for {self.cpu_mon.name} to attack!")
                                shortpause()
                            elif trainStruggle: #np.count_nonzero(self.cpu_mon.PP)==0: #if trainer is out of PP, use struggle
                                self.cpu_mon.move(self.usr_mon,struggle_i)
                            else: #otherwise, cue up one of the known moves
                                self.cpu_mon.move(self.usr_mon,tmovedex)
                            # check for faints as result of 2nd move used
                            if self.usr_mon.fainted:
                                uFaint=True
                            if self.cpu_mon.fainted:
                                tFaint=True
                    ##USER SLOWER##
                    else:
                        ##OPPO ATTACK##
                        if (not trainerShift) and (not self.cpu_mon.resting):
                            if np.count_nonzero(self.cpu_mon.PP)==0: #if trainer is out of PP, use struggle
                                self.cpu_mon.move(self.usr_mon,struggle_i)
                            else: #otherwise, cue up one of the known moves
                                self.cpu_mon.move(self.usr_mon,tmovedex)
                            # check for faints after 1st move used
                            if self.usr_mon.fainted:
                                uFaint=True
                            if self.cpu_mon.fainted:
                                tFaint=True
                            #check for flinch
                            if self.usr_mon.flinched and (not uFaint): #make sure neither pokemon just fainted after this attack
                                flinching=True
                                self.usr_mon.rolling_out=0
                                print(f"\n{self.usr_mon.name} flinches and can't attack!")
                                micropause()
                        ##USER ATTACK##
                        if (fighting or charging) and (not flinching) and (not uFaint):
                            if tFaint:
                                print(f"\nThere is no target for {self.usr_mon.name}'s attack!")
                                shortpause()
                            else:
                                self.usr_mon.move(self.cpu_mon,moveDex)
                            # check for faints after 2nd move used
                            if self.cpu_mon.fainted:
                                tFaint=True
                            if self.usr_mon.fainted:
                                uFaint=True
                    #end of turn, pokemon have attacked
                    #turn off fusion flags
                    self.field.fusionf = False
                    self.field.fusionb = False
                    #empty counter variables
                    self.usr_mon.counter_damage = (0.0, "none")
                    self.cpu_mon.counter_damage = (0.0, "none")
                    #if poke didnt just switch in, first turn flag is turned off
                    if (not switching):
                        self.usr_mon.firstturnout=False
                    if (not trainerShift):
                        self.cpu_mon.firstturnout=False
                    #regardless of whether pokemon fainted this turn, if they were recognized to be resting while the attacks were exchanged, we can repeal the resting tags
                    if resting:
                        self.usr_mon.resting=False
                    if self.cpu_mon.resting:
                        self.cpu_mon.resting=False
                    if flinching: #moves have already been used, we can reset them
                        self.usr_mon.flinched=False
                        self.cpu_mon.flinched=False
                    #check for USER BLACKOUT
                    if checkBlackout(self.usrs)[0]==0:
                        battleOver=True
                        print("\nYou're out of usable Pokemon!")
                        shortpause()
                        print("You blacked out!")
                        shortpause()
                        break
                    #check for TRAINER BLACKOUT
                    if checkBlackout(self.cpus)[0]==0:
                        battleOver=True
                        print(f"\n{self.cpu_name} is out of usable pokemon!\nYou win!")
                        self.user_won = True
                        shortpause()
                        break
                    #print("")
                    #damages for pokemon that made it through the turn
                    ### future sight ###
                    self.field.futuresA-=1
                    self.field.futuresB-=1
                    #user foresaw this attack
                    if self.field.futuresA == 0:
                        if tFaint:
                            print("There's no target for the Future Sight attack!")
                            micropause()
                        else:
                            self.usr_mon.futureSight(self.cpu_mon)
                            if self.cpu_mon.fainted:
                                tFaint=True
                    #cpu foresaw this attack
                    if self.field.futuresB == 0:
                        if uFaint:
                            print("There's no target for the Future Sight attack!")
                            micropause()
                        else:
                            self.cpu_mon.futureSight(self.usr_mon)
                            if self.usr_mon.fainted:
                                uFaint=True
                            #
                    # I think that's all folks
                    #order of end of battle damages: burn,poison,badPoison,weather,grassy heal
                    #burns
                    if self.usr_mon.burned and (not uFaint):
                        self.usr_mon.burnDamage()
                    if self.cpu_mon.burned and (not tFaint):
                        self.cpu_mon.burnDamage()
                    #poisons
                    if self.usr_mon.poisoned and (not uFaint):
                        self.usr_mon.poisonDamage()
                    if self.cpu_mon.poisoned and (not tFaint):
                        self.cpu_mon.poisonDamage()
                    #badPoisons
                    if self.usr_mon.badlypoisoned and (not uFaint):
                        self.usr_mon.badPoison()
                        self.usr_mon.poisonCounter+=1
                    if self.cpu_mon.badlypoisoned and (not tFaint):
                        self.cpu_mon.badPoison()
                        self.cpu_mon.poisonCounter+=1
                    #weather
                    if self.field.weather=="sandstorm":
                        if (not uFaint):
                            self.usr_mon.sandDamage()
                        if (not tFaint):
                            self.cpu_mon.sandDamage()
                    if self.field.weather=="hail":
                        if (not uFaint):
                            self.usr_mon.hailDamage()
                        if (not tFaint):
                            self.cpu_mon.hailDamage()
                    #grassy terrain heal
                    #make sure we're not bringing anyone back to life after possible damages
                    if self.usr_mon.fainted:
                        uFaint=True
                    if self.cpu_mon.fainted:
                        tFaint=True
                    if self.field.terrain=="grassy":
                        if self.usr_mon.grounded and (not uFaint):
                            self.usr_mon.grassyHeal()
                        if self.cpu_mon.grounded and (not tFaint):
                            self.cpu_mon.grassyHeal()
                    # aqua ring healing
                    if self.usr_mon.aquaring and (not uFaint):
                        self.usr_mon.aquaheal()
                    if self.cpu_mon.aquaring and (not tFaint):
                        self.cpu_mon.aquaheal()
                    #make switches in case of faints
                    #user switch
                    if uFaint:
                        #check for USER BLACKOUT
                        if checkBlackout(self.usrs)[0]==0:
                            battleOver=True
                            print("\nYou're out of usable Pokemon!")
                            shortpause()
                            print("You blacked out!")
                            shortpause()
                            break
                        else:
                            bShifted=False #forcing the user to shift to a non-fainted pokemon
                            self.field.faintedA = True #if there was a faint, mark it on the field
                            while 1:
                                print("\n////////////////////////////////\n//////// Party Pokemon /////////\n////////////////////////////////")
                                for i in range(len(self.usrs)):
                                    print(f"[{i+1}] {self.usrs[i].name} \tLv. {self.usrs[i].level} \tHP: {format(self.usrs[i].currenthpp,'.2f')}%")
                                newPoke=input("Select a Pokemon for battle...\n[#]: ")
                                try:
                                    nuserInd=int(newPoke)-1
                                    select=self.usrs[nuserInd]
                                    select.battleSummary()
                                except ValueError:
                                    print("\n** Enter a [#] corresponding to a Pokemon!\nor [b]ack **")
                                except IndexError:
                                    print("\n** Enter a [#] corresponding to a Pokemon!\nor [b]ack **")
                                else:
                                    while 1: #another user input loop to loop at a pokemon
                                        sChoice=input(f"What to do with {select.name}?\n[s]hift into battle, see [m]oves, or [b]ack: ")
                                        #go back
                                        if sChoice=='b' or sChoice=="B":
                                            break
                                        if sChoice=="m" or sChoice=="M":
                                            while 1: #move input loop for displaying move info
                                                select.showMoves()    
                                                movChoice=input("Which move(s) to look at?\n[#] or [b]ack: ")
                                                if movChoice=="b" or movChoice=="B":
                                                    #leave move info selection, back to what to do w pokemon
                                                    break
                                                #try to get numbers from user input
                                                try:
                                                    movez=movChoice.split() #pokemon movelist index (string)
                                                    movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                                    movez=[select.knownMoves[i] for i in movez] #pokemon move movedex index
                                                except ValueError:
                                                    print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                                                except IndexError:
                                                    print("\n** Use the indices to select moves to take a closer look at. **")
                                                else:
                                                    for i in range(len(movez)):
                                                        print("")
                                                        moveInfo(movez[i])
                                                        micropause() #drama
                                                    #we got all the move info out?, go back to pokemon, user NEEDS to switch someone in
                                                    break 
                                        #switch pokemon
                                        if sChoice=='s' or sChoice=="S":
                                            #keep fainted pokemon off the field
                                            if select.fainted:
                                                print("** Cannot switch in fainted Pokemon! **")
                                                break
                                            if nuserInd==userInd:
                                                print("** {select.name} is already in battle! **")
                                                break
                                            #put current pokemon back?
                                            self.usr_mon.withdraw()
                                            self.usrs[userInd]=self.usr_mon
                                            print(f"\n{self.usr_mon.name} come back!")
                                            #set new selection as user pokemon
                                            self.usr_mon=select
                                            userInd=nuserInd
                                            shortpause()
                                            print(f"{self.usr_mon.name}, it's your turn!")
                                            shortpause()
                                            self.usr_mon.chosen("user",self.field)
                                            self.usr_mon.inBattle()
                                            self.field.landing(self.usr_mon)
                                            bShifted=True
                                            break
                                        #anything other than y repeats the loop
                                    if bShifted:
                                        break
                    else: #user's pokemon did not faint,
                        self.field.faintedA=False
                    #oppo switch
                    if tFaint:
                        #check for TRAINER BLACKOUT
                        blk,blkList=checkBlackout(self.cpus)
                        if blk==0:
                            battleOver=True
                            print(f"\n{self.cpu_name} is out of usable pokemon!\nYou win!")
                            self.user_won=True
                            shortpause()
                            break
                        else:
                            self.field.faintedB=True
                            #put fainted one away
                            self.cpu_mon.withdraw()
                            self.cpus[trainerInd]=self.cpu_mon
                            #take out random non fainted one
                            trainerInd=rng.choice(blkList)
                            self.cpu_mon=self.cpus[trainerInd]
                            self.cpu_mon.chosen("cpu",self.field)
                            self.cpu_mon.inBattle()
                            self.field.landing(self.cpu_mon)
                            print(f"\n{self.cpu_name}: {self.cpu_mon.name}! I'm counting on you!")
                            shortpause()
                        #
                    else:
                        self.field.faintedB=False
                    #pokemon have been switched in
                    #print("")
                    #is weather still happening
                    self.field.weatherCounter-=1
                    if self.field.weather=='sunny':
                        if self.field.weatherCounter==0:
                            self.field.weather='clear'
                            self.field.weatherCounter=np.inf
                            print("The harsh sunlight is fading...")
                            shortpause()
                        else:
                            print("The sunlight is harsh!")
                            shortpause()
                    if self.field.weather=='rain':
                        if self.field.weatherCounter==0:
                            self.field.weather='clear'
                            self.field.weatherCounter=np.inf
                            print("The rain stops...")
                            shortpause()
                        else:
                            print("It's raining!")
                            shortpause()
                    if self.field.weather=='sandstorm':
                        if self.field.weatherCounter==0:
                            self.field.weather='clear'
                            self.field.weatherCounter=np.inf
                            print("The sandstorm is subsiding...")
                            shortpause()
                        else:
                            print("The sandstorm is raging!")
                            shortpause()
                    if self.field.weather=='hail':
                        if self.field.weatherCounter==0:
                            self.field.weather='clear'
                            self.field.weatherCounter=np.inf
                            print("The hail stops")
                            shortpause()
                        else:
                            print("It's hailing!")
                            shortpause()
                    #is the terrain still on?
                    self.field.terrainCounter-=1
                    if self.field.terrainCounter==0:
                        self.field.terrain="none"
                        self.field.terrainCounter=np.inf
                        print("The terrain faded away...")
                        shortpause()
                    elif self.field.terrain=="grassy":
                        print("The battlefield is grassy!")
                        shortpause()
                    elif self.field.terrain=="electric":
                        print("The battlefield is electrified!")
                        shortpause()
                    elif self.field.terrain=="psychic":
                        print("The battlefield is weird!")
                        shortpause()
                    elif self.field.terrain=="misty":
                        print("The battlefield is misty!")
                        shortpause()
                    #print("")
                    #if nothing was set, will go from 0 to -1, and keep going negative
                    #until someone sets a screen, at which point itll be set to 5, decrease from there
                    #to 0, which we will catch and call out
                    self.field.lightscACounter-=1
                    self.field.lightscBCounter-=1
                    self.field.reflectACounter-=1
                    self.field.reflectBCounter-=1
                    self.field.veilACounter-=1
                    self.field.veilBCounter-=1
                    #are these screens still up?
                    say = ("Your team's Light Screen fades away...","Their Light Screen fades away...",\
                           "Your team's Reflect fades away...","Their Reflect fades away...", \
                           "Your team's Aurora Veil fades...","Thier Aurora Veil fades...")
                    for ee in list(enumerate((self.field.lightscACounter,self.field.lightscBCounter, self.field.reflectACounter,self.field.reflectBCounter, self.field.veilACounter,self.field.veilBCounter))) :
                        #print([ee[1]])
                        if ee[1] == 0:
                            #scr_flag[ee[0]] = False
                            print("\n"+say[ee[0]])
                            micropause()
                        pass
                    #yo what's next
                    turn+=1
                    #loop to next turn
            if battleOver: #if user ran
                break #breaks battle loop, back to main screen
            #loop back to "turn begins"
            #if a pokemon has fainted, loop ends
        print("The battle ended!")
        #clean up
        self.field.clearfield()
        #self.field.weather=rng.choice(Weathers)
        self.field.weatherCounter=np.inf
        self.field.terrain=rng.choice(Terrains)
        if self.field.terrain=="none":
            self.field.terrainCounter=np.inf
        else:
            self.field.terrainCounter=5
        for i in self.cpus:
            i.withdraw()
            i.restore()
        for i in self.usrs:
            i.withdraw()
        shortpause() #kills
        return self.user_won
    ###end of battle block###
    
    def moreBattleFunctions(self):
        return
#zz:battleclass
##aa:fieldclass## possible in the code, but I like the clarity of battlefield while working all this out
class field:
    def __init__(self, weath = 'clear', terra = 'none', rando = False):
        global Weathers
        global Terrains
        if rando:
            self.weather=rng.choice(Weathers)
            self.terrain=rng.choice(Terrains)
        else:
            self.weather = weath
            self.terrain = terra
        self.weatherCounter=np.inf #weather lasts indefinitely when encountered naturally!
        if self.terrain=='none':
            self.terrainCounter=np.inf
        else:
            self.terrainCounter=5 #terrain only lasts 5 (or 8) turns, all the time
        # fusion bolt flare trackers
        self.fusionb=False
        self.fusionf=False
        #A for Red
        self.tailwindACounter = 0
        self.futuresA = 0 #set to 3, execute an attack at 0
        self.faintedA = False
        #entry hazards
        self.rocksA=False
        self.steelA=False
        self.stickyA=False
        self.spikesA=0 #up to 3
        self.toxicA=0 #up to 2
        #screens
        self.reflectACounter = 0
        self.lightscACounter = 0
        self.veilACounter = 0
        #others        
        #B for Blue?
        self.tailwindBCounter = 0
        self.futuresB = 0   #realized I dont need to specify its a counter
        self.faintedB = False
        self.rocksB=False
        self.stickyB=False
        self.steelB=False
        self.spikesB=0
        self.toxicB=0
        self.reflectBCounter = 0
        self.lightscBCounter = 0
        self.veilBCounter = 0
        #self.reflectA=False
        #self.reflectB=False
        #self.lightscA=False
        #self.lightscB=False
        #feel like we dont need these flags and we can do what
        #we did for toxic and spikes
        #trick room
        #the same way weather and terrain are set globally, i think trick room could be as well
        #also weather and terrain could be an attribute of battle() rn not much difference
        #it would allow us to set up several battlefields w different conditions but thats a little extra
        #so maybe I'll make trick room global for now
        #like a week after I wrote this ^ out I decided the time is now to modularize battle so I can set up several battlefield
        #with different conditions so really just don't believe anything I say
    def bugging(self):
        print('activated')
    def clearfield(self):
        self.weather='clear'
        self.terrain='none'
        self.weatherCounter=np.inf
        self.terrainCounter=5
        self.rocksA=False
        self.rocksB=False
        self.steelA=False
        self.steelB=False
        self.stickyA=False
        self.stickyB=False
        self.fusionf=False
        self.fusionb=False
        self.faintedA=False
        self.faintedB=False
        #feel like we dont need these flags and we can do what
        #we did for toxic and spikes
        #self.reflectA=False
        #self.reflectB=False
        #self.lightscA=False
        #self.lightscB=False
        self.spikesA=0 #up to 3
        self.spikesB=0
        self.toxicA=0 #up to 2 
        self.toxicB=0
        self.reflectACounter = 0
        self.reflectBCounter = 0
        self.lightscACounter = 0
        self.lightscBCounter = 0
        self.veilACounter = 0
        self.tailwindACounter = 0
        self.futuresA = 0
        self.veilBCounter = 0
        self.tailwindBCounter = 0
        self.futuresB = 0
        #etc, etc
    def shuffleweather(self,wea=True,ter=True):
        global Weathers
        global Terrains
        if wea:
            self.weather=rng.choice(Weathers)
            self.weatherCounter=np.inf
            print(f"\nBattlefield weather is {self.weather} now.")
        if ter:
            self.terrain=rng.choice(Terrains)
            self.terrainCounter=5
            print(f"\nBattlefield terrain is {self.terrain} now.")
        return
    def checkScreen(self,color,screen):
            #color = 'red' or 'blue', screen='reflect' or 'lightscreen' eventually 'veil'
            matri= ((self.reflectACounter, self.lightscACounter, self.veilACounter),(self.reflectBCounter, self.lightscBCounter,self.veilBCounter) )
            ans='error'
            for i in list(enumerate(('red','blue'))):
                for j in list(enumerate(('reflect','lightscreen','veil'))):
                    if (color == i[1]) and (screen == j[1]):
                        ans = max( 0., float(matri[i[0]][j[0]]) ) #if counter value is negative, instead return 0.
                    pass
                pass
            return ans
    ### only the hazards on the ground
    def grounding(self,poke):
        #rocksOn = ( poke.battlespot == "red" and self.rocksA ) or ( poke.battlespot == "blue" and self.rocksB )
        stickyOn = ( poke.battlespot == "red" and self.stickyA ) or ( poke.battlespot == "blue" and self.stickyB )
        spikesOn = ( poke.battlespot == "red" and self.spikesA > 0 ) or ( poke.battlespot == "blue" and self.spikesB > 0)
        toxicOn = ( poke.battlespot == "red" and self.toxicA > 0 ) or ( poke.battlespot == "blue" and self.toxicB > 0)
        if stickyOn:
            poke.stickyNerf()
        if spikesOn:
            if poke.battlespot == "red":
                poke.spikesDamage(self.spikesA)
            elif poke.battlespot == "blue":
                poke.spikesDamage(self.spikesB)
        if toxicOn:
            if poke.battlespot == "red":
                #check for poison type
                if 7 in poke.tipe:
                    self.toxicA = 0
                    print(f"{poke.name} absorbs the toxic spikes!")
                    micropause()
                else:
                    poke.toxicAffliction(self.toxicA)
            elif poke.battlespot == "blue":
                if 7 in poke.tipe:
                    self.toxicB = 0
                    print(f"{poke.name} absorbs the toxic spikes!")
                    micropause()
                else:
                    poke.toxicAffliction(self.toxicB)
    ### call when a pokemon comes out
    def landing(self,poke):
        #this function will simulate pokemon being damaged by entry hazards
        #need to make functions for mon() of the entry hazard damages being done
        #need to check for rocks, spikes, toxix spikes (except for poisons) and sticky web
        #only for grounded pokemon tho...
        rocksOn = ( poke.battlespot == "red" and self.rocksA ) or ( poke.battlespot == "blue" and self.rocksB )
        #stickyOn = ( poke.battlespot == "red" and self.stickyA ) or ( poke.battlespot == "blue" and self.stickyB )
        #spikesOn = ( poke.battlespot == "red" and self.spikesA > 0 ) or ( poke.battlespot == "blue" and self.spikesB > 0)
        #toxicOn = ( poke.battlespot == "red" and self.toxicA > 0 ) or ( poke.battlespot == "blue" and self.toxicB > 0)
        ##some hazards
        if rocksOn:
            poke.rocksDamage()
        if poke.grounded:
            self.grounding(poke)
        # there will be more entry hazards unfortunately
        return
    #aa:hazards
    def hazarding(self,elem,side):
        #will place entry hazards on the battlefield
        #hazards on player side
        if side == "red":
            if elem == "rocks":
                if self.rocksA == True:
                    print( "Rocks are already set up!" )
                    return "failed"
                else:
                    self.rocksA = True
                    return "x"
            elif elem == "spikes":
                if self.spikesA >= 3:
                    print("No more spikes will fit!")
                    return "failed"
                else:
                    self.spikesA += 1
                    return "x"
            elif elem == "toxspk":
                if self.toxicA >= 2:
                    print("No more toxic spikes will fit!")
                    return "failed"
                else:
                    self.toxicA += 1
                    return "x"
            elif elem == "sticky":
                if self.stickyA == True:
                    print("The web is already set up!")
                    return "failed"
                else:
                    self.stickyA = True
                    return "x"
            #think thats all the hazards for now
        #opponent side
        elif side == "blue":
            if elem == "rocks":
                if self.rocksB == True:
                    print( "Rocks are already set up!" )
                    return "failed"
                else:
                    self.rocksB = True
                    return "x"
            elif elem == "spikes":
                if self.spikesB >= 3:
                    print("No more spikes will fit!")
                    return "failed"
                else:
                    self.spikesB += 1
                    return "x"
            elif elem == "toxspk":
                if self.toxicB >= 2:
                    print("No more toxic spikes will fit!")
                    return "failed"
                else:
                    self.toxicB += 1
                    return "x"
            elif elem == "sticky":
                if self.stickyB == True:
                    print("The web is already set up!")
                    return "failed"
                else:
                    self.stickyB = True
                    return "x"
            #think thats all the hazards for now
    #aa:screens
    def upScreens(self,scr,side):
        if side=='red':
            ## reflect is already up for player
            if (scr=='reflect') and (self.reflectACounter>0):
                micropause()
                print("\nThe move fails! Reflect is already up!")
                return "failed"
            ## light screen is already up for player
            elif (scr=='lightscreen') and (self.lightscACounter>0):
                micropause()
                print("\nThe move fails! Light Screen is already up!")
                return "failed"
            elif (scr=='veil') and (self.veilACounter>0):
                micropause()
                print("\nThe move fails! Aurora Veil is active!")
                return "failed"
            elif scr=='reflect':
                self.reflectACounter=5
                micropause()
                print("\nThe Pokemon's side is protected by Reflect!")
            ## player puts up light screen
            elif scr=='lightscreen':
                self.lightscACounter=5
                micropause()
                print("\nThe Pokemon's side is protected by Light Screen!")
            elif scr=='veil':
                micropause()
                self.veilACounter=5
                print("\nThe Pokemon's side is protected by a mystical veil!")
            pass
        elif side=='blue':
            ## reflect is already up for cpu
            if (scr=='reflect') and (self.reflectBCounter>0):
                micropause()
                print("\nThe move fails! Reflect is already up!")
                return "failed"
            ## light screen is already up for cpu
            elif (scr=='lightscreen') and (self.lightscBCounter>0):
                micropause()
                print("\nThe move fails! Light Screen is already up!")
                return "failed"
            ## cpu puts up reflect
            elif (scr=='veil') and (self.veilBCounter>0):
                micropause()
                print("\nThe move fails! Aurora Veil is already active!")
                return "failed"
            ## cpu puts up reflect
            elif scr=='reflect':
                self.reflectBCounter=5
                micropause()
                print("\nThe Pokemon's side is protected by Reflect!")
            ## cpu puts up light screen
            elif scr=='lightscreen':
                self.lightscBCounter=5
                micropause()
                print("\nThe Pokemon's side is protected by Light Screen!")
            elif scr=='veil':
                self.veilBCounter=5
                micropause()
                print("\nThe Pokemon's side is protected by a mystical veil!")
            pass
    #more functions of field
##zz:fieldclass
#aa:damagefunction
def damage(attacker,defender,power,moveTipe,isSpecial,note):
    global statStages
    ####damage read-out strings####
    damages=[]
    ####set some variable straight
    level=attacker.level
    screennerf = 1.0
    screen_tag = ("Reflect","Light Screen")
    if isSpecial:
        attack=attacker.bsa
        if 'psystrike' in note:
            defense=defender.bde
        else:
            defense=defender.bsd
        statNerf=statStages[attacker.sastage] #will be ignored if negative and crit
        statBoost=statStages[defender.sdstage] #ignored if positive and crit
        burn=1.
        if ( attacker.field.checkScreen(defender.battlespot, 'lightscreen') + attacker.field.checkScreen(defender.battlespot,'veil') ) > 0.:
            screennerf = 0.5 #light screen or veil protects the defending pokemon
            screen_i = 1
        pass
    else:
        attack=attacker.bat
        defense=defender.bde
        statNerf=statStages[attacker.atstage]
        statBoost=statStages[defender.destage]
        ####burn####
        if attacker.burned:
            burn=0.5
        else:
            burn=1.
        if ( attacker.field.checkScreen(defender.battlespot, 'reflect') + attacker.field.checkScreen(defender.battlespot,'veil') ) > 0.:
            screennerf = 0.5 #reflect or veil protects the defending pokemon
            screen_i = 0
    plaintiffTipe=attacker.tipe
    defendantTipe=defender.tipe
    #### brick break removes screens before doing damage ####
    if 'breakScreens' in note:
        screennerf = 1.
    #### water spout ####
    if 'spout' in note:
        power = np.floor( 150.*attacker.currenthp/attacker.maxhp )
        if power<1.:
            power = 1.
        pass
    #### rollout #### 
    if 'rollout' in note: 
        if attacker.curled: #another boost if poke has used defense curl
            power*=2
        power *= 2** (float(attacker.rolling_out))
    #### getting caught ####
    #digging diving flying
    if ('gust' in note) and defender.flying:
        caught_bonus = 2.
        damages.append(f"{defender.name} is struck in the sky!")
    if ('surf' in note) and defender.diving:
        caught_bonus = 2.
        damages.append(f"{defender.name} is struck underwater!")
    elif ('nerfGrassy' in note) and defender.digging:
        caught_bonus = 2.
        damages.append(f"{defender.name} is struck underground!")
    else:
        caught_bonus = 1.
    #### retaliate ####
    if 'retaliate' in note:
        if ( ((attacker.battlespot == 'red') and attacker.field.faintedA) or ((attacker.battlespot == 'blue') and attacker.field.faintedB) ):
            power*=2.
            damages.append(f"{attacker.name} avenges its fallen ally!")
    #### facade ####
    if ('facade' in note) and (attacker.burned or attacker.poisoned or attacker.badlypoisoned or attacker.paralyzed):
        power*=2.
        burn = 1.0 #facade undoes burn nerf
        damages.append("Power boosted from status condition!")
    if ('hex' in note) and (defender.burned or defender.poisoned or defender.badlypoisoned or defender.paralyzed or defender.sleep or defender.frozen):
        power*=2.
        damages.append("Power boosted by target's status condition!")
    #### fusion move fusion ####
    if ('fusion-b' in note) and attacker.field.fusionf:
        power*=2.
        damages.append("The bolts are strengthened by the lingering flames!")
    elif ('fusion-f' in note) and attacker.field.fusionb:
        power*=2.
        damages.append("The flames are strengthened by the lingering bolts!")
    ####weather ball#### doubles power and changes type
    if ('weatherball' in note) and (attacker.field.weather!='clear'):
        power*=2.
        if attacker.field.weather=="sunny":
            moveTipe=1
        if attacker.field.weather=="rain":
            moveTipe=2
        if attacker.field.weather=="sandstorm":
            moveTipe=12
        if attacker.field.weather=="hail":
            moveTipe=5
        damages.append("Weather Ball changes type!")
    #solarbeam gets nerfed in inclement weather
    if ("solar" in note) and (attacker.field.weather=="rain" or attacker.field.weather=="sandstorm" or attacker.field.weather=="hail"):
        power*=0.5
    #earthquake, bulldoze and magnitude nerfed on grassy terrain
    if ("nerfGrassy" in note) and (attacker.field.terrain=="grassy"):
        power*=0.5
    ####weather damage boost####
    weatherBonus=1.
    if attacker.field.weather=='sunny':
        if moveTipe==1:
            weatherBonus=4./3.
            damages.append("The Sun boosts the attack power!")
        elif moveTipe==2:
            weatherBonus=2./3.
            damages.append("The attack is weakened by the sunlight...")
    elif attacker.field.weather=='rain':
        if moveTipe==1:
            weatherBonus=2./3.
            damages.append("The attack is weakened by the rain...")
        elif moveTipe==2:
            weatherBonus=4./3.
            damages.append("The rain boosts the attack power!")
    #### terrain boosts and nerf ####
    if attacker.field.terrain=='none':
        pass
    else: #only check for terrain boosts when there is a non-none terrain
        #when terrains come into play
        grass=(attacker.field.terrain=="grassy") and (moveTipe==3) and (attacker.grounded)
        psychic=(attacker.field.terrain=="psychic") and (moveTipe==10) and (attacker.grounded)
        electric=(attacker.field.terrain=="electric") and (moveTipe==4) and (attacker.grounded)
        fairy=(attacker.field.terrain=="misty") and (moveTipe==14) and (defender.grounded)
        #realized the three of them would have the exact same effect
        if grass or psychic or electric:
            power*=1.3
            damages.append("Boosted by the terrain!")
        #grounded mon take half damage on fairy terrain
        elif fairy:
            power*=0.5
            damages.append("Weakened by the terrain...")
        #there is some terrain, but the other requirements werent met, no effect
        else:
            pass
    ####critical hit chance####
    critical=1.
    if "highCrit" in note:
        crit=9
    else:
        crit=25
    if rng.integers(1,crit)==1:
        critical=1.5
        if statNerf<1: #if change is not productive to attacker
            attack/=statNerf #undo it
        if statBoost>1: #if change is productive to defender
            defense/=statBoost #undo it
        damages.append("It's a critical hit!")
        screennerf=1.0 #critical hits bypass screens
        burn=1.0 #critical hits bypass burn-attack-nerf
    if screennerf < 1.0:
        damages.append(f"Protected by {screen_tag[screen_i]}")
    ####random fluctuation 85%-100%
    rando=rng.integers(85,101)*0.01
    ####STAB####
    STAB=1.
    if moveTipe in plaintiffTipe:
        STAB=1.5
        damages.append("Same Type Attack Bonus!")
    ####type effectiveness####
    tyype=checkTypeEffectiveness(moveTipe,defendantTipe)
    ## flying pokemon being targeted with ground move is grounded, should lose flying type
    #print(moveTipe,defendantTipe,defender.grounded)
    ## 
    if (moveTipe==8) and (9 in defendantTipe): #be wary of grounds attacking flyings
        if defender.grounded: #easy
            if defender.dualType:
                defendantTipe = [np.squeeze(defendantTipe[np.argwhere(defendantTipe!=9)])]
                #print(defendantTipe)
                tyype = checkTypeEffectiveness(moveTipe, defendantTipe)
            else:  #flying type pokemon is grounded, no other types to compare
                tyype = 1.0
        elif ('arrows' in note): #pokemon not grounded yet, but arrows hits flying regardless
            tyype = 1.0
    #elif ('arrows' in note) and defender.:
    #check if the burn nerf survives (non-crit and non-facade)
    if burn<1.0:
        damages.append("The burn reduces damage...")
    #circumvent normal damage calculation sometimes
    if (('mirrorcoat' in note) and (attacker.counter_damage[1] == 'spec')) or (('counter' in note) and (attacker.counter_damage[1]=='phys')):
        ans = np.floor(2.*attacker.counter_damage[0])
        damages = []
    elif (('mirrorcoat' in note) or ('counter' in note)):
        ans = 0.0
        damages = ["failed"]
    else:
        ####modifiers united####
        #print(tyype)
        damageModifier=weatherBonus*critical*rando*STAB*tyype*burn*screennerf*caught_bonus
        ####damage calculation####
        ans= np.floor( ((((2.*level)/5. + 2.)*power*attack/defense)/50. + 2.)*damageModifier )
    return ans,tyype,damages
#zz:damagefunction
#aa:functions
#calculates pokemon stats (non-HP)
def stats(level,base,IV,EV,nature):
    ans=((2.*base+IV+EV/4.)*level/100.+5.)*nature
    return ans
#calculates HP stat
def HP(level,base,IV,EV):
    ans=np.floor( ((2.*base+IV+EV/4.)*level/100.)+level+10. )
    return ans
def checkTypeEffectiveness(moveTipe,defendantTipe):
    global codex
    matchup1=codex[moveTipe,defendantTipe[0]]
    if len(defendantTipe)>1:
        matchup2=codex[moveTipe,defendantTipe[1]]
    else:
        matchup2=1.0
    return matchup1*matchup2
#create a pokemon from the pokedex
def makeMon(pokedexNumber,level=1,nacher = (0,0)):
    Hp=dex[pokedexNumber]['hp']
    At=dex[pokedexNumber]['at']
    De=dex[pokedexNumber]['de']
    Sa=dex[pokedexNumber]['sa']
    Sd=dex[pokedexNumber]['sd']
    Sp=dex[pokedexNumber]['sp']
    nayme=dex[pokedexNumber]['name']
    tipe1=dex[pokedexNumber]['type1']
    tipe2=dex[pokedexNumber]['type2']
    if dex[pokedexNumber]['type2']==20: #single-typed mon
        return mon(level,nayme,nature=nacher,hpbase=Hp,atbase=At,debase=De,sabase=Sa,sdbase=Sd,spbase=Sp,tipe=np.array([tipe1]))
    else: #dual-typed
        return mon(level,nayme,nature=nacher,hpbase=Hp,atbase=At,debase=De,sabase=Sa,sdbase=Sd,spbase=Sp,tipe=np.array([tipe1,tipe2]))
#load pokemon
def loadMon(savefile):
    try:
        dat=np.loadtxt(savefile,delimiter=",",dtype='U140')
        loadPokes=[]
        if type(dat[0])==np.str_: #only the case if there's only 1 pokemon
            dat=dat.reshape((1,-1)) #to treat this pokemon like any other line in a list of saved pokemon
        for i in dat:
            if int(i[1])<=0: #invalid levels
                return [0]
            baseI=[int(ii) for ii in i[2].split()]
            if min(baseI)<=0:
                return [0]
            ivz=[int(ii) for ii in i[3].split()]
            if min(ivz)<0: #i guess im going to allow ivs beyond 31 via save files, go nuts, negatives are a big no though
                return [0]
            evz=[int(iii) for iii in i[4].split()]
            if min(evz)<0: #same with evs, no positive limits
                return [0]
            typ=np.array([int(iiii) for iiii in i[5].split()])
            if max(typ)>18 or min(typ)<0: #invalid types
                return [0]
            nacher = np.array([int(iv) for iv in i[6].split()])
            newP=mon(int(i[1]),i[0],nature=nacher,hpbase=baseI[0],atbase=baseI[1],debase=baseI[2],sabase=baseI[3],sdbase=baseI[4],spbase=baseI[5],tipe=typ)
            newP.knownMoves=[int(iiiii) for iiiii in i[7].split()]
            newP.hpiv,newP.ativ,newP.deiv,newP.saiv,newP.sdiv,newP.spiv=ivz
            newP.hpev,newP.atev,newP.deev,newP.saev,newP.sdev,newP.spev=evz
            newP.PP=[getMoveInfo(i)['pp'] for i in newP.knownMoves]
            newP.reStat()
            loadPokes.append(newP)
            print(f"Loaded {newP.name}!")
            micropause()
        return loadPokes
    except FileNotFoundError:
        print("! The file name wasn't found... !\n")
        return [0]
    except OSError:
        print("! The file name wasn't found... !\n")
        return [0]
    except IndexError:
        print("!! The save file is corrupted !!")
        return [0]
def makeRandom(level=int(rng.normal(loc=80,scale=30)),numMoves=6):
    global mov,mo
    dome = makeMon( rng.integers( len(dex) ), level, (int(rng.choice([0,1,2,3,4])),int(rng.choice([0,1,2,3,4]))))
    ranMoves = rng.choice(mo,size=numMoves,replace=False)
    dome.knownMoves = list(ranMoves)
    dome.PP=[mov[i]["pp"] for i in ranMoves]
    return dome
#check party for non fainted pokemon
def checkBlackout(party):
    """
    party : list of mon() objects
        a party of pokemon
    p : integer
        number of nonfainted pokemon
    alive : list of intgers
        indeces of nonfainted pokemon
    """
    p=0
    alive=[]
    for i in range(len(party)):
        if party[i].fainted==False:
            p+=1
            alive.append(i)
    return p,alive
#moves have pwr, phys/spec, type, accu, descipt
def moveInfo(moveCode):
    global mov, typeStrings
    move=mov[moveCode]
    print(f"------------ {move['name']} ------------")
    print(f"Power: {move['pwr']} | Accuracy: {move['accu']}%")
    if move['special?']==2:
        print(f"[{typeStrings[move['type']]}] | [Status] | PP: {move['pp']}")
    elif move['special?']==1:
        print(f"[{typeStrings[move['type']]}] | [Special] | PP: {move['pp']}")
    elif move['special?']==0:
        print(f"[{typeStrings[move['type']]}] | [Physical] | PP: {move['pp']}")
    print("-\n"+move['desc'])
    if move['contact?']:
        print("-The user makes contact with the target.")
    else:
        print("-The user does not make contact with the target.")
def elite4_healquit(poke_party):
    heal1 = input("\nWould you like me to heal your Pokemon?\n[y]es, [n]o: ")     
    if heal1 == 'b' or heal1=='B':
        print("Leaving Indigo Plateau...")
        micropause()
        return "quitted"
    elif heal1 == 'y' or heal1=='Y':
        #heal all them
        for i in poke_party:
            i.restore()
        print("\nYour party is looking better than ever!!")
        shortpause()
        return "healed"
    else:
        return "advance"
def micropause():
    t.sleep(0.4)
    return
def shortpause():
    t.sleep(0.9)
    return
def dramaticpause():
    t.sleep(1.4)
    return
codex=np.ones((19,19))
#order: normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,dark 15,
#steel 16,fairy 17,typeless (no relationships) 18
codex[0,12],codex[0,13],codex[0,16]=0.5,0,0.5 #normal
codex[1,1],codex[1,2],codex[1,3],codex[1,5],codex[1,11],codex[1,12],codex[1,14],codex[1,16]=0.5,0.5,2.0,2.0,2.0,0.5,0.5,2.0 #fire
codex[2,1],codex[2,2],codex[2,3],codex[2,8],codex[2,12],codex[2,14]=2.0,0.5,0.5,2.0,2.0,0.5 #water
codex[3,1],codex[3,2],codex[3,3],codex[3,7],codex[3,8],codex[3,9],codex[3,11],codex[3,12],codex[3,14],codex[3,16]=0.5,2.0,0.5,0.5,2.0,0.5,0.5,2.0,0.5,0.5 #grass
codex[4,2],codex[4,3],codex[4,4],codex[4,8],codex[4,9],codex[4,14]=2.0,0.5,0.5,0.0,2.0,0.5 #electric
codex[5,1],codex[5,2],codex[5,3],codex[5,5],codex[5,8],codex[5,9],codex[5,14],codex[5,16]=0.5,0.5,2.0,0.5,2.0,2.0,2.0,0.5 #ice
codex[6,1],codex[6,5],codex[6,7],codex[6,9],codex[6,10],codex[6,11],codex[6,12],codex[6,13],codex[6,15],codex[6,16],codex[6,17]=2.0,2.0,0.5,0.5,0.5,0.5,2.0,0.0,2.0,2.0,0.5 #fighting
codex[7,3],codex[7,7],codex[7,8],codex[7,12],codex[7,13],codex[7,16],codex[7,17]=2.0,0.5,0.5,0.5,0.5,0.0,2.0 #poison
codex[8,1],codex[8,3],codex[8,4],codex[8,7],codex[8,9],codex[8,11],codex[8,12],codex[8,16]=2.0,0.5,2.0,2.0,0.0,0.5,2.0,2.0 #ground
codex[9,3],codex[9,4],codex[9,6],codex[9,11],codex[9,12],codex[9,16]=2.0,0.5,2.0,2.0,0.5,0.5 #flying
codex[10,6],codex[10,7],codex[10,10],codex[10,15],codex[10,16]=2.0,2.0,0.5,0.0,0.5 #psychic
codex[11,1],codex[11,3],codex[11,6],codex[11,7],codex[11,9],codex[11,10],codex[11,13],codex[11,15],codex[11,16],codex[11,17]=0.5,2.0,0.5,0.5,0.5,2.0,0.5,2.0,0.5,0.5  #bug
codex[12,1],codex[12,5],codex[12,6],codex[12,8],codex[12,9],codex[12,11],codex[12,16]=2.0,2.0,0.5,0.5,2.0,2.0,0.5 #rock
codex[13,0],codex[13,10],codex[13,13],codex[13,15]=0.0,2.0,2.0,0.5 #ghost
codex[14,14],codex[14,16],codex[14,17]=2.0,0.5,0.0 #dragon
codex[15,6],codex[15,10],codex[15,13],codex[15,15],codex[15,17]=0.5,2.0,2.0,0.5,0.5 #dark
codex[16,1],codex[16,2],codex[16,4],codex[16,5],codex[16,12],codex[16,16],codex[16,17]=0.5,0.5,0.5,2.0,2.0,0.5,2.0 #steel
codex[17,1],codex[17,6],codex[17,7],codex[17,14],codex[17,15],codex[17,16]=0.5,2.0,0.5,2.0,2.0,0.5 #fairy
typeStrings=["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy","Typeless"]
statStages=[2/8,2/7,2/6,2/5,2/4,2/3,2/2,3/2,4/2,5/2,6/2,7/2,8/2] #0 to 6 to 12
acevStages=[3/9,3/8,3/7,3/6,3/5,3/4,3/3,4/3,5/3,6/3,7/3,8/3,9/3] #0 to 6 to 12, based in accuracy stages, evasion stages are reverse don't think about it too hard
stageStrings=["fell severely","fell harshly","fell","[BLANK]","rose","rose sharply","rose drastically"] #0(-3) to 2(-1) to 4(+1) to 6(+3)
nature_stat_str = ["Atk","Def","SpA","SpD","Spe"]
Weathers=['clear','sunny','rain','sandstorm','hail']
Terrains=['none','electric','grassy','misty','psychic']
struggle_i=struggle #move index of struggle
futuresight_i = futuresigh
mo=list(range(len(mov)))
mo.remove(struggle_i) #get struggle out of pool of moves
if __name__ == "__main__":
    pass
else:
    pass
