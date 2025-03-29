#
"""
Copyright (C) 2023 Adarius
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
#this script will use base_pokemon, moves, and dexpoke, to create 5 specific pokemon parties for pokemon.py
#let's go!
import os
import copy
import numpy as np
from .base_pokemon import mon, makeMon, makeRandom, mo, saveParty
from .moves import mov,struggle
#from dexpoke import dex
from . import dex
from .texter import copyrigh
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
    while ii < 5: #do 5 times
        #take random values [0,min(252,remaining ev allowance)]
        limit = min(252,508-sum(evv))
        opts = np.arange(0,limit+1,4)
        evv.append(rng_wild.choice(opts))
        ii+=1
    evv.append(508-sum(evv)) #for 6th recorded entry, take the remaining allowance
    return evv[1:]
def learn_sets(poke, sets):
    global mov
    #sets should be a list of str with names of moves to learn
    poke.knownMoves=[ int( np.argwhere( mov['name'] == sets[i])[0][0] ) for i in range(len(sets))]
    poke.PP = [ mov['pp'][i] for i in poke.knownMoves]
    return
def add_random_moves(poke, number=2):
    global mov,mo
    mo2 = mo.copy()
    for ii in poke.knownMoves:
        mo2.remove(ii) #remove known move from list of possible moves
    new_moves = list(rng_wild.choice(mo2, size=number))
    new_pp = [ mov['pp'][i] for i in new_moves ]
    poke.knownMoves += new_moves
    poke.PP += new_pp
    return
def make_teams():
    global c1_name,c2_name,c3_name,c4_name,c5_name
    #gonna put the stuff here so we dont run all of it on import
    lvl_m = []
    for i in range(4):
        level_multipliers = [ rng_wild.normal(loc=1.0,scale=0.03)  for i in range(4) ]
        lvl_m.append( level_multipliers )
    lvl_m.append( [ rng_wild.normal(loc=1.,scale=.03) for i in range(6)]  )

    #silver, Weavile, crobat, h-typhlosion(register), lugia
    silver1 = makeMon(460,level=levil+6,nacher=(0, 3),how_created='elite') #weavile
    silver2 = makeMon(168,level=levil+3,nacher=(4, 0),how_created='elite') #crobat
    silver3 = makeMon(914,level=levil+7,nacher=(2, 4),how_created='elite') #typhlosion
    silver4 = makeMon(248,level=levil+8,nacher=(2, 1),how_created='elite') #lugia
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
    learn_sets(silver1,weavi_set)
    learn_sets(silver2,croba_set)
    learn_sets(silver3,typhl_set)
    learn_sets(silver4,lugia_set)
    #add 2 random to everyone
    #silver1.summary()
    add_random_moves(silver1,number=2)
    add_random_moves(silver2,number=2)
    add_random_moves(silver3,number=2)
    add_random_moves(silver4,number=2)
    #these pokemon are done
    #fill the party
    c1_party = [silver2, silver1, silver3, silver4]
    #zinnia, salamence, tyrantrum, goodra, zygarde-complete
    zin1 = makeMon(916,level=levil+3,nacher=(4, 1),how_created='elite') #salamence-m
    zin2 = makeMon(696,level=levil+5,nacher=(1, 3),how_created='elite') #tyran
    zin3 = makeMon(705,level=levil+7,nacher=(3, 1),how_created='elite') #goo
    zin4 = makeMon(910,level=levil+8,nacher=(1, 1),how_created='elite') #zy
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
    learn_sets(zin1, salam_set)
    learn_sets(zin2, tyran_set)
    learn_sets(zin3, goodr_set)
    learn_sets(zin4, zygar_set)
    add_random_moves(zin1, number=2)
    add_random_moves(zin2, number=2)
    add_random_moves(zin3, number=2)
    add_random_moves(zin4, number=2)
    #partyfill
    c2_party = [zin1,zin2,zin3,zin4]
    #cynthia, spiritomb 441, 447 lucario, milotic 349, giratina-origin(register) 911
    cyn1 = makeMon(441,level=levil+4,nacher=(2, 0),how_created='elite') #spirit
    cyn2 = makeMon(915,level=levil+6,nacher=(4, 3),how_created='elite') #luke-mega?
    cyn3 = makeMon(349,level=levil+5,nacher=(3, 0),how_created='elite') #milo
    cyn4 = makeMon(911,level=levil+8,nacher=(4, 2),how_created='elite') #gira
    #evs ivs
    set_ivs(cyn1, (31,30,30,31,31,31))
    set_ivs(cyn2, (30,31,30,31,31,31))
    set_ivs(cyn3, (31,30,31,31,31,30))
    set_ivs(cyn4, (31,31,30,31,30,31))
    set_evs(cyn1, tuple(random_evs()))
    set_evs(cyn2, tuple(random_evs()))
    set_evs(cyn3, tuple(random_evs()))
    set_evs(cyn4, tuple(random_evs()))
    #
    #moves
    learn_sets(cyn1, spiri_set)
    learn_sets(cyn2, lucar_set)
    learn_sets(cyn3, milot_set)
    learn_sets(cyn4, girat_set)
    add_random_moves(cyn1, number=2)
    add_random_moves(cyn2, number=2)
    add_random_moves(cyn3, number=2)
    add_random_moves(cyn4, number=2)
    #partyfill
    c3_party = [cyn1,cyn2,cyn3,cyn4]
    #N, 643 zekrom, 583 vanilluxe,566  archeops, zoroark 570 (no illusion :() 
    nnn1 = makeMon(918,level=levil+8,nacher=(2, 0),how_created='elite') #zekrom-kyurem
    nnn2 = makeMon(583,level=levil+4,nacher=(4, 3),how_created='elite') #vanill
    nnn3 = makeMon(566,level=levil+6,nacher=(3, 0),how_created='elite') #arch
    nnn4 = makeMon(570,level=levil+7,nacher=(4, 2),how_created='elite') #zoro
    #evs ivs
    set_ivs(nnn1, (30,31,31,31,30,0))
    set_ivs(nnn2, (30,31,30,31,31,31))
    set_ivs(nnn3, (31,31,31,30,30,31))
    set_ivs(nnn4, (30,31,31,31,30,31))
    set_evs(nnn1, tuple(random_evs()))
    set_evs(nnn2, tuple(random_evs()))
    set_evs(nnn3, tuple(random_evs()))
    set_evs(nnn4, tuple(random_evs()))
    #
    #moves
    learn_sets(nnn1, zekro_set)
    learn_sets(nnn2, vanil_set)
    learn_sets(nnn3, arche_set)
    learn_sets(nnn4, zoroa_set)
    add_random_moves(nnn1, number=2)
    add_random_moves(nnn2, number=2)
    add_random_moves(nnn3, number=2)
    add_random_moves(nnn4, number=2)
    #partyfill
    c4_party = [nnn1,nnn2,nnn3,nnn4]
    #Champ,2 venusaur, 24 pikachu, 5 charizard, 8 blastoise, 913 mega-mewtwo Y(register), mew 150
    grn1 = makeMon(2,  level=levil+ 6,nacher=(4, 0),how_created='elite') #venu
    grn2 = makeMon(24, level=levil+ 9,nacher=(4, 3),how_created='elite') #pika
    grn3 = makeMon(5,  level=levil+ 6,nacher=(3, 3),how_created='elite') #char
    grn4 = makeMon(8,  level=levil+ 6,nacher=(1, 2),how_created='elite') #blas
    grn5 = makeMon(913,level=levil+ 8,nacher=(3, 0),how_created='elite') #mew2
    grn6 = makeMon(150,level=levil+10,nacher=(0, 0),how_created='elite') #mew
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
    learn_sets(grn1, venus_set)
    learn_sets(grn2, pikac_set)
    learn_sets(grn3, chari_set)
    learn_sets(grn4, blast_set)
    learn_sets(grn5, mewtw_set)
    add_random_moves(grn1, number=2)
    add_random_moves(grn2, number=2)
    add_random_moves(grn3, number=2)
    add_random_moves(grn4, number=2)
    add_random_moves(grn5, number=2)
    grn6.randomizeMoveset(numb=6) #mew gets entirely random moveset
    #partyfilling
    c5_party=[grn1,grn2,grn3,grn4,grn5,grn6]
    return ( (c1_name,c1_party),(c2_name,c2_party),(c3_name,c3_party),(c4_name,c4_party),(c5_name,c5_party)  )
rng_wild=np.random.default_rng()
levil = 150
c1_name = "Silver from Johto"
c2_name = "Zinnia of the Draconids"
c3_name = "Cynthia the Sinnoh Champion"
c4_name = "N, King of Team Plasma"
c5_name = "Pokémon Trainer Red"
#silvers movesets
weavi_set = ("Shadow Claw","Night Slash","Icy Wind","Metal Claw")
croba_set = ("Air Cutter","Bite","Confuse Ray","Toxic")
typhl_set = ("Infernal Parade","Flamethrower","Swift","Rollout")
lugia_set = ("Aeroblast","Future Sight","Hydro Pump","Recover")
#zinnia movesets
salam_set = ("Dragon Claw","Fire Fang","Crunch","Thunder Fang")
tyran_set = ("Dragon Claw","Crunch","Dragon Pulse","Stone Edge")
goodr_set = ("Dragon Pulse","Muddy Water","Thunderbolt","Ice Beam")
zygar_set = ("Core Enforcer","Thousand Arrows","Crunch","Zen Headbutt")
#cynths movesets
spiri_set = ("Dark Pulse","Psychic","Silver Wind","Ominous Wind")
lucar_set = ("Aura Sphere","Dragon Pulse","Psychic","Earthquake")
milot_set = ("Surf","Ice Beam","Mirror Coat","Aqua Ring")
girat_set = ("Shadow Force","Dragon Claw","Earth Power","Aura Sphere")
#N movesets
zekro_set = ("Fusion Bolt","Zen Headbutt","Giga Impact","Light Screen")
vanil_set = ("Blizzard","Hail","Flash Cannon","Frost Breath")
arche_set = ("Stone Edge","Acrobatics","Dragon Claw","Crunch")
zoroa_set = ("Flamethrower","Focus Blast","Night Slash","Retaliate")
#champ movesets
pikac_set = ("Volt Tackle","Iron Tail","Brick Break","Fake Out")
venus_set = ("Leaf Storm","Sludge Bomb","Earthquake","Sleep Powder")
chari_set = ("Fire Blast","Focus Blast","Air Slash","Dragon Pulse")
blast_set = ("Water Spout","Hydro Pump","Blizzard","Focus Blast")
#mew_set   = ("","","","")
mewtw_set = ("Psystrike","Aura Sphere","Recover","Amnesia")
#FreePalestine

if __name__ == "__main__":
    copyrigh(prespace=True)
    savehere = input('\nDirectory to save to: ') or 'elite_four_teams'
    if not os.path.exists(savehere):
        os.makedirs(savehere)
    bigg = make_teams()
    for i in range(5): saveParty(savehere +f'/elite_{i+1:0>1}.npy',bigg[i][1])
else:
    pass
