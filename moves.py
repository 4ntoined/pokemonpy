#companion to pokemon.py
#Antoine Washington
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17

import numpy as np
#from astropy import table as tbl

def getMoveInfo(moveIndex):
    return mov[moveIndex]

moremoves=[
        ("Hyper Beam",150,90,5,1,0,0,"The user attacks with a powerful beam! Must rest on next turn.","mustRest"),
        ("Blast Burn",150,90,5,1,0,1,"The user attacks with a fiery explosion! Must rest on next turn","mustRest"),
        ("Frenzy Plant",150,90,5,1,0,3,"Big roots! Must rest on next turn.","mustRest"),
        ("Hydro Cannon",150,90,5,1,0,2,"Blast of water! Must rest on next turn.","mustRest"),
        ("Giga Impact",150,90,5,0,1,0,"Must rest on next turn.","mustRest"),
        ("Roar of Time",150,90,5,1,0,14,"The user roars to distort time and inflict damage. Must rest on next turn.","mustRest"),
        ("Rock Wrecker",150,90,5,0,0,12,"Must rest on next turn.","mustRest"),
        ("Double-Edge",120,100,15,0,1,0,"User takes 1/3 recoil damage.","recoil 1/3"),
        ("Volt Tackle",120,100,15,0,1,4,"User takes 1/3 recoil damage.","recoil 1/3 para 10"),
        ("Brave Bird",120,100,15,0,1,9,"Takes 1/3 recoil damage.","recoil 1/3"),
        ("Flare Blitz",120,100,15,0,1,1,"User takes 1/3 recoil damage.","recoil 1/3 burn 10 thaws"),
        ("Wood Hammer",120,100,15,0,1,3,"Takes 1/3 recoil damage.","recoil 1/3"),
        ("Earthquake",100,100,10,0,0,8,"The user causes a powerful earthquake.","nerfGrassy"), #one day we'll generalize moves having their power nerfed under certain conditions....not today tho
        ("Judgement",100,100,10,1,0,0,"The user pelts the battlefield with bolts of light from the sky.",""),
        ("Flamethrower",90,100,15,1,0,1,"The user attacks with a powerful flame! 10% chance to burn.","burn 10"),
        ("Ice Beam",90,100,15,1,0,5,"The user focuses a stream of ice at the target! 10% chance to freeze.","frze 10"),
        ("Thunderbolt",90,100,15,1,0,4,"The user attacks with a bolt of lightning! 10% chance to paralyze.","para 10"),
        ("Leaf Blade",90,100,15,0,1,3,"The user attacks with a sharpened leaf! High crit' ratio.","highCrit"),
        ("Attack Order",90,100,15,0,0,11,"The user attacks with a powerful flame! High crit' ratio.","highCrit"),
        ("Tackle",40,100,35,0,1,0,"The user charges to attack.","null"),
        ("Close Combat",120,100,5,0,1,6,"The user drops their guard to achieve an all out attack. Lowers Def. and SpD. 1 stage each.","stat self,de:sd,-1:-1,100"),
        ("Dark Pulse",80,100,15,1,0,15,"The user sends malicious energy in a powerful wave. 20% chance to flinch.","flinch 20"),
        ("Ominous Wind",60,100,5,1,0,13,"The user attacks with a mysterious wind. 10% chance to raise all stats 1 stage.","stat self,at:de:sa:sd:sp,1:1:1:1:1,10"),
        ("Meteor Mash",90,90,10,0,1,16,"The user punches with the power of a meteor. 20% chance to raise user's Atk. 1 stage.","stat self,at,1,20"),
        ("Flame Wheel",60,100,15,0,1,1,"The user covers itself in fire and rolls into the target! 10% chance to burn","burn 10 thaws"),
        ("Stomp",65,100,20,0,1,0,"The user forcefully stomps on the target!","flinch 30 noMissMinimize"), #doesn't miss if target used minimize
        ("Solar Beam",120,100,10,1,0,3,"The user focuses sunlight into a beam to attack!\nTwo-turn move, one-turn in harsh sunlight.","2turn solar"),
        ("Solar Blade",125,100,10,0,1,3,"The user focuses sunlight into a blade to attack!\nTwo-turn move, one-turn in harsh sunlight.","2turn solar"),
        ("Skull Bash",130,100,10,0,1,0,"The user tucks its head in and charges at the target.\nTwo-turn move.","2turn skullbash"), #needs to raise defense 1 stage on the prep
        ("Weather Ball",50,100,10,1,0,0,"The user harnesses the power of the weather to attack!\nChanges type and doubles power in non-clear weather.","weatherball"),
        ("X-Scissor",80,100,15,0,1,11,"The user slashes the target by crossing its claws!","null"),
        ("Signal Beam",75,100,15,1,0,11,"The user attacks with an odd beam of light! 10% chance to confuse.","conf 10"),
        ("Draco Meteor",130,90,5,1,0,14,"The user calls upon its draconic powers...\nand unleashes a storm of meteors!\nLowers SpA. 2 stages.","stat self,sa,-2,100"),
        ("Dragon Pulse",85,100,10,1,0,14,"The user summons a beastly beam from its mouth!","null"),
        ("Dragon Claw",80,100,15,0,1,14,"The user slashes the target with shape claws!","null"),
        ("Clanging Scales",110,100,5,1,0,14,"Scales go bang.","stat self,de,-1,100"),
        ("Boomburst",140,100,10,1,0,0,"The user attacks with a terrible, explosive sound!","null"), #at some point we'll track sound-based moves
        ("Crush Claw",75,95,10,0,1,0,"The user slashes the target with hard, sharp claws\n May lower Def. 1 stage.","stat targ,de,-1,50"), #at some point we'll track sound-based moves
        ("Cut",50,95,30,0,1,0,"The use cuts the target with a scythe or claw!","null"),
        #("Dizzy Punch",70,100,10,0,1,0,"","conf 20"), Why did dizzy punch get kicked out of the game :(
        ("Facade",70,100,20,0,1,0,"An attack that does double damage if the user is poisoned, burned, or paralyzed.","facade"),
        ("Head Charge",120,100,15,0,1,0,"The user charges with its head and powerful guard hair!\nDoes 1/4 recoil damage.","recoil 1/4"),
        ("Headbutt",70,100,15,0,1,0,"The user sticks out its head and attacks!\n30% chance to flinch target.","flinch 30"),

        #weather moves
        ("Sunny Day",0,100,5,2,0,1,"The user calls on the Sun and causes harsh sunlight!","sun noMiss"),
        ("Rain Dance",0,100,5,2,0,2,"The user disrupts the air pressure and causes rain!","rain noMiss"),
        ("Sandstorm",0,100,5,2,0,12,"The user calls on the local sands to whip up a sandstorm!","sand noMiss"),
        ("Hail",0,100,5,2,0,5,"The user summons a cloudy cold front and creates a hailstorm!","hail noMiss"),
        #terrain moves
        ("Electric Terrain",0,100,10,2,0,4,"The user electrifies the battlefield! Electric-type moves get a 30% boost.","electric noMiss"),
        ("Grassy Terrain",0,100,10,2,0,3,"The user covers the battlefield with grass! Grass-type moves get a 30% boost.","grassy noMiss"),
        ("Misty Terrain",0,100,10,2,0,17,"The user covers the battlefield in mist! Dragon-type moves get a 50% nerf.","misty noMiss"),
        ("Psychic Terrain",0,100,10,2,0,10,"The user makes the battlefield weird! Psychic-type moves get a 30% boost.","psychic noMiss"),
        #entry hazards
        ("Spikes",0,100,20,2,0,8,"The user spreads spikes on the opponent's side of the field!\nStack up to 3 times!","noMiss spikes"),
        ("Toxic Spikes",0,100,20,2,0,7,"The user sends out toxic barbs on the target's side of the field!\nPokemon are poisoned on entry.\nStacks up to 2 times for bad poisoned.","noMiss toxspk"),
        ("Stealth Rocks",0,100,20,2,0,12,"The user spreads pointed stones on the opponent's side of the field!\nDoes rock-type damge.","noMiss rocks"),
        ("Sticky Web",0,100,20,2,0,11,"The user weaves a web on the target's side of the field!\nLowers Spe. stat 1 stage upon entry.","noMiss sticky"),
        #status moves
         #stat(istic) changes
        ("Harden",0,100,40,2,0,0,"The user stiffens the muscles in its body!\nRaises Def. 1 stage.","stat self,de,1 noMiss"),
        ("Swords Dance",0,100,20,2,0,0,"Boosts Atk. 2 stages.","stat self,at,2 noMiss"),
        ("Nasty Plot",0,100,20,2,0,15,"Boosts SpA. 2 stages.","stat self,sa,2 noMiss"),
        ("Dragon Dance",0,100,20,2,0,14,"Boosts Atk. and Sp. 1 stage each.","stat self,at:sp,1:1 noMiss"),
        ("Growth",0,100,20,2,0,0,"The user's body grows all at once!\nBoosts Atk. and Sp.A 1 stage each. Two each in harsh sunlight.","stat self,at:sa,1:1 noMiss growth"),
        ("Geomancy",0,100,10,2,0,17,"The user absorbs energy from its surroundings to power up!\nBoosts Sp.A Sp.D Spd. 2 stages each.\nTwo-turn move.","stat self,sa:sd:sp,2:2:2 noMiss 2turn geomance"),
        ("Confide",0,100,20,2,0,0,"The user tells the target a (quite inappropriate) secret.\nIt lowers the target's Sp.A 1 stage.","stat targ,sa,-1 noMiss"),
        ("String Shot",0,95,40,2,0,11,"The user spins silk to bind the target! Lowers target's Spd. 1 stage.","stat targ,sp,-1"),
        ("Double Team",0,100,15,2,0,0,"The user moves so quick it creates afterimages.\nRaises evasiveness 1 stage.","stat targ,ev,1 noMiss"),
        ("Growl",0,100,40,2,0,0,"The user growls cutely.\nIt lowers the target's Atk. 1 stage.","stat targ,at,-1"),
         #stat(us) conditions
        ("Stun Spore",0,75,30,2,0,3,"The user releases spores that paralyze the target!","para 100 typeImmune grass"), #typeImmune for poke types with immunities
        ("Sleep Powder",0,75,15,2,0,3,"The user uses a powder to lull the target to sleep!","sleep 100 typeImmune grass"),
        ("Poison Powder",0,75,35,2,0,7,"The user creates a powder to poison the target!","pois 100 typeImmune grass"),
        ("Toxic",0,90,10,2,0,7,"The user badly poisons the target!","badPois 100 noMissPoisons"), #doesn't miss if used by a poison-type
        ("Confuse Ray",0,100,10,2,0,13,"The user lets loose a sinister beam that causes confusion!","conf 100"),
        #to do: max moves! terrain pulse
        ("Struggle",50,100,1,0,1,18,"The user is otherwise out of moves.","noMiss recoil 1/4maxhp")
        ]
