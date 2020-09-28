#companion to pokemon.py
#Antoine Washington

import numpy as np
import astropy.table as tbl

def getMoveInfo(moveIndex):
    return umm[moveIndex]

movedex1=("Hyper Beam",150,90,5,1,0,"The user attacks with a powerful beam! Must rest on next turn.","mustRest")
movedex2=("Blast Burn",150,90,5,1,1,"The user attacks with a fiery explosion! Must rest on next turn","mustRest")
umm = tbl.Table(rows=(movedex1,movedex2),names=('name','pwr','accu','pp','special?','type','desc','notes'),dtype=('U25','i4','i4','i4','i4','i4','U140','U140'))
moremoves=[
        ("Frenzy Plant",150,90,5,1,3,"Big roots! Must rest on next turn.","mustRest"),
        ("Hydro Cannon",150,90,5,1,2,"Blast of water! Must rest on next turn.","mustRest"),
        ("Giga Impact",150,90,5,0,0,"Must rest on next turn.","mustRest"),
        ("Roar of Time",150,90,5,1,14,"The user roars to distort time and inflict damage. Must rest on next turn.","mustRest"),
        ("Rock Wrecker",150,90,5,0,13,"Must rest on next turn.","mustRest"),
        ("Double-Edge",120,100,15,0,0,"User takes 1/3 recoil damage.","recoilThird"),
        ("Volt Tackle",120,100,15,0,4,"User takes 1/3 recoil damage.","recoilThird para10"),
        ("Brave Bird",120,100,15,0,9,"Takes 1/3 recoil damage.","recoilThird"),
        ("Flare Blitz",120,100,15,0,1,"User takes 1/3 recoil damage.","recoilThird burn10"),
        ("Wood Hammer",120,100,15,0,3,"Takes 1/3 recoil damage.","recoilThird"),
        ("Earthquake",100,100,10,0,8,"The user causes a powerful earthquake.",""),
        ("Judgement",100,100,10,1,0,"The user pelts the battlefield with bolts of light from the sky.",""),
        ("Flamethrower",90,100,15,1,1,"The user attacks with a powerful flame! 10% chance to burn.","burn10"),
        ("Ice Beam",90,100,15,1,5,"The user focuses a stream of ice at the target! 10% chance to freeze.","frze10"),
        ("Thunderbolt",90,100,15,1,4,"The user attacks with a bolt of lightning! 10% chance to paralyze.","para10"),
        ("Leaf Blade",90,100,15,0,3,"The user attacks with a sharpened leaf! High crit' ratio.","highCrit"),
        ("Attack Order",90,100,15,0,12,"The user attacks with a powerful flame! 10% chance to burn.","highCrit"),
        ("Tackle",40,100,35,0,0,"The user charges to attack.",""),
        ("Swords Dance",0,100,20,2,0,"Boosts Atk. 2 stages.","A2")
        ]
for i in moremoves:
    umm.add_row(i)
coll=tbl.Column(range(0,len(umm)),dtype='i4')
umm.add_column(coll,index=0,name='index')
