 #companion to pokemon.py
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
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
import numpy as np
def getMoveInfo(moveIndex):
    return mov[moveIndex]
def movers():
    return
# missing: absorb moves, protect moves, minimize mechanics, multi-hit moves, Flying Press, Transform, Forest's Curse/Soak/Burn Up/etc.,
#          trapping moves, binding moves, endeavor, sucker punch, charge, glaive rush, defog,
## move name // power // accuracy // pp // phys/spec/status // contact? // type // priority // description // code-notes
moremoves=[
        ("V-create",180,95,5,0,1,1,0,0"The user ignites its forehead and hurls itself at the target!\n-Lowers the user's Def. Sp.D and Spe. 1 stage each.","stat self,de:sd:sp,-1:-1:-1,100"),

        ("Prismatic Laser",160,100,10,1,0,10,0,0,"The user attacks the target with lasers using the power of a prism!\n-The user must rest on the next turn.","mustRest"),
        ("Eternabeam",160,90,5,1,0,14,0,0,"The user harnesses Dynamax energy and releases it in a beam!\n-The user must rest on the next turn.","mustRest"),
        
        ("Hyper Beam",150,90,5,1,0,0,0,0,"The user attacks with a powerful beam!\n-The user must rest on next turn.","mustRest"),
        ("Giga Impact",150,90,5,0,1,0,0,0,"The user charges at the target using every bit of its power!\n-The user must rest on next turn.","mustRest"),
        ("Blast Burn",150,90,5,1,0,1,0,0,"The user razes the target with a fiery explosion!\n-The user must rest on next turn.","mustRest"),
        ("Eruption",1,100,5,1,0,1,0,1,"The user attacks with explosive fury!\n-Power = 150 x userHP%.","spout"),
        ("Hydro Cannon",150,90,5,1,0,2,0,"The user attacks the target with a watery blast!\n-The user must rest on next turn.","mustRest"),
        ("Water Spout",1,100,5,1,0,2,0,1,"The user spouts water to damage the target!\n-Power = 150 x userHP%.","spout"), #'spout' = this, eruption, drag energy
        ("Frenzy Plant",150,90,5,1,0,3,0,0,"The user slams the target with roots from an enormous tree!\n-The user must rest on next turn.","mustRest"),
        ("Chloroblast",150,95,5,1,0,3,0,0,"The user amasses chlorophyll and launches it at the target!\n-The user loses half of its max HP to recoil damage.","recoil 1/2maxhp"),
        ("Meteor Assault",150,100,5,0,0,6,0,0,"The user attacks wildly with its thick leek!\n-The user must rest on next turn.","mustRest"),
        ("Rock Wrecker",150,90,5,0,0,12,0,0,"The user launches a huge boulder at the target!\n-The user must rest on next turn.\n-Bomb/ball move.","mustRest bullet"), #bulletproof ability is immune
        ("Head Smash",150,80,5,0,1,12,0,0,"The user attacks the target with a full-power headbutt!\n-The user takes 1/2 recoil damage.","recoil 1/2"),
        ("Roar of Time",150,90,5,1,0,14,0,0,"The user shouts a roar that distorts time and inflicts chronological damage on the target!\n-The user must rest on next turn.","mustRest"),
        ("Dragon Energy",1,100,5,1,0,14,0,1,"The user attacks by converting its life-force into power!\n-Power = 150 x userHP%.","spout"),

   
         #stat(us) conditions
        ("Will-O-Wisp",     0,85,15,2,0,1,0,"The user shoots a sinister flame to burn the target!","burn 100"),
        ("Stun Spore",      0,75,30,2,0,3,0,"The user releases spores that paralyze the target!","para 100 typeImmune grass"), #typeImmune for poke types with immunities
        ("Sleep Powder",    0,75,15,2,0,3,0,"The user uses a powder to lull the target to sleep!","sleep 100 typeImmune grass"),
        ("Thunder Wave",    0,90,20,2,0,4,0,"The user launches a jolt of electricity that paralyzes the target!","para 100"),
        ("Poison Powder",   0,75,35,2,0,7,0,"The user creates a powder to poison the target!","pois 100 typeImmune grass"),
        ("Toxic",           0,90,10,2,0,7,0,"The user badly poisons the target!","badPois 100 noMissPoisons"), #doesn't miss if used by a poison-type
        ("Hypnosis",        0,60,20,2,0,10,0,"The user employs hypnotic suggestion to make the target fall asleep!","sleep 100"),
        ("Confuse Ray",     0,100,10,2,0,13,0,"The user lets loose a sinister beam that causes confusion!","conf 100"),
        ("Dark Void",       0,50,10,2,0,15,0,"The user banishes the target to a world of total darkness that puts them to sleep!","sleep 100 typeImmune grass"),
        #
        ("Struggle", 50,100,1,0,1,18,0,"The user is otherwise out of moves!","noMiss recoil 1/4maxhp")
        ]
