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
## move name // power // accuracy // pp // phys/spec/status // contact? // type // priority // description // code-notes
moremoves=[
        ("Hyper Beam",150,90,5,1,0,0,0,"The user attacks with a powerful beam! Must rest on next turn.","mustRest"),
        ("Blast Burn",150,90,5,1,0,1,0,"The user attacks with a fiery explosion! Must rest on next turn","mustRest"),
        ("Frenzy Plant",150,90,5,1,0,3,0,"Big roots! Must rest on next turn.","mustRest"),
        ("Hydro Cannon",150,90,5,1,0,2,0,"Blast of water! Must rest on next turn.","mustRest"),
        ("Giga Impact",150,90,5,0,1,0,0,"Must rest on next turn.","mustRest"),
        ("Roar of Time",150,90,5,1,0,14,0,"The user roars to distort time and inflict damage. Must rest on next turn.","mustRest"),
        ("Rock Wrecker",150,90,5,0,0,12,0,"Must rest on next turn.","mustRest"),
        ("Water Spout",150,100,5,1,0,2,0,"The user spouts water to damage the target!\nThe lower the user's HP, the lower this move's power.","spout"), #will use 'spout' for this, eruption, and drag energy
        ("Eruption",150,100,5,1,0,1,0,"The user attacks with a furious explosion!\nThe lower the user's HP, the lower this move's power.","spout"),
        ("Dragon Energy",150,100,5,1,0,14,0,"The user attacks by converting its life-force into power.\nThe lower the user's HP, the lower this move's power.","spout"),
        ("Boomburst",140,100,10,1,0,0,0,"The user attacks with a terrible, explosive sound!","null"), #at some point we'll track sound-based moves
        ("Draco Meteor",130,90,5,1,0,14,0,"The user calls upon its draconic powers and unleashes a storm of meteors!\nLowers SpA. 2 stages.","stat self,sa,-2,100"),
        ("Skull Bash",130,100,10,0,1,0,0,"The user tucks its head in and charges at the target.\nTwo-turn move.","2turn skullbash"), #needs to raise defense 1 stage on the prep
        ("Leaf Storm",130,90,5,1,0,3,0,"The user whips up a storm of leaves around the target.\nLowers the user's SpA. by 2 stages.",'stat self,sa,-2,100'),
        ("Solar Blade",125,100,10,0,1,3,0,"The user focuses sunlight into a blade to attack!\nTwo-turn move, one-turn in harsh sunlight.","2turn solar"),
        ("Double-Edge",120,100,15,0,1,0,0,"User takes 1/3 recoil damage.","recoil 1/3"),
        ("Volt Tackle",120,100,15,0,1,4,0,"User takes 1/3 recoil damage.","recoil 1/3 para 10"),
        ("Brave Bird",120,100,15,0,1,9,0,"Takes 1/3 recoil damage.","recoil 1/3"),
        ("Flare Blitz",120,100,15,0,1,1,0,"User takes 1/3 recoil damage.","recoil 1/3 burn 10 thaws"),
        ("Wood Hammer",120,100,15,0,1,3,0,"Takes 1/3 recoil damage.","recoil 1/3"),
        ("Close Combat",120,100,5,0,1,6,0,"The user drops their guard to achieve an all out attack. Lowers Def. and SpD. 1 stage each.","stat self,de:sd,-1:-1,100"),
        ("Solar Beam",120,100,10,1,0,3,0,"The user focuses sunlight into a beam to attack!\nTwo-turn move, one-turn in harsh sunlight.","2turn solar"),
        ("Head Charge",120,100,15,0,1,0,0,"The user charges with its head and powerful guard hair!\nDoes 1/4 recoil damage.","recoil 1/4"),
        ("Focus Blast",120,70,5,1,0,6,0,"The user heightens its mental focus an unleashs its power\n10% chance to lower target's SpD. 1 stage.","stat targ,sa,-1,10"),
        ("Shadow Force",120,100,5,0,1,13,0,"The user disappears and strikes the target on the next turn.","shadowforce 2turn semi-invul"),
        ("Future Sight",120,100,5,1,0,10,0,"The user looks into the future and predicts an attack.","futuresight"),
        ("Clanging Scales",110,100,5,1,0,14,0,"Scales go bang.","stat self,de,-1,100"),
        ("Fire Blast",110,85,5,1,0,1,0,"The user attacks with a blast of all-consuming flames.\n10% chance to burn target.","burn 10"),
        ("Hydro Pump",110,80,5,1,0,2,0,"The user blasts the target with a huge volume of water under great pressure!","null"),
        ("Blizzard",110,70,5,1,0,5,0,"The user summons a howling blizzard to strike the target.\n10% chance to freeze.","frze 10 blizzard"), #doesn't miss in hail, need to program
        ("Thunder",110,70,10,1,0,4,0,"The user drops a wicked lightningbolt on the target to inflict damage!\n30% chance to paralyze.","para 30 thunder"),
        ("Hurricane",110,70,10,1,0,9,0,"The user wraps its target in a fierce wind from a furious storm!\n30% chance to confuse.","conf 30 thunder"),
        ("Earthquake",100,100,10,0,0,8,0,"The user causes a powerful earthquake!","nerfGrassy"), #one day we'll generalize moves having their power nerfed under certain conditions....not today tho
        ("Judgement",100,100,10,1,0,0,0,"The user pelts the battlefield with bolts of light from the sky!","null"),
        ("Stone Edge",100,80,5,0,0,12,0,"The user stabs the target from below with sharpened stones!\nHigh crit. ratio.","highCrit"),
        ("Aeroblast",100,95,5,1,0,9,0,"The user shoots a vortex of air at the target!\nHigh crit. ratio.","highCrit"),
        ("Iron Tail",100,75,15,0,1,16,0,"The user slams the target wit a steel-hard tail!\n30% chance to lower target's Def. 1 stage.","stat targ,de,-1,30"),
        ("Psystrike",100,100,10,1,0,10,0,"The user materializes an odd psychic wave to attack!\nDamage is calculated with the user's SpA. and the target's Def.","psystrike"), #will use psystrike tag for psyshock and secret sword
        ("Core Enforcer",100,100,10,1,0,14,0,"The user unleases a super sick laser and draws a 'Z'!","null"), #otherwise would suppress abilities, but we have none
        ("Fusion Bolt",100,100,5,0,0,4,0,"The user throws down a giant lightning bolt!\nMore powerful if used after Fusion Flare.","fusion-b"),
        ("Fusion Flare",100,100,5,1,0,1,0,"The user throws down a giant flame!\nMore powerful if used after Fusion Bolt.","fusion-f thaws"),
        ("Earth Power",90,100,10,1,0,8,0,"The user makes the ground under the target erupt with power!\nMay lower target's Sp.D 1 stage.","stat targ,sd,-1,10"),
        ("Flamethrower",90,100,15,1,0,1,0,"The user attacks with a powerful flame! 10% chance to burn.","burn 10"),
        ("Ice Beam",90,100,15,1,0,5,0,"The user focuses a stream of ice at the target! 10% chance to freeze.","frze 10"),
        ("Thunderbolt",90,100,15,1,0,4,0,"The user attacks with a bolt of lightning! 10% chance to paralyze.","para 10"),
        ("Leaf Blade",90,100,15,0,1,3,0,"The user attacks with a sharpened leaf! High crit' ratio.","highCrit"),
        ("Attack Order",90,100,15,0,0,11,0,"The user attacks with a powerful flame! High crit' ratio.","highCrit"),
        ("Sludge Bomb",90,100,10,1,0,7,0,"Unsanitary sludge is hurled at the target.\n30% chance to poison the target.","pois 30"),
        ("Psychic",90,100,10,1,0,10,0,"The user hits the target with a strong telekinetic force!\nMay lower target's Sp.D 1 stage.","stat targ,sd,-1,10"),
        ("Surf",90,100,15,1,0,2,0,"The user swamps everything around it with a giant wave!","null"), #hits during dive? if Im doing Shadow Sneak, fly and dive are on the table, in which case the likes of thunder and surf and earthquake also come into play
        ("Muddy Water",90,85,10,1,0,2,0,"The user attacks by shooting muddy water at the target!\nMay lower the target's accuracy.","stat targ,ac,-1,30"),
        ("Thousand Arrows",90,100,10,0,0,8,0,"The user creates arrows from the very ground and hurls them at the target.\nHits ungrounded targets and grounds them.","arrows"),
        ("Phantom Force",90,100,10,0,1,13,0,"dedc","2turn shadowforce"),
        ("Fly",90,95,15,0,1,9,0,"dedc","2turn flying"),
        ("Bounce",85,85,5,0,1,9,0,"dedc","2turn flying para 30"),
        ("Dragon Pulse",85,100,10,1,0,14,0,"The user summons a beastly beam from its mouth!","null"),
        ("Secret Sword",85,100,10,1,0,6,0,"The user uses odd power to cut with its long horn!\nDamage is calculated with the user's SpA. and the target's Def.","psystrike"),
        ("X-Scissor",80,100,15,0,1,11,0,"The user slashes the target by crossing its claws!","null"),
        ("Dragon Claw",80,100,15,0,1,14,0,"The user slashes the target with shape claws!","null"),
        ("Zen Headbutt",80,90,15,0,1,10,0,"The user focuses its willpower into its head and attacks the target!\n20% chance to make the target flinch.","flinch 20"),
        ("Aura Sphere",80,100,20,1,0,6,0,"The user looses a blast of auro from deep within its body.\nThis attack will not miss.","noMiss"),
        ("Crunch",80,100,15,0,1,15,0,"The user crunches on the target with sharp fangs.\nMay lower the target's Def. 1 stage.","stat targ,de,-1,20"),
        ("Dark Pulse",80,100,15,1,0,15,0,"The user releases a terrible aura imbued with dark thoughts!\n20% chance to make the target flinch.","flinch 20"),
        ("Flash Cannon",80,100,10,1,0,16,0,"The user gathers all its light energy and releases it all at once at the target. May lower target's Sp.D 1 stage.","stat targ,sd,-1,10"),
        ("Psyshock",80,100,10,1,0,10,0,"The user materializes an odd psychic wave to attack.\nDamage is calculated with the user's SpA. and the target's Def.","psystrike"),
        ("Extreme Speed",80,100,5,0,1,0,+2,"The user charges at the target with blinding speed.\nThis move has +2 priority.","null"),
        ("Dive",80,100,10,0,1,2,0,"The user dives.\nTwo-turn move.","2turn diving"),
        ("Dig",80,100,10,0,1,8,0,"The user digs.\nTwo-turn move.","2turn digging"),
        ("Signal Beam",75,100,15,1,0,11,0,"The user attacks with an odd beam of light! 10% chance to confuse.","conf 10"),
        ("Crush Claw",75,95,10,0,1,0,0,"The user slashes the target with hard, sharp claws\n May lower Def. 1 stage.","stat targ,de,-1,50"), #at some point we'll track sound-based moves
        ("Brick Break",75,100,15,0,1,6,0,'The user attacks with a swift chop. This removes Light Screen and Reflect.','breakScreens'), #need to program light screen and reflect and aurora veil
        ("Air Slash",75,95,15,1,0,9,0,"The user attacks with a blade of air that slices the sky.\n30% chance to make the target flinch.","flinch 30"),
        #("Dizzy Punch",70,100,10,0,1,0,0,"","conf 20"), Why did dizzy punch get kicked out of the game :(
        ("Facade",70,100,20,0,1,0,0,"An attack that does double damage if the user is poisoned, burned, or paralyzed.","facade"),
        ("Retaliate",70,100,5,0,1,0,0,"The user gets revenge for a fainted ally.\nDoubles in power if an ally fainted in the previous turn.","retaliate"),
        ("Headbutt",70,100,15,0,1,0,0,"The user sticks out its head and attacks!\n30% chance to flinch target.","flinch 30"),
        ("Night Slash",70,100,15,0,1,15,0,"The user sneaks in and slashes the target the instant it gets the opportunity\nHigh crit. ratio.","highCrit"),
        ("Shadow Claw",70,100,15,0,1,13,0,"The user materializes a sharp claw from the shadows and slashes at the target!\nHigh crit. ratio.","highCrit"),
        ("Stomp",65,100,20,0,1,0,0,"The user forcefully stomps on the target!","flinch 30 noMissMinimize"), #doesn't miss if target used minimize
        ("Hex",65,100,10,1,0,13,0,"The user attacks relentlessly, doing double damage to a target with status conditions!","hex"),
        ("Fire Fang",65,95,15,0,1,1,0,"The user bites with flame-cloaked fangs.\n10% chance to flinch, 10% chance to burn.","burn 10 flinch 10"),
        ("Thunder Fang",65,95,15,0,1,4,0,"The user bites with electrified fangs.\n10% chance to flinch, 10% chance to paralyze.","para 10 flinch 10"),
        ("Ice Fang",65,95,15,0,1,5,0,"The user bites with frozen fangs.\n10% chance to flinch, 10% chance to freeze.","frze 10 flinch 10"),
        ("Ominous Wind",60,100,5,1,0,13,0,"The user attacks with a mysterious wind. 10% chance to raise all stats 1 stage.","stat self,at:de:sa:sd:sp,1:1:1:1:1,10"),
        ("Air Cutter",60,95,25,1,0,9,0,"The user launches razor-sharp winds to slash opponents.\nHigh crit. ratio.","highCrit"),
        #("Feint Attack",60,100,20,0,1,15,0,"",""), uhhh feint attack was nixed in gen 8, and i just programmed night slash so maybes thats a fine replacement?
        ("Flame Wheel",60,100,15,0,1,1,0,"The user covers itself in fire and rolls into the target! 10% chance to burn","burn 10 thaws"),
        ("Silver Wind",60,100,5,1,0,11,0,"The user attacks with powderly scales carried on the wind.\n10% chance to raise all stats 1. stage.","stat self,at:de:sa:sd:sp,1:1:1:1:1,10"), #not in SwSh, but IN LegendsArceus so we move!
        ("Bite",60,100,25,0,1,15,0,"The user bites the target with viciously sharp fangs.\nMay make the target flinch.","flinch 30"),
        ("Infernal Parade",60,100,15,1,0,13,0,"The user attacks with a myriad of fireballs!\nMay leave a burn. Double damaged when the target has a status condition.","hex burn 30"), #this is a LegendsArceus exclusive and i feel like it's a little overpowered in this meta, but like...whatever its fine
        ("Swift",60,100,20,1,0,0,0,"The user shoots star-shaped rays at the target!\nThis move will not miss.","noMiss"),
        ("Frost Breath",60,90,10,1,0,5,0,"The user blows cold breath on the target!\nThis move always lands a critical hit.","frostbreath"),
        ("Storm Throw",60,100,10,0,1,6,0,"The user strikes the target with a fierce blow.\nThis move always lands a critical hit.","frostbreath"),
        ("Icy Wind",55,95,15,1,0,5,0,"The user attacks with a gust of chilled air.\nLowers the target's Spe. 1 stage.","stat targ,sp,-1,100"),
        ("Acrobatics",110,100,15,0,1,9,0,"The user nimbly strikes the target!","null"), #Im going to just double acrobatics' power bc its canon and we dont have items yet
        ("Weather Ball",50,100,10,1,0,0,0,"The user harnesses the power of the weather to attack!\nChanges type and doubles power in non-clear weather.","weatherball"),
        ("Cut",50,95,30,0,1,0,0,"The use cuts the target with a scythe or claw!","null"),
        ("Metal Claw",50,95,35,0,1,16,0,"The user rakes the target with steel claws.\nMay raise the user's Atk. 1 stage.","stat self,at,1,10"),
        ("Quick Attack",40,100,30,0,1,0,+1,"The user lunges at the target so fast it becomes invisible!\nThis move has +1 priority.","null"),
        ("Gust",40,100,35,1,0,9,0,"desc","gust"),
        ("Twister",40,100,20,1,0,14,0,"desc","gust flinch 20"),
        ("Tackle",40,100,35,0,1,0,0,"The user charges to attack.","null"),
        ("Fake Out",40,100,10,0,1,0,+3,"The user hits first and makes the target flinch.\nOnly works on the first turn after the user enters battle.\This move has +3 priority","flinch 100 fakeout"), #need priority AND first-turn tracking
        ("Rollout",30,90,20,0,1,12,0,"The user rolls into the target for fives turns!\nDoes more damage each consecutive turn.","rollout"),
        #counter and mirror coat,
        ("Counter",1,100,20,0,1,6,-5,"Counter","counter"),
        ("Mirror Coat",1,100,20,1,0,10,-5,"Special move counter","mirrorcoat"),
        #status moves
         #weather moves
        ("Sunny Day",0,100,5,2,0,1,0,"The user calls on the Sun and causes harsh sunlight!","sun noMiss noTarg"),
        ("Rain Dance",0,100,5,2,0,2,0,"The user disrupts the air pressure and causes rain!","rain noMiss noTarg"),
        ("Sandstorm",0,100,5,2,0,12,0,"The user calls on the local sands to whip up a sandstorm!","sand noMiss noTarg"),
        ("Hail",0,100,5,2,0,5,0,"The user summons a cloudy cold front and creates a hailstorm!","hail noMiss noTarg"),
         #terrain moves
        ("Electric Terrain",0,100,10,2,0,4,0,"The user electrifies the battlefield! Electric-type moves get a 30% boost.","electric noMiss noTarg"),
        ("Grassy Terrain",0,100,10,2,0,3,0,"The user covers the battlefield with grass! Grass-type moves get a 30% boost.","grassy noMiss noTarg"),
        ("Misty Terrain",0,100,10,2,0,17,0,"The user covers the battlefield in mist! Dragon-type moves get a 50% nerf.","misty noMiss noTarg"),
        ("Psychic Terrain",0,100,10,2,0,10,0,"The user makes the battlefield weird! Psychic-type moves get a 30% boost.","psychic noMiss noTarg"),
         #entry hazards
        ("Spikes",0,100,20,2,0,8,0,"The user spreads spikes on the opponent's side of the field!\nStack up to 3 times!","noMiss spikes noTarg"),
        ("Toxic Spikes",0,100,20,2,0,7,0,"The user sends out toxic barbs on the target's side of the field!\nPokemon are poisoned on entry.\nStacks up to 2 times for bad poisoned.","noMiss toxspk noTarg"),
        ("Stealth Rocks",0,100,20,2,0,12,0,"The user spreads pointed stones on the opponent's side of the field!\nDoes rock-type damge.","noMiss rocks noTarg"),
        ("Sticky Web",0,100,20,2,0,11,0,"The user weaves a web on the target's side of the field!\nLowers Spe. stat 1 stage upon entry.","noMiss sticky noTarg"),
         #reflect, lightscreen
        ("Reflect",0,100,20,2,0,10,0,"The user creates a wall of light that reduces damage from physical attacks for 5 turns!","reflect noMiss noTarg"),
        ("Light Screen",0,100,20,2,0,10,0,"he user creates a wall of light that reduces damage from special attacks for 5 turns!","lightscreen noMiss noTarg"),
        ("Aurora Veil",0,100,20,2,0,5,0,"that veil","veil needHail noTarg"),
         #healing
        ("Recover",0,100,10,2,0,0,0,"The user regenerates cells to heal itself by half its max HP.","heals recover noMiss noTarg"),
        ("Synthesis",0,100,5,2,0,3,0,"The user takes in sunlight to restore HP.\nRestores more HP in harsh sunlight, less in non-sunny, non-clear weather.","heals synthesis noMiss noTarg"),
        ("Aqua Ring",0,100,20,2,0,2,0,"The user envelops itself with a veil of healing waters.","aquaring noMiss noTarg"),
         #stat(istic) changes
        ("Harden",0,100,40,2,0,0,0,"The user stiffens the muscles in its body!\nRaises Def. 1 stage.","stat self,de,1 noMiss noTarg"),
        ("Defense Curl",0,100,40,2,0,0,0,"The user curls up to hide its weak spots!\nRaises Def. 1 stage.","stat self,de,1 noMiss curled noTarg"),
        ("Swords Dance",0,100,20,2,0,0,0,"Boosts Atk. 2 stages.","stat self,at,2 noMiss noTarg"),
        ("Nasty Plot",0,100,20,2,0,15,0,"Boosts SpA. 2 stages.","stat self,sa,2 noMiss noTarg"),
        ("Amnesia",0,100,20,2,0,10,0,"The user empties its mind and forgets its concerns.\nBoosts SpD. 2 stages.","stat self,sd,2 noMiss noTarg"),
        ("Dragon Dance",0,100,20,2,0,14,0,"Boosts Atk. and Sp. 1 stage each.","stat self,at:sp,1:1 noMiss noTarg"),
        ("Growth",0,100,20,2,0,0,0,"The user's body grows all at once!\nBoosts Atk. and Sp.A 1 stage each. Two each in harsh sunlight.","stat self,at:sa,1:1 noMiss growth noTarg"),
        ("Geomancy",0,100,10,2,0,17,0,"The user absorbs energy from its surroundings to power up!\nBoosts Sp.A Sp.D Spe. 2 stages each.\nTwo-turn move.","stat self,sa:sd:sp,2:2:2 noMiss 2turn geomance noTarg"),
        ("Double Team",0,100,15,2,0,0,0,"The user moves so quick it creates afterimages.\nRaises evasiveness 1 stage.","stat self,ev,1 noMiss noTarg"),
        ("Confide",0,100,20,2,0,0,0,"The user tells the target a (quite inappropriate) secret.\nIt lowers the target's Sp.A 1 stage.","stat targ,sa,-1 noMiss"),
        ("String Shot",0,95,40,2,0,11,0,"The user spins silk to bind the target! Lowers target's Spd. 1 stage.","stat targ,sp,-1"),
        ("Growl",0,100,40,2,0,0,0,"The user growls cutely.\nIt lowers the target's Atk. 1 stage.","stat targ,at,-1"),
        ("Metal Sound",0,85,40,2,0,16,0,"The user creates horrible metal-scraping sounds to unnerve the target.\nLowers target's Sp.D 2 stages.","stat targ,sd,-2"), #sound-based, soundproof ability is immune,
         #stat(us) conditions
        ("Stun Spore",0,75,30,2,0,3,0,"The user releases spores that paralyze the target!","para 100 typeImmune grass"), #typeImmune for poke types with immunities
        ("Sleep Powder",0,75,15,2,0,3,0,"The user uses a powder to lull the target to sleep!","sleep 100 typeImmune grass"),
        ("Poison Powder",0,75,35,2,0,7,0,"The user creates a powder to poison the target!","pois 100 typeImmune grass"),
        ("Toxic",0,90,10,2,0,7,0,"The user badly poisons the target!","badPois 100 noMissPoisons"), #doesn't miss if used by a poison-type
        ("Confuse Ray",0,100,10,2,0,13,0,"The user lets loose a sinister beam that causes confusion!","conf 100"),
        #to do: max moves! terrain pulse
        ("Struggle",50,100,1,0,1,18,0,"The user is otherwise out of moves.","noMiss recoil 1/4maxhp")
        ]
#constructing dtypes and names to accompany data
#labels = np.dtype( [('name','U25'),('pwr','i4'),('accu','i4'),('pp','i4'),('special?','i4'),('contact?','i4'),('type','i4'),('desc','U140'),('notes','U140')] )
#for when i'm ready for priority
labels = np.dtype( [('name','U25'),('pwr','i4'),('accu','i4'),('pp','i4'),('special?','i4'),('contact?','i4'),('type','i4'),('priority','i4'),('desc','U140'),('notes','U140')] )
#creating structed arrays
mov = np.array(moremoves, dtype=labels)
#new dtype to add the index column and priority 
new_dt = np.dtype( [('index','i4')] + mov.dtype.descr)
#print(len(mov.dtype.descr))
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
#find future sight
ind2 = np.argwhere(mov["name"]=="Future Sight")
futuresigh=int(mov[ind2]["index"])
tackl = int(mov[int(np.argwhere(mov["name"]=="Tackle"))]["index"])
#save the table, especially for readability
mov.tofile('movedex.txt', sep='\n')
with open('movedex.txt', 'a') as ofile:
    ofile.write('\n')
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
if __name__ == "__main__":
    np.save("saved_movedex.npy",mov)
else:
    pass

