#Antoine Washington
#Pokemon x Python
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
#*********to do list: ABILITIES *cough*, genders ugh
#*******************: user set battle setting,
#*******************: 
#

import copy
import time as t
import numpy as np
#import astropy.table as tbl
#import astropy.io.ascii as asc
from moves import getMoveInfo,mov,struggle,natures
from pokedex import dex

rng=np.random.default_rng()

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
        self.currenthpp=100
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
        #battle statuses
        self.sleep=False
        self.sleepCounter=0
        self.frozen=False
        self.burned=False
        self.paralyzed=False
        self.poisoned=False
        self.badlypoisoned=False
        self.poisonCounter=0
        self.confused=False
        self.confusionCounter=0
        self.flinched=False #might not necessarily need this? idk
        self.resting=False #for moves where pokemon need to recharge
        self.charged=False #when true, pokemon has a 2turn move ready to use

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
    def chosen(self, trainer):
        global indigo
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
        #undo confusion
        self.confused=False
        self.confusionCounter=0
        #reset bad poison counter
        if self.poisonCounter>0:
            self.poisonCounter=1
        self.resting=False
        self.flinched=False
        self.charged=False
    
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
        print(f"{self.name} faints!")
        t.sleep(0.5)
    
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
            if weather=='sandstorm':
                #rock type sp.def boost in a sandstorm!
                self.bsd*=1.5
                print(f"{self.name} is boosted by the sandstorm!")
        #ground or unground pokemon?
        #further in the list
    
    def stageChange(self,stat,level):
        #stat='at','de','sa','sd','sp'
        #level= 1,2,3 or -1,-2,-3
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
        global weather
        global terrain
        afflicted=self.sleep or self.frozen or self.paralyzed or self.burned or self.poisoned or self.badlypoisoned
        mistyCheck=(terrain=="misty") and self.grounded #is the pokemon grounded on misty terrain?
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
                    t.sleep(0.4)
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
                    t.sleep(0.4)
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
                    t.sleep(0.4)
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
                    t.sleep(0.4)
        #sleep
        if "sleep" in notes:
            electricCheck=(terrain=="electric") and self.grounded #electric terrain prevents sleep
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
                    t.sleep(0.4)
        #freeze
        if "frze" in notes:
            if weather=='sunny': #harsh sunlight prevents freezing
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
                    t.sleep(0.4)
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
                    t.sleep(0.4)
                #more status move effects
        return
    
    #pokemon move
    def move(self, opponent, moveIndex):
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
                return #end move() user still frozen
        #asleep, can't move
        if self.sleep:
            self.sleepCounter-=1
            if self.sleepCounter==0:
                self.sleep=False
                print(f"\n{self.name} wakes up!")
            else:
                print(f"\n{self.name} is fast asleep!")
                return
        #paralysis prevents move execution
        if self.paralyzed:
            if rng.random()<0.25:
                print(f"\n{self.name} is fully paralyzed!")
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
                    return
        global weather
        #check if move needs to be charged
        if "2turn" in notas:
            if self.charged: #pokemon has charged the move already
                self.charged=False #pokemon will release the move
            else: #all of these will lead to a return, ending move() before anything else happens
                if "solar" in notas:
                    print(f"\n{self.name} is taking in sunlight!")
                    self.charged=True
                    if weather=="sunny": #if sun is out, continue to use the move
                        self.charged=False
                    else: #otherwise end the move
                        return
                elif "skullbash" in notas:
                    print(f"\n{self.name} tucks its head in...")
                    self.charged=True
                    self.stageChange("de",1)
                    return
                elif "geomance" in notas:
                    print(f"\n{self.name} is absorbing energy!")
                    self.charged=True
                    return
                #other labels for other moves and charging contexts
        print(f"\n{self.name} uses {moveI['name']}!")
        if moveIndex!=struggle:
            self.PP[int(np.argwhere(np.array(self.knownMoves)==moveIndex))]-=1 #deduct PP for move usage
        t.sleep(0.4)
        ###accuracy check###
        if "noMiss" in notas:
            hitCheck=True
        else:
            #check evasion and accuracy stats
            effAccu=self.acstage-opponent.evstage+6 #get difference in evasion/accuracy stats, offset by proper center, index 6
            if effAccu>12:
                effAccu=12
            elif effAccu<0:
                effAccu=0
            effAccu=acevStages[effAccu]
            hitCheck = rng.random() <= effAccu * ( moveI['accu'] / 100. )
        if hitCheck==False: #move misses
            print(f"\n{self.name}'s attack misses!")
            t.sleep(0.4)
            return
        else: #move will connect
            ##===========================status moves==========================##
            if moveI['special?']==2:
                ##stat changes
                if "stat" in notas:
                    statInfo=notas[1+int(np.argwhere(np.array(notas)=='stat'))]
                    targ,stat,phase=statInfo.split(",")[0:3]
                    stat=stat.split(":")
                    phase=phase.split(":")
                    if targ=='self':
                        for i in range(len(stat)):
                            self.stageChange(stat[i],int(phase[i]))
                        self.inBattle()
                    if targ=='targ':
                        for i in range(len(stat)):
                            opponent.stageChange(stat[i],int(phase[i]))
                        opponent.inBatle()
                #end of stat changes
                ##weathers
                global weatherCounter
                if "sun" in notas:
                    if weather=='sunny':
                        print("The move fails! It's already sunny!")
                    else:
                        weather='sunny'
                        weatherCounter=5
                        print("The sunlight turns harsh!")
                if "rain" in notas:
                    if weather=='rain':
                        print("The move fails! It's already raining!")
                    else:
                        weather='rain'
                        weatherCounter=5
                        print("It starts raining!")
                if 'sand' in notas:
                    if weather=='sandstorm':
                        print("The move fails! There's already a sandstorm!")
                    else:
                        weather='sandstorm'
                        weatherCounter=5
                        print("A sandstorm kicks up!")                
                if 'hail' in notas:
                    if weather=='hail':
                        print("The move fails! It's already hailing")
                    else:
                        weather='hail'
                        weatherCounter=5
                        print("It starts hailing!")
                #end of the weathers
                #terrains
                global terrain
                global terrainCounter
                if "electric" in notas:
                    if terrain=="electric":
                        print("The move fails! The battlefield is already electrified!")
                    else:
                        terrain="electric"
                        terrainCounter=5
                        print("Electricity surges throughout the battlefield!")
                if "grassy" in notas:
                    if terrain=="grassy":
                        print("The move fails! The battlefield is already grassy!")
                    else:
                        terrain="grassy"
                        terrainCounter=5
                        print("Grass grows all over the place!")
                if "misty" in notas:
                    if terrain=="misty":
                        print("The move fails! The battlefield is already covered in mist!")
                    else:
                        terrain="misty"
                        terrainCounter=5
                        print("A mist descends on the battlefield!")
                if "psychic" in notas:
                    if terrain=="psychic":
                        print("The move fails! The battlefield is already weird!")
                    else:
                        terrain="psychic"
                        terrainCounter=5
                        print("The battlefield gets weird!")
                #statuses bro
                statuses=[]
                if "para" in notas:
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
                #entry hazards oh boy oh geeze
                global indigo
                hazs = ["rocks", "spikes", "toxspk", "sticky"]
                haz_dialog = ["Pointed rocks are scattered on the opposing side!", "Pointy spikes are scattered on the opposing side!", "Poison spikes are scattered on the opposing side!", "The opposing side is covered in a sticky web!"]
                for i in range(len(hazs)):
                    if hazs[i] in notas: #i know theres a better way to do this but if i sit here and fixate on that before i start a rough draft i'm never gonna get anywhere
                        if self.battlespot=="red": #user's pokemon
                            xx = indigo.hazarding(hazs[i], "blue")
                        elif self.battlespot=="blue": #cpu
                            xx = indigo.hazarding(hazs[i], "red")
                        if xx == "x": #makes sure hazard was executed successfully before printing the dialog
                            print(haz_dialog[i])
                #end of entry hazards
                #more status move effects
                return
            ##=================================================================##
            ans,eff,comment=damage(self,opponent,moveI['pwr'],moveI['type'],moveI['special?'],notas)
            opponent.hit(self,ans,eff,notas,moveI['type'],comment)
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
    
    def hit(self,attacker,damagepoints,effectiveness,notes,moveTipe,comments):
        if effectiveness==0.:
            print(f"{self.name} is immune!")
        else:
            print(f"\n{self.name} is hit!")
            t.sleep(0.4)
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
                t.sleep(0.4) #for drama
                print(f"{i}")
            t.sleep(0.4)
            #show effectiveness
            if effectiveness>2.:
                print("It's MEGA-effective!!")
            if effectiveness<=2. and effectiveness>1.:
                print("It's super-effective!")
            if effectiveness<0.5 and effectiveness>0.:
                print("It's barely effective...")
            if effectiveness>=0.5 and effectiveness<1.:
                print("It's not very effective.")
            t.sleep(0.4)
            #result of hit
            print(f"{self.name} lost {format(100*damagepoints/self.maxhp,'.2f')}% HP!")
            t.sleep(0.7)
            #check for faint
            if self.currenthp<=0.:
                self.faint()
            else:
                print(f"{self.name} has {format(self.currenthpp,'.2f')}% HP left!")
                t.sleep(0.7)
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
                    attacker.recoil(recoilDmg,1/3)
                elif amnt=="1/4maxhp":
                    attacker.recoil(attacker.maxhp,1/4)
                #more possible recoil amounts?
            #recoil belongs in hit, because it doesn't happen if the target is immune to the hit()
            #setting need to rest
            if "mustRest" in notes:
                attacker.resting=True
        #end of hit()
    
    #flinching
    def flinch(self):
        self.flinched=True
    #recoil, gonna experiment with spacing here I guess whatever
    def recoil(self, damagedone, recoilAmount):
        self.currenthp -= damagedone * recoilAmount
        self.currenthpp = 100 * self.currenthp / self.maxhp
        print( f"{self.name} takes recoil damage!" )
        t.sleep(0.3)
        if self.currenthp <= 0.:
            self.faint()
        #i don't hate it
    #confusion
    def confusionDamage(self):
        dmg = (((( 2. * self.level ) / 5. + 2.) * 40. * self.bat / self.bde) / 50. + 2. )
        self.currenthp -= dmg
        self.currenthpp = 100 * self.currenthp / self.maxhp
        print( f"{self.name} hurt itself in its confusion!" )
        t.sleep(0.3)
        if self.currenthp <= 0.:
            self.faint()
    #poison
    def poisonDamage(self):
        self.currenthp-=self.maxhp/8.
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took poison damage!")
        t.sleep(0.3)
        if self.currenthp<=0.:
            self.faint()
    #badly poisoned
    def badPoison(self):
        self.currenthp-=self.poisonCounter*self.maxhp/16.
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took bad poison damage!")
        t.sleep(0.3)
        if self.currenthp<=0.0:
            self.faint()
    #burn
    def burnDamage(self):
        #would be the same as poisonDamage tbh
        self.currenthp-=self.maxhp/8.
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took burn damage!")
        t.sleep(0.3)
        if self.currenthp<=0.:
            self.faint()
    #sandstorm
    def sandDamage(self):
        immune=(12 in self.tipe) or (8 in self.tipe) or (16 in self.tipe) #check for rock, ground, and steel types
        if immune:
            print(f"{self.name} is unaffected by the sandstorm!")
            t.sleep(0.3)
        else:
            self.currenthp-=self.maxhp/16.
            self.currenthpp=100*self.currenthp/self.maxhp
            print(f"{self.name} took some damage from the sandstorm!")
            t.sleep(0.3)
            if self.currenthp<=0.:
                self.faint()
    #hail
    def hailDamage(self):
        if 5 in self.tipe:
            print(f"{self.name} is unaffected by the hail!")
            t.sleep(0.3)
        else:
            self.currenthp-=self.maxhp/16.
            self.currenthpp=100*self.currenthp/self.maxhp
            print(f"{self.name} took some damage from the hail!")
            t.sleep(0.3)
            if self.currenthp<=0.:
                self.faint()
    #healing from grassy terrain
    def grassyHeal(self):
        if self.currenthp==self.maxhp:
            return #do nothing, say nothing
        else:
            self.currenthp+=self.maxhp/16.
            print(f"{self.name} is healed by the grassy terrain!")
            t.sleep(0.3)
            if self.currenthp>self.maxhp: #lets not heal above the max lol
                self.currenthp=self.maxhp
                self.currenthpp=100
            else:
                self.currenthpp=100.*self.currenthp/self.maxhp
    #entry hazard damages
    #guess we should check for faint after entry hazard damage
    #stealthrock
    def rocksDamage(self):
        self.currenthp-=self.maxhp/8.*checkTypeEffectiveness(12, self.tipe)
        print(f"Pointed stones dig into {self.name}!")
        t.sleep(0.4)
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
        t.sleep(0.4)
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
            t.sleep(0.3)
            return
        elif level == 2:
            self.badlypoisoned=True
            self.poisonCounter=1
            print(f"\n{self.name} is badly poisoned by the spikes!")
            t.sleep(0.3)
            return
        
    def stickyNerf(self):
        self.stageChange('sp', -1)
        print(f"{self.name} is slowed down by the web!")
        return
    
    def checkup(self):
        print(f"Name: {self.name} // Lv. {self.level}")
        if len(self.tipe)==1:
            print(f"{typeStrings[self.tipe[0]]}")
        if len(self.tipe)>1:
            print(f"{typeStrings[self.tipe[0]]} / {typeStrings[self.tipe[1]]}")
        print(f"Current HP: {self.currenthp}, {self.currenthp/self.maxhp*100}%")
        
    def summary(self):
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
        print("\n** These stats reflect in-battle boosts and nerfs...")
        self.showMoves()
        print("##############################################")
    
    def showMoves(self):
        print(f"############ {self.name}'s Moves #############")
        for i in range(len(self.knownMoves)):
            print(f"[{i+1}] {mov[self.knownMoves[i]]['name']}\t{typeStrings[int(mov[self.knownMoves[i]]['type'])]}\t{self.PP[i]}/{mov[self.knownMoves[i]]['pp']} PP")
    
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
        
