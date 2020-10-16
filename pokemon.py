# -*- coding: utf-8 -*-
#Antoine Washington
#Pokemon
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
#*********to do list: natures, terrains, stat stages, ABILITIES *cough*, moves make contact, genders ugh
#
#

import numpy as np
import astropy.table as tbl
import astropy.io.ascii as asc
import time as t
from moves import getMoveInfo
from moves import umm
from pokedex import dex
from pokedex import types

rng=np.random.default_rng(24)

class mon:
    def __init__(self,level,named,hpbase=70,atbase=70,debase=70,sabase=70,sdbase=70,spbase=70,tipe=np.array([0])): #add natures
        #print("its a pokemon!")
        self.level=level
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
        self.hpb=hpbase
        self.atb=atbase
        self.deb=debase
        self.sab=sabase
        self.sdb=sdbase
        self.spb=spbase
        self.maxhp=HP(self.level,self.hpb,self.hpiv,self.hpev)
        self.currenthp=self.maxhp
        self.currenthpp=100
        self.attack=stats(self.level,self.atb,self.ativ,self.atev,1)
        self.defense=stats(self.level,self.deb,self.deiv,self.deev,1)
        self.spatk=stats(self.level,self.sab,self.saiv,self.saev,1)
        self.spdef=stats(self.level,self.sdb,self.sdiv,self.sdev,1)
        self.speed=stats(self.level,self.spb,self.spiv,self.spev,1)
        self.name=named
        self.tipe=tipe
        if len(tipe)>1:
            self.dualType=True
        else:
            self.dualType=False
        self.fainted=False
        self.knownMoves=[19]
        self.PP=[35]
        #battle stat stages
        self.atstage=6
        self.destage=6
        self.sastage=6
        self.sdstage=6
        self.spstage=6
        #in battle stats ugh
        self.bat=self.attack*statStages[self.atstage]
        self.bde=self.defense*statStages[self.destage]
        self.bsa=self.spatk*statStages[self.sastage]
        self.bsd=self.spdef*statStages[self.sdstage]
        self.bsp=self.speed*statStages[self.spstage]
        #battle statuses
        self.sleep=False
        self.sleepCounter=0
        self.frozen=False
        self.freezeCounter=0
        self.burned=False
        self.paralyzed=False
        self.poisoned=False
        self.badlypoisoned=False
        self.poisonCounter=0
        self.confused=False
        self.confusionCounter=0

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
        for i in mvs:
            line+=f" {i}"
        f.write(line+"\n")
        f.close()

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
        print(f"{self.name} fainted!")
        t.sleep(1)
    
    #back to full health!
    def restore(self):
        self.currenthp=self.maxhp
        self.currenthpp=100.
        self.PP=[getMoveInfo(i)['pp'] for i in self.knownMoves]
        self.fainted=False
        
    ####things to call when a pokemon is thrown into battle
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
        if 12 in self.tipe:
            if weather=='sandstorm':
                #rock type sp.def boost in a sandstorm!
                self.bsd*=1.5
                print(f"{self.name}'s boosted by the sandstorm!")
        #further in the list
        
    ####things to reset upon being withdrawn
    def withdraw(self):
        self.atstage=6
        self.destage=6
        self.sastage=6
        self.sdstage=6
        self.spstage=6
        self.confused=False
        self.confusionCounter=0
        if self.poisonCounter>0:
            self.poisonCounter=1
        #other withdraw things
    
    #pokemon move
    def move(self,opponent,moveIndex):
        print(f"{self.name} used {getMoveInfo(moveIndex)['name']}!")
        #paralysis prevents move execution
        if self.paralyzed:
            if rng.random()>0.75:
                print(f"{self.name} is fully paralyzed!")
                return
        #confusion prevents rest of move execution
        if self.confused:
            print(f"{self.name} is confused!")
            #lower confusion counter for chance to snap out of confusion
            self.confusionCounter-=1
            #if counter is at 0, undo confusion
            if self.confusionCounter==0:
                self.confused=False
                print(f"{self.name} snapped out of confusion!")
            #if still confused, chance to hurt self, end move()
            if self.confused:
                if rng.random()>0.5:
                    self.confusionDamage()
                    return
        moveI=getMoveInfo(moveIndex)
        notas=moveI['notes'].split()
        ###accuracy check###
        if rng.random()>moveI['accu']/100.:
            print(f"{self.name}'s attack missed!")
            return
        else:
            #check if status?#
            #check if physical or special
            if moveI['special?']==0:
                #check for burns on physical attacks
                if self.burned:
                    notas.append("burned")
                ans,comment=damage(self.level,self.bat,self.tipe,opponent.bde,opponent.tipe,moveI['pwr'],moveI['type'],notas)
            if moveI['special?']:
                ans,comment=damage(self.level,self.bsa,self.tipe,opponent.bsd,opponent.tipe,moveI['pwr'],moveI['type'],notas)
            eff=checkTypeEffectiveness(moveI['type'],opponent.tipe)
            opponent.hit(self,ans,eff,notas,comment)
    
    #confusion
    def confusionDamage(self):
        dmg=((((2*self.level)/5 + 2)*40*self.bat/self.bde)/50 + 2)
        self.currenthp-=dmg
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} hurt itself in its confusion!")
        if self.currenthp<=0.:
            self.faint()
    
    #poison
    def poisonDamage(self):
        dmg=self.maxphp/8.
        self.currenthp-=dmg
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took poison damage!")
        if self.currenthp<=0.:
            self.faint()
    
    def burnDamage(self):
        #would be the same as poisondamage tbh
        dmg=self.maxhp/8.
        self.currenthp-=dmg
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took burn damage!")
        if self.currenthp<=0.:
            self.faint()
    
    #badly poisoned
    def badPoison(self):
        dmg=self.poisonCounter/16*self.maxhp
        self.currenthp-=dmg
        self.currenthpp=100*self.currenthp/self.maxhp
        print(f"{self.name} took bad poison damage!")
        t.sleep(1)
        if self.currenthp<=0.0:
            self.faint()
        
    def hit(self,attacker,damagepoints,effectiveness,notes,comments):
        if effectiveness==0.:
            print(f"{self.name} is immune!")
        else:
            print(f"{self.name} was hit!")
            t.sleep(0.7)
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
                print(f"\n{i}")
            t.sleep(0.7)
            #show effectiveness
            if effectiveness>2.0:
                print("It was MEGA-effective!!")
            if effectiveness<=2.0 and effectiveness>1:
                print("It was super-effective!")
            if effectiveness<0.5 and effectiveness>0:
                print("It was barely effective...")
            if effectiveness>=0.5 and effectiveness<1:
                print("It was not very effective.")
            t.sleep(0.7)
            #result of hit
            print(f"{self.name} lost {format(100*damagepoints/self.maxhp,'.2f')}% HP!")
            #check for faint
            if self.currenthp<=0.:
                self.faint()
            else:
                print(f"{self.name} has {format(self.currenthpp,'.2f')}% HP left!")
                #status conditions
                notAfflicted=(self.sleep or self.frozen or self.paralyzed or self.burned or self.poisoned or self.badlypoisoned)
                notAfflicted=not notAfflicted
                #paralyze
                if "para10" in notes:
                    if (rng.random()<=0.1) and notAfflicted:
                        self.paralyzed=True
                        print(f"{self.name} is paralyzed by the hit!")
                        t.sleep(0.4)
                #burn
                if "burn10" in notes:
                    if (rng.random()<=0.1) and notAfflicted:
                        self.burned=True
                        print(f"{self.name} is burned by the hit!")
                        t.sleep(0.4)
                #poison
                if "pois10" in notes:
                    if (rng.random()<=0.1) and notAfflicted:
                        self.poisoned=True
                        print(f"{self.name} is poisoned by the hit!")
                        t.sleep(0.4)
            
            #check for recoil, apply recoil if present
            if "recoilThird" in notes:
                attacker.recoil(recoilDmg,1/3)
    
    #recoil
    def recoil(self,damagedone,recoilAmount):
        print(f"{self.name} takes recoil damage!")
        self.currenthp-=damagedone*recoilAmount
        self.currenthpp=100*self.currenthp/self.maxhp
        if self.currenthp<=0.:
            self.faint()

    #recalculate stats
    def reStat(self):
        self.maxhp=HP(self.level,self.hpb,self.hpiv,self.hpev)
        self.attack=stats(self.level,self.atb,self.ativ,self.atev,1)
        self.defense=stats(self.level,self.deb,self.deiv,self.deev,1)
        self.spatk=stats(self.level,self.sab,self.saiv,self.saev,1)
        self.spdef=stats(self.level,self.sdb,self.sdiv,self.sdev,1)
        self.speed=stats(self.level,self.spb,self.spiv,self.spev,1)
        self.currenthp=self.maxhp
        self.currenthpp=100

    def checkup(self):
        print(f"Name: {self.name} // Lv. {self.level}")
        if len(self.tipe)==1:
            print(f"{typeStrings[self.tipe[0]]}")
        if len(self.tipe)>1:
            print(f"{typeStrings[self.tipe[0]]} / {typeStrings[self.tipe[1]]}")
        print(f"Current HP: {self.currenthp}, {self.currenthp/self.maxhp*100}%")
        
    def summary(self):
        print(f"\n###### {self.name} Summary ######")
        if self.dualType:
            print(f"{typeStrings[self.tipe[0]]} // {typeStrings[self.tipe[1]]}")
        else:
            print(f"{typeStrings[self.tipe[0]]}")
        print(f"HP  : \t{format(self.currenthp,'.2f')}/{self.maxhp} \t{format(self.currenthpp,'.2f')}%")
        print(f"Atk : \t{self.attack}")
        print(f"Def : \t{self.defense}")
        print(f"Sp.A: \t{self.spatk}")
        print(f"Sp.D: \t{self.spdef}")
        print(f"Spe : \t{self.speed}")
        print(f"############ {self.name}'s Moves #############")
        for i in range(len(self.knownMoves)):
            print(f"\n{getMoveInfo(self.knownMoves[i])['name']} \t{self.PP[i]}/{getMoveInfo(self.knownMoves[i])['pp']} PP")
        print("##############################################")

    def showMoves(self):
        print("\n---- {self.name}'s Moves ----")
        for i in range(len(self.knownMoves)):
            print(f"{self.knownMoves[i]['name']} ")
        
        
