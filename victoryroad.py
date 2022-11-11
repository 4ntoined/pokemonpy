#Antoine
#this script will use base_pokemon, moves, and dexpoke, to create 5 specific pokemon parties for pokemon.py
#let's go!
import copy
import numpy as np
from base_pokemon import mon, makeMon, makeRandom
from moves import mov,struggle
from dexpoke import dex
rng_wild=np.random.default_rng()
def set_ivs(poke, vals):
    #vals is list or tuple of 6
    poke.hpiv,poke.ativ,poke.deiv,poke.saiv,poke.sdiv,poke.spiv = vals
    poke.reStat()
    return
def set_evs(poke, vals):
    #vals is list or tuple of 6
    poke.hpev,poke.atev,poke.deev,poke.saev,poke.sdev,poke.spev = vals
    poke.reStat()
    return
def random_evs():
    global rng_wild
    ii = 0
    evv = [0]
    while ii < 6: #do 6 times
        #take random values [0,min(252,remaining ev allowance)]
        limit = min(252,508-evv[ii])
        opts = np.arange(0,limit+1,4)
        evv.append(rng_wild.choice(opts))
        ii+=1
    return evv[1:]
def learn_sets(poke, sets):
    global mov
    #sets should be a list of str with names of moves to learn
    poke.knownMoves=[ int(np.argwhere( mov['name'] == sets[i])) for i in range(len(sets))]
    poke.PP = [ mov['pp'][i] for i in silver1.knownMoves]
    return
def add_random_moves(poke, number=2):
    global mov,mo
    return
levil = 145
c1_name = "Silver of Johto"
c2_name = "Zinnia of the Draconids"
c3_name = "Cynthia the Sinnoh Champion"
c4_name = "Former King N of Unova"
c5_name = "Pokemon Trainer Red"
#silvers movesets
weavi_set = ("Shadow Claw","Night Slash","Icy Wind","Metal Claw")
croba_set = ("Air Cutter","Bite","Confuse Ray","Toxic")
typhl_set = ("Infernal Parade","Flamethrower","Swift","Rollout")
lugia_set = ("Aeroblast","Future Sight","Hydro Pump","Recover")
#zinnia movesets
#cynths movesets
#N movesets
#champ movesets

#silver, Weavile, crobat, h-typhlosion(register), lugia
#c1_party = []
silver1 = makeMon(460,level=levil+3,nacher=(0, 3)) #weavile
silver2 = makeMon(168,level=levil+0,nacher=(4, 0)) #crobat
silver3 = makeMon(914,level=levil+3,nacher=(2, 4)) #typhlosion
silver4 = makeMon(248,level=levil+5,nacher=(2, 1)) #lugia
#set evs and ivs
#silver1.summary()
set_ivs(silver1, (31,31,30,31,30,30))
set_ivs(silver2, (30,31,30,31,30,31))
set_ivs(silver3, (30,31,31,31,30,30))
set_ivs(silver4, (31,30,31,30,31,30))
#
#silver1.summary()
set_evs(silver1, tuple(random_evs()))
set_evs(silver2, tuple(random_evs()))
set_evs(silver3, tuple(random_evs()))
set_evs(silver4, tuple(random_evs()))
#have to do moves sigh
#silver1.summary()
#moves####
#silver1.knownMoves=[ int(np.argwhere( mov['name'] == weavi_set[i])) for i in range(len(weavi_set))]
#silver1.PP = [ mov['pp'][i] for i in silver1.knownMoves]
learn_sets(silver1,weavi_set)
learn_sets(silver2,croba_set)
learn_sets(silver3,typhl_set)
learn_sets(silver4,lugia_set)
#add 2 random to everyone

#silver1.summary()
#fill the party
c1_party = [silver2, silver1, silver3, silver4]
#zinnia, salamence, tyrantrum, goodra, zygarde-complete(need to register in dex)
zin1 = makeMon(372,level=levil+3,nacher=(4, 1)) #salamence
zin2 = makeMon(696,level=levil+3,nacher=(1, 3)) #tyran
zin3 = makeMon(705,level=levil+0,nacher=(3, 1)) #goo
zin4 = makeMon(910,level=levil+5,nacher=(1, 1)) #zy
#evs ivs
set_ivs(zin1, (30,31,30,31,30,31))
set_ivs(zin2, (30,30,31,30,31,31))
set_ivs(zin3, (30,30,30,31,31,31))
set_ivs(zin4, (31,30,31,31,30,30))
set_evs(zin1, tuple(random_evs()))
set_evs(zin2, tuple(random_evs()))
set_evs(zin3, tuple(random_evs()))
set_evs(zin4, tuple(random_evs()))
#
#moves