#constructing dtypes and names to accompany data
labels = np.dtype( [('name','U25'),('pwr','i4'),('accu','i4'),('pp','i4'),('special?','i4'),('contact?','i4'),('type','i4'),('desc','U140'),('notes','U140')] )
#creating structed arrays
mov = np.array(moremoves, dtype=labels)
#new dtype to add the index column
new_dt = np.dtype( [('index','i4')] + mov.dtype.descr)
#new structured array for the new dtype
mov2 = np.zeros(mov.shape, dtype=new_dt)
#dump data from old array into new array
for i in mov.dtype.names:
    mov2[i] = mov[i]
    pass
mov = mov2
mov['index'] = np.arange(0,len(mov), dtype=int)
#find struggle
ind=np.argwhere(mov["name"]=="Struggle")
struggle=int(mov[ind]["index"])
#save the table, especially for readability
mov.tofile('movedex2.txt', sep='\n')
with open('movedex2.txt', 'a') as ofile:
    ofile.write('\n')

#with open('movedex2.dat','w') as ofile:
#    ofile.write('index name pwr accu pp special? contact? type desc notes\n')
#    for i in range(len(mov)):
#        for j in range(len(mov[i])):
#            file.write("{j}, ")

#
#Natures?
#no idea the best way to store this data
#okay got it
#atk = 0, def = 1, spatk = 2, spdef = 3, speed = 4
natures = [ ["Hardy","Lonely","Adamant","Naughty","Brave"], \
           ["Bold","Docile","Impish","Lax","Relaxed"], \
               ["Modest","Mild","Bashful","Rash","Quiet"],\
                   ["Calm","Gentle","Careful","Quirky","Sassy"], \
                       ["Timid","Hasty","Jolly","Naive","Serious"] ]
natures = np.array(natures,dtype=object)