def damage(level,attack,plaintiffTipe,defense,defendantTipe,power,moveTipe,note):
    ####damage boost strings####
    damages=[]
    ####weather damage boost####
    weatherBonus=1.0
    if weather=='sunny':
        if moveTipe==1:
            weatherBonus=4/3
            damages.append("Sun boost!")
        if moveTipe==2:
            weatherBonus=2/3
            damages.append("Weakened by the sunlight...")
    if weather=='rain':
        if moveTipe==1:
            weatherBonus=2/3
            damages.append("Weakened by the rain...")
        if moveTipe==2:
            weatherBonus=4/3
            damages.append("Rain boost!")
    ####critical hit chance####
    critical=1.
    if rng.integers(1,25)==24:
        critical=1.5
        damages.append("It's a critical hit!")
    ####random fluctuation 85%-100%
    rando=rng.integers(85,101)*0.01
    ####STAB####
    STAB=1.
    if moveTipe in plaintiffTipe:
        STAB=1.5
    ####type effectiveness####
    tyype=checkTypeEffectiveness(moveTipe,defendantTipe)
    ####Burn###
    burn=1.
    if "burned" in note:
        burn=0.5
        damages.append("The burn reduces damage...")
    damageModifier=weatherBonus*critical*rando*STAB*tyype*burn
    ####damage calculation####
    ans=((((2*level)/5 + 2)*power*attack/defense)/50 + 2)*damageModifier
    return ans,damages

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
def makeMon(pokedexNumber,level=1):
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
        return mon(level,nayme,hpbase=Hp,atbase=At,debase=De,sabase=Sa,sdbase=Sd,spbase=Sp,tipe=np.array([tipe1]))
    else: #dual-typed
        return mon(level,nayme,hpbase=Hp,atbase=At,debase=De,sabase=Sa,sdbase=Sd,spbase=Sp,tipe=np.array([tipe1,tipe2]))