class battle:
    def __init__(self):
        #A for Red B for Blue?
        self.rocksA=False
        self.rocksB=False
        self.steelA=False
        self.steelB=False
        self.stickyA=False
        self.stickyB=False
        self.spikesA=0 #up to 3
        self.spikesB=0
        self.toxicA=0 #up to 2 
        self.toxicB=0
        #tailwind?
        #reflect
        #light screen
    
    def clearfield(self):
        self.rocksA=False
        self.rocksB=False
        self.steelA=False
        self.steelB=False
        self.stickyA=False
        self.stickyB=False
        self.spikesA=0 #up to 3
        self.spikesB=0
        self.toxicA=0 #up to 2 
        self.toxicB=0
    
    def landing(self,poke,side):
        #this function will simulate pokemon being damaged by entry hazards
        #need to make functions for mon() of the entry hazard damages being done
        #need to check for rocks, spikes, toxix spikes (except for poisons) and sticky web
        #only for grounded pokemon tho...
        rocksOn = ( side == "red" and self.rocksA ) or ( side == "blue" and self.rocksB )
        stickyOn = ( side == "red" and self.stickyA ) or ( side == "blue" and self.stickyB )
        spikesOn = ( side == "red" and self.spikesA > 0 ) or ( side == "blue" and self.spikesB > 0)
        toxicOn = ( side == "red" and self.toxicA > 0 ) or ( side == "blue" and self.toxicB > 0)
        ##some hazards
        if rocksOn:
            poke.rocksDamage()
        ##hazards flying and levitating are immune to
        if poke.grounded:
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
                        t.sleep(0.3)
                    else:
                        poke.toxicAffliction(self.toxicA)
                elif poke.battlespot == "blue":
                    if 7 in poke.tipe:
                        self.toxicB = 0
                        print(f"{poke.name} absorbs the toxic spikes!")
                        t.sleep(0.3)
                    else:
                        poke.toxicAffliction(self.toxicB)
        # there will be more entry hazards unfortunately
        return
        
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
                    
            
#def damage(level,attack,plaintiffTipe,defense,defendantTipe,power,moveTipe,note):
def damage(attacker,defender,power,moveTipe,isSpecial,note):
    ####damage read-out strings####
    damages=[]
    ####set some variable straight
    level=attacker.level
    if isSpecial:
        attack=attacker.bsa
        defense=defender.bsd
        statNerf=statStages[attacker.sastage] #will be ignored if negative and crit
        statBoost=statStages[defender.sdstage] #ignored if positive and crit
        burn=1.
    else:
        attack=attacker.bat
        defense=defender.bde
        statNerf=statStages[attacker.atstage]
        statBoost=statStages[defender.destage]
        ####burn####
        if attacker.burned:
            burn=0.5
            damages.append("The burn reduces damage...")
        else:
            burn=1.
    plaintiffTipe=attacker.tipe
    defendantTipe=defender.tipe
    ####weather ball#### doubles power and changes type
    if ("weatherball" in note) and (weather!="clear"):
        power*=2.
        if weather=="sunny":
            moveTipe=1
        if weather=="rain":
            moveTipe=2
        if weather=="sandstorm":
            moveTipe=12
        if weather=="hail":
            moveTipe=5
        damages.append("Weather Ball changes type!")
    #solarbeam gets nerfed in inclement weather
    if ("solar" in note) and (weather=="rain" or weather=="sandstorm" or weather=="hail"):
        power*=0.5
    #earthquake, bulldoze and magnitude nerfed on grassy terrain
    if ("nerfGrassy" in note) and (terrain=="grassy"):
        power*=0.5
    ####weather damage boost####
    weatherBonus=1.
    if weather=='sunny':
        if moveTipe==1:
            weatherBonus=4/3
            damages.append("Sun boost!")
        elif moveTipe==2:
            weatherBonus=2/3
            damages.append("Weakened by the sunlight...")
    elif weather=='rain':
        if moveTipe==1:
            weatherBonus=2/3
            damages.append("Weakened by the rain...")
        elif moveTipe==2:
            weatherBonus=4/3
            damages.append("Rain boost!")
    ####terrain moves####
    if terrain=='none':
        pass
    else: #only check for terrain boosts when there is a non-none terrain
        #when terrains come into play
        grass=(terrain=="grassy") and (moveTipe==3) and (attacker.grounded)
        psychic=(terrain=="psychic") and (moveTipe==10) and (attacker.grounded)
        electric=(terrain=="electric") and (moveTipe==4) and (attacker.grounded)
        fairy=(terrain=="misty") and (moveTipe==14) and (defender.grounded)
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
    ####random fluctuation 85%-100%
    rando=rng.integers(85,101)*0.01
    ####STAB####
    STAB=1.
    if moveTipe in plaintiffTipe:
        STAB=1.5
        damages.append("Same Type Attack Bonus!")
    ####type effectiveness####
    tyype=checkTypeEffectiveness(moveTipe,defendantTipe)
    ####modifiers united####
    damageModifier=weatherBonus*critical*rando*STAB*tyype*burn
    ####damage calculation####
    ans=((((2*level)/5 + 2)*power*attack/defense)/50 + 2)*damageModifier
    return ans,tyype,damages

