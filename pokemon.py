# -*- coding: utf-8 -*-
#Antoine Washington
#Pokemon
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17

import numpy as np
import math
np.random.seed(24)

class mon:
    def __init__(self,level,named,hpbase=70,atbase=70,debase=70,sabase=70,sdbase=70,spbase=70,tipe=np.array([0])):
        print("its a pokemon!")
        self.level=level
        self.hpiv=np.random.randint(0,32)
        self.ativ=np.random.randint(0,32)
        self.deiv=np.random.randint(0,32)
        self.saiv=np.random.randint(0,32)
        self.sdiv=np.random.randint(0,32)
        self.spiv=np.random.randint(0,32)
        self.maxhp=HP(self.level,hpbase,self.hpiv,0)
        self.currenthp=self.maxhp
        self.attack=stats(self.level,atbase,self.ativ,0,1)
        self.defense=stats(self.level,debase,self.deiv,0,1)
        self.spatk=stats(self.level,sabase,self.saiv,0,1)
        self.spdef=stats(self.level,sdbase,self.sdiv,0,1)
        self.speed=stats(self.level,spbase,self.spiv,0,1)
        self.name=named
        self.tipe=tipe
        
    def move(self,opponent,power,special,moveTipe=0):
        print(f"{self.name} used a move!")
        if special==0:
            ans=damage(self.level,self.attack,self.tipe,opponent.defense,opponent.tipe,power,moveTipe)
        if special==1:
            ans=damage(self.level,self.spatk,self.tipe,opponent.spdef,opponent.tipe,power,moveTipe)
        eff=checkTypeEffectiveness(moveTipe,opponent.tipe)
        opponent.hit(ans,eff)
        
    def hit(self,damagepoints,effectiveness):
        if effectiveness==0:
            print(f"{self.name} is immune!")
        else:
            print(f"{self.name} was hit!")
            self.currenthp-=damagepoints
            if effectiveness>2.0:
                print("It was MEGA-effective!!")
            if effectiveness<=2.0 and effectiveness>1:
                print("It was super-effective!")
            if effectiveness<0.5 and effectiveness>0:
                print("It was barely effective...")
            if effectiveness>=0.5 and effectiveness<1:
                print("It was not very effective.")
            print(f"{self.name} lost {damagepoints} HP!")
            print(f"{self.name} has {self.currenthp} HP left")
        
    def checkup(self):
        print(f"Name: {self.name}")
        print(f"Current HP: {self.currenthp}, {self.currenthp/self.maxhp*100}%")
        
    def appraise(self):
        print("\n######Appraisal######")
        print(f"Here are {self.name}'s stats:\n")
        print(f"HP : \t{format(self.currenthp,'.2f')}/{self.maxhp}")
        print(f"Atk: \t{self.attack}")
        print(f"Def: \t{self.defense}")
        print(f"Sp.A: \t{self.spatk}")
        print(f"Sp.D: \t{self.spdef}")
        print(f"Spe: \t{self.speed}")
        print("#####################")
        
        
def damage(level,attack,plaintiffTipe,defense,defendantTipe,power,moveTipe):
    ####weather damage boost####
    weatherBonus=1.0
    if weather=='sunny':
        if moveTipe==1:
            weatherBonus=4/3
            print("Sun boost!")
        if moveTipe==2:
            weatherBonus=2/3
            print("Weakened by the sunlight...")
    if weather=='rain':
        if moveTipe==1:
            weatherBonus=2/3
            print("Weakened by the rain...")
        if moveTipe==2:
            weatherBonus=4/3
            print("Rain boost!")
    ####critical hit chance####
    critical=1.0
    if np.random.randint(1,25)==24:
        critical=1.5
        print("It's a critical hit!")
    ####random fluctuation 85%-100%
    rando=np.random.randint(85,101)*0.01
    ####STAB####
    STAB=1.0
    if moveTipe in plaintiffTipe:
        STAB=1.5
    ####type effectiveness####
    tyype=checkTypeEffectiveness(moveTipe,defendantTipe)
    ####Burn###
    burn=1
    damageModifier=weatherBonus*critical*rando*STAB*tyype*burn
    
    ####damage calculation####
    ans=((((2*level)/5 + 2)*power*attack/defense)/50 + 2)*damageModifier
    return ans

def stats(level,base,IV,EV,nature):
    ans=((2*base+IV+EV/4)*level/100+5)*nature
    return ans

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

#moves have pwr, phys/spec, type, accu, descipt
def moveInfo(moveCode):
    movepower=0
    moveSpecial=0
    moveTiipe=0
    return movepower,moveSpecial,moveTiipe

movedex=np.array
movedex = np.array([("razor leaf",50,100,0,3,"these shits are sharp"),("flame wheel",50,100,0,1,"HOT HOT HOT")], \
                   dtype=[('move_name', 'S10'),('pwr', 'f4'),('accu', 'f4'), \
                          ('phys/spec', 'i4'),('move_type', 'i4'),('desc', 'S140')])
print(movedex['desc'][1])
#codex encodes all type matchups, first index is attacking the second index
codex=np.ones((18,18))
#order: normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,ground 8,flying 9,psychic 10,bug 11,
#rock 12,ghost 13,dragon 14,dark 15,steel 16,fairy 17
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
    

#weather='clear'
#weather='rain'
weather='sunny'
#weather='hail'
#weather='sandstorm'

while 1:
    userChoice=input("You can: \n[B]attle! \n")
    if userChoice=='b':
        print("A battle has started!")
        userMon=mon(100,"irwin",tipe=np.array([14]))
        print(f"{userMon.name}! I choose you!")
        enemy=mon(100,"darwin",tipe=np.array([17]))
        print(f"{enemy.name}! Go!")
        while userMon.currenthp>0 and enemy.currenthp>0:
            userMove=input(f"What should {userMon.name} do? \n \n[F]ight \n[R]un \n")
            if userMove=='f':
                userFight=input(f"What move should {userMon.name} use?\n[1] Piss Attack\n[2]Roar of Time\n")
                if userFight==1:
                    print(f"{userMon.name} used Piss Attack!")
                    userMon.move(enemy,50,1,7)

                if userFight==2:
                    print(f"{userMon.name} used Roar of Time!")
                    userMon.move(enemy,100,1,14)

            if userMove=='r':
                print(f"You and {userMon.name} ran away!")
                break
            enMove=np.random.rand(1)
            if enMove>=0.5:
                print(f"{enemy.name} used Slam!")
                enemy.move(userMon,60,0,0)
            if enMove<0.5:
                print(f"{enemy.name} used Fairy Dust!")
                enemy.move(userMon,50,0,17)
        print("The battle ended!")




'''
bulba=mon(60,"eve",tipe=np.array([3,11]))
chard=mon(50,"steve",tipe=np.array([13]))
bulba.checkup()
bulba.move(chard,100,1,0)
chard.checkup()
chard.move(bulba,40,1,moveTipe=1)
chard.checkup()
bulba.appraise()
'''
#bulba=mon(34,"bulbasaur")
#char=mon(32, "charmander")
#bulba.move(char,60,0,moveTipe='fire')
