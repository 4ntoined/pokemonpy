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
        ("V-create",180,95,5,0,1,1,0,"The user ignites its forehead and hurls itself at the target!\n-Lowers the user's Def. Sp.D and Spe. 1 stage each.","stat self,de:sd:sp,-1:-1:-1,100"),

        ("Prismatic Laser",160,100,10,1,0,10,0,"The user attacks the target with lasers using the power of a prism!\n-The user must rest on the next turn.","mustRest"),
        ("Eternabeam",160,90,5,1,0,14,0,"The user harnesses Dynamax energy and releases it in a beam!\n-The user must rest on the next turn.","mustRest"),
        
        ("Hyper Beam",150,90,5,1,0,0,0,"The user attacks with a powerful beam!\n-The user must rest on next turn.","mustRest"),
        ("Giga Impact",150,90,5,0,1,0,0,"The user charges at the target using every bit of its power!\n-The user must rest on next turn.","mustRest"),
        ("Blast Burn",150,90,5,1,0,1,0,"The user razes the target with a fiery explosion!\n-The user must rest on next turn.","mustRest"),
        ("Eruption",1,100,5,1,0,1,0,"The user attacks with explosive fury!\n-Power = 150 x userHP%.","spout"),
        ("Hydro Cannon",150,90,5,1,0,2,0,"The user attacks the target with a watery blast!\n-The user must rest on next turn.","mustRest"),
        ("Water Spout",1,100,5,1,0,2,0,"The user spouts water to damage the target!\n-Power = 150 x userHP%.","spout"), #'spout' = this, eruption, drag energy
        ("Frenzy Plant",150,90,5,1,0,3,0,"The user slams the target with roots from an enormous tree!\n-The user must rest on next turn.","mustRest"),
        ("Chloroblast",150,95,5,1,0,3,0,"The user amasses chlorophyll and launches it at the target!\n-The user loses half of its max HP to recoil damage.","recoil 1/2maxhp"),
        ("Meteor Assault",150,100,5,0,0,6,0,"The user attacks wildly with its thick leek!\n-The user must rest on next turn.","mustRest"),
        ("Rock Wrecker",150,90,5,0,0,12,0,"The user launches a huge boulder at the target!\n-The user must rest on next turn.\n-Bomb/ball move.","mustRest bullet"), #bulletproof ability is immune
        ("Head Smash",150,80,5,0,1,12,0,"The user attacks the target with a full-power headbutt!\n-The user takes 1/2 recoil damage.","recoil 1/2"),
        ("Roar of Time",150,90,5,1,0,14,0,"The user shouts a roar that distorts time and inflicts chronological damage on the target!\n-The user must rest on next turn.","mustRest"),
        ("Dragon Energy",1,100,5,1,0,14,0,"The user attacks by converting its life-force into power!\n-Power = 150 x userHP%.","spout"),

        ("Boomburst",       140,100,10,1,0,0,0,"The user attacks with a terrible, explosive sound!\n-Sound-based move.","sound"), #sound move
        ("Freeze Shock",    140,90,5,0,0,5,0,"On the next turn, the user hits the target with electrically charged ice!\n-Two-turn move.\n-30% chance to paralyze.","2turn para 30"),
        ("Ice Burn",        140,90,5,1,0,5,0,"On the next turn, the user surrounds the target withan ultra-cold, freezing wind!\n-Two-turn move.\n-30% chance to burn.","2turn burn 30"),
        ("Psycho Boost",    140,90,5,1,0,10,0,"The user attacks with all its might!\n-Lowers the user's Sp.A 2 stages.","stat self,sa,-2,100"),

        ("Skull Bash",      130,100,10,0,1,0,0,"The user tucks its head in and charges at the target!\n-Two-turn move.\n-Raises the user's Def. 1 stage on the first turn.","2turn skullbash"), #needs to raise defense 1 stage on the prep
        ("Overheat",        130,90,5,1,0,1,0,"The user attacks with its full power!\n-Lowers the user's Sp.A 2 stages.","stat self,sa,-2,100"),
        ("Blue Flare",      130,85,5,1,0,1,0,"The user engulfs the target in an beautiful, intense blue flame!\n-20% chance to burn.","burn 20"),
        ("Leaf Storm",      130,90,5,1,0,3,0,"The user whips up a storm of leaves around the target!\n-Lowers the user's Sp.A 2 stages.",'stat self,sa,-2,100'),
        ("Bolt Strike",     130,85,5,0,1,4,0,"The user surrounds itself with electricity and charges the target!\n-20% chance to paralyze.","para 20"),
        ("Electro Shot",    130,100,10,1,0,4,0,"The user gathers electricity on the first turn and fires a high-voltage shot on the next!\n-Two-turn move.\n-Raises the user's Sp.A 1 stage on the first turn.\n-Skips the charging turn in rain.","electroshot 2turn"),
        ("Draco Meteor",    130,90,5,1,0,14,0,"The user calls upon its draconic heritage and unleashes a storm of meteors!\n-Lowers the user's Sp.A 2 stages.","stat self,sa,-2,100"),

        ("Solar Blade", 125,100,10,0,1,3,0,"The user focuses sunlight into a blade to attack!\n-Two-turn move.\n-Skips the charging turn in harsh sunlight.\n-Power is halved in rain, sandstorm, hail.","2turn solar"),

        #("Tera Starstorm",120,100,5,1,0,0,0,"The user bombards the target with the power of its crystals... \nand eliminates them.","null"),
        ("Double-Edge", 120,100,15,0,1,0,0,"The user rushes the target with a reckless tackle!\n-The user takes 1/3 recoil damage.","recoil 1/3"),
        ("Head Charge", 120,100,15,0,1,0,0,"The user charges with its head and powerful guard hair!\n-The user takes 1/4 recoil damage.","recoil 1/4"),
        ("Mega Kick",   120,75,5,0,1,0,0,"The user launches a kick with muscle-packed power!","null"),
        ("Crush Grip",  1,100,5,0,1,0,0,"The user crushes the target with great force!\n-Power = 120 x targetHP%","crushgrip"),
        ("Multi-Attack [Normal]",   120,100,10,0,1,0,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Normal Memory.","null"),
        ("Multi-Attack [Fire]",     120,100,10,0,1,1,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Fire Memory.","null"),
        ("Multi-Attack [Water]",    120,100,10,0,1,2,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Water Memory.","null"),
        ("Multi-Attack [Grass]",    120,100,10,0,1,3,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Grass Memory.","null"),
        ("Multi-Attack [Electric]", 120,100,10,0,1,4,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Electric Memory.","null"),
        ("Multi-Attack [Ice]",      120,100,10,0,1,5,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Ice Memory.","null"),
        ("Multi-Attack [Fighting]", 120,100,10,0,1,6,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Fighting Memory.","null"),
        ("Multi-Attack [Poison]",   120,100,10,0,1,7,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Poison Memory.","null"),
        ("Multi-Attack [Ground]",   120,100,10,0,1,8,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Ground Memory.","null"),
        ("Multi-Attack [Flying]",   120,100,10,0,1,9,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Flying Memory.","null"),
        ("Multi-Attack [Psychic]",  120,100,10,0,1,10,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Psychic Memory.","null"),
        ("Multi-Attack [Bug]",      120,100,10,0,1,11,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Bug Memory.","null"),
        ("Multi-Attack [Rock]",     120,100,10,0,1,12,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Rock Memory.","null"),
        ("Multi-Attack [Ghost]",    120,100,10,0,1,13,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Ghost Memory.","null"),
        ("Multi-Attack [Dragon]",   120,100,10,0,1,14,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Dragon Memory.","null"),
        ("Multi-Attack [Dark]",     120,100,10,0,1,15,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Dark Memory.","null"),
        ("Multi-Attack [Steel]",    120,100,10,0,1,16,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Steel Memory.","null"),
        ("Multi-Attack [Fairy]",    120,100,10,0,1,17,0,"The user cloaks itself in powerful energy and slams into the target!\n-Holding the Fairy Memory.","null"),
        ("Techno Blast [Normal]",   120,100,5,1,0,0,0,"The user fires a beam of light at its target!\n-Not holding a drive.","null"),
        ("Techno Blast [Fire]",     120,100,5,1,0,1,0,"The user fires a beam of light at its target!\n-Holding the Burn drive.","null"),
        ("Techno Blast [Water]",    120,100,5,1,0,2,0,"The user fires a beam of light at its target!\n-Holding the Douse drive.","null"),
        ("Techno Blast [Electric]", 120,100,5,1,0,4,0,"The user fires a beam of light at its target!\n-Holding the Shock drive.","null"),
        ("Techno Blast [Ice]",      120,100,5,1,0,5,0,"The user fires a beam of light at its target!\n-Holding the Chill drive.","null"),
        ("Armor Cannon",        120,100,5,1,0,1,0,"The user shoots its own armor out as blazing projectiles!\n-Lowers the user's Def. Sp.D 1 stage each.","stat self,de:sd,-1:-1,100"),
        ("Flare Blitz",         120,100,15,0,1,1,0,"The user cloaks itself in fire and charges the target!\n-The user takes 1/3 recoil damage.\n-10% chance to burn.\n-Thaws the user if frozen.","recoil 1/3 burn 10 thaws"),
        ("Pyro Ball",           120,90,5,0,0,1,0,"The user turns a small stone to a fiery meteor and launches it at the target!\n-10% chance to burn.\n-Thaws the user if frozen.\n-Bomb/ball move.","burn 10 thaws bullet"),
        ("Wave Crash",          120,100,10,0,1,2,0,"The user summons a giant wave and crashes into the target!\n-The user takes 1/3 recoil damage.","recoil 1/3"),
        ("Wood Hammer",         120,100,15,0,1,3,0,"The user slams its rugged body into the target!\n-The user takes 1/3 recoil damage.","recoil 1/3"),
        ("Seed Flare",          120,85,5,1,0,3,0,"The user emits a shockwave from its body to attack the target!\n-40% chance to lower the target's Sp.D 2 stages.","stat targ,sd,-2,40"),
        ("Solar Beam",          120,100,10,1,0,3,0,"The user focuses sunlight into a beam to attack!\n-Two-turn move.\n-Skips the charging turn in harsh sunlight.\n-Power is halved in rain, sandstorm, hail.","2turn solar"),
        ("Volt Tackle",         120,100,15,0,1,4,0,"The user electrifies itself and charges the target!\n-The user takes 1/3 recoil damage.\n-10% chance to paralyze.","recoil 1/3 para 10"),
        ("Zap Cannon",          120,50,5,1,0,4,0,"The user fires an eletric blast like a cannon!\n-100% chance to paralyze.\n-Ball/bomb move.","para 100 bullet"),
        ("Close Combat",        120,100,5,0,1,6,0,"The user drops their guard to achieve an all out attack!\n-Lowers the user's Def. Sp.D 1 stage each.","stat self,de:sd,-1:-1,100"),
        ("Superpower",          120,100,15,0,1,6,0,"The user draws on its latent potential and attacks the target with great power!\n-Lowers the user's Atk. Def. 1 stage each.","stat self,at:de,-1:-1,100"),
        ("Focus Blast",         120,70,5,1,0,6,0,"The user heightens its mental focus an unleashs its power!\n-10% chance to lower the target's Sp.D 1 stage.\n-Bomb/ball move.","stat targ,sa,-1,10 bullet"),
        ("Precipice Blades",    120,85,10,0,0,8,0,"The user manifests the power of the land and attacks the target with fearsome blades of stone!","null"),
        ("Brave Bird",          120,100,15,0,1,9,0,"The user tucks in its wings and charges at a low altitude!\n-The user takes 1/3 recoil damage.","recoil 1/3"),
        ("Dragon Ascent",       120,100,5,0,1,9,0,"The user attacks by dropping out of the sky at high speed!\n-Lowers the user's Def. Sp.D 1 stage each.","stat self,de:sd,-1:-1,100"),
        ("Future Sight",        120,100,5,1,0,10,0,"The user looks into the future and predicts an attack!\n-The opponent is attacked two turns later, at the end of the turn.","futuresight"),
        ("Megahorn",            120,85,10,0,1,11,0,"The user rams into the target with its tough and impressive horn!","null"),
        ("Headlong Rush",       120,100,5,0,1,12,0,"The user smashes into the target in a full-body tackle!\n-Lowers the user's Def. Sp.D 1 stage each.","stat self,de:sd,-1:-1,100"),
        ("Shadow Force",        120,100,5,0,1,13,0,"The user disappears into the dark and strikes the target on the next turn!\n-Two turn move.","shadowforce 2turn semi-invul"),
        ("Dragon Fist",         120,100,5,0,1,14,0,"If the user doesn't do it, who will?\n-Raises the user's Spe. 1 stage.\n-Lowers the user's Def. 2 stages, Sp.D 1 stage.","stat self,de:sd:sp,-2:-1:1,100"),
        ("Make It Rain",        120,100,5,1,0,16,0,"The user throws a mass of gold coins at the target!\n-Lowers the user's Sp.A 1 stage.","stat self,sa,-1,100"),

        ("Fire Blast",      110,85,5,1,0,1,0,"The user attacks with a blast of all-consuming flames!\n-10% chance to burn.","burn 10"),
        ("Origin Pulse",    110,85,10,1,0,2,0,"The user attacks the target with countless beams of glowing blue light!\n-Pulse move.","pulse"), #pulse = powered by mega-launcher
        ("Hydro Pump",      110,80,5,1,0,2,0,"The user blasts the target with a huge volume of water under great pressure!","null"),
        ("Steam Eruption",  110,95,5,1,0,2,0,"The user immerses the target in a superheated steam!\n-30% chance to burn.\n-Thaws a frozen user or target.","burn 30 thaws thawsTarg scald"), #scald for non-fire hot moves (they thaw a frozen target)
        ("Thunder",         110,70,10,1,0,4,0,"The user drops a wicked lightningbolt on the target to inflict damage!\n-30% chance to paralyze.\n-Bypasses accuracy check in rain.","para 30 noMissRain thunder"),
        ("Blizzard",        110,70,5,1,0,5,0,"The user summons a howling blizzard to strike the target!\n-10% chance to freeze.\n-Bypasses accuracy check in hail.","frze 10 blizzard"), #doesn't miss in hail, need to program
        ("Hurricane",       110,70,10,1,0,9,0,"The user wraps its target in a fierce wind from a furious storm!\n-30% chance to confuse.\n-Bypasses accuracy check in rain.","conf 30 noMissRain thunder"),
        ("Clanging Scales", 110,100,5,1,0,14,0,"The user rubs the scales on its body and makes a huge noise to inflict damage on the target!\n-Lowers the user's Def. 1 stage.\n-Sound-based move.","stat self,de,-1,100 sound"),
        #normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
        #ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,
        #dark 15,steel 16,fairy 17
        ("Judgement [Normal]",      100,100,10,1,0,0,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Blank Plate.","null"),
        ("Judgement [Fire]",        100,100,10,1,0,1,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Flame Plate.","null"),
        ("Judgement [Water]",       100,100,10,1,0,2,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Splash Plate.","null"),
        ("Judgement [Grass]",       100,100,10,1,0,3,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Meadow Plate.","null"),
        ("Judgement [Electric]",    100,100,10,1,0,4,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Zap Plate.","null"),
        ("Judgement [Ice]",         100,100,10,1,0,5,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Icicle Plate.","null"),
        ("Judgement [Fighting]",    100,100,10,1,0,6,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Fist Plate.","null"),
        ("Judgement [Poison]",      100,100,10,1,0,7,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Toxic Plate.","null"),
        ("Judgement [Ground]",      100,100,10,1,0,8,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Earth Plate.","null"),
        ("Judgement [Flying]",      100,100,10,1,0,9,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Sky Plate.","null"),
        ("Judgement [Psychic]",     100,100,10,1,0,10,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Mind Plate.","null"),
        ("Judgement [Bug]",         100,100,10,1,0,11,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Insect Plate.","null"),
        ("Judgement [Rock]",        100,100,10,1,0,12,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Stone Plate.","null"),
        ("Judgement [Ghost]",       100,100,10,1,0,13,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Spooky Plate.","null"),
        ("Judgement [Dragon]",      100,100,10,1,0,14,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Draco Plate.","null"),
        ("Judgement [Dark]",        100,100,10,1,0,15,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Dread Plate.","null"),
        ("Judgement [Steel]",       100,100,10,1,0,16,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Iron Plate.","null"),
        ("Judgement [Fairy]",       100,100,10,1,0,17,0,"The user pelts the battlefield with bolts of light from the sky!\n-Holding the Pixie Plate.","null"),
        ("Ivy Cudgel [Fire]",       100,100,10,0,0,1,0,"The user strikes the target with a thorny ivy-wrapped cudgel!\n-Increased crit' ratio.\n-Holding the Hearthflame Mask.","highCrit"),
        ("Ivy Cudgel [Water]",      100,100,10,0,0,2,0,"The user strikes the target with a thorny ivy-wrapped cudgel!\n-Increased crit' ratio.\n-Holding the Wellspring Mask.","highCrit"),
        ("Ivy Cudgel [Grass]",      100,100,10,0,0,3,0,"The user strikes the target with a thorny ivy-wrapped cudgel!\n-Increased crit' ratio.\n-Holding the Teal Mask.","highCrit"),
        ("Ivy Cudgel [Rock]",       100,100,10,0,0,12,0,"The user strikes the target with a thorny ivy-wrapped cudgel!\n-Increased crit' ratio.\n-Holding the Cornerstone Mask.","highCrit"),
        ("Fusion Flare",        100,100,5,1,0,1,0,"The user throws down a giant flame!\n-Doubles in power if used after Fusion Bolt.\n-Thaws a frozen user.","fusion-f thaws"),
        ("Sacred Fire",         100,95,5,1,0,1,0,"The user razes the target with a mystical fire of great intensity!\n-50% chance to burn the target.\n-Thaws a frozen user.","thaws burn 50"),
        ("Crabhammer",          100,90,10,0,1,2,0,"The target is hammered with a large pincer!\n-Increased crit' ratio.","highCrit"),
        ("Fusion Bolt",         100,100,5,0,0,4,0,"The user throws down a giant lightning bolt!\n-Doubles in power if used after Fusion Flare.","fusion-b"),
        ("Wildbolt Storm",      100,80,10,1,0,4,0,"The user summons a thunderous tempest and savagely attacks the target with lightning and wind!\n-20% chance to paralyze.\n-Bypasses accuracy check in rain.","para 20 noMissRain"),
        ("Electro Drift",       100,100,5,1,1,4,0,"The user races forward at ultrafast speeds and pierces its target with futuristic electricity!\n-Damage boosted by 33.33% if it's a super-effective hit.","collision"), #collision for the 'raidon signature moves
        ("Mountain Gale",       100,85,10,0,0,5,0,"The user hurls giant chunks of ice at the target!\n-30% chance to make the target flinch.","flinch 30"),
        ("Collision Course",    100,100,5,0,1,6,0,"The user transforms and crashes into the ground with a massive prehistoric explosion!\n-Damage boosted by 33.33% if it's a super-effective hit.","collision"), #collision for the 'raidon signature moves
        ("Malignant Chain",     100,100,5,1,0,7,0,"The user wraps the target in a corrosive chain and pours toxins into them!\n-50% chance to badly poison.","badPois 50"),
        ("Earthquake",          100,100,10,0,0,8,0,"The user causes a powerful earthquake!\n-Power is halved if used on Grassy Terrain.","nerfGrassy"), #one day we'll generalize moves having their power nerfed under certain conditions....not today tho
        ("Sandsear Storm",      100,80,10,1,0,8,0,"The user wraps the target in fierce winds and searlingly hot sand!\n-20% chance burn.\n-Bypasses accuracy check in rain.","burn 20 noMissRain"),
        ("Aeroblast",           100,95,5,1,0,9,0,"The user shoots a vortex of air at the target!\n-Increased crit. ratio.","highCrit"),
        ("Bleakwind Storm",     100,80,10,1,0,9,0,"The user attacks with savagely cold winds that cause both body and spirit to tremble!\n-30% chance to lower the target's Spe. 1 stage.\n-Bypasses accuracy check in rain.","stat targ,sp,-1,30 noMissRain"),
        ("Psystrike",           100,100,10,1,0,10,0,"The user materializes an odd psychic wave to attack!\n-Damage is calculated with the user's Sp.A and the target's Def.","psystrike"), #will use psystrike tag for psyshock and secret sword
        ("Stone Edge",          100,80,5,0,0,12,0,"The user stabs the target from below with sharpened stones!\n-Increased crit' ratio.","highCrit"),
        ("Diamond Storm",       100,95,5,0,0,12,0,"The user whips up a storm of diamonds to damage the target!\n-50% chance to raise the user's Def. 2 stages.","stat self,de,2,50"),
        ("Moongeist Beam",      100,100,5,1,0,13,0,"The user attacks the target by emitting a sinister ray!\n-Ignores the target's ability.","moldbreaker"), #'moldbreaker' moves ignore abilities
        ("Core Enforcer",       100,100,10,1,0,14,0,"The user unleashes a super sick laser and draws a 'Z'!","null"), #otherwise would suppress abilities, but we have none
        ("Spacial Rend",        100,95,5,1,0,14,0,"The user tears the fabric of space around the target!\n-Increased crit' ratio.","highCrit"),
        ("Dynamax Cannon",      100,100,5,1,0,14,0,"The user condenses energy within its body and unleashes it at the target!","null"),
        ("Hyperspace Fury",     100,100,5,0,0,15,0,"The user unleashes a barrage of attacks using its many arms!\n-Bypasses accuracy checks.\n-Lowers the user's Def. 1 stage.","breaksProtect noMiss stat self,de,-1,100"),
        ("Sunsteel Strike",     100,100,5,0,1,16,0,"The user slams into the target with the force of a meteor!\n-Ignores the target's ability.","moldbreaker"), #'moldbreaker' moves ignore abilities
        ("Behemoth Blade",      100,100,5,0,1,16,0,"The user wields a large, powerful sword and cuts the target with a vigorous slash!","null"),
        ("Behemoth Bash",       100,100,5,0,1,16,0,"The user's body becomes a firm shield, and it slams into the target fiercely!","null"),
        ("Iron Tail",           100,75,15,0,1,16,0,"The user slams the target with a steel-hard tail!\n-30% chance to lower target's Def. 1 stage.","stat targ,de,-1,30"),
        ("Spin Out",            100,100,5,0,1,16,0,"The user spins furiously by straining its legs!\n-Lowers the user's Spe. 2 stages.","stat self,sp,-2,100"),
        ("Springtide Storm",    100,80,10,1,0,17,0,"The user wraps the target in fierce winds brimming with love and hate!\n-30% chance to lower the target's Atk. 1 stage.","stat targ,at,-1,30"),

        ("Heat Wave",   95,90,10,1,0,1,0,"The user exhales hot breath on the target!\n-10% chance to burn.","burn 10"),
        ("Moonblast",   95,100,15,1,0,17,0,"The user calls on the power of the Moon to attack the target!\n-30% chance to lower the target's Sp.A 1 stage.","stat targ,sa,-1,30"),
        
        ("Revelation Dance",90,100,15,1,0,0,0,"The user attacks the target by dancing with all its might!\n-Changes type to match the user's primary type.","revelation dance"), #dance moves activate the dancer ability
        #("Revelation Dance",90,100,15,1,0,1,0,"The user attacks the target by dancing with all its might!\n-This is the Fire-type version.","null"),
        #("Revelation Dance",90,100,15,1,0,4,0,"The user attacks the target by dancing with all its might!\n-This is the Electric-type version.","null"),
        #("Revelation Dance",90,100,15,1,0,10,0,"The user attacks the target by dancing with all its might!\n-This is the Psychic-type version.","null"),
        #("Revelation Dance",90,100,15,1,0,13,0,"The user attacks the target by dancing with all its might!\n-This is the Ghost-type version.","null"),
        ("Flamethrower",    90,100,15,1,0,1,0,"The user attacks with a powerful flame!\n-10% chance to burn.","burn 10"),
        ("Surf",            90,100,15,1,0,2,0,"The user swamps everything around it with a giant wave!","surf"), #hits during dive
        ("Muddy Water",     90,85,10,1,0,2,0,"The user attacks by shooting muddy water at the target!\n-30% chance to lower the target's Accu. 1 stage.","stat targ,ac,-1,30"),
        ("Aqua Tail",       90,90,10,0,1,2,0,"The user swings its tail like a vicious wave in a raging storm!","null"),
        ("Leaf Blade",      90,100,15,0,1,3,0,"The user attacks with a sharpened leaf!\n-Increased crit' ratio.","highCrit"),
        ("Energy Ball",     90,100,10,1,0,3,0,"The user draws power from nature and fires it at the target!\n-10% chance to lower the target's Sp.D 1 stage.\n-Bomb/ball move.","stat targ,sd,-1,10 bullet"),
        ("Wild Charge",     90,100,15,0,1,4,0,"The user shrouds itself in electricity and smashes into the target!\n-The user takes 1/4 recoil damage.","recoil 1/4"),
        ("Thunderbolt",     90,100,15,1,0,4,0,"The user attacks with a bolt of lightning!\n-10% chance to paralyze.","para 10"),
        ("Ice Beam",        90,100,15,1,0,5,0,"The user focuses a stream of ice at the target!\n-10% chance to freeze.","frze 10"),
        ("Triple Arrows",   90,100,10,0,1,6,0,"The user kicks, then fires three arrows!\n-Increased crit' ratio.\n-50% chance to lower target's Def. 1 stage.\n-30% chance to make the target flinch.","highCrit flinch 30 stat targ,de,-1,50"),
        ("Sludge Bomb",     90,100,10,1,0,7,0,"The user hurls unsanitary sludge at the target!\n-30% chance to poison.\n-Ball/bomb move.","pois 30 bullet"),
        ("Earth Power",     90,100,10,1,0,8,0,"The user makes the ground under the target erupt with power!\n-10% chance to lower target's Sp.D 1 stage.","stat targ,sd,-1,10"),
        ("Thousand Arrows", 90,100,10,0,0,8,0,"The user creates arrows from the very ground and hurls them at the target!\n-Hits ungrounded targets and grounds them.","arrows"),
        ("Fly",             90,95,15,0,1,9,0,"The user flies up into the sky, then attacks on the next turn!\n-Vulnerable to Smack Down, Sky Uppercut, Thunder, Hurricane and double damage from Gust, Twister on the first turn.","2turn flying"),
        ("Psychic",         90,100,10,1,0,10,0,"The user hits the target with a strong telekinetic force!\n-10% chance to lower target's Sp.D 1 stage.","stat targ,sd,-1,10"),
        ("Mystical Power",  90,70,10,1,0,10,0,"The user attacks by emitting a mysterious power!\n-Raises the user's Sp.A 1 stage.","stat self,sa,+1,100"),
        ("Attack Order",    90,100,15,0,0,11,0,"The user calls on its underlings to pummel the target!\n-Increased crit' ratio.","highCrit"),
        ("First Impression",90,100,10,0,1,11,+2,"The user dashes forward and slashes at the target as soon as it gets the opportunity!\n-Priority +2.\n-Only works on the first turn after the user enters battle.","fakeout"),
        ("Phantom Force",   90,100,10,0,1,13,0,"The user vanishes into another plane, then strikes the target on the next turn!","2turn shadowforce"),
        ("Play Rough",      90,90,10,0,1,17,0,"The user attacks by playing rough with the target!\n-10% chance to lower the target's Atk. 1 stage.","stat targ,at,-1,10"),
        ("Strange Steam",   90,95,10,1,0,17,0,"The user mixes a special steam and shoots it at the target!\n-20% chance to confuse.","conf 20"),
        
        ("Blaze Kick",      85,90,10,0,1,1,0,"The user attacks with a fiery kick!\n-10% chance to burn.\n-Increased crit' ratio.","highCrit burn 10"),
        ("Kamehameha",      85,100,10,1,0,2,0,"The user concentrates their ki and releases it in a beam!\n-50% chance to lower the target's Def. 2 stages.","stat targ,de,-2,50"),
        ("Secret Sword",    85,100,10,1,0,6,0,"The user uses odd power to cut with its long horn!\n-Damage is calculated with the user's Sp.A and the target's Def.","psystrike"),
        ("Bounce",          85,85,5,0,1,9,0,"The user bounces up high on the first turn, then drops onto the target on the next turn!\n-Vulnerable to Smack Down, Sky Uppercut, Thunder, Hurricane and double damage from Gust, Twister on the first turn.","2turn flying para 30"),
        ("Dragon Pulse",    85,100,10,1,0,14,0,"The user summons a beastly beam from its mouth!\n-Pulse move.","pulse"),
        ("Kowtow Cleave",   85,100,10,0,1,15,0,"The user kowtows to make the target lower its guard... and then slashes at them!\n-Bypasses accuracy checks.","slicing noMiss"),

        ("Extreme Speed",   80,100,5,0,1,0,+2,"The user charges at the target with blinding speed!\n-Priority +2.","null"),
        ("Torch Song",      80,100,10,1,0,1,0,"The user breathes raging flames at the target like it's singing a song!\n-Raises the user's Sp.A 1 stage.\n-Sound-based move.","stat self,sa,1,100 sound"),
        ("Lava Plume",      80,100,15,1,0,1,0,"The user torches its surroundings with an inferno of flames!\n-30% chance to burn.","burn 30"),
        ("Fiery Dance",     80,100,10,1,0,1,0,"The user cloaks itself in flames and attacks the target by dancing and flapping its wings!\n-50% chance to raise the user's Sp.A 1 stage.","stat self,sa,1,50"),
        ("Fire Lash",       80,100,15,0,1,1,0,"The user strikes with a burning lash!\n-Lowers the target's Def. 1 stage.","stat targ,de,-1,100"),
        ("Hydro Steam",     80,100,15,1,0,2,0,"The user blasts the target with prehistoric, boiling-hot water!\n-50% boost in harsh sunlight, while also ignoring the usual Water-type nerf.","hydrosteam"),
        ("Dive",            80,100,10,0,1,2,0,"The user dives on the first turn, then resurfaces to attack on the next turn!\n-Double damage from Surf, Whirlpool on the first turn.","2turn diving"),
        ("Waterfall",       80,100,15,0,1,2,0,"The user charges at the target with a wall of water!\n-20% chance to make the target flinch.","flinch 20"),
        ("Aqua Step",       80,100,10,0,1,2,0,"The user attacks the target with light and fluid dance steps!\n-Raises the user's Spe. 1 stage.","stat self,sp,+1,100"),
        ("Scald",           80,100,15,1,0,2,0,"The user shoots boiling-hot water at the target!\n-30% chance to burn.\n-Thaws a frozen user or target.","burn 30 thaws thawsTarg scald"),
        ("Seed Bomb",       80,100,15,0,0,3,0,"The user attacks by pummeling the target with hard-shelled seeds!\n-Bomb/ball move.","bullet"),
        ("Drum Beating",    80,100,10,0,0,3,0,"The user plays its drum, controlling its roots to attack the target!\n-Lowers the target's Spe. 1 stage.","stat targ,sp,-1,100"),
        ("Zing Zap",        80,100,10,0,1,4,0,"The user crashes into the target, delivering a powerful electric shock!\n-30% chance to make the target flinch.","flinch 30"),
        ("Aura Sphere",     80,100,20,1,0,6,0,"The user looses a blast of aura from deep within its body!\n-Bypasses accuracy checks.\n-Bomb/ball move.\n-Pulse move.","noMiss bullet pulse"),
        ("Dig",             80,100,10,0,1,8,0,"The user burrows into the ground on the first turn, then attacks on the next turn!\n-Double damage from Earthquake, Magnitude, Fissure on the first turn.","2turn digging"),
        ("Zen Headbutt",    80,90,15,0,1,10,0,"The user focuses its willpower into its head and attacks the target!\n-20% chance to make the target flinch.","flinch 20"),
        ("Esper Wing",      80,100,10,1,0,10,0,"The user slashes the target with aura-enriched wings!\n-Raises the user's Spe. 1 stage.\n-Increased crit' ratio.","highCrit stat self,sp,1,100"),
        ("Psyshock",        80,100,10,1,0,10,0,"The user materializes an odd psychic wave to attack!\n-Damage is calculated with the user's Sp.A and the target's Def.","psystrike"),
        ("Psyblade",        80,100,15,0,1,10,0,"The user rends the target with a futuristic, ethereal blade!\n-50% boost on Electric Terrain.","psyblade slicing"), #slicing moves are boosted by sharpness
        ("Lumina Crash",    80,100,10,1,0,10,0,"The user attacks by unleashing a peculiar light that affects the mind!\n-Lowers the target's Sp.D 2 stages.","stat targ,sd,-2,100"),
        ("Hyperspace Hole", 80,100,5,1,0,10,0,"The user employs a hyperspace hole to appear right next to the target... and then strikes!\n-Bypasses accuracy checks.","breaksProtect noMiss"),
        ("X-Scissor",       80,100,15,0,1,11,0,"The user slashes the target by crossing its claws!","null"),
        ("Shadow Ball",     80,100,15,1,0,13,0,"The user hurls a shadowy blob at the target!\n-20% chance to lower the target's Sp.D 1 stage.\n-Ball/bomb move.","stat targ,sd,-1,20 bullet"),
        ("Dragon Claw",     80,100,15,0,1,14,0,"The user slashes the target with sharp claws!","null"),
        ("Fickle Beam",     80,100,5,1,0,14,0,"The user corrals its many heads to shoot beams of light at the target!\n-30% chance to double in power.","fickle"), #fickle, has a 30% chance to double in base power
        ("Crunch",          80,100,15,0,1,15,0,"The user crunches on the target with sharp fangs!\n-20% chance to lower the target's Def. 1 stage.","stat targ,de,-1,20"),
        ("Dark Pulse",      80,100,15,1,0,15,0,"The user releases a terrible aura imbued with dark thoughts!\n-20% chance to make the target flinch.\n-Pulse move.","flinch 20 pulse"),
        ("Flash Cannon",    80,100,10,1,0,16,0,"The user gathers all its light energy and releases it all at once at the target!\n-10% chance to lower target's Sp.D 1 stage.","stat targ,sd,-1,10"),
        
        ("Crush Claw",75,95,10,0,1,0,0,"The user slashes the target with hard, sharp claws!\n-50% chance to lower the target's Def. 1 stage.","stat targ,de,-1,50"), 
        ("Relic Song",  75,100,10,1,0,0,0,"The user sings an ancient song and attacks by appealing to the heart of the target!\n-10% chance to impose sleep.","sound sleep 10"),
        ("Mystical Fire",75,100,10,1,0,1,0,"The user attacks by breathing a special, hot fire!\n-Lowers the target's Sp.A 1 stage.","stat targ,sa,-1,100"),
        ("Fire Punch",75,100,15,0,1,1,0,"The user hits the target with a fiery punch!\n-10% chance to burn.","burn 10"),
        ("Brick Break",75,100,15,0,1,6,0,"The user attacks with a swift chop!\n-Removes Light Screen, Reflect, Aurora Veil from the opponent's side.","breakScreens"),
        ("Air Slash",75,95,15,1,0,9,0,"The user attacks with a blade of air that slices the sky!\n-30% chance to make the target flinch.","flinch 30"),
        ("Signal Beam",75,100,15,1,0,11,0,"The user attacks with an odd beam of light!\n-10% chance to confuse.","conf 10"),
        ("Bitter Malice",75,100,10,1,0,13,0,"The user attacks the target with spine-chilling resentment!\n-Lowers the target's Atk. 1 stage.","stat targ,at,-1,100"),
        
        #("Dizzy Punch",70,100,10,0,1,0,0,"","conf 20"), Why did dizzy punch get kicked out of the game :(
        ("Facade",          70,100,20,0,1,0,0,"An attack that does double damage if the user is poisoned, burned, or paralyzed.","facade"),
        ("Retaliate",       70,100,5,0,1,0,0,"The user gets revenge for a fainted ally!\n-Doubles in power if an ally fainted in the previous turn.","retaliate"),
        ("Headbutt",        70,100,15,0,1,0,0,"The user sticks out its head and attacks!\n-30% chance to make the target flinch.","flinch 30"),
        ("Aqua Cutter",     70,100,20,0,0,2,0,"The user expels pressurized water to cut the target like a blade!\n-Increased crit' ratio.","highCrit"),
        ("Trop Kick",       70,100,15,0,1,3,0,"The user lands an intense kick of tropical origins on the target!\n-Lowers the target's Atk. 1 stage.","stat targ,at,-1,100"),
        ("Flower Trick",    70,100,10,0,0,3,0,"The user throws a rigged bouquet of flowers at the target!\n-Bypasses accuracy check.\n-Always lands a critical hit.","noMiss frostbreath"),
        ("Scorching Sands", 70,100,10,1,0,8,0,"The user buries the target in searing-hot sand!\n-30% chance to burn the target.\n-Thaws the user if frozen.","burn 30 thaws thawsTarg scald"), #thawsTarg is brand new, i believe fire type moves thaw the target by default and this does that because its a hot/burning move but it is not Fire-type so I'll have to work that in gameside
        ("Shadow Claw",     70,100,15,0,1,13,0,"The user materializes a sharp claw from the shadows and slashes at the target!\n-Increased crit' ratio.","highCrit"),
        ("Night Slash",     70,100,15,0,1,15,0,"The user sneaks in and slashes the target the instant it gets the opportunity!\n-Increased crit' ratio.","highCrit"),
        
        ("Stomp",           65,100,20,0,1,0,0,"The user forcefully stomps on the target!\n-30% chance to make the target flinch.","flinch 30 noMissMinimize"), #doesn't miss if target used minimize
        ("Fire Fang",       65,95,15,0,1,1,0,"The user bites with flame-cloaked fangs!\n-10% chance to make the target flinch.\n-10% chance to burn.","burn 10 flinch 10"),
        ("Bubble Beam",     65,100,20,1,0,2,0,"The user forcefully ejects a spray of bubbles at the target!\n-10% chance to lower target's Spe. 1 stage.","stat targ,sp,-1,10"),
        ("Octazooka",       65,85,10,1,0,2,0,"The user sprays ink in the target's face!\n-50% chance to lower the target's Accu. 1 stage.\n-Bomb/ball move.","stat targ,ac,-1,50 bullet"), #bullet-move
        ("Thunder Fang",    65,95,15,0,1,4,0,"The user bites with electrified fangs!\n-10% chance to make the target flinch\n-10% chance to paralyze.","para 10 flinch 10"),
        ("Spark",           65,100,20,0,1,4,0,"The user attacks the target with an electrically charged tackle!\n-30% chance to paralyze.","para 30"),
        ("Ice Fang",        65,95,15,0,1,5,0,"The user bites with frozen fangs!\n-10% chance to make the target flinch.\n-10% chance to freeze.","frze 10 flinch 10"),
        ("Glaciate",        65,95,10,1,0,5,0,"The user blows freezing cold air at the target!\n-Lowers the target's Spe. 1 stage.","stat targ,sp,-1,100"),
        ("Hex",             65,100,10,1,0,13,0,"The user attacks relentlessly!\n-Doubles damage when the target has a status condition.","hex"),
        #("Ceaseless Edge",  65,90,15,0,1,15,0,"The user slashes its shell blade at the target!\n-Puts up Spikes on the target's side.","spikes"), #this might not work... i will have to see if we check for spikes tags in damaging moves
        
        ("Swift",           60,100,20,1,0,0,0,"The user shoots star-shaped rays at the target!\n-Bypasses accuracy checks.","noMiss"),
        ("Flame Wheel",     60,100,15,0,1,1,0,"The user covers itself in fire and rolls into the target!\n-10% chance to burn.\n-Thaws a frozen user.","burn 10 thaws"),
        ("Incinerate",      60,100,15,1,0,1,0,"The user attacks with a destructive fire!","null"),#no items to burn up rn
        ("Water Pulse",     60,100,20,1,0,2,0,"The user attacks the target with a pulsing blast of water!\n-20% chance to confuse.\n-Pulse move.","conf 20 pulse"),
        ("Jet Punch",       60,100,15,0,1,2,+1,"The user summons a torrent around its fist and punches at blinding speed.\n-Priority +1.","null"),
        ("Frost Breath",    60,90,10,1,0,5,0,"The user blows cold breath on the target!\n-Always lands a critical hit.","frostbreath"),
        ("Storm Throw",     60,100,10,0,1,6,0,"The user strikes the target with a fierce blow!\n-Always lands a critical hit.","frostbreath"),
        ("Air Cutter",      60,95,25,1,0,9,0,"The user launches razor-sharp winds to slash opponents!\n-Increased crit' ratio.","highCrit"),
        ("Aerial Ace",      60,100,20,0,1,9,0,"The user confounds the target with speed, then slashes!\n-Bypasses accuracy checks.","noMiss"),
        ("Silver Wind",     60,100,5,1,0,11,0,"The user attacks with powderly scales carried on the wind!\n-10% chance to raise all stats 1. stage each.","stat self,at:de:sa:sd:sp,1:1:1:1:1,10"), #not in SwSh, but IN LegendsArceus so we move!
        ("Ominous Wind",    60,100,5,1,0,13,0,"The user attacks with a mysterious wind!\n-10% chance to raise all stats 1 stage each.","stat self,at:de:sa:sd:sp,1:1:1:1:1,10"),
        ("Infernal Parade", 60,100,15,1,0,13,0,"The user attacks with a myriad of fireballs!\n-30% chance to burn.\n-Doubles damage when the target has a status condition.","hex burn 30"),
        #("Feint Attack",60,100,20,0,1,15,0,"",""), uhhh feint attack was nixed in gen 8, and i just programmed night slash so maybes thats a fine replacement?
        ("Bite",60,100,25,0,1,15,0,"The user bites the target with viciously sharp fangs!\n-30% chance to make the target flinch.","flinch 30"),
        
        ("Icy Wind",55,95,15,1,0,5,0,"The user attacks with a gust of chilled air!\n-Lowers the target's Spe. 1 stage.","stat targ,sp,-1,100"),
        ("Acrobatics",110,100,15,0,1,9,0,"The user nimbly strikes the target!","null"), #Im going to just double acrobatics' power bc its canon and we dont have items yet
        
        ("Weather Ball",    50,100,10,1,0,0,0,"The user harnesses the power of the weather to attack!\n-Changes type and doubles power in non-clear weather.\n-Ball/bomb move.","weatherball bullet"),
        ("Terrain Pulse",   50,100,10,1,0,0,0,"The user utilizes the energy of the terrain to attack!\n-Changes type and doubles power in terrain.\n-Pulse move.","terrainpulse pulse"),
        ("Cut",             50,95,30,0,1,0,0,"The user cuts the target with a scythe or claw!","null"),
        ("Flame Charge",    50,100,20,0,1,1,0,"The user cloaks itself in flames and builds momentum to attack!\n-Raises the user's Spe. 1 stage.","stat self,sp,1,100"),
        ("Chilling Water",  50,100,20,1,0,2,0,"The user attacks the target with water so cold it saps the target's power!\n-Lowers target's Atk. 1 stage.","stat targ,at,-1,100"),
        ("Poison Fang",     50,100,15,0,1,7,0,"The user bites the target with toxic fangs!\n-50% chance to badly poison.","badPois 50"),
        ("Metal Claw",      50,95,35,0,1,16,0,"The user rakes the target with steel claws!\n-10% chance to raise the user's Atk. 1 stage.","stat self,at,1,10"),
        
        ("Fake Out",    40,100,10,0,1,0,+3,"The user hits first and makes the target flinch!\n-Priority +3.\n-Only works on the first turn after the user enters battle.","flinch 100 fakeout"), #need priority AND first-turn tracking
        ("Quick Attack",40,100,30,0,1,0,+1,"The user lunges at the target so fast it becomes invisible!\n-Priority +1.","null"),
        ("Tackle",      40,100,35,0,1,0,0,"The user charges to attack!","null"),
        ("Ember",       40,100,25,1,0,1,0,"The user attacks with small flames!\n-10% chance to burn.","burn 10"),
        ("Aqua Jet",    40,100,20,0,1,2,+1,"The user covers itself in water and lunges at the target!\n-Priority +1.","null"),
        ("Ice Shard",   40,100,30,0,0,5,+1,"The user flash-freezes chunks of ice and hurls them at the target!\n-Priority +1.","null"),
        ("Vacuum Wave", 40,100,30,1,0,6,+1,"The user whirls its fists to send a wave of pure vacuum at the target!\n-Priority +1.","null"),
        ("Mach Punch",  40,100,30,0,1,6,+1,"The user throws a punch at blinding speed!\n-Priority +1.","null"),
        ("Gust",        40,100,35,1,0,9,0,"The user whips up a gust of wind with its wings and launches it at the target!","gust"),
        ("Accelerock",  40,100,20,0,1,12,+1,"The user smashes into the target at high speed!\n-Priority +1.","null"),
        ("Shadow Sneak",40,100,30,0,1,13,+1,"The user extends its shadow and attacks the target from behind!\n-Priority +1.","null"),
        ("Twister",     40,100,20,1,0,14,0,"The user whips up a vicious tornado to tear at the target!\n-20% chance to make the target flinch.","gust flinch 20"),
        ("Bullet Punch",40,100,30,0,1,16,+1,"The user strikes the taret with tough punches as fast as bullets!\n-Priority +1.","null"),

        ("Rollout",30,90,20,0,1,12,0,"The user rolls into the target for fives turns!\n-Doubles in damage for each consecutive hit.","rollout"),

        #z-moves,                power,accuracy,PP,phys/spec,contact,type,prority,flavor-text,tags
        #("Breakneak Blitz (P)"  ,200,100,1,0,1,0,0,"The user builds momentum using its Z-Power and crashes into the target at full speed!","zmove"),
        #("Breakneak Blitz (S)"  ,200,100,1,1,0,0,0,"The user builds momentum using its Z-Power and crashes into the target at full speed!","zmove"),
        #("Inferno Overdrive (P)",220,100,1,0,1,1,0,"The user breathes a stream of intense fire toward the target using its Z-Power!","zmove"),
        #("Inferno Overdrive (S)",200,100,1,1,0,1,0,"The user breathes a stream of intense fire toward the target using its Z-Power!","zmove"),
        #("Hydro Vortex (P)"     ,180,100,1,0,1,2,0,"The user swallows the target with a huge whirling current using its Z-Power!","zmove"),
        #("Hydro Vortex (S)"     ,200,100,1,1,0,2,0,"The user swallows the target with a huge whirling current using its Z-Power!","zmove"),
        #("Bloom Doom (P)"       ,190,100,1,0,1,3,0,"The user draws energy from the plants and attacks the target with full force using its Z-Power!","zmove"),
        #("Bloom Doom (S)"       ,200,100,1,1,0,3,0,"The user draws energy from the plants and attacks the target with full force using its Z-Power!","zmove"),
        #("Gigavolt Havoc (P)"   ,195,100,1,0,1,4,0,"The user hits the target with an electric current collected by its Z-Power!","zmove"),
        #("Gigavolt Havoc (S)"   ,190,100,1,1,0,4,0,"The user hits the target with an electric current collected by its Z-Power!","zmove"),
        #electric, ice, fighting, poison
        #("Subzero Slammer (P)"  ,200,100,1,0,1,5,0,"The user drops the temperature and freezes the target with its Z-Power!","zmove"),
        #("Subzero Slammer (S)"  ,200,100,1,1,0,5,0,"The user drops the temperature and freezes the target with its Z-Power!","zmove"),
        #("All-Out Pummeling (P)",200,100,1,0,1,5,0,"The user rams an energy orb created by its Z-Power into the target with full force!","zmove"),
        #("All-Out Pummeling (S)",190,100,1,1,0,5,0,"The user rams an energy orb created by its Z-Power into the target with full force!","zmove"),
        #("Acid Downpour (P)"    ,190,100,1,1,0,5,0,"The user sinks the target in a poisonous swamp with its Z-Power!","zmove"),
        #("Acid Downpour (S)"    ,190,100,1,1,0,5,0,"The user sinks the target in a poisonous swamp with its Z-Power!","zmove"),
        #ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,
        #dark 15,steel 16,fairy 17


        #max moves
        #("Max Strike (P)",150,100,3,0,1,0,0,"A Normal-type Dynamax move! Decreases the target's Spe. 1 stage.","maxmove stat targ,sp,-1,100"),
        #("Max Strike (S)",150,100,3,1,0,0,0,"A Normal-type Dynamax move! Decreases the target's Spe. 1 stage.","maxmove stat targ,sp,-1,100"),
        #("Max Flare (P)",150,100,3,0,1,1,0,"A Fire-type Dynamax move! Summons harsh sunlight for five turns.","maxmove sun"),
        #("Max Flare (S)",150,100,3,1,0,1,0,"A Fire-type Dynamax move! Summons harsh sunlight for five turns.","maxmove sun"),
        #("Max Geyser (P)",130,100,3,0,1,2,0,"A Water-type Dynamax move! Summons rain for five turns.","maxmove rain"),
        #("Max Geyser (S)",150,100,3,1,0,2,0,"A Water-type Dynamax move! Summons rain for five turns.","maxmove rain"),
        #("Max Overgrowth (P)",140,100,3,0,1,3,0,"A Grass-type Dynamax move! Sprouts grassy terrain for five turns.","maxmove grassy"),
        #("Max Overgrowth (S)",150,100,3,1,0,3,0,"A Grass-type Dynamax move! Sprouts grassy terrain for five turns.","maxmove grassy"),
        #electric, ice, fighting, poison
        #("Max Lightning (P)",140,100,3,0,1,4,0,"An Electric-type Dynamax move! Sparks electric terrain for five turns.","maxmove electric"),
        #("Max Lightning (S)",140,100,3,1,0,4,0,"An Electric-type Dynamax move! Sparks electric terrain for five turns.","maxmove electric"),
        #("Max Hailstorm (P)",140,100,3,0,1,5,0,"An Ice-type Dynamax move! Summons a hailstorm for five turns.","maxmove hail snow"),
        #("Max Hailstorm (S)",140,100,3,1,0,5,0,"An Ice-type Dynamax move! Summons a hailstorm for five turns.","maxmove hail snow"),
        #("Max Knuckle (P)",100,100,3,0,1,6,0,"A Fighting-type Dynamax move! Boosts user's Atk. 1 stage.","maxmove stat self,at,1,100"),
        #("Max Knuckle (S)",100,100,3,1,0,6,0,"A Fighting-type Dynamax move! Boosts user's Atk. 1 stage.","maxmove stat self,at,1,100"),
        #("Max Ooze (P)",95,100,3,0,1,7,0,"A Poison-type Dynamax move! Boosts user's Sp.A 1 stage.","maxmove stat self,sa,1,100"),
        #("Max Ooze (S)",95,100,3,1,0,7,0,"A Poison-type Dynamax move! Boosts user's Sp.A 1 stage.","maxmove stat self,sa,1,100"),
        #ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,
        #dark 15,steel 16,fairy 17
        #("Max Quake (P)",140,100,3,0,1,8,0,"A Ground-type Dynamax move! Boosts user's Def. 1 stage.","maxmove stat self,de,1,100"),
        #("Max Quake (S)",130,100,3,1,0,8,0,"A Ground-type Dynamax move! Boosts user's Def. 1 stage.","maxmove stat self,de,1,100"),
        #("Max Airstream (P)",140,100,3,0,1,9,0,"A Flying-type Dynamax move! Boosts user's Spe. 1 stage.","maxmove stat self,sp,1,100"),
        #("Max Airstream (S)",140,100,3,1,0,9,0,"A Flying-type Dynamax move! Boosts user's Spe. 1 stage.","maxmove stat self,sp,1,100"),
        #("Max Mindstorm (P)",130,100,3,0,1,10,0,"A Psychic-type Dynamax move! Weirdly causes psychic terrain for five turns.","maxmove psychic"),
        #("Max Mindstorm (S)",150,100,3,1,0,10,0,"A Psychic-type Dynamax move! Weirdly causes psychic terrain for five turns.","maxmove psychic"),
        #("Max Flutterby (P)",140,100,3,0,1,11,0,"A Bug-type Dynamax move! Lowers target's Sp.A 1 stage.","maxmove stat targ,sa,-1,100"),
        #("Max Flutterby (S)",130,100,3,1,0,11,0,"A Bug-type Dynamax move! Lowers target's Sp.A 1 stage.","maxmove stat targ,sa,-1,100"),
        #("Max Rockfall (P)",150,100,3,0,1,12,0,"A Rock-type Dynamax move! Summons a sandstorm for five turns.","maxmove sand"),
        #("Max Rockfall (S)",140,100,3,1,0,12,0,"A Rock-type Dynamax move! Summons a sandstorm for five turns.","maxmove sand"),
        #("Max Phantasm (P)",140,100,3,0,1,13,0,"A Ghost-type Dynamax move! Lowers target's Def. 1 stage.","maxmove stat targ,de,-1,100"),
        #("Max Phantasm (S)",140,100,3,1,0,13,0,"A Ghost-type Dynamax move! Lowers target's Def. 1 stage.","maxmove stat targ,de,-1,100"),
        #("Max Wyrmwind (P)",140,100,3,0,1,14,0,"A Dragon-type Dynamax move! Lowers target's Atk. 1 stage.","maxmove stat targ,at,-1,100"),
        #("Max Wyrmwind (S)",150,100,3,1,0,14,0,"A Dragon-type Dynamax move! Lowers target's Atk. 1 stage.","maxmove stat targ,at,-1,100"),
        #("Max Darkness (P)",130,100,3,0,1,15,0,"A Dark-type Dynamax move! Lowers target's Sp.D 1 stage.","maxmove stat targ,sd,-1,100"),
        #("Max Darkness (S)",130,100,3,1,0,15,0,"A Dark-type Dynamax move! Lowers target's Sp.D 1 stage.","maxmove stat targ,sd,-1,100"),
        #("Max Steelspike (P)",140,100,3,0,1,16,0,"A Steel-type Dynamax move! Boosts user's Def. 1 stage.","maxmove stat self,de,1,100"),
        #("Max Steelspike (S)",140,100,3,1,0,16,0,"A Steel-type Dynamax move! Boosts user's Def. 1 stage.","maxmove stat self,de,1,100"),
        #("Max Starfall (P)",130,100,3,0,1,17,0,"A Fairy-type Dynamax move! Mystifies a misty terrain for five turns.","maxmove misty"),
        #("Max Starfall (S)",140,100,3,1,0,17,0,"A Fairy-type Dynamax move! Mystifies a misty terrain for five turns.","maxmove misty"),
        #("Max Guard",0,100,3,1,0,10,0," ","maxmove guard? protect? noMiss?noTarg?"),


        # half remaining hp moves
        ("Super Fang",          1,90,10,0,1,0,0,"The user chomps hard on the target with its sharp fangs!\n-Does damage equal to half of the target's remaining HP.","ruination"),
        ("Ruination",           1,90,10,1,0,15,0,"The user summons a disaster that leaves the target in ruins!\n-Does damage equal to half of the target's remaining HP.","ruination"),
        ("Nature's Madness",    1,90,10,1,0,17,0,"The user hits the target with the full wrath of nature!\n-Does damage equal to half of the target's remaining HP.","ruination"),
        #counter and mirror coat,
        ("Counter",     1,100,20,0,1,6,-5,"An attack for countering any physical move.\n-Inflicts on the target double the damage taken by the user.","counter"),
        ("Mirror Coat", 1,100,20,1,0,10,-5,"An attack for countering any special move.\n-Inflicts on the target double the damage taken by the user.","mirrorcoat"),#]
#moves22 = [
        #status moves
         #weather moves
        ("Sunny Day",  0,100,5,2,0,1,0,"The user calls on the Sun and causes harsh sunlight!","sun noMiss noTarg"),
        ("Rain Dance", 0,100,5,2,0,2,0,"The user disrupts the air pressure and causes rain!","rain noMiss noTarg"),
        ("Hail",       0,100,5,2,0,5,0,"The user summons a cloudy cold front and creates a hailstorm!","hail noMiss noTarg"),
        #("Snowscape", 0,100,5,2,0,5,0,"The user summons a cloudy cold front that produces snow!","snow noMiss noTarg"),
        ("Sandstorm",  0,100,5,2,0,12,0,"The user calls on the local sands to whip up a sandstorm!","sand noMiss noTarg"),
         #terrain moves
        ("Grassy Terrain",   0,100,10,2,0,3,0,"The user covers the battlefield with grass for 5 turns!\n-Grass-type moves from grounded Pokémon get a 30% damage boost.\n-Grounded Pokémon heal 1/16 of their max HP each turn.\n-Bulldoze, Earthquake, Magnitude are halved in power.","grassy noMiss noTarg"),
        ("Electric Terrain", 0,100,10,2,0,4,0,"The user electrifies the battlefield for 5 turns!\n-Electric-type moves from grounded Pokémon get a 30% damage boost.\n-Grounded Pokémon cannot be put to sleep.","electric noMiss noTarg"),
        ("Psychic Terrain",  0,100,10,2,0,10,0,"The user makes the battlefield weird for 5 turns!\n-Psychic-type moves from grounded Pokémon get a 30% damage boost.\n-Grounded Pokémon cannot be hit by priority moves.","psychic noMiss noTarg"),
        ("Misty Terrain",    0,100,10,2,0,17,0,"The user covers the battlefield in mist for 5 turns!\n-Dragon-type moves targeting grounded Pokémon get a 50% damage nerf.\n-Grounded Pokémon cannot be afflicted with status conditions.","misty noMiss noTarg"),
         #entry hazards
        ("Toxic Spikes",  0,100,20,2,0,7,0,"The user sends out toxic barbs on the target's side of the field!\n-Grounded Pokémon are poisoned upon entry.\n-Stacks up to 2 times for bad poison.\n-Grounded Poison-type Pokémon will absorb already placed Toxic Spikes.","noMiss toxspk noTarg"),
        ("Spikes",        0,100,20,2,0,8,0,"The user spreads spikes on the target's side of the field!\n-Grounded Pokémon are damaged upon entry.\n-Stacks up to 3 times for more damage.","noMiss spikes noTarg"),
        ("Sticky Web",    0,100,20,2,0,11,0,"The user weaves a web on the target's side of the field!\n-Lowers Spe. of grounded Pokémon 1 stage upon entry.","noMiss sticky noTarg"),
        ("Stealth Rocks", 0,100,20,2,0,12,0,"The user spreads pointed stones on the target's side of the field!\n-Does Rock-type damage to all Pokémon upon entry.","noMiss rocks noTarg"),
         #reflect, lightscreen
        ("Aurora Veil",  0,100,20,2,0,5,0,"The user draws on the hail to create a barrier that reduces damage from physical and special attacks for 5 turns!\nFails if it isn't hailing.","veil needHail noTarg"),
        ("Reflect",      0,100,20,2,0,10,0,"The user creates a wall of light that reduces damage from physical attacks for 5 turns!","reflect noMiss noTarg"),
        ("Light Screen", 0,100,20,2,0,10,0,"The user creates a wall of light that reduces damage from special attacks for 5 turns!","lightscreen noMiss noTarg"),
         #healing
        ("Recover",         0,100,10,2,0,0,0,"The user regenerates cells to heal itself by half its max HP!","heals recover noMiss noTarg"),
        ("Milk Drink",      0,100,5,2,0,0,0,"The user drinks some milk to restore half its max HP!","heals recover noMiss noTarg "),
        ("Soft-Boiled",     0,100,5,2,0,0,0,"The user eats a tasty egg and restores half its max HP!","heals recover noMiss noTarg "),
        ("Slack-Off",       0,100,5,2,0,0,0,"The user takes a well-deserved break and restores half its max HP!","heals recover noMiss noTarg "),
        ("Morning Sun",     0,100,5,2,0,0,0,"The user basks in the morning sun to restore HP!\n-Restores 2/3 of the user's max HP in harsh sunlight.\n-1/2 max HP in clear weather.\n-1/4 max HP in rain, sandstorm, hail.","heals synthesis noMiss noTarg"),
        ("Aqua Ring",       0,100,20,2,0,2,0,"The user envelops itself with a veil of healing waters!\n-Restores 1/16 of the user's max HP at the end of each turn.","aquaring noMiss noTarg"),
        ("Take Heart",      0,100,10,2,0,2,0,"The user focuses on the positives to lift its spirits!\n-Raises the user's Sp.A Sp.D 1 stage each.\n-Heals status conditions.","stat self,sa:sd,1:1,100 refresh noMiss noTarg"),
        ("Synthesis",       0,100,5,2,0,3,0,"The user takes in sunlight to restore HP!\n-Restores 2/3 of the user's max HP in harsh sunlight.\n-1/2 max HP in clear weather.\n-1/4 max HP in rain, sandstorm, hail.","heals synthesis noMiss noTarg"),
        ("Shore Up",        0,100,5,2,0,8,0,"The user draws in sand to restore itself!\n-Restores 2/3 of the user's max HP in a sandstorm.\n-1/2 max HP in all other conditions.","heals shoreup"),
        ("Jungle Healing",  0,100,5,2,0,3,0,"The user becomes one with the jungle!\n-Restores 25% of the user's max HP.\n-Heals status conditions.","heals blessing refresh noMiss noTarg"),
        ("Lunar Blessing",  0,100,5,2,0,10,0,"The user receives a blessing from the crescent moon!\n-Restores 25% of the user's max HP.\n-Heals status conditions.","heals blessing refresh noMiss noTarg"),
        ("Moonlight",       0,100,5,2,0,17,0,"The user basks in the moonlight to restore HP!\n-Restores 2/3 of the user's max HP in harsh sunlight.\n-1/2 max HP in clear weather.\n-1/4 max HP in rain, sandstorm, hail.","heals synthesis noMiss noTarg"),

         #stat(istic) changes
        ("Focus Energy",    0,100,30,2,0,0,0,"The user takes a deep breath and heightens its focus!\n-Increases chances of landing crit' hits.","focusenergy noMiss noTarg"),
        ("Harden",          0,100,40,2,0,0,0,"The user stiffens the muscles in its body!\n-Raises the user's Def. 1 stage.","stat self,de,1 noMiss noTarg"),
        ("Defense Curl",    0,100,40,2,0,0,0,"The user curls up to hide its weak spots!\n-Raises the user's Def. 1 stage.","stat self,de,1 noMiss curled noTarg"),
        ("Swords Dance",    0,100,20,2,0,0,0,"The user uplifts the fighting spirit with a frenetic dance!\n-Raises the user's Atk. 2 stages.","stat self,at,2 noMiss noTarg"),
        ("Growth",          0,100,20,2,0,0,0,"The user's body grows all at once!\n-Raises the user's Atk. Sp.A 1 stage each.\n-2 stages each in harsh sunlight.","stat self,at:sa,1:1 noMiss growth noTarg"),
        ("Double Team",     0,100,15,2,0,0,0,"The user moves so quick it creates afterimages!\n-Raises the user's Evas. 1 stage.","stat self,ev,1 noMiss noTarg"),
        ("Confide",         0,100,20,2,0,0,0,"The user tells the target a (quite inappropriate) secret!\n-Lowers the target's Sp.A 1 stage.","stat targ,sa,-1 noMiss"),
        ("Growl",           0,100,40,2,0,0,0,"The user growls cutely to disarm the target!\n-Lowers the target's Atk. 1 stage.","stat targ,at,-1"),
        ("Withdraw",        0,100,40,2,0,2,0,"The user withdraws into its body!\n-Raises the user's Def. 1 stage.","stat self,de,1,100 noMiss noTarg"),
        ("Victory Dance",   0,100,10,2,0,6,0,"The user performs an intense dance to usher in victory!\n-Raises the user's Atk. Def. Spe. 1 stage each.","stat self,at:de:sp,1:1:1,100 noMiss noTarg"),
        ("Feather Dance",   0,100,15,2,0,9,0,"The user covers the target with a mass of down!\n-Lowers the target's Atk. 2 stages.","stat targ,at,-2,100"),
        ("Amnesia",         0,100,20,2,0,10,0,"The user empties its mind and forgets its concerns!\n-Raises the user's Sp.D 2 stages.","stat self,sd,2 noMiss noTarg"),
        ("String Shot",     0,95,40,2,0,11,0,"The user spins silk to bind the target!\n-Lowers the target's Spe. 1 stage.","stat targ,sp,-1"),
        ("Quiver Dance",    0,100,20,2,0,11,0,"The user lightly performs a beautiful, mystic dance!\n-Raises the user's Sp.A Sp.D Spe. 1 stage each.","stat self,sa:sd:sp,1:1:1,100 noMiss noTarg"),
        ("Defend Order",    0,100,10,2,0,11,0,"The user calls on its underlings to fortify its defenses!\n-Raises the user's Def. Sp.D 1 stage each.","stat self,de:sd,1:1,100 noMiss noTarg"),
        ("Dragon Dance",    0,100,20,2,0,14,0,"The user vigorously performs a mystic, poweful dance!\n-Raises the user's Atk. Spe. 1 stage each.","stat self,at:sp,1:1 noMiss noTarg"),
        ("Nasty Plot",      0,100,20,2,0,15,0,"The user stimulates the brain by thinking bad thoughts!\n-Raises the user's Sp.A 2 stages.","stat self,sa,2 noMiss noTarg"),
        ("Metal Sound",     0,85,40,2,0,16,0,"The user creates horrible metal-scraping sounds to unnerve the target!\n-Lowers the target's Sp.D 2 stages.","stat targ,sd,-2 sound"), #sound-based, soundproof ability is immune,
        ("Shelter",         0,100,10,2,0,16,0,"The user makes its skin as hard as an iron shield!\n-Raises the user's Def. 2 stages.","stat self,de,2,100 noMiss noTarg"),
        ("Shift Gear",      0,100,10,2,0,16,0,"The user powers up by rotating its gears!\n-Raises the user's Atk. 1 stage, Spe. 2 stages.","noMiss noTarg stat self,at:sp,1:2,100"),
        ("Geomancy",        0,100,10,2,0,17,0,"The user absorbs energy from its surroundings and powers up on the next turn!\n-Raises the user's Sp.A Sp.D Spe. 2 stages each.\n-Two-turn move.","stat self,sa:sd:sp,2:2:2 noMiss 2turn geomance noTarg"),
        ("Baby-Doll Eyes",  0,100,30,2,0,17,+1,"The user stares at the target with its baby-doll eyes!\n-Lowers the target's Atk. 1 stage.\n-Priority +1.","stat targ,at,-1,100"),
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



#constructing dtypes and names to accompany data
labels = np.dtype( [('name','U25'),('pwr','i4'),('accu','i4'),('pp','i4'),('special?','i4'),('contact?','i4'),('type','i4'),('priority','i4'),('desc','U400'),('notes','U140')] )
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

