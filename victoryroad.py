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
levil = 145
c1_name = "Silver of Johto"
c2_name = "Zinnia of the Draconids"
c3_name = "Cynthia the Sinnoh Champion"
c4_name = "Former King N of Unova"
c5_name = "Pokemon Trainer Red"
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
c1_party = [silver2, silver1, silver3, silver4]
#zinnia, salamence, tyrantrum, goodra, zygarde-complete(need to register in dex)
zin1 = makeMon(372,level=levil+3,nacher=(4, 1)) #salamence
zin2 = makeMon(696,level=levil+3,nacher=(1, 3)) #tyran
zin3 = makeMon(705,level=levil+0,nacher=(3, 1)) #goo
zin4 = makeMon(910,level=levil+5,nacher=(1, 1)) #zy


#cynthia, spiritomb, lucario, milotic, giratina-origin(register)



#N, zekrom, vanilluxe, archeops, zoroark (no illusion :() 



#Champ,venusaur, pikachu, charizard, blastoise, mega-mewtwo Y(register), mew


if __name__ == "__main__":
    pass
else:
    pass