# notes about the notes
# stat - raise or lower stats like so:// stat self,at,1,100 // <- raise user's atk. stat 1 stage 100% of the time // stat targ,de:sd:sp,1:-1:1,50 // <- raise target's def. and speed 1 stage each and lower sp.def 1 stage 50% of the time. attack = at, defense = de, special attack = sa, special defense = sd, speed = sp, evasion = ev, accuracy = ac
# burn, para, sleep, frze, pois, badPois, conf - inflict status conditions
# flinch - chance to flinch
# recoil - move damages the user, sometimes based on damage done, sometimes as a proportion of max HP
# hex - move does double damage if the target has a status condition
# solar - 2-turn move that becomes 1 move in sunlight, has power halved in hail, sandstorm, and rain
# dance - moves the activate the dance ability
# moldbreaker - move ignores ability
# collision - move that does 4/3 damage if supereffective
# bullet - move is blocked by bulletproof
# highCrit - move has an increased critical hit ratio
# mustRest - the user will be forced to rest on the next turn
# 2turn - the user will attack on the next turn
# arrows - ground type move that can hit and will ground flying types
# gust - catches Fly-ing pokemon and does double damage
# thunder - catching Fly-ing pokemon and less accurate in sun
# thaws - thaws the user out of the frozen condition
# scald - a non-fire-type "hot" move, thaws the user and target
# pulse - move is boosted by mega launcher
# slicing - move is boosted by sharpness
# noMiss - bypasses accuracy check to always hit/unless the target is semi-invulnerable
# noMissRain - bypasses accuracy check in rain
# noMissPoisons - bypasses accuracy check when used by a Poison-type
# noTarg - does not target the opponent / does target the self
# revelation - move changes type to match the user's primary type
# blessing - recovery move deals 25% max HP
# refresh - heals status conditions

# range key, thank God for bulbapedia, I owe her my life
# 0 - hits 1 target (could be ally, in theory)
# 1 - hits 2 targets (has to be opponents i think)
# 2 - hits specifically an ally (beneficial usually)
# 3 - all but the user
# 4 - all on the field
# 5 - affects user
# 6 - affects user and allies
# 7 - affects a single opponent (specifically opponents)
# 8 - user or ally (you can choose!)

#constructing dtypes and names to accompany data
labels = np.dtype( [('name','U25'),('pwr','i4'),('accu','i4'),('pp','i4'),('special?','i4'),('contact?','i4'),('type','i4'),('priority','i4'),('range','i4'),('desc','U400'),('notes','U140')] )
mov = np.array(moremoves, dtype=labels)
new_dt = np.dtype( [('index','i4')] + mov.dtype.descr)
mov2 = np.zeros(mov.shape, dtype=new_dt)
#creating structed arrays
#new dtype to add the index column and priority 
#new structured array for the new dtype
#dump data from old array into new array
for i in mov.dtype.names:
    mov2[i] = mov[i]
    pass
mov = mov2
mov['index'] = np.arange(0,len(mov), dtype=int)
#find struggle, future sight, tackle
ind=np.argwhere(mov["name"]=="Struggle")
struggle=int(mov[ind]["index"])
ind2 = np.argwhere(mov["name"]=="Future Sight")
futuresigh=int(mov[ind2]["index"])
tackl = int(mov[int(np.argwhere(mov["name"]=="Tackle"))]["index"])
### find the max and z moves, keep their indices stored somewhere so as to easily exclude them ###
maxx = [ "maxmove" in i for i in mov['notes'] ]
max2 = np.argwhere( maxx )
maxset = [ i[0] for i in max2 ]
zzzs = [ "zmove" in i for i in mov['notes'] ]
zzz2 = np.argwhere( zzzs )
zzzset = [ i[0] for i in zzz2 ]
### xx ###

#Natures
#no idea the best way to store this data
#okay got it
#atk = 0, def = 1, spatk = 2, spdef = 3, speed = 4
natures = [ ["Hardy","Lonely","Adamant","Naughty","Brave"], \
           ["Bold","Docile","Impish","Lax","Relaxed"], \
               ["Modest","Mild","Bashful","Rash","Quiet"],\
                   ["Calm","Gentle","Careful","Quirky","Sassy"], \
                       ["Timid","Hasty","Jolly","Naive","Serious"] ]
natures = np.array(natures,dtype=object)
#

#Abilities
abilities = [
    #ability name, flavor text
    ("Rough Skin",""),
    ("Dancer",""),
    #start weathers, terrains
    ("Drizzle",""),
    ("Drought",""),
    ("Sand Stream",""),
    ("Snow Warning",""),
    ("Electric Surge",""),
    ("Grassy Surge",""),
    ("Misty Surge",""),
    ("Psychic Surge",""),
    #immunities
    ("Levitate",""),
    ("Bulletproof","The Pokémon is immune to ball and bomb moves."), #immunity to moves with "bullet" in the notes
    ("Soundproof",""),
    ("Sap Sipper",""),
    ("Wind Rider",""),
    ("Wind Power",""),
    ("Volt Absorb",""),
    ("Water Absorb",""),
    ("Lightning Rod",""),
    #attackpower boosts
    ("Guts",""),
    ("Sharpness",""),
    ("Strong Jaw",""),
    ("Tough Claws","Boosts by 30% the power of moves that make contact with the target."),
    ("Mega Launcher","Boosts by 50% the power of pulse moves."),
    ("Overgrow","Boosts by 50% the power of Grass-type moves when HP is less than 1/3 maximum HP."),
    ("Blaze","Boosts by 50% the power of Fire-type moves when HP is less than 1/3 maximum HP."),
    ("Torrent","Boosts by 50% the power of Water-type moves when HP is less than 1/3 maximum HP."),
    ("Swarm","Boosts by 50% the power of Bug-type moves when HP is less than 1/3 maximum HP."),
    ("Technician","Boosts by 50% the power of moves with base power 60 or less."), #doesn't apply to confusion damage, considers variable base power, (Gust, acrobatics)
    
    ("The Last Ability","null")
]

if __name__ == "__main__":
    np.save("saved_movedex.npy",mov)
    #np.save("saved_natures.npy",natures)
else:
    pass