#partyfill
c2_party = [zin1,zin2,zin3,zin4]
#cynthia, spiritomb 441, 447 lucario, milotic 349, giratina-origin(register) 911
cyn1 = makeMon(441,level=levil+0,nacher=(2, 0)) #spirit
cyn2 = makeMon(447,level=levil+3,nacher=(4, 3)) #luke
cyn3 = makeMon(349,level=levil+3,nacher=(3, 0)) #nilo
cyn4 = makeMon(911,level=levil+5,nacher=(4, 2)) #gira
#evs ivs
set_ivs(cyn1, (31,30,30,31,31,31))
set_ivs(cyn2, (30,31,30,31,30,31))
set_ivs(cyn3, (31,30,31,30,31,30))
set_ivs(cyn4, (31,31,30,31,30,30))
set_evs(cyn1, tuple(random_evs()))
set_evs(cyn2, tuple(random_evs()))
set_evs(cyn3, tuple(random_evs()))
set_evs(cyn4, tuple(random_evs()))
#
#moves

#partyfill
c3_party = [cyn1,cyn2,cyn3,cyn4]
#N, 643 zekrom, 583 vanilluxe,566  archeops, zoroark 570 (no illusion :() 
nnn1 = makeMon(643,level=levil+8,nacher=(2, 0)) #zekrom
nnn2 = makeMon(583,level=levil+3,nacher=(4, 3)) #vanill
nnn3 = makeMon(566,level=levil+5,nacher=(3, 0)) #arch
nnn4 = makeMon(570,level=levil+5,nacher=(4, 2)) #zoro
#evs ivs
set_ivs(nnn1, (30,31,31,31,30,31))
set_ivs(nnn2, (30,31,30,31,31,31))
set_ivs(nnn3, (31,31,31,30,30,31))
set_ivs(nnn4, (30,31,31,31,30,31))
set_evs(nnn1, tuple(random_evs()))
set_evs(nnn2, tuple(random_evs()))
set_evs(nnn3, tuple(random_evs()))
set_evs(nnn4, tuple(random_evs()))
#
#moves

#partyfill
c4_party = [nnn1,nnn2,nnn3,nnn4]
#Champ,2 venusaur, 24 pikachu, 5 charizard, 8 blastoise, 913 mega-mewtwo Y(register), mew 150
grn1 = makeMon(2,level=levil+4,nacher=(4, 0)) #venu
grn2 = makeMon(24,level=levil+8,nacher=(4, 3)) #pika
grn3 = makeMon(5,level=levil+4,nacher=(3, 3)) #char
grn4 = makeMon(8,level=levil+4,nacher=(1, 2)) #blas
grn5 = makeMon(913,level=levil+9,nacher=(3, 0)) #mew2
grn6 = makeMon(150,level=levil+10,nacher=(0, 0)) #mew
#evs ivs
set_ivs(grn1, (31,30,31,31,31,31) )
set_ivs(grn2, (30,31,31,31,31,31) )
set_ivs(grn3, (31,31,30,31,31,31) )
set_ivs(grn4, (31,31,31,31,31,30) )
set_ivs(grn5, (31,30,31,31,31,31) )
set_ivs(grn6, (31,31,31,31,31,30) )
set_evs(grn1, tuple( random_evs() ))
set_evs(grn2, tuple( random_evs() ))
set_evs(grn3, tuple( random_evs() ))
set_evs(grn4, tuple( random_evs() ))
set_evs(grn5, tuple( random_evs() ))
set_evs(grn6, tuple( random_evs() ))
#movs

#partyfilling
c5_party=[grn1,grn2,grn3,grn4,grn5,grn6]

if __name__ == "__main__":
    pass
else:
    pass