#load pokemon
def loadMon(savefile):
    try:
        dat=np.loadtxt(savefile,delimiter=",",dtype='U140')
        loadPokes=[]
        multi=type(dat[0])==np.ndarray
        if multi:
            for i in dat:
                loadMe=i
                name=loadMe[0]
                lvl=int(loadMe[1])
                bases=loadMe[2].split() #should give list of 6 base stats, technically strings
                baseI=[int(ii) for ii in bases]
                ivys=loadMe[3].split()
                ivz=[int(ii) for ii in ivys]
                evys=loadMe[4].split()
                evz=[int(iii) for iii in evys]
                typ=np.array([int(iiii) for iiii in loadMe[5].split()])
                mves=[int(iiiii) for iiiii in loadMe[6].split()]
                newP=mon(lvl,name,hpbase=baseI[0],atbase=baseI[1],debase=baseI[2],sabase=baseI[3],sdbase=baseI[4],spbase=baseI[5],tipe=typ)
                newP.knownMoves=mves
                newP.hpiv,newP.ativ,newP.deiv,newP.saiv,newP.sdiv,newP.spiv=ivz
                newP.hpev,newP.atev,newP.deev,newP.saev,newP.sdev,newP.spev=evz
                newP.reStat()
                loadPokes.append(newP)
                print(f"Loaded {newP.name}!")
        else:
            name=dat[0]
            lvl=int(dat[1])
            bases=dat[2].split()
            baseI=[int(ii) for ii in bases]
            ivys=dat[3].split()
            ivz=[int(ii) for ii in ivys]
            evys=dat[4].split()
            evz=[int(iii) for iii in evys]
            typ=np.array([int(iiii) for iiii in dat[5].split()])
            mves=[int(iiiii) for iiiii in dat[6].split()]
            newP=mon(lvl,name,hpbase=baseI[0],atbase=baseI[1],debase=baseI[2],sabase=baseI[3],sdbase=baseI[4],spbase=baseI[5],tipe=typ)
            newP.knownMoves=mves
            newP.hpiv,newP.ativ,newP.deiv,newP.saiv,newP.sdiv,newP.spiv=ivz
            newP.hpev,newP.atev,newP.deev,newP.saev,newP.sdev,newP.spev=evz
            newP.reStat()
            loadPokes.append(newP)
            print(f"Loaded {newP.name}!")
        return loadPokes
    except FileNotFoundError:
        print("! The file name wasn't found... !\n")
        return [0]
    except OSError:
        print("! The file name wasn't found... !\n")
        return [0]
    except:
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

#moves have pwr, phys/spec, type, accu, descipt
def moveInfo(moveCode):
    movepower=0
    moveSpecial=0
    moveTiipe=0
    return movepower,moveSpecial,moveTiipe