#calculates pokemon stats (non-HP)
def stats(level,base,IV,EV,nature):
    ans=((2*base+IV+EV/4)*level/100+5)*nature
    return ans

#calculates HP stat
def HP(level,base,IV,EV):
    ans=((2*base+IV+EV/4)*level/100)+level+10
    return ans

def checkTypeEffectiveness(moveTipe,defendantTipe):
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
            t.sleep(0.4)
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
    
#check party for non fainted pokemon
def checkBlackout(party):
    p=0
    alive=[]
    for i in range(len(party)):
        if party[i].fainted==False:
            p+=1
            alive.append(i)
    return p,alive

#check status of battle
def checkBattle(red,blue):
    print(f"\n****** {blue.name} ({opponentName}) ******")
    if blue.dualType:
            print(f"{typeStrings[blue.tipe[0]]} // {typeStrings[blue.tipe[1]]}")
    else:
        print(f"{typeStrings[blue.tipe[0]]}")
    #should be all status conditions
    if blue.poisoned:
        print("__ POISONED __")
    if blue.badlypoisoned:
        print("__ BADLY POISONED __")
    if blue.burned:
        print("__ BURNED __")
    if blue.paralyzed:
        print("__ PARALYZED __")
    if blue.frozen:
        print("__ FROZEN __")
    if blue.sleep:
        print("__ ASLEEP __")
    if blue.confused:
        print("** confused **")
    #show hp
    if blue.currenthpp>=91:
        print(f"HP |############| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<91 and blue.currenthpp>=82:
        print(f"HP |###########.| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=82 and blue.currenthpp>75:
        print(f"HP |##########..| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=75 and blue.currenthpp>66:
        print(f"HP |#########...| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=66 and blue.currenthpp>58:
        print(f"HP |########....| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=58 and blue.currenthpp>50:
        print(f"HP |#######.....| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=50 and blue.currenthpp>41:
        print(f"HP |######......| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=41 and blue.currenthpp>33:
        print(f"HP |#####.......| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=33 and blue.currenthpp>25:
        print(f"HP |####........| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=25 and blue.currenthpp>16:
        print(f"HP |###.........| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=16 and blue.currenthpp>8:
        print(f"HP |##..........| {format(blue.currenthpp,'.2f')}%")
    if blue.currenthpp<=8 and blue.currenthpp>0:
        print(f"HP |#...........| {format(blue.currenthpp,'.2f')}%")
    #stat boosts
    blueStats=[blue.atstage-6,blue.destage-6,blue.sastage-6,blue.sdstage-6,blue.spstage-6,blue.acstage-6,blue.evstage-6]
    statstrs=["Atk :","Def :","Sp.A:","Sp.D:","Spd :","Accu:","Evas:"]
    print("\nStat Boosts and Nerfs\n****************************")
    for i in range(len(blueStats)):
        if blueStats[i]==0:
            print(statstrs[i]+" none")
        elif blueStats[i]>0:
            print(statstrs[i]+f" +{blueStats[i]}")
        elif blueStats[i]<0:
            print(statstrs[i]+f" {blueStats[i]}")
    print("------------------------------------")
    print(f"************ {red.name} (You) ************")
    if red.dualType:
            print(f"{typeStrings[red.tipe[0]]} // {typeStrings[red.tipe[1]]}")
    else:
        print(f"{typeStrings[red.tipe[0]]}")
    #should be all status conditions
    if red.poisoned:
        print("__POISONED__")
    if red.badlypoisoned:
        print("__BADLY_POISONED__")
    if red.burned:
        print("__BURNED__")
    if red.paralyzed:
        print("__PARALYZED__")
    if red.frozen:
        print("__FROZEN__")
    if red.sleep:
        print("__ASLEEP__")
    if red.confused:
        print("**confused**")
    #show hp
    if red.currenthpp>=91:
        print(f"HP |############| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<91 and red.currenthpp>=82:
        print(f"HP |###########.| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=82 and red.currenthpp>75:
        print(f"HP |##########..| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=75 and red.currenthpp>66:
        print(f"HP |#########...| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=66 and red.currenthpp>58:
        print(f"HP |########....| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=58 and red.currenthpp>50:
        print(f"HP |#######.....| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=50 and red.currenthpp>41:
        print(f"HP |######......| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=41 and red.currenthpp>33:
        print(f"HP |#####.......| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=33 and red.currenthpp>25:
        print(f"HP |####........| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=25 and red.currenthpp>16:
        print(f"HP |###.........| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=16 and red.currenthpp>8:
        print(f"HP |##..........| {format(red.currenthpp,'.2f')}%")
    if red.currenthpp<=8 and red.currenthpp>0:
        print(f"HP |#...........| {format(red.currenthpp,'.2f')}%")
    #stat boosts
    redStats=[red.atstage-6,red.destage-6,red.sastage-6,red.sdstage-6,red.spstage-6,red.acstage-6,red.evstage-6]
    statstrs=["Atk :","Def :","Sp.A:","Sp.D:","Spd :","Accu:","Evas:"]
    print("\nStat Boosts and Nerfs\n****************************")
    for i in range(len(redStats)):
        if redStats[i]==0:
            print(statstrs[i]+" none")
        elif redStats[i]>0:
            print(statstrs[i]+f" +{redStats[i]}")
        elif redStats[i]<0:
            print(statstrs[i]+f" {redStats[i]}")
    print("------------------------------------")
    print("-------Battle Settings-------")
    if weather=="clear":
        weat="CLEAR"
    elif weather=="sunny":
        weat="SUNNY"
    elif weather=="rain":
        weat="RAINING"
    elif weather=="sandstorm":
        weat="SANDSTORM"
    elif weather=="hail":
        weat="HAILING"
    print(f"Weather : {weat}")
    if terrain=="none":
        terr="NONE"
    elif terrain=="grassy":
        terr="GRASSY"
    elif terrain=="electric":
        terr="ELECTRIC"
    elif terrain=="psychic":
        terr="PSYCHIC"
    elif terrain=="misty":
        terr="MISTY"
    print(f"Terrain : {terr}")
    print("\n___ End of battle status ___")
    
    
#moves have pwr, phys/spec, type, accu, descipt
def moveInfo(moveCode):
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

#class party():
    #def __init__(self):
        
#codex encodes all type matchups, first index is attacking the second index
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
struggleInd=struggle #move index of struggle
mo=list(range(len(mov)))
mo.remove(struggleInd) #get struggle out of pool of moves

#battle setting
Weathers=['clear','sunny','rain','sandstorm','hail']
Terrains=['none','electric','grassy','misty','psychic']
#set weather and terrain, random
weather=rng.choice(Weathers)
terrain=rng.choice(Terrains)
indigo = battle()
#but i still make the rules
#weather='sandstorm'
#terrain='grassy'
weatherCounter=np.inf #weather lasts indefinitely when encountered naturally!
if terrain=='none':
    terrainCounter=np.inf
else:
    terrainCounter=5 #terrain only lasts 5 (or 8) turns, all the time

#team settings
#user
#starter=mon(int(rng.normal(loc=80,scale=3.)),"Bulbasaur",hpbase=45,atbase=49,debase=49,sabase=65,sdbase=65,spbase=45,tipe=np.array([3,7]))
starter=makeMon(rng.integers(len(dex)),int(rng.normal(loc=80,scale=30)))
ranMoves=rng.choice(mo,size=6,replace=False)
starter.knownMoves=list(ranMoves)
starter.PP=[mov[i]["pp"] for i in ranMoves]
#oppo
rival=makeMon(rng.integers(len(dex)),starter.level-1)
rival2=makeMon(rng.integers(len(dex)),starter.level+5)
bugs=rng.choice(mo,size=6,replace=False)
#bugs=[28,26,32,42]
rival.knownMoves=list(bugs)
rival.PP=[mov[i]["pp"] for i in bugs]
boos=rng.choice(mo,size=6,replace=False)
rival2.knownMoves=list(boos)
rival2.PP=[mov[i]["pp"] for i in boos]
#stuff them into their parties
userParty=[starter]
trainerParty=[rival,rival2]
#
opponentName="OPPONENT"
################

print("\n... A Python game by Antoine D. ...")
t.sleep(0.7)
print("** Welcome to the Wonderful World of Pokemon Simulation! **")
t.sleep(0.7)
while 1:
    userChoice=input("\n[P]okemon\n[B]attle!\n[N]ursery\n[D]ex Selection\n[T]raining\n[M]ove Tutor\nPokemon [C]enter\n[O]pponent Set\nBattle [S]etting\n[R]eset Party\n[L]oad\nMove D[E]leter\n:")
    
    #user setting the weather and terrain
    if userChoice=="s" or userChoice=="S":
        print("\n------------ Set the Stage of Battle ------------\n-------------------------------------------------")
        t.sleep(0.4)
        while 1: #user input loop
            print("Current Battle conditions:")
            t.sleep(0.4)
            print(f"Weather: {weather}\nTerrain: {terrain}")
            print("\nOptions:\n[1] Randomize weather and terrain\n[2] Randomize just weather\n[3] Randomize just terrain\n[4] Set manually\n")
            setChoice=input("What [#] would you like to do?\nor [b]ack: ")
            #go back
            if setChoice=="b" or setChoice=="B":
                break
            #randomize both
            if setChoice=="1":
                weather=rng.choice(Weathers)
                terrain=rng.choice(Terrains)
                print("Conditions have been randomized!")
                t.sleep(0.4)
            #randomize weather
            if setChoice=="2":
                weather=rng.choice(Weathers)
                print("Weather has been randomized!")
                t.sleep(0.4)
            #randomize terrain
            if setChoice=="3":
                terrain=rng.choice(Terrains)
                print("Terrain has been randomized!")
                t.sleep(0.4)
            #manual set
            if setChoice=="4":
                while 1: #user input loop, weather or terrain
                    conChoice=input("Set\n[1] Weather \n[2] Terrain\nor [b]ack: ")
                    if conChoice=="b" or conChoice=="B":
                        break
                    #weather
                    if conChoice=="1":
                        while 1: #user input loop, whats the new terrain
                            print("")
                            for i in range(len(Weathers)):
                                print(f"{i}\t{Weathers[i]}")
                            newWeath=input("What should the new weather be?\n[#] or [b]ack: ")
                            if newWeath=="b" or newWeath=="B":
                                break
                            try:
                                weather=Weathers[int(newWeath)]
                                print("New weather set!")
                                break
                            except IndexError:
                                print("*\n** Entry out of range **\n*")
                            except ValueError:
                                print("*\n** Not a valid entry **\n*")
                    #weather
                    if conChoice=="2":
                        while 1: #user input loop, whats the new terrain
                            print("")
                            for i in range(len(Terrains)):
                                print(f"{i}\t{Terrains[i]}")
                            newTerr=input("What should the new terrain be?\n[#] or [b]ack: ")
                            if newTerr=="b" or newTerr=="B":
                                break
                            try:
                                terrain=Terrains[int(newTerr)]
                                print("New terrain set!")
                                break
                            except IndexError:
                                print("*\n** Entry out of range **\n*")
                            except ValueError:
                                print("*\n** Not a valid entry **\n*")
            #more options to change cattle conditions
                                
    ####Reseting the Opponent in Battle function####
    if userChoice=='o' or userChoice=="O":
        print("\n________ Opponent Reset ________")
        t.sleep(0.7)
        aceChoice=input("Would you like to set your current team as the battle opponent?\n[y] or [b] to go back:")
        if aceChoice=='y' or aceChoice=="Y":
            trainerParty=copy.deepcopy(userParty)
            print("The Battle Opponent has a new Party! Good Luck!")
            t.sleep(0.7) #kills
        else:
            print("Leaving Opponent Reset...")
            t.sleep(0.7) #kills
        #end of opponent set, back to main screen

    ####Battles####
    if userChoice=="b" or userChoice=="B":
        ####Battle starts####
        print("\nYou've been challenged to a Pokemon Battle!")
        t.sleep(1)
        userMon=userParty[0]
        userInd=0
        print(f"\n{userMon.name}! I choose you!")
        t.sleep(1)
        trainerMon=trainerParty[0]
        trainerInd=0
        print(f"\n{opponentName}: {trainerMon.name}! Go!")
        t.sleep(1)
        turn=1
        ####turn begins####
        while 1: #only breaks when BattleOver is True
            #battle conditions?
            #indigo=battle()
            ####fight/run/pokemon/bag####
            while 1: #turn loop, advances to pokemon move usage if user uses a move or shifts, otherwise the loop accomplishes nothing
                battleOver=False
                switching=False
                fighting=False
                charging=False
                print(f"\n____________ Turn {turn} ____________\n")
                userMon.chosen("user")
                trainerMon.chosen("cpu")
                userMon.inBattle()
                trainerMon.inBattle()
                #----UI----#
                print(f"\n{opponentName}:\n{trainerMon.name} // Level {trainerMon.level}")
                print(f"HP: {format(trainerMon.currenthpp,'.2f')}%")
                print("\n............Your team:")
                print(f"............{userMon.name} // Level {userMon.level}")
                print(f"............HP: {format(userMon.currenthp,'.2f')}/{format(userMon.maxhp,'.2f')} ({format(userMon.currenthpp,'.2f')}%)")
                if userMon.resting:
                    resting=True
                    charging=False
                    print(f"\n{userMon.name} is recharging and can't move...")
                elif userMon.charged:
                    charging=True
                    resting=False
                else:
                    resting=False
                    charging=False
                    userMove=input(f"What should {userMon.name} do?\n[F]ight\n[P]okemon\n[S]tatus\n[R]un\n: ")
                    ####run away to end battle####
                    if userMove=='r':
                        print(f"You and {userMon.name} get away safely!")
                        battleOver=True
                        break
                    ###check status of battle?
                    if userMove=="s" or userMove=="S":
                        checkBattle(userMon,trainerMon)
                        input("enter anything to go back...")
    
                    #go party pokemon
                    if userMove=='p':
                        while 1:
                            print("\n****************\nParty Pokemon:")
                            for i in range(len(userParty)):
                                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}%")
                            partyChoice=input("Select a Pokemon...\n[#] or [b] to go back: ")
                            if partyChoice=='b' or partyChoice=="B":
                                break #goes back to user turn loop from pokemon selection
                            try:
                                select=userParty[int(partyChoice)-1]
                                nuserInd=int(partyChoice)-1
                                select.battleSummary()
                            except ValueError:
                                print("\nEnter the [#] corresponding to a Pokemon!\nor [b]ack")
                            except IndexError:
                                print("\nEnter the [#] corresponding to a Pokemon!\nor [b]ack")
                            else:
                                while 1:
                                    pChoice=input(f"What to do with {select.name}?\n[s]hift into battle, see [m]oves, or [b]ack: ")
                                    #go back
                                    if pChoice=="b" or pChoice=="B":
                                        break
                                    #show move details
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
                                                    t.sleep(0.4) #drama
                                                #we got all the move info out?, go back to pokemon?
                                                pause=input("\nEnter anything to continue back to Pokemon summary...")
                                                break 
                                    #switch pokemon
                                    if pChoice=="s" or pChoice=="S":
                                        #keep fainted pokemon off the field
                                        if select.fainted:
                                            print("\n** Cannot switch in fainted Pokemon! **")
                                            break
                                        if nuserInd==userInd:
                                            print(f"\n** {select.name} is already in battle! **")
                                            break
                                        switching=True
                                        break
                                    #anything other than approved things repeat the loop
                                if switching:
                                    break
                            #end of pokemon selection loop
                        #end of party pokemon block
                        #just dawned on me that user pokemon switching does not need to take place entirely in this if statement
    
                    #fight
                    if userMove=='f':                    
                        #fighting options
                        while 1: #move input loop
                            for i in range(len(userMon.knownMoves)):
                                print(f"[{i+1}] \t{getMoveInfo(userMon.knownMoves[i])['name']} \t{userMon.PP[i]} PP")
                            if np.count_nonzero(userMon.PP)==0:
                                print(f"{userMon.name} can only Struggle!")
                                fighting=True
                                moveDex=struggleInd
                                break
                            userFight=input(f"What move should {userMon.name} use?\n[#] or [b]: ")
                            #go back
                            if userFight=='b':
                                break
                            if userFight.split()[0]=="i" or userFight.split()[0]=="I":
                                try:
                                    movez=userFight.split()[1:] #pokemon movelist index (string)
                                    movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                    movez=[userMon.knownMoves[i] for i in movez] #pokemon move movedex index
                                except ValueError:
                                    print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                                except IndexError:
                                    print("\n** Use the indices to select moves to take a closer look at. **")
                                else:
                                    for i in range(len(movez)):
                                        print("")
                                        moveInfo(movez[i])
                                        t.sleep(0.4) #drama
                                    #we got all the move info out?, go back to pokemon?
                                    input("\nenter anything to continue...")
                            else:
                                #try to use user input to call a move
                                try:
                                    fightChoice=int(userFight)-1 #make sure given input refers to a move
                                    if userMon.PP[fightChoice]==0:
                                        print(f"{userMon.name} does not have enough energy to use this move!")
                                        continue
                                    moveDex=userMon.knownMoves[fightChoice]
                                    fighting=True
                                    break
                                except:
                                    print("\n**Enter one of the numbers above.**")
                    
                ####after either swithing or attacking
                if fighting or switching or resting or charging:
                    #user shifting?
                    if switching:
                        #put current pokemon back?
                        userMon.withdraw()
                        userParty[userInd]=userMon
                        print(f"\n{userMon.name} come back!")
                        t.sleep(0.7)
                        #set new selection as user pokemon
                        userMon=select
                        userInd=nuserInd
                        print(f"{userMon.name}, it's your turn!")
                        t.sleep(0.7)
                        userMon.chosen("user")
                        userMon.inBattle()
                        indigo.landing(userMon, "red")
                    #does the trainer mon need to rest?
                    if trainerMon.resting:
                        trainerRest=True
                        print(f"\n{trainerMon.name} must recharge and cannot attack!")
                    else:
                        trainerRest=False
                    if trainerMon.charged:
                        trainerCharge=True
                    else:
                        trainerCharge=False
                    trainerShift=False
                    #10% chance for opponent to randomly switch pokemon
                    #check how many nonfainted pokemon trainer has
                    nfp,nfpList=checkBlackout(trainerParty)
                    if nfp>1 and rng.random()<0.1 and (not trainerRest) and (not trainerMon.charged): #if trainer has more than 1 non fainted pokemon, 10% of the time, but not if their pokemon has to recharge
                        del nfpList[int(np.argwhere(np.array(nfpList)==trainerInd))] #removing the current pokemon from the list of nonfainted pokemon in the party
                        trainerMon.withdraw()
                        trainerParty[trainerInd]=trainerMon #put pokemon away
                        print(f"\n{opponentName}'s {trainerMon.name} is withdrawn!")
                        t.sleep(0.7)
                        #take new pokemon out, random
                        nTrainerInd=rng.choice(nfpList)
                        trainerInd=nTrainerInd
                        trainerMon=trainerParty[trainerInd]
                        print(f"{opponentName}: {trainerMon.name}! Finish them off!")
                        t.sleep(0.7)
                        trainerMon.chosen("cpu")
                        trainerMon.inBattle()
                        indigo.landing(trainerMon,"blue")
                        trainerShift=True
                        #end of trainer switching
                    #set boolean to true if user has higher effective speed stat
                    userFast=userMon.bsp>=trainerMon.bsp
                    uFaint=False
                    tFaint=False
                    flinching=False
                    if trainerMon.charged:
                        pass #trainMoveInd should already be set from last round
                    else:
                        trainMoveInd=rng.choice(range(len(trainerMon.knownMoves)))
                    ##USER FASTER##
                    if userFast:
                        #USER ATTACK
                        #make sure user/trainer didn't switch in this turn
                        if fighting or charging: #is never set to true if resting is true this turn, not set to true if the user decided to switch mons
                            userMon.move(trainerMon, moveDex)
                            if trainerMon.fainted:
                                tFaint=True
                            if userMon.fainted:
                                uFaint=True
                            if trainerMon.flinched and (not tFaint):
                                flinching=True
                                print(f"\n{opponentName}'s {trainerMon.name} flinches and can't attack!")
                                t.sleep(0.7)
                        ##OPPO ATTACK
                        if (not trainerShift) and (not flinching) and (not tFaint):
                            if uFaint:
                                print(f"\nThere is no target for {trainerMon.name} to attack!")
                                t.sleep(0.7)
                            elif np.count_nonzero(trainerMon.PP)==0: #if trainer is out of PP, use struggle
                                trainerMon.move(userMon,struggleInd)
                            else: #otherwise, cue up one of the known moves
                                trainerMon.move(userMon,trainerMon.knownMoves[trainMoveInd])
                            if userMon.fainted:
                                uFaint=True
                            if trainerMon.fainted:
                                tFaint=True
                    ##USER SLOWER##
                    else:
                        ##OPPO ATTACK##
                        if (not trainerShift) and (not trainerRest):
                            if np.count_nonzero(trainerMon.PP)==0: #if trainer is out of PP, use struggle
                                trainerMon.move(userMon,struggleInd)
                            else: #otherwise, cue up one of the known moves
                                trainerMon.move(userMon,trainerMon.knownMoves[trainMoveInd])
                            #check for faints
                            if userMon.fainted:
                                uFaint=True
                            if trainerMon.fainted:
                                tFaint=True
                            #check for flinch
                            if userMon.flinched and (not uFaint): #make sure neither pokemon just fainted after this attack
                                flinching=True
                                print(f"\n{userMon.name} flinches and can't attack!")
                                t.sleep(0.7)
                        ##USER ATTACK##
                        if (fighting or charging) and (not flinching) and (not uFaint):
                            if tFaint:
                                print(f"\nThere is no target for {userMon.name}'s attack!")
                                t.sleep(0.7)
                            else:
                                userMon.move(trainerMon,moveDex)
                            if trainerMon.fainted:
                                tFaint=True
                            if userMon.fainted:
                                uFaint=True
                    #end of turn, pokemon have attacked
                    #regardless of whether pokemon fainted this turn, if they were recognized to be resting while the attacks were exchanged, we can repeal the resting tags
                    if resting:
                        userMon.resting=False
                    if trainerRest:
                        trainerMon.resting=False
                    if flinching: #moves have already been used, we can reset them
                        userMon.flinched=False
                        trainerMon.flinshed=False
                    #check for USER BLACKOUT
                    if checkBlackout(userParty)[0]==0:
                        battleOver=True
                        print("\nYou're out of usable Pokemon!")
                        t.sleep(0.7)
                        print("You blacked out!")
                        t.sleep(0.7)
                        break
                    #check for TRAINER BLACKOUT
                    if checkBlackout(trainerParty)[0]==0:
                        battleOver=True
                        print(f"\n{opponentName} is out of usable pokemon!\nYou win!")
                        t.sleep(0.7)
                        break
                    print("")
                    #damages for pokemon that made it through the turn
                    #order of end of battle damages: burn,poison,badPoison,weather,grassy heal
                    #burns
                    if userMon.burned and (not uFaint):
                        userMon.burnDamage()
                    if trainerMon.burned and (not tFaint):
                        trainerMon.burnDamage()
                    #poisons
                    if userMon.poisoned and (not uFaint):
                        userMon.poisonDamage()
                    if trainerMon.poisoned and (not tFaint):
                        trainerMon.poisonDamage()
                    #badPoisons
                    if userMon.badlypoisoned and (not uFaint):
                        userMon.badPoison()
                        userMon.poisonCounter+=1
                    if trainerMon.badlypoisoned and (not tFaint):
                        trainerMon.badPoison()
                        trainerMon.poisonCounter+=1
                    #weather
                    if weather=="sandstorm":
                        if (not uFaint):
                            userMon.sandDamage()
                        if (not tFaint):
                            trainerMon.sandDamage()
                    if weather=="hail":
                        if (not uFaint):
                            userMon.hailDamage()
                        if (not tFaint):
                            trainerMon.hailDamage()
                    #grassy terrain heal
                    #make sure we're not bringing anyone back to life after possible damages
                    if userMon.fainted:
                        uFaint=True
                    if trainerMon.fainted:
                        tFaint=True
                    if terrain=="grassy":
                        if userMon.grounded and (not uFaint):
                            userMon.grassyHeal()
                        if trainerMon.grounded and (not tFaint):
                            trainerMon.grassyHeal()
                    #make switches in case of faints
                    #user switch
                    if uFaint:
                        #check for USER BLACKOUT
                        if checkBlackout(userParty)[0]==0:
                            battleOver=True
                            print("\nYou're out of usable Pokemon!")
                            t.sleep(0.7)
                            print("You blacked out!")
                            t.sleep(0.7)
                            break
                        else:
                            bShifted=False #forcing the user to shift to a non-fainted pokemon
                            while 1:
                                print("\n****************\nParty Pokemon:")
                                for i in range(len(userParty)):
                                    print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                                newPoke=input("Select a Pokemon for battle...\n[#]: ")
                                try:
                                    nuserInd=int(newPoke)-1
                                    select=userParty[nuserInd]
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
                                                        t.sleep(0.4) #drama
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
                                            userMon.withdraw()
                                            userParty[userInd]=userMon
                                            print(f"\n{userMon.name} come back!")
                                            t.sleep(0.4)
                                            #set new selection as user pokemon
                                            userMon=select
                                            userInd=nuserInd
                                            print(f"{userMon.name}, it's your turn!")
                                            t.sleep(0.4)
                                            userMon.chosen("user")
                                            userMon.inBattle()
                                            indigo.landing(userMon,"red")
                                            bShifted=True
                                            break
                                        #anything other than y repeats the loop
                                    if bShifted:
                                        break
                    #oppo switch
                    if tFaint:
                        #check for TRAINER BLACKOUT
                        blk,blkList=checkBlackout(trainerParty)
                        if blk==0:
                            battleOver=True
                            print(f"\n{opponentName} is out of usable pokemon!\nYou win!")
                            t.sleep(0.7)
                            break
                        else:
                            #put fainted one away
                            trainerMon.withdraw()
                            trainerParty[trainerInd]=trainerMon
                            #take out random non fainted one
                            trainerInd=rng.choice(blkList)
                            trainerMon=trainerParty[trainerInd]
                            trainerMon.chosen("cpu")
                            trainerMon.inBattle()
                            indigo.landing(trainerMon, "blue")
                            print(f"\n{opponentName}: {trainerMon.name}! I'm counting on you!")
                            t.sleep(0.7)
                    #pokemon have been switched in
                    print("")
                    #is weather still happening
                    weatherCounter-=1
                    if weather=='sunny':
                        if weatherCounter==0:
                            weather='clear'
                            weatherCounter=np.inf
                            print("The harsh sunlight is fading...")
                            t.sleep(0.7)
                        else:
                            print("The sunlight is harsh!")
                            t.sleep(0.7)
                    if weather=='rain':
                        if weatherCounter==0:
                            weather='clear'
                            weatherCounter=np.inf
                            print("The rain stops...")
                            t.sleep(0.7)
                        else:
                            print("It's raining!")
                            t.sleep(0.7)
                    if weather=='sandstorm':
                        if weatherCounter==0:
                            weather='clear'
                            weatherCounter=np.inf
                            print("The sandstorm is subsiding...")
                            t.sleep(0.7)
                        else:
                            print("The sandstorm is raging!")
                            t.sleep(0.7)
                    if weather=='hail':
                        if weatherCounter==0:
                            weather='clear'
                            weatherCounter=np.inf
                            print("The hail stops")
                            t.sleep(0.7)
                        else:
                            print("It's hailing!")
                            t.sleep(0.7)
                    #is the terrain still on?
                    terrainCounter-=1
                    if terrainCounter==0:
                        terrain="none"
                        terrainCounter=np.inf
                        print("The terrain faded away...")
                        t.sleep(0.7)
                    elif terrain=="grassy":
                        print("The battlefield is grassy!")
                        t.sleep(0.7)
                    elif terrain=="electric":
                        print("The battlefield is electrified!")
                        t.sleep(0.7)
                    elif terrain=="psychic":
                        print("The battlefield is weird!")
                        t.sleep(0.7)
                    elif terrain=="misty":
                        print("The battlefield is misty!")
                        t.sleep(0.7)
                    turn+=1
                    #loop to next turn
            if battleOver: #if user ran
                break #breaks battle loop, back to main screen
            #loop back to "turn begins"
            #if a pokemon has fainted, loop ends
        print("The battle ended!")
        #clean up
        indigo.clearfield()
        weather=rng.choice(Weathers)
        weatherCounter=np.inf
        terrain=rng.choice(Terrains)
        if terrain=="none":
            terrainCounter=np.inf
        else:
            terrainCounter=5
        for i in trainerParty:
            i.withdraw()
            i.restore()
        for i in userParty:
            i.withdraw()
        t.sleep(0.7) #kills
    ###end of battle block###
        
    #### check party pokemon? aa:pokemonparty ####
    if userChoice=="p" or userChoice=="P":
        while 1:
            print("\n******** Party Pokemon ********\n*******************************\n")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
            print("\n*******************************\n")
            partyChoice=input("Enter a number to see a Pokemon's summary...\n[#] or [b]ack: ")
            #go back to main screen
            if partyChoice=='b' or partyChoice=="B":
                print("Leaving Party screen...")
                t.sleep(0.7) #kills
                break
            try:
                pokeInd=int(partyChoice)-1
                selMon=userParty[pokeInd]
            except ValueError:
                print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
            except IndexError:
                print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
            else:
                while 1:
                    selMon.summary()
                    sumChoice=input(f"What to do with {selMon.name}?\nset [f]irst, see [m]oves [s]ave, [j]udge or [b]ack: ")
                    #go back to pokemon selection
                    if sumChoice=='b' or sumChoice=="B":
                        t.sleep(0.7)
                        break
                    #save
                    if sumChoice=='s':
                        while 1:
                            savename=input("Enter name of savefile...\n[blank] to use default savefile name\nor [b]ack\n: ")
                            if (savename=='b') or (savename=='B'):
                                t.sleep(0.7)
                                break
                            if savename=='':
                                selMon.save()
                                print(f"{selMon.name} was saved to the file!\n")
                                t.sleep(0.7) #kills
                                continue
                            else:
                                selMon.save(savename)
                                print(f"{selMon.name} was saved to the file!\n")
                                t.sleep(0.7) #kills
                                continue
                        #
                    #set first
                    if sumChoice=='f':
                        if pokeInd==0:
                            print(f"{selMon.name} is already first!")
                            continue
                        moving=userParty.pop(pokeInd)
                        userParty.insert(0,moving)
                        print(f"{moving.name} was moved to the front!")
                        t.sleep(0.7) #kills
                        continue
                    #
                    if sumChoice=="m" or sumChoice=="M":
                        while 1: #user input loop
                            selMon.showMoves()
                            movChoice=input("Which move to look at?\n[#] or [b]ack: ")
                            if movChoice=="b" or movChoice=="B":
                                #leave move info selection, back to what to do w pokemon
                                break
                            #try to get numbers from user input
                            try:
                                movez=movChoice.split() #pokemon movelist index (string)
                                movez=[int(i)-1 for i in movez] #pokemon movelist indices (int)
                                movez=[selMon.knownMoves[i] for i in movez] #pokemon move movedex index
                            except ValueError:
                                print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                            except IndexError:
                                print("\n** Use the indices to select moves to take a closer look at. **")
                            else:
                                for i in range(len(movez)):
                                    print("")
                                    moveInfo(movez[i])
                                    t.sleep(0.4) #drama
                                #we got all the move info out?, go back to pokemon?
                                pause=input("\nEnter anything to continue back to Pokemon summary...")
                                break
                    #judge
                    if sumChoice=="j" or sumChoice=="J":
                        selMon.appraise()
            #end of while block
        print("Going back to main screen...")
        t.sleep(1)
        #end of party pokemon
    ###end of party display block###

    ####pokemon aa:nursery####
    if userChoice=='n' or userChoice=='N':
        print("\n____ Welcome to the Pokemon Nursery! ____")
        t.sleep(1)
        print("Here, you can create Pokemon from scratch!")
        t.sleep(1)
        ####nursery loop####
        while 1:
            nurseChoice=input("What do you want to do?\nNew [P]okemon!!\n[B]ack\n:")
            if nurseChoice=='b' or nurseChoice=='B':
                break #exits nursery loop
            ####new pokemon####
            if nurseChoice=='p':
                newName=input("Would you like to give your Pokemon a name?: ")
                print(f"Let's get {newName} some STATS")
                while 1: #stat input loop
                    statS=input("Enter 6 stats [1-255]\n[HP] [ATK] [DEF] [SPA] [SPD] [SPE]\n")
                    try:
                        stat=[int(float(i)) for i in statS.split(" ")]
                        if len(stat)!=6:
                            print("\n!! Enter all 6 stats at once !!")
                            continue
                        if min(stat)>0:
                            break #stats acccepted, exits stat input loop
                        else:
                            print("\n**Base stats must be at least 1**")
                    except ValueError:
                        print("\n** Stats must be numbers **")
                ##type choice##
                print("****************\nPokemon Types:\n0 Normal\n1 Fire\n2 Water\n3 Grass\n4 Electric\n5 Ice\n6 Fighting\n7 Poison\n8 Ground\n9 Flying\n10 Psychic\n11 Bug\n12 Rock\n13 Ghost\n14 Dragon\n15 Dark\n16 Steel\n17 Fairy\n****************")
                while 1: #type input loop
                    newTipe=input(f"Use the legend above to give {newName} a type or two: ")
                    try:
                        newTipe=[int(i) for i in newTipe.split()]
                        if max(newTipe)<=18: #no types above 18
                            if min(newTipe)>=0: #no types below 0
                                break #input valid, exit type input loop
                            else:
                                print("\n** Highest type: 17, lowest type: 0 **")
                        else:
                            print("\n** Highest type: 17, lowest type: 0 **")
                    except ValueError:
                        print("\n** Use the legend above and enter a number (or 2 separated with a space) **")
                ##level input##
                while 1: #level input loop
                    lvlS=input(f"What level should {newName} be? 1-100: ")
                    try:
                        lvlS=int(lvlS)
                        if lvlS>=1:
                            break #break level input
                        else:
                            print("\n** Level must be at least 1 **")
                    except ValueError:
                        print("\n** Enter a number! **")
                ##oh boy nature input###
                while 1:
                    print("Attack : 0\nDefense: 1\nSp. Atk: 2\nSp. Def: 3\nSpeed  : 4\n~~~~~~~~~~")
                    nachup = input(f"What should be {newName}'s boosted stat: ")
                    try:
                        nachup = int(nachup)
                        if (nachup <= 4) and (nachup >= 0):
                            break #stat good
                        else:
                            print("\n!! Enter a number between 0 and 4 !!")
                            t.sleep(.3)
                    except ValueError:
                        print("\n!! Enter a number !!")
                        t.sleep(.3)
                    ##okay if all goes well the code should progress here and we need to ask for hindered nature
                while 1:
                    print("\n~~~~~~~~~~\nAttack : 0\nDefense: 1\nSp. Atk: 2\nSp. Def: 3\nSpeed  : 4\n~~~~~~~~~~")
                    nachdo = input(f"What should be {newName}'s nerfed stat: ")
                    try:
                        nachdo = int(nachdo)
                        if (nachdo <= 4) and (nachdo >= 0):
                            break #stat is good, break input loop
                        else:
                            print("\n!! Enter a number between 0 and 4 !!")
                            t.sleep(.3)
                    except ValueError:
                        print("\n!! Enter a number !!")
                        t.sleep(.3)
                nacher = (nachup, nachdo)
                ##make the pokemon!##
                if len(newTipe)==1:
                    newMon=mon(lvlS,newName,nature=nacher,hpbase=stat[0],atbase=stat[1],debase=stat[2],sabase=stat[3],sdbase=stat[4],spbase=stat[5],tipe=np.array(newTipe))
                if len(newTipe)>1:
                    newMon=mon(lvlS,newName,nature=nacher,hpbase=stat[0],atbase=stat[1],debase=stat[2],sabase=stat[3],sdbase=stat[4],spbase=stat[5],tipe=np.array([newTipe[0],newTipe[1]]))
                print(f"\n{newName} is born!")
                t.sleep(1)
                userParty.append(newMon)
                print("Take good care of them!")
            pass #loops back to start of nursery
        pass #loops back to start of game
    ###end of nursery block
    
    ####training####
    if userChoice=='t':
        print("\n********SuperHyper Training********\nYou can add EVs and IVs to your Pokemon!")
        while 1:
            #choose a pokemon
            print("\n")
            for i in range(len(userParty)):
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level}")
            trainChoice=input("Which Pokemon will we train?:\n[#] or [b]ack: ")
            
            #option to go back, from pokemon selection to main screen
            if trainChoice=='b':
                break
            #user input loop, making sure input is poke#
            while 1:
                try:
                    pokeIndex=int(trainChoice)-1
                    pokeTrain=userParty[pokeIndex]
                    break #confirmed numbers are good, exit user loop
                except:
                    print("\n**Must enter a number of a Pokemon**")
                    trainChoice=input("\nWhich Pokemon will we train?:\n[#]")
                    #ends error catch for pokemon selection
            print(f"\n**** {pokeTrain.name} ****")
            superHyper=input("Manage [E]Vs or [I]Vs or [L]evels\n:") #anything other than options below will skip to the next loop of choose a pokemon
            
            #EVs
            if superHyper=='e':
                while 1:
                    evs=input("Enter 6 numbers (0-252) all at once.\nEVs cannot sum >510.:\n")
                    #option to go back
                    if evs=='b':
                        break #throws us back to choose a pokemon
                    else:
                        evs=evs.split()
                        try:
                            eves=np.array([int(evs[0]),int(evs[1]),int(evs[2]),int(evs[3]),int(evs[4]),int(evs[5])])
                            #make sure values are legal
                            if np.max(eves)<=252.:
                                if np.sum(eves)<=510.:
                                    pokeTrain.hpev=int(evs[0])
                                    pokeTrain.atev=int(evs[1])
                                    pokeTrain.deev=int(evs[2])
                                    pokeTrain.saev=int(evs[3])
                                    pokeTrain.sdev=int(evs[4])
                                    pokeTrain.spev=int(evs[5])
                                    pokeTrain.reStat()
                                    t.sleep(1)
                                    print("\nTraining...")
                                    t.sleep(1)
                                    print(f"\n{pokeTrain.name} finished Super Training and has new stats!")
                                    break #ends ev training, sends back to choose a pokemon
                                else:
                                    print("\n**No more than 510 EVs**")
                                    pass
                                pass
                            else:
                                print("\n**No more than 252 EVs in any stat.**")
                                pass
                            pass
                        except: #catch non-numbers, incomplete sets
                            print("\n**Max EV is 252.**\n**Total EVs cannot sum more than 510.**\n**Input 6 numbers separated by spaces.**")    
                        #if code is here, EV training while loop continues
                    pass
                #end of ev training loop
            
            #IVs        
            if superHyper=='i':
                while 1:
                    ivs=input("Enter 6 numbers (0-31) all at once.:\n")
                    #option to go back, from iv input to choose a pokemon
                    if ivs=='b':
                        break
                    else:
                        ivs=ivs.split() #6 numbers into list of strings
                        try:
                            #make sure we have 6 numbers
                            ives=np.array([int(ivs[0]),int(ivs[1]),int(ivs[2]),int(ivs[3]),int(ivs[4]),int(ivs[5])])
                            if np.max(ives)<=31:
                                pokeTrain.hpiv=int(ivs[0])
                                pokeTrain.ativ=int(ivs[1])
                                pokeTrain.deiv=int(ivs[2])
                                pokeTrain.saiv=int(ivs[3])
                                pokeTrain.sdiv=int(ivs[4])
                                pokeTrain.spiv=int(ivs[5])
                                pokeTrain.reStat()
                                t.sleep(1)
                                print("\nTraining...")
                                t.sleep(1)
                                print(f"{pokeTrain.name} finished Hyper Training and has new stats!")
                                t.sleep(1)
                                break #ends IV training, goes back to choose a pokemon
                            else:
                                print("\n**Maximum IV is 31**")
                        except IndexError: #input couldn't fill 6-item array
                            print("\n**Enter !6! numbers separated by spaces**")
                        except ValueError: #we tried to make an int() out of something non-number
                            print("\n**Enter 6 !numbers! separated by spaces**")
                        #if we get here, an IV was more than 31, loops back to IV input
                    #end of iv input loop
                #end of IV training loop
            
            #level
            if superHyper=='l':
                while 1:
                    try:
                        levl=int(input(f"What level should {pokeTrain.name} be?: "))
                        if levl>0.: #if input was a positive number
                            pokeTrain.level=levl #set pokemon's new level
                            pokeTrain.reStat() #recalcs stats
                            print("\nTraining...")
                            t.sleep(1)
                            print(f"\n{pokeTrain.name} finished training and has new stats!")
                            t.sleep(1)
                            break #exits user input loop
                        else:
                            print("\n**Level must be at least 1**")
                    except:
                        print("\n**Enter a number greater than 0.**")
                    #end of level input while block
                #end of level training block
                
            pass #loops back to training screen
        print("\nLeaving SuperHyper Training...")
        t.sleep(1) #exiting training
    ###end of training block###

    ####move learner####
    if userChoice=='m':
        print("\n****************************\n******** Move Tutor ********\n****************************\n\nYou can teach your Pokemon new moves!\n")
        while 1: #choose a pokemon
            print("\n******** Party Pokemon ********\n*******************************\n")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
            print("*******************************\n")
            learnChoice=input("Enter the number of a Pokemon\n[#], [m]ove info, or [b]ack: ")
            #go back
            if learnChoice=='b' or learnChoice=='B':
                print("Leaving Move Tutor...")
                t.sleep(0.7) #kills
                break #go back to main screen
            if learnChoice=="m" or learnChoice=="M":
                #print all the moves
                print("\n------------ Pokemon Moves ------------")
                for i in range(len(mov)):
                    print(f"{mov[i]['index']}\t| {mov[i]['name']}\t| {typeStrings[mov[i]['type']]}")
                print("------------------------")
                while 1:
                    mpChoice=input("Which moves do you want to see?\n[#] or [b]ack: ")
                    if mpChoice=="b" or mpChoice=="B":
                        t.sleep(0.7)
                        break
                    try:
                        movez=mpChoice.split() #pokemon movelist index (string)
                        movez=[int(i) for i in movez] #pokemon movelist indices (int)
                    except ValueError:
                        print("\n** Entry must be a [#] or list of [#]s, separated by spaces! **")
                    except IndexError:
                        print("\n** Use the indices to select moves to take a closer look at. **")
                    else:
                        for i in range(len(movez)):
                            print("")
                            moveInfo(movez[i])
                            t.sleep(0.4) #drama
                        pause=input("\nEnter anything to continue back to Pokemon summary...")
                        continue
            else:
                try:
                    learnChoice=int(learnChoice)
                    studentMon=userParty[learnChoice-1]
                    print(f"{studentMon.name} is ready to learn...") #confirmation readout, user choice intiated a pokemon
                except ValueError:
                    print("** Enter a [#] corresponding to a Pokemon !!**\n")
                except IndexError:
                    print("** Enter a [#] corresponding to a Pokemon !!**\n")
                else:
                    #otherwise, print the moves, godspeed
                    print("\n------------ Pokemon Moves ------------")
                    for i in range(len(mov)):
                        print(f"{mov[i]['index']}\t| {mov[i]['name']}\t| {typeStrings[mov[i]['type']]}")
                    print("------------------------")
                    while 1: #input loop
                        chooseMove=input(f"Which moves should {studentMon.name} learn?\n[#] separated by spaces: ")
                        #go back to choose a pokemon
                        if chooseMove=='b':
                            break
                        if chooseMove=='B':
                            break
                        #extract and apply moves
                        try:
                            chooseMoves=chooseMove.split() #separate move indices into own strings
                            moveInts=[int(i) for i in chooseMoves] #(try to) convert strings to ints
                            incomplete=False
                            if max(moveInts)<len(mov): #make sure all indices have an entry in the movedex
                                if min(moveInts)>=0: #ward off negative numbers
                                    for i in moveInts:
                                        if i in studentMon.knownMoves:
                                            print(f"! {studentMon.name} already knows {getMoveInfo(i)['name']} !\n")
                                            incomplete=True
                                        else:
                                            studentMon.knownMoves.append(i)
                                            studentMon.PP.append(getMoveInfo(i)['pp'])
                                            print(f"{studentMon.name} learned {getMoveInfo(i)['name']}!")
                                    if incomplete==False: #if there are no conflicts
                                        break #all moves added, breaks loop and goes back to choose a pokemon
                                    #otherwise, choose moves loop is restated
                                else: #failing brings you back to move selection
                                    print("** That's out of bounds.. **\n")
                            else: #failing brings you back to move selection
                                print("** That's out of bounds.. **\n")
                        except ValueError:
                            print("** Enter [#] corresponding to desired moves **\n")
                        except IndexError:
                            print("** Use move legend to add moves **\n")
                    #end of move selection while block, moves have been picked
            #choose a new pokemon
        #goes back to choose a pokemon
    ###end of move learner block####

    ####make pokemon from pokedex (use preset stats)####
    if userChoice=='d':
        print("\n*****************************\n******** The Pokedex ********\n*****************************\n\n")
        t.sleep(1)
        while 1: #choose new pokemon loop
            print(dex)
            pokeChoice=input("Which pokemon would you like to add to your team?\n[#] or [b]ack: ")
            if pokeChoice=='b':
                print("Leaving Pokedex...")
                t.sleep(0.7) #kills
                break
            if pokeChoice=='B':
                print("Leaving Pokedex...")
                t.sleep(0.7) #kills
                break
            try:
                pokeChoices=pokeChoice.split()
                pokInts=[int(i) for i in pokeChoices]
                if max(pokInts)<len(dex):
                    if min(pokInts)>=0:
                        for i in pokInts:
                            newbie=makeMon(i,userParty[0].level)
                            print(f"{newbie.name} is born!")
                            t.sleep(1)
                            userParty.append(newbie)
                            print(f"{newbie.name} has been added to your party!")
                            t.sleep(1)
                            print("Take good care of them!")
                    else: #failing brings you back to new pokemon loop
                        print("** That's out of bounds... **\n")
                else: #new pokemon loop
                    print("** That's out of bounds... **\n")
            except ValueError:
                print("** Try again **\n")
            except IndexError:
                print("** That's out of bounds... **\n")
    ###end of making preset pokemon
    
    ####Loading pokemon
    if userChoice=='l':
        print("******** Load Pokemon ********\n\nYou can load previously saved pokemon!\n")
        while 1: #savefile input loop
            saveChoice=input("What save file to load?\n[blank] entry to use default or [b]ack\n: ")
            #go back
            if saveChoice=='b' or saveChoice=='b':
                print("Leaving Load Pokemon..")
                t.sleep(0.7)
                break
            if saveChoice=="":
                newMons=loadMon("pypokemon.sav")
                if newMons[0]==0: #if error in loading data, ask for savefile again
                    print("\n!! Something is wrong with this savefile !!")
                    continue
                #add all the pokemon to the party
                for i in newMons:
                    userParty.append(i)
                    print(f"{i.name} has joined your party!")
                    t.sleep(1)
                print("Finished loading Pokemon!\n")
                t.sleep(1)
            else:
                try:
                    newMons=loadMon(saveChoice)
                except IndexError:
                    print("! That filename wasn't found !**\nno reason why this should run")
                else:
                    if newMons[0]==0: #error in loading data
                        continue
                    for i in newMons:
                        userParty.append(i)
                        print(f"{i.name} has joined your party!")
                        t.sleep(1)
                    print("Finished loading Pokemon!\n")
                    t.sleep(1)
                    #loop back to load a save
                #
            #loop back to load a save
        #done loading save
    ###end of load save block###
    
    ####pokemon center#### let's heal em up
    if userChoice=="c":
        print("\n******** Welcome to the Pokemon Center ********\n")
        t.sleep(0.7)
        print("We can heal your Pokemon to full health!")
        t.sleep(1)
        while 1:
            cenChoice=input("[y] to restore your party or [b]ack\n: ")

            if cenChoice=='b':
                print("See you soon!\n")
                t.sleep(0.7)
                break
            
            if cenChoice=='y':
                print("\n")
                for i in userParty:
                    i.restore()
                    print(f"{i.name} is ready for more battles!")
                    t.sleep(0.4)
                print("\nYour party is looking better than ever!!")
                t.sleep(0.7)
                print("\nHave a nice day! and have fun!")
                t.sleep(0.7)
                break #back to main screen
    
    ####resetting user Party to Bulbasaur
    if userChoice=='r':
        print("\n******** Party Reset ********")
        t.sleep(0.7)
        print("\nYou can remove individual Pokemon from your party...")
        t.sleep(0.4)
        print("Or you can reset your team to just the starter (Bulbasaur for now)")
        t.sleep(0.7)
        while 1: #input loop only to catch players leaving individual pokemon removal
            resChoice=input("What would you like to do?\n[C]hoose Pokemon, [R]eset team, or [b]ack: ")
            
            if resChoice==("b" or "B"):
                print("Leaving Party Reset...")
                t.sleep(0.7) #kills
                break
                
            if resChoice==("r" or "R"):
                userParty.clear()
                starter=makeMon(0)
                userParty.append(starter)
                print("Your party has been reset!")
                t.sleep(0.7)
                print("Leaving Party Reset...")
                t.sleep(0.7) #kills
                break
            
            if resChoice==("c" or "C"):
                #user input loop
                while 1:
                    #display current party
                    print("\n******** Party Pokemon ********\n*******************************\n")
                    for i in range(len(userParty)):
                        if userParty[i].dualType:
                            thipe=typeStrings[userParty[i].tipe[0]]
                            thipe+=" // "
                            thipe+=typeStrings[userParty[i].tipe[1]]
                        else:
                            thipe=typeStrings[userParty[i].tipe[0]]
                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
                    print("\n*******************************\n")
                    remChoice=input("Which Pokemon to remove?\n[#] or [b]ack: ")
                    
                    if remChoice==("b" or "B"):
                        print("Going back...")
                        #t.sleep(0.7)
                        break
                    try:
                        choices=np.array([int(i)-1 for i in remChoice.split()])
                        for i in range(len(choices)):
                            if len(userParty)==1: #catch players trying to dump whole party
                                print("!! Cannot remove last Pokemon from Party !!")
                                break
                            if i==0: #keeps us from checking empty arrays i.e. choices[0:0]
                                byeMon=userParty.pop(choices[i])
                                print(f"{byeMon.name} has been released to the wild...")
                            else:
                                removedIndices=np.count_nonzero(choices[0:i]<choices[i]) #how many selected indices that are *lower* than current one have already been removed
                                choices[i]-=removedIndices
                                byeMon=userParty.pop(choices[i])
                                print(f"{byeMon.name} has been released to the wild...")
                        print("Selected Pokemon have been released!")
                        t.sleep(0.7) #kills
                        break
                    except ValueError:
                        print("\n!! Entry must be number or list of numbers separated by spaces !!")
                    except IndexError:
                        print("\n!! Entry must correspond to Party Pokemon !!")
    
    #move deleting
    if userChoice=="e" or userChoice=="E":
        print("\n******** Move Deleter ********")
        t.sleep(0.7)
        print("\nHere you can get rid of unwanted moves.")
        t.sleep(0.7)
        while 1: #user input loop
            print("\n******** Party Pokemon ********\n*******************************\n")
            for i in range(len(userParty)):
                if userParty[i].dualType:
                    thipe=typeStrings[userParty[i].tipe[0]]
                    thipe+=" // "
                    thipe+=typeStrings[userParty[i].tipe[1]]
                else:
                    thipe=typeStrings[userParty[i].tipe[0]]
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {format(userParty[i].currenthpp,'.2f')}% \t{thipe}")
            print("\n*******************************\n")
            leteChoice=input("Select a Pokemon [#] to look at\nor [b]ack: ")
            #go back
            if leteChoice=="b" or leteChoice=="B":
                print("Leaving Move Deleter...")
                t.sleep(0.7)
                break
            try:
                select=userParty[int(leteChoice)-1]
            except ValueError:
                print("\n** Enter [#] of a pokemon above! **")
            except IndexError:
                print("\n** Use the legend to enter [#] of a Pokemon! **")
            else:
                while 1: #user input loop
                    select.summary()
                    mvChoice=input("Which moves should be deleted?\n[#] or [b]ack: ")
                    if mvChoice=="b" or mvChoice=="B":
                        t.sleep(0.7)
                        break
                    try:
                        chooz=np.array([int(i)-1 for i in mvChoice.split()])
                        for i in range(len(chooz)):
                            if len(select.knownMoves)==1: #catch players trying to dump whole moveset
                                print("** Pokemon cannot forget its last move **")
                                break
                            if i==0: #keeps us from checking empty arrays i.e. choices[0:0]
                                byeMove=select.knownMoves.pop(chooz[i])
                                print(f"{select.name} forgets {mov[byeMove]['name']}...")
                            else:
                                removedIndices=np.count_nonzero(chooz[0:i]<chooz[i]) #how many selected indices that are *lower* than current one have already been removed
                                chooz[i]-=removedIndices
                                byeMove=select.knownMoves.pop(chooz[i])
                                print(f"{select.name} forgets {mov[byeMove]['name']}...")
                        print("Selected moves have been forgetten!")
                        t.sleep(0.7) #kills
                        break
                    except ValueError:
                        print("\n** Entry must be [#] or list of [#]s separated by spaces! **")
                    except IndexError:
                        print("\n** Entry must correspond to Pokemon move! **")
            #
    ####what's the next spot?####

    #end of game, loops back to main screen
#runs after intial while loop