def indexToType(x):
    ["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]

#class party():
    #def __init__(self):
        
#codex encodes all type matchups, first index is attacking the second index
codex=np.ones((18,18))
#order: normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,ground 8,flying 9,psychic 10,bug 11,
#rock 12,ghost 13,dragon 14,dark 15,steel 16,fairy 17, typeless 18
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
typeStrings=["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]
statStages=[2/8,2/7,2/6,2/5,2/4,2/3,2/2,3/2,4/2,5/2,6/2,7/2,8/2] #0 to 6 to 12

#weather='clear'
#weather='rain'
weather='sunny'
#weather='hail'
#weather='sandstorm'

starter=mon(1,"Bulbasaur",hpbase=45,atbase=49,debase=49,sabase=65,sdbase=65,spbase=45,tipe=np.array([3,7]))
rival=makeMon(3)
rival2=makeMon(9,150)
rival2.name="Misty's Starmie"
userParty=[starter]
trainerParty=[rival,rival2]
print(dex)
t.sleep(0.5)
print(umm)
t.sleep(0.5)
#asc.write(umm,'movedex.dat',overwrite=True)
print("** Welcome to the Wonderful World of Pokemon Simulation! **")
t.sleep(1)
while 1:
    userChoice=input("\n[P]okemon\n[B]attle!\n[N]ursery\n[D]ex Selection\n[T]raining\n[M]ove Tutor\nPokemon [C]enter\nSet [O]pponent\n[L]oad\n:")

    ####Reseting the Opponent in Battle function####
    if userChoice=='o':
        print("\n________ Opponent Reset ________\n")
        t.sleep(1)
        aceChoice=input("Would you like to set your current team as the battle opponent?\n[y] or [b] to go back:")
        if aceChoice=='y':
            trainerParty=userParty.copy()
            print("The Battle Opponent has a new Party! Good Luck!")
            t.sleep(0.7) #kills
        if aceChoice=='Y':
            trainerParty=userParty.copy()
            print("The Battle Opponent has a new Party! Good Luck!")
            t.sleep(0.7) #kills
        else:
            print("Leaving Opponent Reset...")
            t.sleep(0.7) #kills
        #end of opponent set, back to main screen

    ####Battles####
    if userChoice=='b':
        ####Battle starts####
        print("A battle has started!")
        t.sleep(1)
        userMon=userParty[0]
        userInd=0
        print(f"{userMon.name}! I choose you!")
        t.sleep(1)
        trainerMon=trainerParty[0]
        trainerInd=0
        print(f"{trainerMon.name}! Go!")
        t.sleep(1)
        turn=1
        ####turn begins####
        while 1: #only breaks when BattleOver is True
            ####fight/run/pokemon/bag####
            while 1: #turn loop, advances to pokemon move usage if user uses a move or shifts, otherwise the loop accomplishes nothing
                print(f"\n________ Turn {turn} ________\n")
                battleOver=False
                userMon.inBattle()
                trainerMon.inBattle()
                fightShift=False
                shifted=False
                #----UI----#
                print(f"Opponent:\n{trainerMon.name} // Level {trainerMon.level}")
                print(f"HP: {format(trainerMon.currenthpp,'.2f')}%")
                print("\n............Your team:")
                print(f"............{userMon.name} // Level {userMon.level}")
                print(f"............HP: {format(userMon.currenthp,'.2f')}/{format(userMon.maxhp,'.2f')}")
                userMove=input(f"What should {userMon.name} do?\n[F]ight\n[P]okemon\n[R]un\n")
                
                ####run away to end battle####
                if userMove=='r':
                    print(f"You and {userMon.name} ran away!")
                    battleOver=True
                    break

                #go party pokemon
                if userMove=='p':
                    while 1:
                        print("\n****************\nParty Pokemon:")
                        for i in range(len(userParty)):
                            print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                        partyChoice=input("Select a Pokemon...\n[#] or [b] to go back: ")
                        if partyChoice=='b':
                            break #goes back to user turn loop from pokemon selection
                        try:
                            select=userParty[int(partyChoice)-1]
                            nuserInd=int(partyChoice)-1
                            select.summary()
                        except ValueError:
                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                        except IndexError:
                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                        else:
                            while 1:
                                pChoice=input(f"Shift {select.name} into battle?\n[y] or [b] to go back: ")
                                #go back
                                if pChoice=='b':
                                    break
                                #switch pokemon
                                if pChoice=='y':
                                    #keep fainted pokemon off the field
                                    if select.fainted:
                                        print("**Cannot switch in fainted Pokemon!**")
                                        break
                                    #put current pokemon back?
                                    userMon.withdraw()
                                    userParty[userInd]=userMon
                                    print(f"{userMon.name} come back!")
                                    t.sleep(1)
                                    #set new selection as user pokemon
                                    userMon=select
                                    userInd=nuserInd
                                    print(f"{userMon.name}, it's your turn!")
                                    t.sleep(1)
                                    userMon.inBattle()
                                    shifted=True
                                    fightShift=True
                                    break
                                #anything other than y repeats the loop
                            if shifted:
                                break
                        #end of pokemon selection loop
                    #end of party pokemon block

                #fight
                if userMove=='f':                    
                    #fighting options
                    while 1: #move input loop
                        for i in range(len(userMon.knownMoves)):
                            print(f"[{i+1}] \t{getMoveInfo(userMon.knownMoves[i])['name']} \t{userMon.PP[i]} PP")
                        userFight=input(f"What move should {userMon.name} use?\n[#] or [b]:")
                        #go back
                        if userFight=='b':
                            break
                        #try to use user input to call a move
                        try:
                            fightChoice=int(userFight)-1 #make sure given input refers to a move
                            if userMon.PP[fightChoice]==0:
                                print(f"{userMon.name} does not have enough energy to use this move!")
                                continue
                            moveDex=userMon.knownMoves[fightChoice]
                            fightShift=True
                            break
                        except:
                            print("\n**Enter one of the numbers above.**")
                
                ####after either swithing or attacking
                if fightShift:
                    trainerDice=rng.random()
                    trainerShift=False
                    #10% chance for opponent to randomly switch pokemon
                    #check how many nonfainted pokemon trainer has
                    nfp,nfpList=checkBlackout(trainerParty)
                    #if trainer has more than 1 non fainted pokemon
                    if nfp>1:
                        if trainerDice>0.9:
                            trainerMon.withdraw()
                            #put pokemon away
                            trainerParty[trainerInd]=trainerMon
                            print(f"{trainerMon.name} is withdrawn!")
                            t.sleep(1)
                            #take new pokemon out
                            trainerInd=rng.choice(nfpList)
                            trainerMon=trainerParty[trainerInd]
                            trainerMon.inBattle()
                            print(f"{trainerMon.name}! is sent out!")
                            t.sleep(1)
                            trainerShift=True
                    #set boolean to true if user has higher effective speed stat
                    userFast=userMon.bsp>=trainerMon.bsp
                    uFaint=False
                    tFaint=False
                    ##USER FASTER##
                    if userFast:
                        #USER ATTACK
                        #make sure user/trainer didn't switch in this turn
                        if shifted==False:
                            userMon.move(trainerMon,moveDex)
                            userMon.PP[fightChoice]-=1
                            #check for faint, attacked pokemon first, and then attacker
                            if trainerMon.fainted:
                                #check for OPPO BLACKOUT
                                blk,blkList=checkBlackout(trainerParty)
                                if blk==0:
                                    battleOver=True
                                    print("The opponent is out of usable pokemon!\nYou win!")
                                    t.sleep(1)
                                    break
                                else:
                                    #reassign opponent's active pokemon
                                    trainerInd=rng.choice(blkList)
                                    trainerMon=trainerParty[trainerInd]
                                    print(f"{trainerMon.name} was switched in!")
                                    trainerShift=True
                                    tFaint=True
                            if userMon.fainted:
                                #check for USER BLACKOUT
                                if checkBlackout(userParty)[0]==0:
                                    battleOver=True
                                    print("You're out of usable Pokemon!")
                                    t.sleep(1)
                                    print("You blacked out!")
                                    t.sleep(1)
                                    break
                                else:
                                    bShifted=False #forcing the user to shift to a non-fainted pokemon
                                    print("\n****************\nParty Pokemon:")
                                    for i in range(len(userParty)):
                                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                                    while 1:
                                        newPoke=input("Select a Pokemon to battle...\n[#]")
                                        try:
                                            nuserInd=int(newPoke)-1
                                            select=userParty[nuserInd]
                                            select.summary()
                                        except ValueError:
                                            print("\n! Enter a [#] corresponding to a Pokemon!\nor [b]ack !")
                                        except IndexError:
                                            print("\n! Enter a [#] corresponding to a Pokemon!\nor [b]ack !")
                                        else:
                                            while 1:
                                                sChoice=input(f"Shift {select.name} into battle?\n[y] or [b] to go back")
                                                #go back
                                                if sChoice=='b':
                                                    break
                                                #switch pokemon
                                                if sChoice=='y':
                                                    #keep fainted pokemon off the field
                                                    if select.fainted:
                                                        print("**Cannot switch in fainted Pokemon!**")
                                                        break
                                                    #put current pokemon back?
                                                    userMon.withdraw()
                                                    userParty[userInd]=userMon
                                                    print(f"{userMon.name} come back!")
                                                    t.sleep(1)
                                                    #set new selection as user pokemon
                                                    userMon=select
                                                    userInd=nuserInd
                                                    print(f"{userMon.name}, it's your turn!")
                                                    t.sleep(1)
                                                    userMon.inBattle()
                                                    bShifted=True
                                                    uFaint=True
                                                    trainerShift=True #just to kill the opponent trying to use a move, user is already fainted
                                                    break
                                                #anything other than y repeats the loop
                                            if bShifted:
                                                break
                        ##OPPO ATTACK
                        if trainerShift==False:
                            trainMove=rng.choice(range(len(trainerMon.knownMoves)))
                            trainerMon.move(userMon,trainerMon.knownMoves[trainMove])
                            trainerMon.PP[trainMove]-=1
                            if userMon.fainted:
                                #check for USER BLACKOUT
                                if checkBlackout(userParty)[0]==0:
                                    battleOver=True
                                    print("You're out of usable Pokemon!")
                                    t.sleep(1)
                                    print("You blacked out!")
                                    t.sleep(1)
                                    break
                                else:
                                    bShifted=False #forcing the user to shift to a non-fainted pokemon
                                    print("\n****************\nParty Pokemon:")
                                    for i in range(len(userParty)):
                                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                                    while 1:
                                        newPoke=input("Select a Pokemon to battle...\n[#]")
                                        try:
                                            #assign new active pokemon party-index
                                            nuserInd=int(newPoke)-1
                                            #stage selected pokemon
                                            select=userParty[nuserInd]
                                            select.summary()
                                        except ValueError:
                                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                        except IndexError:
                                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                        else:
                                            while 1:
                                                sChoice=input(f"Shift {select.name} into battle?\n[y] or [b] to go back")
                                                #go back
                                                if sChoice=='b':
                                                    break
                                                #switch pokemon
                                                if sChoice=='y':
                                                    #keep fainted pokemon off the field
                                                    if select.fainted:
                                                        print("**Cannot switch in fainted Pokemon!**")
                                                        break
                                                    #put current pokemon back?
                                                    userMon.withdraw()
                                                    userParty[userInd]=userMon
                                                    print(f"{userMon.name} come back!")
                                                    t.sleep(1)
                                                    #set new selection as user pokemon
                                                    userMon=select
                                                    userInd=nuserInd
                                                    print(f"{userMon.name}, it's your turn!")
                                                    t.sleep(1)
                                                    userMon.inBattle()
                                                    bShifted=True
                                                    break
                                                #anything other than y repeats the loop
                                            if bShifted:
                                                break
                            if trainerMon.fainted:
                                #check for TRAINER BLACKOUT
                                blk,blkList=checkBlackout(trainerParty)
                                if blk==0:
                                    battleOver=True
                                    print("The opponent is out of usable pokemon!\nYou win!")
                                    t.sleep(0.7)
                                    break
                                else:
                                    trainerInd=rng.choice(blkList)
                                    trainerMon=trainerParty[trainerInd]
                                    print(f"{trainerMon.name} was switched in!")
                                    t.sleep(0.7)
                    ##USER SLOWER##
                    else:
                        ##OPPO ATTACK##
                        if trainerShift==False:
                            trainMove=rng.choice(range(len(trainerMon.knownMoves)))
                            trainerMon.move(userMon,trainerMon.knownMoves[trainMove])
                            trainerMon.PP[trainMove]-=1
                            if userMon.fainted:
                                #check for USER BLACKOUT
                                if checkBlackout(userParty)[0]==0:
                                    battleOver=True
                                    print("You're out of usable Pokemon!")
                                    t.sleep(1)
                                    print("You blacked out!")
                                    t.sleep(1)
                                    break
                                else:
                                    bShifted=False #forcing the user to shift to a non-fainted pokemon
                                    print("\n****************\nParty Pokemon:")
                                    for i in range(len(userParty)):
                                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                                    while 1:
                                        newPoke=input("Select a Pokemon to battle...\n[#]")
                                        try:
                                            nuserInd=int(newPoke)-1
                                            select=userParty[nuserInd]
                                            select.summary()
                                        except ValueError:
                                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                        except IndexError:
                                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                        else:
                                            while 1:
                                                sChoice=input(f"Shift {select.name} into battle?\n[y] or [b] to go back")
                                                #go back
                                                if sChoice=='b':
                                                    break
                                                #switch pokemon
                                                if sChoice=='y':
                                                    #keep fainted pokemon off the field
                                                    if select.fainted:
                                                        print("**Cannot switch in fainted Pokemon!**")
                                                        break
                                                    #put current pokemon back?
                                                    userMon.withdraw()
                                                    userParty[userInd]=userMon
                                                    print(f"{userMon.name} come back!")
                                                    t.sleep(1)
                                                    #set new selection as user pokemon
                                                    userMon=select
                                                    userInd=nuserInd
                                                    print(f"{userMon.name}, it's your turn!")
                                                    t.sleep(1)
                                                    userMon.inBattle()
                                                    bShifted=True
                                                    shifted=True #just to kill the user's chance to attack, as it was just switched in
                                                    fightShift=True
                                                    break
                                                #anything other than y repeats the loop
                                            if bShifted:
                                                break
                            if trainerMon.fainted:
                                #check for TRAINER BLACKOUT
                                blk,blkList=checkBlackout(trainerParty)
                                if blk==0:
                                    battleOver=True
                                    print("The opponent is out of usable pokemon!\nYou win!")
                                    break
                                else:
                                    trainerInd=rng.choice(blkList)
                                    trainerMon=trainerParty[trainerInd]
                                    print(f"{trainerMon.name} was switched in!")
                        ##USER ATTACK##
                        if shifted==False:
                            userMon.move(trainerMon,moveDex)
                            userMon.PP[fightChoice]-=1
                            if trainerMon.fainted:
                                #check for TRAINER BLACKOUT
                                blk,blkList=checkBlackout(trainerParty)
                                if blk==0:
                                    battleOver=True
                                    print("The opponent is out of usable pokemon!\nYou win!")
                                    break
                                else:
                                    trainerInd=rng.choice(blkList)
                                    trainerMon=trainerParty[trainerInd]
                                    print(f"{trainerMon.name} was switched in!")
                            if userMon.fainted:
                                #check for USER BLACKOUT
                                if checkBlackout(userParty)[0]==0:
                                    battleOver=True
                                    print("You're out of usable Pokemon!")
                                    t.sleep(1)
                                    print("You blacked out!")
                                    t.sleep(1)
                                    break
                                else:
                                    bShifted=False #forcing the user to shift to a non-fainted pokemon
                                    print("\n****************\nParty Pokemon:")
                                    for i in range(len(userParty)):
                                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                                    while 1:
                                        newPoke=input("Select a Pokemon to battle...\n[#]")
                                        try:
                                            nuserInd=int(newPoke)-1
                                            select=userParty[nuserInd]
                                            select.summary()
                                        except ValueError:
                                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                        except IndexError:
                                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                        else:
                                            while 1:
                                                sChoice=input(f"Shift {select.name} into battle?\n[y] or [b] to go back")
                                                #go back
                                                if sChoice=='b':
                                                    break
                                                #switch pokemon
                                                if sChoice=='y':
                                                    #keep fainted pokemon off the field
                                                    if select.fainted:
                                                        print("**Cannot switch in fainted Pokemon!**")
                                                        break
                                                    #put current pokemon back?
                                                    userMon.withdraw()
                                                    userParty[userInd]=userMon
                                                    print(f"{userMon.name} come back!")
                                                    t.sleep(1)
                                                    #set new selection as user pokemon
                                                    userMon=select
                                                    userInd=nuserInd
                                                    print(f"{userMon.name}, it's your turn!")
                                                    t.sleep(1)
                                                    userMon.inBattle()
                                                    bShifted=True
                                                    fightShift=True
                                                    break
                                                #anything other than y repeats the loop
                                            if bShifted:
                                                break
                    #end of turn, pokemon have attacked
                    #poison and burn damage
                    if userMon.poisoned:
                        userMon.poisonDamage()
                    if userMon.burned:
                        userMon.burnDamage()
                    if userMon.badlypoisoned:
                        userMon.badPoison()
                        userMon.poisonCounter+=1
                    if trainerMon.poisoned:
                        trainerMon.poisonDamage()
                    if trainerMon.burned:
                        trainerMon.burnDamage()
                    if trainerMon.badlypoisoned:
                        trainerMon.badPoison()
                        trainerMon.poisonCounter+=1
                    #check for faints after end of turn damage
                    if trainerMon.fainted:
                        #check for TRAINER BLACKOUT
                        blk,blkList=checkBlackout(trainerParty)
                        if blk==0:
                            battleOver=True
                            print("The opponent is out of usable pokemon!\nYou win!")
                            break
                        else:
                            trainerInd=rng.choice(blkList)
                            trainerMon=trainerParty[trainerInd]
                            print(f"{trainerMon.name} was switched in!")
                    if userMon.fainted:
                        #check for USER BLACKOUT
                        if checkBlackout(userParty)[0]==0:
                            battleOver=True
                            print("You're out of usable Pokemon!")
                            t.sleep(1)
                            print("You blacked out!")
                            t.sleep(1)
                            break
                        else:
                            bShifted=False #forcing the user to shift to a non-fainted pokemon
                            print("\n****************\nParty Pokemon:")
                            for i in range(len(userParty)):
                                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                                while 1:
                                    newPoke=input("Select a Pokemon to battle...\n[#]")
                                    try:
                                        nuserInd=int(newPoke)-1
                                        select=userParty[nuserInd]
                                        select.summary()
                                    except ValueError:
                                        print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                    except IndexError:
                                        print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                                    else:
                                        while 1:
                                            sChoice=input(f"Shift {select.name} into battle?\n[y] or [b] to go back")
                                            #go back
                                            if sChoice=='b':
                                                break
                                            #switch pokemon
                                            if sChoice=='y':
                                                #keep fainted pokemon off the field
                                                if select.fainted:
                                                    print("**Cannot switch in fainted Pokemon!**")
                                                    break
                                                #put current pokemon back?
                                                userMon.withdraw() #should be redundant? since faint() already calls withdraw() idk we'll leave it for now
                                                userParty[userInd]=userMon
                                                print(f"{userMon.name} come back!")
                                                t.sleep(1)
                                                #set new selection as user pokemon
                                                userMon=select
                                                userInd=nuserInd
                                                print(f"{userMon.name}, it's your turn!")
                                                t.sleep(1)
                                                userMon.inBattle()
                                                bShifted=True
                                                break
                                            #anything other than y repeats the loop
                                        if bShifted:
                                            break
                    #checked for faints
                    turn+=1
                    #loop to next turn
            if battleOver: #if user ran
                break #breaks battle loop, back to main screen
            #loop back to "turn begins"
            #if a pokemon has fainted, loop ends
        print("The battle ended!")
        t.sleep(1)
    ###end of battle block###
        
    ####check party pokemon?####
    if userChoice=='p':
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
            if partyChoice=='b':
                print("Leaving Party screen...")
                t.sleep(0.7) #kills
                break
            if partyChoice=='B':
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
                    sumChoice=input(f"What to do with {selMon.name}?\n[s]ave or [b]ack: ")
                    #go back to pokemon selection
                    if sumChoice=='b':
                        t.sleep(0.7)
                        break
                    if sumChoice=='B':
                        t.sleep(0.7)
                        break
                    if sumChoice=='s':
                        while 1:
                            savename=input("Enter name of savefile...\n[blanck] to use default savefile name\nor [b]ack\n: ")
                            if savename=='b':
                                t.sleep(0.7)
                                break
                            if savename=='B':
                                t.sleep(0.7)
                                break
                            if savename=='':
                                selMon.save()
                                print(f"{selMon.name} was saved to the file!\n")
                                t.sleep(0.7) #kills
                                break
                            else:
                                selMon.save(savename)
                                print(f"{selMon.name} was saved to the file!\n")
                                t.sleep(0.7) #kills
                                break
                            #
                        #
            #end of while block
        print("Going back to main screen...")
        t.sleep(1)
        #end of party pokemon
    ###end of party display block###

    ####pokemon nursery####
    if userChoice=='n':
        print("\n____Welcome to the Pokemon Nursery!____")
        t.sleep(1)
        print("Here, you can create Pokemon from scratch!")
        t.sleep(1)
        ####nursery loop####
        while 1:
            nurseChoice=input("What do you want to do?\nNew [P]okemon!!\n[B]ack\n:")
            
            ####new pokemon####
            if nurseChoice=='p':
                newName=input("Would you like to give your Pokemon a name?: ")
                print(f"Let's get {newName} some STATS")
                while 1:
                    HPstatS=input("HP stat? 1-255: ")
                    ATstatS=input("Attack stat? 1-255: ")
                    DEstatS=input("Defense stat? 1-255: ")
                    SAstatS=input("Sp. Atk stat? 1-255: ")
                    SDstatS=input("Sp. Def stat? 1-255: ")
                    SPstatS=input("Speed stat? 1-255: ")
                    try:
                        HPstat=int(HPstatS)
                        ATstat=int(ATstatS)
                        DEstat=int(DEstatS)
                        SAstat=int(SAstatS)
                        SDstat=int(SDstatS)
                        SPstat=int(SPstatS)
                        if np.min(np.array([HPstat,ATstat,DEstat,SAstat,SDstat,SPstat]))>0:
                            break #stats acccepted, exits stat input loop
                        else:
                            print("\n**Base stats must be at least 1**")
                    except:
                        print("\n**Stats must be numbers**")
                ##type choice##
                print("****************\nPokemon Types:\n0 Normal\n1 Fire\n2 Water\n3 Grass\n4 Electric\n5 Ice\n6 Fighting\n7 Poison\n8 Ground\n9 Flying\n10 Psychic\n11 Bug\n12 Rock\n13 Ghost\n14 Dragon\n15 Dark\n16 Steel\n17 Fairy\n****************")
                while 1: #type input loop
                    newTipe=input(f"Use the legend above to give {newName} a type or two: ")
                    try:
                        newTipes=newTipe.split()
                        newTipe1=int(newTipes[0])
                        newTipeInt=np.array([newTipe1])
                        if len(newTipes)>1: #if second type was inputted
                            newTipe2=int(newTipes[1])
                            newTipeInt=np.append(newTipeInt,newTipe2)
                        if np.max(newTipeInt)<=17: #no types above 17
                            if np.min(newTipeInt)>=0: #no types below 0
                                break #input valid, exit type input loop
                            else:
                                print("\n**Highest number: 17, lowest number: 0**")
                        else:
                            print("\n**Highest number: 17, lowest number: 0**")
                    except ValueError:
                        print("\n**Use the legend above and enter a number (or 2 separated with a space)**")
                
                ##level input##
                while 1: #level input loop
                    lvlS=input(f"What level should {newName} be? 1-100: ")
                    try:
                        lvl=int(lvlS)
                        if lvl>=1:
                            break
                        else:
                            print("\n**Level must be at least 1!**")
                    except:
                        print("\n**Enter a number!**")
                    #end of while block
                                    
                ##make the pokemon!##
                if len(newTipes)==1:
                    newMon=mon(lvl,newName,hpbase=HPstat,atbase=ATstat,debase=DEstat,sabase=SAstat,sdbase=SDstat,spbase=SPstat,tipe=np.array([newTipe1]))
                if len(newTipes)>1:
                    newMon=mon(lvl,newName,hpbase=HPstat,atbase=ATstat,debase=DEstat,sabase=SAstat,sdbase=SDstat,spbase=SPstat,tipe=np.array([newTipe1,newTipe2]))
                print(f"\n{newName} is born!")
                t.sleep(1)
                userParty.append(newMon)
                print("Take good care of them!")
            
            if nurseChoice=='b':
                break #exits nursery loop
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
            trainChoice=input("\nWhich Pokemon will we train?:\n[#] or [B]ack: ")
            
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
            learnChoice=input("Enter the number of a Pokemon\n[#] or [b]ack: ")
            #go back
            if learnChoice=='b':
                print("Leaving Move Tutor...")
                t.sleep(0.7) #kills
                break #go back to main screen
            if learnChoice=='B':
                print("Leaving Move Tutor...")
                t.sleep(0.7) #kills
                break #go back to main screen
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
                print(umm)
                #np.savetxt("movecodex.txt",umm)
                asc.write(umm,'movecodex.dat',overwrite=True)
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
                        if max(moveInts)<len(umm): #make sure all indices have an entry in the movedex
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
            pass #choose a new pokemon
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
                            newbie=makeMon(i)
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
            if saveChoice=='b':
                print("Leaving Load Pokemon..")
                t.sleep(0.7)
                break
            if saveChoice=='B':
                print("Leaving Load Pokemon..")
                t.sleep(0.7)
                break
            if saveChoice=="":
                newMons=loadMon("pypokemon.sav")
                if newMons[0]==0: #if error in loading data, ask for savefile again
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
                except:
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
    ####what's the next spot?####

    #end of game, loops back to main screen
#runs after intial while loop
